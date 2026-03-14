from datetime import datetime

from detection.regex_detector import RegexDetector
from classification.classifier import PIIClassifier

class PIIDetector:
    def __init__(self):
        self.regex_detector = RegexDetector()
        self.classifier = PIIClassifier()

    def process_text(self, text: str, file_name: str, source: str) -> dict:
        entities = []

        regex_entities = self.regex_detector.detect(text)
        entities.extend(regex_entities)

        unique_entities = []
        seen = set()
        for ent in entities:
            identifier = (ent['value'], ent['entity_type'])
            if identifier not in seen:
                seen.add(identifier)
                unique_entities.append(ent)

        final_entities = []

        for ent in unique_entities:
            entity_type = ent['entity_type']
            method = ent.get('method', 'Unknown')

            if 'classification' in ent:
                classification = ent['classification']
            else:
                classification = self.classifier.classify(entity_type)

            final_entities.append({
                'entity_type': entity_type,
                'value': ent['value'],
                'classification': classification,
                'method': method
            })

        return {
            'file_name': file_name,
            'source': source,
            'entities': final_entities
        }
