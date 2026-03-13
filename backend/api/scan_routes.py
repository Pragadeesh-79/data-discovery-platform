"""
Routes for handling scan operations and result ingestion.
"""

from fastapi import APIRouter, HTTPException, status
from models.pii_model import PIIRecord
from database.mongo_client import test_collection, check_db_connection
import pymongo.errors

# Create an APIRouter instance to group our scan-related routes together
router = APIRouter()

@router.post("/scan-results")
def save_scan_result(record: PIIRecord):
    """
    Endpoint to receive a single PII scan result and save it into MongoDB Atlas.
    
    The 'record' parameter is automatically validated against the PIIRecord Pydantic model.
    """
    
    # 1. Check database connection first
    if not check_db_connection():
        # Return a 500 Internal Server Error with a clear message instead of crashing
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to connect to MongoDB Atlas"
        )
        
    try:
        # 2. Convert the Pydantic model into a standard Python dictionary.
        # Check for model_dump (Pydantic v2) or fallback to dict (Pydantic v1) for compatibility
        record_dict = record.model_dump() if hasattr(record, "model_dump") else record.dict()
        
        # 3. Insert the record into the MongoDB database
        test_collection.insert_one(record_dict)
        
        # 4. Return a success message back to the client
        return {
            "message": "PII record stored successfully"
        }
        
    except pymongo.errors.ServerSelectionTimeoutError as e:
        # Handle specific connection timeout error during insertion
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"MongoDB Atlas cluster timed out while connecting: {str(e)}"
        )
    except pymongo.errors.PyMongoError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"MongoDB error: {str(e)}"
        )
    except Exception as e:
        # Catch any other unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while saving the record: {str(e)}"
        )
