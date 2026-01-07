import re


def anonymize_resume(text: str) -> str:
    text = re.sub(r"\b[A-Z][a-z]+ [A-Z][a-z]+\b", "[REDACTED_NAME]", text)
    text = re.sub(r"\S+@\S+", "[REDACTED_EMAIL]", text)
    text = re.sub(r"\+?\d[\d\s\-]{8,}", "[REDACTED_PHONE]", text)
    return text
