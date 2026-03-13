import os
import sys

# Add project root to path to import backend
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.database.mongo_client import get_db

def test_connection():
    try:
        db = get_db()
        print("Connection successful!")
        
        # Test basic insertion
        collection = db['test_collection']
        result = collection.insert_one({"message": "Hello MongoDB"})
        print(f"Inserted document ID: {result.inserted_id}")
        
        # Test basic retrieval
        doc = collection.find_one({"_id": result.inserted_id})
        print(f"Retrieved document: {doc}")
        
        # Clean up
        collection.delete_one({"_id": result.inserted_id})
        print("Cleaned up document.")
        
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    test_connection()
