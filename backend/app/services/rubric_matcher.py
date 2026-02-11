from typing import List, Dict
import logging
import re

logger = logging.getLogger(__name__)


class RubricMatcher:
    """
    Keyword-based rubric matching service
    Analyzes concept coverage using text matching and keyword extraction
    """
    
    def __init__(self):
        """
        Initialize the rubric matcher
        """
        logger.info("Initializing keyword-based rubric matcher")
        logger.info("Rubric matcher initialized successfully")
    
    def _extract_keywords(self, text: str) -> set:
        """Extract keywords from text"""
        # Convert to lowercase and split into words
        words = re.findall(r'\b\w+\b', text.lower())
        # Filter out common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                     'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
                     'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
                     'would', 'should', 'could', 'may', 'might', 'must', 'can', 'this',
                     'that', 'these', 'those', 'it', 'its', 'which', 'who', 'what', 'where',
                     'when', 'why', 'how'}
        return set(w for w in words if w not in stop_words and len(w) > 2)
    
    def _calculate_coverage(self, rubric_keywords: set, answer_keywords: set) -> float:
        """Calculate how well the answer covers the rubric keywords"""
        if not rubric_keywords:
            return 1.0
        
        intersection = rubric_keywords & answer_keywords
        coverage = len(intersection) / len(rubric_keywords)
        return coverage
    
    def analyze_rubric_coverage(
        self,
        student_answer: str,
        rubrics: List[str],
        correct_answer: str
    ) -> Dict:
        """
        Analyze how well the student answer covers the rubric points
        
        Args:
            student_answer: Student's response
            rubrics: List of key concepts/rubrics
            correct_answer: Model answer for reference
            
        Returns:
            Dictionary with score and analysis
        """
        covered_concepts = []
        missing_concepts = []
        partial_concepts = []
        
        student_keywords = self._extract_keywords(student_answer)
        
        for rubric in rubrics:
            rubric_keywords = self._extract_keywords(rubric)
            coverage = self._calculate_coverage(rubric_keywords, student_keywords)
            
            if coverage >= 0.7:  # 70% of keywords found
                covered_concepts.append(rubric)
            elif coverage >= 0.3:  # 30-70% of keywords found
                partial_concepts.append(rubric)
            else:
                missing_concepts.append(rubric)
        
        # Calculate score
        total_rubrics = len(rubrics)
        if total_rubrics == 0:
            score = 1.0
        else:
            # Full points for covered, half points for partial
            score = (len(covered_concepts) + 0.5 * len(partial_concepts)) / total_rubrics
        
        logger.info(f"Rubric coverage: {score:.3f} ({len(covered_concepts)}/{total_rubrics} covered)")
        
        return {
            "score": score,
            "covered_concepts": covered_concepts,
            "partial_concepts": partial_concepts,
            "missing_concepts": missing_concepts,
            "total_rubrics": total_rubrics
        }
    
    def get_detailed_feedback(self, analysis: Dict) -> str:
        """
        Generate detailed feedback from rubric analysis
        
        Args:
            analysis: Analysis dictionary from analyze_rubric_coverage
            
        Returns:
            Feedback string
        """
        feedback_parts = []
        
        if analysis["covered_concepts"]:
            feedback_parts.append(
                f"✓ Well covered concepts: {', '.join(analysis['covered_concepts'])}"
            )
        
        if analysis["partial_concepts"]:
            feedback_parts.append(
                f"⚠ Partially covered concepts: {', '.join(analysis['partial_concepts'])}"
            )
        
        if analysis["missing_concepts"]:
            feedback_parts.append(
                f"✗ Missing concepts: {', '.join(analysis['missing_concepts'])}"
            )
        
        return " | ".join(feedback_parts) if feedback_parts else "All concepts covered adequately."
