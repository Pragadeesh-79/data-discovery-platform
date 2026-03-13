import sys
import os

# Add root to python path to allow importing backend module
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from backend.detection.nlp_detector import NLPDetector

def test_spacy():
    print("Initializing SpaCy NLPDetector...")
    detector = NLPDetector()
    
    sample_text = """
    Apple is looking at buying a U.K. startup for $1 billion on Tuesday. 
    Tim Cook is the CEO of the company. 
    He lives in California and his phone number is 555-0199 but we only care about his name here.
    """
    
    print(f"\nProcessing text: {sample_text.strip()}")
    print("-" * 50)
    
    results = detector.detect(sample_text)
    
    print("\nEntities detected by SpaCy:")
    if not results:
        print("No entities found.")
    else:
        for res in results:
            print(f"- {res}")

if __name__ == "__main__":
    test_spacy()
