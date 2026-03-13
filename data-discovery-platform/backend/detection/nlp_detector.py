import spacy

class NLPDetector:
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            import spacy.cli
            spacy.cli.download("en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")

    def detect(self, text: str) -> list:
        # Some texts could be very long, spacy has max length limit, but we'll assume valid chunks
        doc = self.nlp(text)
        results = []
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                results.append({
                    "value": ent.text,
                    "entity_type": "Name"
                })
        return results
