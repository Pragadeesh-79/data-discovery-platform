import re

REGEX_PATTERNS = {
    "PAN": r"\b[A-Z]{5}[0-9]{4}[A-Z]\b",
    "Aadhaar": r"\b\d{12}\b",
    "Phone": r"\b\d{10}\b",
    "Email": r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
}

COMPILED_PATTERNS = {name: re.compile(pattern) for name, pattern in REGEX_PATTERNS.items()}
