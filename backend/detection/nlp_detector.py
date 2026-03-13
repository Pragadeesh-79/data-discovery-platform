import spacy
from spacy.cli import download

class NLPDetector:
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            download("en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")

    def detect(self, text: str) -> list:
        # Some texts could be very long, spacy has max length limit, but we'll assume valid chunks
        doc = self.nlp(text)
        results = []
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                results.append({
                    "value": ent.text,
                    "entity_type": "Name",
                    "classification": "Personal",
                    "method": "Spacy"
                })
            elif ent.label_ == "ORG":
                results.append({
                    "value": ent.text,
                    "entity_type": "Organization",
                    "classification": "Personal",
                    "method": "Spacy"
                })
            elif ent.label_ == "GPE":
                results.append({
                    "value": ent.text,
                    "entity_type": "Location",
                    "classification": "Personal",
                    "method": "Spacy"
                })
            elif ent.label_ == "DATE":
                results.append({
                    "value": ent.text,
                    "entity_type": "Date",
                    "classification": "Sensitive",
                    "method": "Spacy"
                })
            elif ent.label_ == "MONEY":
                results.append({
                    "value": ent.text,
                    "entity_type": "Financial",
                    "classification": "Highly Sensitive",
                    "method": "Spacy"
                })
        return results
