CLASSIFICATION_MAPPING = {
    "Name": "Personal",
    "Phone": "Sensitive",
    "Email": "Sensitive",
    "PAN": "Highly Sensitive",
    "Aadhaar": "Highly Sensitive",
    "Financial Data": "Highly Sensitive",
    "Health Data": "Highly Sensitive"
}

class PIIClassifier:
    def classify(self, entity_type: str) -> str:
        return CLASSIFICATION_MAPPING.get(entity_type, "Unknown")
