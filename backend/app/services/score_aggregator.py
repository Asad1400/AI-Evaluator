from typing import Dict
import logging

logger = logging.getLogger(__name__)


class ScoreAggregator:
    """
    Aggregates scores from different analysis components
    """
    
    def __init__(
        self,
        rubric_weight: float = 0.5,
        semantic_weight: float = 0.3,
        nli_weight: float = 0.2
    ):
        """
        Initialize score aggregator with weights
        
        Args:
            rubric_weight: Weight for rubric matching score
            semantic_weight: Weight for semantic similarity score
            nli_weight: Weight for NLI/entailment score
        """
        # Normalize weights to sum to 1.0
        total = rubric_weight + semantic_weight + nli_weight
        self.rubric_weight = rubric_weight / total
        self.semantic_weight = semantic_weight / total
        self.nli_weight = nli_weight / total
        
        logger.info(
            f"Score weights - Rubric: {self.rubric_weight:.2f}, "
            f"Semantic: {self.semantic_weight:.2f}, "
            f"NLI: {self.nli_weight:.2f}"
        )
    
    def aggregate_scores(
        self,
        rubric_score: float,
        semantic_score: float,
        nli_score: float
    ) -> float:
        """
        Calculate weighted average of all scores
        
        Args:
            rubric_score: Score from rubric matching (0-1)
            semantic_score: Score from semantic similarity (0-1)
            nli_score: Score from NLI analysis (0-1)
            
        Returns:
            Final aggregated score (0-1)
        """
        final_score = (
            self.rubric_weight * rubric_score +
            self.semantic_weight * semantic_score +
            self.nli_weight * nli_score
        )
        
        # Ensure score is between 0 and 1
        final_score = max(0.0, min(1.0, final_score))
        
        logger.info(
            f"Score aggregation - Rubric: {rubric_score:.3f}, "
            f"Semantic: {semantic_score:.3f}, "
            f"NLI: {nli_score:.3f}, "
            f"Final: {final_score:.3f}"
        )
        
        return final_score
    
    def generate_comprehensive_feedback(
        self,
        rubric_feedback: str,
        semantic_feedback: str,
        nli_feedback: str,
        final_score: float,
        total_marks: float
    ) -> str:
        """
        Generate comprehensive feedback combining all analyses
        
        Args:
            rubric_feedback: Feedback from rubric analysis
            semantic_feedback: Feedback from semantic analysis
            nli_feedback: Feedback from NLI analysis
            final_score: Final aggregated score
            total_marks: Total marks for the question
            
        Returns:
            Comprehensive feedback string
        """
        suggested_marks = final_score * total_marks
        percentage = final_score * 100
        
        # Overall assessment
        if percentage >= 85:
            overall = "Excellent answer"
        elif percentage >= 70:
            overall = "Good answer"
        elif percentage >= 55:
            overall = "Satisfactory answer"
        elif percentage >= 40:
            overall = "Needs improvement"
        else:
            overall = "Insufficient answer"
        
        feedback_parts = [
            f"**Overall Assessment:** {overall} ({percentage:.1f}%)",
            f"**Suggested Grade:** {suggested_marks:.1f}/{total_marks}",
            "",
            f"**Rubric Analysis:** {rubric_feedback}",
            f"**Semantic Quality:** {semantic_feedback}",
            f"**Consistency Check:** {nli_feedback}"
        ]
        
        return "\n".join(feedback_parts)
