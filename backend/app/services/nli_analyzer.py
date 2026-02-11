import logging
import re

logger = logging.getLogger(__name__)


class NLIAnalyzer:
    """
    Text-based consistency analyzer for detecting contradictions
    Uses keyword matching and negation detection
    """
    
    def __init__(self):
        """
        Initialize the NLI analyzer
        """
        logger.info("Initializing text-based NLI analyzer")
        self.negation_words = {'not', 'no', 'never', 'neither', 'nor', 'none', 'nobody',
                               'nothing', 'nowhere', 'cannot', 'can\'t', 'won\'t', 'wouldn\'t',
                               'shouldn\'t', 'isn\'t', 'aren\'t', 'wasn\'t', 'weren\'t',
                               'hasn\'t', 'haven\'t', 'hadn\'t', 'doesn\'t', 'don\'t', 'didn\'t'}
        logger.info("NLI analyzer initialized successfully")
    
    def _has_negation(self, text: str) -> bool:
        """Check if text contains negation words"""
        words = set(re.findall(r'\b\w+\'?\w*\b', text.lower()))
        return bool(words & self.negation_words)
    
    def _extract_keywords(self, text: str) -> set:
        """Extract keywords from text"""
        words = re.findall(r'\b\w+\b', text.lower())
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                     'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were'}
        return set(w for w in words if w not in stop_words and len(w) > 2)
    
    def analyze_entailment(
        self,
        student_answer: str,
        correct_answer: str
    ) -> dict:
        """
        Analyze if student answer is consistent with correct answer
        
        Args:
            student_answer: Student's response
            correct_answer: Model/correct answer
            
        Returns:
            Dictionary with entailment score and label
        """
        try:
            # Extract keywords from both answers
            student_keywords = self._extract_keywords(student_answer)
            correct_keywords = self._extract_keywords(correct_answer)
            
            # Calculate keyword overlap
            if not correct_keywords:
                overlap = 1.0
            else:
                intersection = student_keywords & correct_keywords
                overlap = len(intersection) / len(correct_keywords)
            
            # Check for negations
            student_has_negation = self._has_negation(student_answer)
            correct_has_negation = self._has_negation(correct_answer)
            
            # Determine support score
            # High overlap + similar negation pattern = high support
            # High overlap + different negation pattern = potential contradiction
            if overlap > 0.5:
                if student_has_negation == correct_has_negation:
                    support_score = 0.7 + (overlap * 0.3)  # 0.7-1.0
                    label = "supports the concept"
                else:
                    support_score = 0.3  # Potential contradiction
                    label = "contradicts the concept"
            else:
                support_score = 0.5  # Neutral/unrelated
                label = "unrelated to the concept"
            
            contradict_score = 1.0 - support_score if label == "contradicts the concept" else 0.1
            
            # Calculate final entailment score
            entailment_score = support_score - (contradict_score * 0.5)
            entailment_score = max(0.0, min(1.0, entailment_score))
            
            logger.info(f"NLI Analysis - Label: {label}, Score: {entailment_score:.3f}")
            
            return {
                "score": entailment_score,
                "label": label,
                "support_score": support_score,
                "contradict_score": contradict_score,
                "all_scores": {
                    "supports the concept": support_score,
                    "contradicts the concept": contradict_score,
                    "unrelated to the concept": 1.0 - support_score - contradict_score
                }
            }
            
        except Exception as e:
            logger.error(f"Error in NLI analysis: {e}")
            return {
                "score": 0.5,
                "label": "neutral",
                "support_score": 0.5,
                "contradict_score": 0.0,
                "all_scores": {}
            }
    
    def get_entailment_feedback(self, analysis: dict) -> str:
        """
        Generate feedback based on NLI analysis
        
        Args:
            analysis: Analysis dictionary from analyze_entailment
            
        Returns:
            Feedback string
        """
        label = analysis["label"]
        score = analysis["score"]
        
        if "supports" in label.lower():
            return f"Answer is consistent with expected concepts (confidence: {score:.1%})."
        elif "contradicts" in label.lower():
            return f"⚠ Answer contains contradictory information (contradiction detected with {analysis['contradict_score']:.1%} confidence)."
        else:
            return "Answer is neutral or tangentially related to the expected concepts."
