from datetime import datetime
import pymongo

from backend.detection.regex_detector import RegexDetector
from backend.detection.nlp_detector import NLPDetector
from backend.classification.classifier import PIIClassifier

class PIIDetector:
    def __init__(self):
        self.regex_detector = RegexDetector()
        self.nlp_detector = NLPDetector()
        self.classifier = PIIClassifier()

        self.mongo_uri = "mongodb+srv://data-discovery-platform:Pragadeesh79@cluster0.9jrovtp.mongodb.net/"
        try:
            self.client = pymongo.MongoClient(self.mongo_uri, serverSelectionTimeoutMS=5000)
            self.db = self.client["data_discovery"]
            self.collection = self.db["pii_inventory"]
        except Exception as e:
            print(f"MongoDB connection error: {e}")
            self.client = None

    def process_text(self, text: str, file_name: str, source: str) -> dict:
        """
        Main pipeline logic:
        1. Regex Detection
        2. NLP Detection
        3. Merge & Remove Duplicates
        4. Classification
        5. Store in MongoDB
        6. Return JSON struct
        """
        entities = []
        
        # 1. Regex Detection
        regex_entities = self.regex_detector.detect(text)
        entities.extend(regex_entities)
        
        # 2. NLP Detection
        nlp_entities = self.nlp_detector.detect(text)
        entities.extend(nlp_entities)
        
        # 3. Remove duplicates
        unique_entities = []
        seen = set()
        for ent in entities:
            identifier = (ent["value"], ent["entity_type"])
            if identifier not in seen:
                seen.add(identifier)
                unique_entities.append(ent)
                
        # 4. Run classification engine
        final_entities = []
        db_records = []
        timestamp = datetime.utcnow().isoformat(timespec='seconds')
        
        try:
            from utils.encryption import encryptor
        except ImportError:
            from backend.utils.encryption import encryptor
        
        for ent in unique_entities:
            entity_type = ent["entity_type"]
            method = ent.get("method", "Unknown")
            
            # Use classification if provided by detector, else classify
            if "classification" in ent:
                classification = ent["classification"]
            else:
                classification = self.classifier.classify(entity_type)
            
            # Encrypt sensitive values before storing
            encrypted_val = encryptor.encrypt(ent["value"])
            
            final_entities.append({
                "entity_type": entity_type,
                "value": ent["value"], # Still mask on frontend if needed, but include for checking
                "classification": classification,
                "method": method
            })
            
            db_records.append({
                "file_name": file_name,
                "source": source,
                "entity_type": entity_type,
                "encrypted_value": encrypted_val,
                "classification": classification,
                "method": method,
                "timestamp": timestamp
            })
            
        # 5. Store results in MongoDB
        if db_records and self.client:
            try:
                self.collection.insert_many(db_records)
            except Exception as e:
                print(f"Error inserting records to MongoDB: {e}")
                
        # 6. Return JSON output
        return {
            "file_name": file_name,
            "source": source,
            "entities": final_entities
        }
