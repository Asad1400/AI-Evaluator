from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from typing import Dict

from app.models import EvaluationRequest, EvaluationResponse, ScoreBreakdown
from app.services.rubric_matcher import RubricMatcher
from app.services.semantic_analyzer import SemanticAnalyzer
from app.services.nli_analyzer import NLIAnalyzer
from app.services.score_aggregator import ScoreAggregator
from app.utils.text_preprocessing import clean_text

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global service instances
services: Dict = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for loading models on startup
    """
    logger.info("Starting application and loading models...")
    
    try:
        # Initialize all services
        services["rubric_matcher"] = RubricMatcher()
        services["semantic_analyzer"] = SemanticAnalyzer()
        services["nli_analyzer"] = NLIAnalyzer()
        services["score_aggregator"] = ScoreAggregator(
            rubric_weight=0.5,
            semantic_weight=0.3,
            nli_weight=0.2
        )
        logger.info("All models loaded successfully!")
        
    except Exception as e:
        logger.error(f"Error loading models: {e}")
        raise
    
    yield
    
    # Cleanup
    logger.info("Shutting down application...")
    services.clear()


# Create FastAPI app
app = FastAPI(
    title="Automated Evaluation of Descriptive Answers",
    description="NLP-based system for evaluating student answers using rubric matching, semantic similarity, and contradiction detection",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "Automated Evaluation API is running",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "models_loaded": len(services) == 4,
        "services": list(services.keys())
    }


@app.post("/evaluate", response_model=EvaluationResponse)
async def evaluate_answer(request: EvaluationRequest):
    """
    Evaluate a student's answer against rubrics and correct answer
    
    Args:
        request: EvaluationRequest containing question, rubrics, answers, etc.
        
    Returns:
        EvaluationResponse with scores and feedback
    """
    try:
        logger.info("Received evaluation request")
        
        # Clean inputs
        student_answer = clean_text(request.student_answer)
        correct_answer = clean_text(request.correct_answer)
        
        # Validate inputs
        if not student_answer or len(student_answer) < 10:
            raise HTTPException(
                status_code=400,
                detail="Student answer is too short or empty"
            )
        
        # Get services
        rubric_matcher = services.get("rubric_matcher")
        semantic_analyzer = services.get("semantic_analyzer")
        nli_analyzer = services.get("nli_analyzer")
        score_aggregator = services.get("score_aggregator")
        
        if not all([rubric_matcher, semantic_analyzer, nli_analyzer, score_aggregator]):
            raise HTTPException(
                status_code=503,
                detail="Services not initialized. Please try again."
            )
        
        # 1. Rubric Analysis
        logger.info("Performing rubric analysis...")
        rubric_analysis = rubric_matcher.analyze_rubric_coverage(
            student_answer=student_answer,
            rubrics=request.rubrics,
            correct_answer=correct_answer
        )
        rubric_score = rubric_analysis["score"]
        rubric_feedback = rubric_matcher.get_detailed_feedback(rubric_analysis)
        
        # 2. Semantic Similarity Analysis
        logger.info("Calculating semantic similarity...")
        semantic_score = semantic_analyzer.calculate_similarity(
            student_answer=student_answer,
            correct_answer=correct_answer
        )
        semantic_feedback = semantic_analyzer.get_similarity_feedback(semantic_score)
        
        # 3. NLI Analysis (Contradiction Detection)
        logger.info("Performing NLI analysis...")
        nli_analysis = nli_analyzer.analyze_entailment(
            student_answer=student_answer,
            correct_answer=correct_answer
        )
        nli_score = nli_analysis["score"]
        nli_feedback = nli_analyzer.get_entailment_feedback(nli_analysis)
        
        # 4. Aggregate Scores
        logger.info("Aggregating scores...")
        final_score = score_aggregator.aggregate_scores(
            rubric_score=rubric_score,
            semantic_score=semantic_score,
            nli_score=nli_score
        )
        
        # 5. Generate Comprehensive Feedback
        comprehensive_feedback = score_aggregator.generate_comprehensive_feedback(
            rubric_feedback=rubric_feedback,
            semantic_feedback=semantic_feedback,
            nli_feedback=nli_feedback,
            final_score=final_score,
            total_marks=request.total_marks
        )
        
        # Calculate final grades
        suggested_grade = final_score * request.total_marks
        percentage = final_score * 100
        
        # Prepare response
        response = EvaluationResponse(
            scores=ScoreBreakdown(
                rubric_score=rubric_score,
                semantic_score=semantic_score,
                nli_score=nli_score,
                final_score=final_score
            ),
            suggested_grade=round(suggested_grade, 2),
            total_marks=request.total_marks,
            percentage=round(percentage, 2),
            feedback=comprehensive_feedback,
            rubric_analysis={
                "covered_concepts": rubric_analysis["covered_concepts"],
                "partial_concepts": rubric_analysis["partial_concepts"],
                "missing_concepts": rubric_analysis["missing_concepts"],
                "total_rubrics": rubric_analysis["total_rubrics"]
            }
        )
        
        logger.info(f"Evaluation complete. Final score: {final_score:.3f}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during evaluation: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error during evaluation: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
