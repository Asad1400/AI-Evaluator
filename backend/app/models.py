from pydantic import BaseModel, Field
from typing import List, Optional


class EvaluationRequest(BaseModel):
    """Request model for answer evaluation"""
    question: str = Field(..., description="The question statement")
    rubrics: List[str] = Field(..., description="List of key points/concepts to evaluate")
    correct_answer: str = Field(..., description="The model/correct answer")
    student_answer: str = Field(..., description="The student's response")
    total_marks: float = Field(..., gt=0, description="Total marks for the question")
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "Explain the concept of machine learning",
                "rubrics": [
                    "Definition of machine learning",
                    "Types of machine learning",
                    "Real-world applications",
                    "Examples"
                ],
                "correct_answer": "Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed. There are three main types: supervised learning, unsupervised learning, and reinforcement learning. It is used in various applications like recommendation systems, image recognition, and natural language processing.",
                "student_answer": "Machine learning allows computers to learn from data. It includes supervised and unsupervised learning. Examples include Netflix recommendations and face recognition.",
                "total_marks": 10.0
            }
        }


class ScoreBreakdown(BaseModel):
    """Detailed breakdown of evaluation scores"""
    rubric_score: float = Field(..., ge=0, le=1, description="Score from rubric matching (0-1)")
    semantic_score: float = Field(..., ge=0, le=1, description="Semantic similarity score (0-1)")
    nli_score: float = Field(..., ge=0, le=1, description="Entailment/consistency score (0-1)")
    final_score: float = Field(..., ge=0, le=1, description="Weighted final score (0-1)")


class EvaluationResponse(BaseModel):
    """Response model for answer evaluation"""
    scores: ScoreBreakdown
    suggested_grade: float = Field(..., description="Suggested marks out of total")
    total_marks: float = Field(..., description="Total marks for the question")
    percentage: float = Field(..., ge=0, le=100, description="Percentage score")
    feedback: str = Field(..., description="Detailed evaluation feedback")
    rubric_analysis: dict = Field(..., description="Analysis of rubric coverage")
    
    class Config:
        json_schema_extra = {
            "example": {
                "scores": {
                    "rubric_score": 0.75,
                    "semantic_score": 0.82,
                    "nli_score": 0.90,
                    "final_score": 0.80
                },
                "suggested_grade": 8.0,
                "total_marks": 10.0,
                "percentage": 80.0,
                "feedback": "Good understanding demonstrated. Covered most key concepts.",
                "rubric_analysis": {
                    "covered_concepts": ["Definition", "Types"],
                    "missing_concepts": ["Applications detail"]
                }
            }
        }
