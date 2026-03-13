"""
Routes for handling scan operations and result ingestion.
"""

from fastapi import APIRouter
from models.pii_model import PIIRecord
from database.mongo_client import test_collection

# Create an APIRouter instance to group our scan-related routes together
router = APIRouter()

@router.post("/scan-results")
async def save_scan_result(record: PIIRecord):
    """
    Endpoint to receive a single PII scan result and save it into MongoDB Atlas.
    
    The 'record' parameter is automatically validated against the PIIRecord Pydantic model.
    """
    
    # 1. Convert the Pydantic model into a standard Python dictionary.
    # We use model_dump() (or dict() in older Pydantic versions) for this.
    record_dict = record.model_dump()
    
    # 2. Insert the record into the MongoDB database using pymongo
    test_collection.insert_one(record_dict)
    
    # 3. Return a success message back to the client
    return {
        "message": "PII record stored successfully"
    }
