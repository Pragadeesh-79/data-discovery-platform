import sys
import os

# Add root to python path to allow importing backend module
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from backend.detection.pii_detector import PIIDetector

def run_test():
    print("Initializing full PIIDetector pipeline...")
    detector = PIIDetector()
    
    # Let's create a mock text string that represents what might be inside "Patient Info.pdf"
    sample_patient_text = """
    Patient Information Record
    --------------------------
    Name: Rahul Sharma
    Age: 45
    Doctor: Dr. Anjali Desai
    Contact: 9876543210
    Email: rahul.sharma@example.com
    PAN: ABCDE1234F
    
    Notes: Patient Rahul Sharma has been advised to visit the clinic on Tuesday.
    """
    
    print(f"\nProcessing mock Patient PDF text:")
    print("-" * 50)
    
    result = detector.process_text(sample_patient_text, "Patient Info.pdf", "test_script")
    
    import json
    print("\nFinal JSON Output (similar to API response):")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    run_test()
