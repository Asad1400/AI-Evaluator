from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import logging

logger = logging.getLogger(__name__)


class SemanticAnalyzer:
    """
    Semantic similarity analyzer using TF-IDF and cosine similarity
    Measures how semantically similar the student answer is to the correct answer
    """
    
    def __init__(self):
        """
        Initialize the semantic analyzer with TF-IDF vectorizer
        """
        logger.info("Initializing TF-IDF based semantic analyzer")
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            ngram_range=(1, 2),
            stop_words='english'
        )
        logger.info("Semantic analyzer initialized successfully")
    
    def calculate_similarity(
        self,
        student_answer: str,
        correct_answer: str
    ) -> float:
        """
        Calculate semantic similarity between student and correct answers using TF-IDF
        
        Args:
            student_answer: Student's response
            correct_answer: Model/correct answer
            
        Returns:
            Similarity score between 0 and 1
        """
        try:
            # Create TF-IDF vectors
            vectors = self.vectorizer.fit_transform([correct_answer, student_answer])
            
            # Calculate cosine similarity
            similarity_matrix = cosine_similarity(vectors[0:1], vectors[1:2])
            score = float(similarity_matrix[0][0])
            
            # Ensure score is between 0 and 1
            score = max(0.0, min(1.0, score))
            
            logger.info(f"Semantic similarity score (TF-IDF): {score:.3f}")
            return score
            
        except Exception as e:
            logger.error(f"Error calculating semantic similarity: {e}")
            return 0.5  # Return neutral score on error
    
    def get_similarity_feedback(self, score: float) -> str:
        """
        Generate feedback based on similarity score
        
        Args:
            score: Similarity score (0-1)
            
        Returns:
            Feedback string
        """
        if score >= 0.85:
            return "Excellent semantic alignment with the model answer."
        elif score >= 0.70:
            return "Good semantic similarity to the expected answer."
        elif score >= 0.55:
            return "Moderate semantic similarity. Some key ideas captured."
        elif score >= 0.40:
            return "Low semantic similarity. Answer may be off-topic or incomplete."
        else:
            return "Very low semantic similarity. Answer does not align with expected response."
