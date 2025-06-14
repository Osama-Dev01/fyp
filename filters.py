import re
from langdetect import detect, LangDetectException

def validate_tweet(text: str) -> tuple[bool, str]:
    """
    Runs a series of checks to validate a tweet before classification.
    This function is self-contained and does not depend on FastAPI.

    
    Returns:
        A tuple containing:
        - bool: True if the tweet is valid, False otherwise.
        - str: A message explaining the validation result.
    """
    # Tier 1: Basic Sanity Checks
    cleaned_text = text.strip()
    if not cleaned_text:
        return False, "Tweet is empty or contains only whitespace."

    # Using word count can be simpler for very short tweets
    if len(cleaned_text.split()) < 8:
        return False, "Tweet is too short to be a verifiable claim (less than 4 words)."
    
    # Optional character count check
    if len(cleaned_text) < 25:
        return False, "Tweet is too short (less than 25 characters)."

    # Tier 2: Language Detection
    try:
       
        allowed_langs = ['en', 'ur']
        lang = detect(cleaned_text)
        if lang not in allowed_langs:
            return False, f"Language '{lang}' is not supported. Only English, Urdu, and Roman Urdu are handled."
    except LangDetectException:
       
        return False, "Tweet does not contain recognizable text (e.g., only emojis or symbols)."


    # Remove all URLs, mentions, and hashtags to see if any real text remains
    text_without_symbols = re.sub(r"http\S+|www\S+|@\w+|#\w+", "", cleaned_text).strip()
    if not text_without_symbols:
        return False, "Tweet only contains links, hashtags, or user mentions."
        
    
    return True, "Tweet is valid for classification."