def is_text_clean(text, bad_words=None):
    """
    Check if a string contains any bad words.

    Returns True if clean, False if it contains a bad word.
    """
    if bad_words is None:
        bad_words = [
            "ass", "bitch", "bastard", "crap", "damn", "dick", "fuck", 
            "idiot", "jerk", "piss", "shit", "slut", "whore"
        ]

    text_lower = text.lower()
    for word in bad_words:
        if word in text_lower:
            return False
    return True

