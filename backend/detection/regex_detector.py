from detection.regex_patterns import COMPILED_PATTERNS

class RegexDetector:
    def __init__(self):
        self.patterns = COMPILED_PATTERNS

    def detect(self, text: str) -> list:
        results = []
        for entity_type, pattern in self.patterns.items():
            for match in pattern.finditer(text):
                results.append({
                    'value': match.group(),
                    'entity_type': entity_type,
                    'method': 'Regex'
                })
        return results
