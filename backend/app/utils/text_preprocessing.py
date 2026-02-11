import re
from typing import List


def clean_text(text: str) -> str:
    """
    Clean and normalize text for processing
    
    Args:
        text: Raw text input
        
    Returns:
        Cleaned text
    """
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    # Normalize punctuation spacing
    text = re.sub(r'\s+([.,!?;:])', r'\1', text)
    
    return text


def split_into_sentences(text: str) -> List[str]:
    """
    Split text into sentences
    
    Args:
        text: Input text
        
    Returns:
        List of sentences
    """
    # Simple sentence splitting (can be enhanced with nltk if needed)
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    return sentences


def extract_key_phrases(text: str) -> List[str]:
    """
    Extract potential key phrases from text
    
    Args:
        text: Input text
        
    Returns:
        List of key phrases
    """
    # Split by common delimiters
    phrases = re.split(r'[,;.]', text)
    phrases = [p.strip() for p in phrases if p.strip() and len(p.strip()) > 10]
    return phrases
