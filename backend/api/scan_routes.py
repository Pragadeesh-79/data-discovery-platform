"""
Routes for handling scan operations and result ingestion.
"""

from fastapi import APIRouter, HTTPException, status, Query
from models.pii_model import PIIRecord
from database.mongo_client import test_collection, check_db_connection
import pymongo.errors

# Create an APIRouter instance to group our scan-related routes together
router = APIRouter()

@router.post("/scan-results")
def save_scan_result(record: PIIRecord):
    """
    Endpoint to receive a single PII scan result and save it into MongoDB Atlas.
    
    Uses upsert to check if the exact same value inside the given location exists
    to prevent duplicates if a scanner runs redundantly over the same files.
    """
    
    # 1. Check database connection first
    if not check_db_connection():
        # Return a 500 Internal Server Error with a clear message instead of crashing
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to connect to MongoDB Atlas"
        )
        
    try:
        # Convert the Pydantic model into a standard Python dictionary.
        record_dict = record.model_dump() if hasattr(record, "model_dump") else record.dict()
        
        # 2. Insert or update the record into the MongoDB database (Upsert)
        test_collection.update_one(
            {"value": record_dict["value"], "location": record_dict["location"]},
            {"$set": record_dict},
            upsert=True
        )
        
        # 3. Return a success message back to the client
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

@router.get("/inventory")
def get_inventory(page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100)):
    """
    Returns detected PII records stored in MongoDB with pagination support.
    This prevents memory overload issues with millions of records.
    """
    if not check_db_connection():
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to connect to MongoDB Atlas"
        )
        
    try:
        # Pagination calculations
        skip = (page - 1) * limit
        
        # Fetch the total number of records for the frontend to render the paginator
        total_records = test_collection.count_documents({})
        
        # Fetch paginated records excluding the _id field
        records = list(test_collection.find({}, {"_id": 0}).skip(skip).limit(limit))
        
        return {
            "total_records": total_records,
            "page": page,
            "limit": limit,
            "data": records
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching inventory: {str(e)}"
        )


@router.get("/risk-summary")
def get_risk_summary():
    """
    Calculates total system risk based on the risk_score of each detected data element.
    This powers risk dashboards and charts.
    """
    if not check_db_connection():
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to connect to MongoDB Atlas"
        )
        
    try:
        # Fetch only the risk_score field to optimize performance
        records = list(test_collection.find({}, {"_id": 0, "risk_score": 1}))
        
        total_records = len(records)
        # Sum all risk scores
        total_risk_score = sum(record.get("risk_score", 0) for record in records)
        # Calculate average safely to avoid division by zero
        average_risk_score = round(total_risk_score / total_records, 2) if total_records > 0 else 0
        
        return {
            "total_records": total_records,
            "total_risk_score": total_risk_score,
            "average_risk_score": average_risk_score
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching risk summary: {str(e)}"
        )


@router.get("/pii-types")
def get_pii_types():
    """
    Returns counts of each type of PII detected.
    This powers dashboard charts such as PII by Type.
    """
    if not check_db_connection():
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to connect to MongoDB Atlas"
        )
        
    try:
        # Fetch only the type field
        records = list(test_collection.find({}, {"_id": 0, "type": 1}))
        
        # Count frequency of each type
        pii_counts = {}
        for record in records:
            pii_type = record.get("type", "Unknown")
            pii_counts[pii_type] = pii_counts.get(pii_type, 0) + 1
            
        return pii_counts
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching PII types: {str(e)}"
        )


@router.get("/dpdpa-report")
def get_dpdpa_report():
    """
    Generates a compliance summary aligned with India's DPDPA law.
    """
    if not check_db_connection():
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to connect to MongoDB Atlas"
        )
        
    try:
        # Fetch only the sensitivity field
        records = list(test_collection.find({}, {"_id": 0, "sensitivity": 1}))
        
        total_records = len(records)
        # Count records with High sensitivity
        high_risk_data = sum(1 for record in records if record.get("sensitivity") == "High")
        
        # If any record has sensitivity = "High" then compliance_status = "Review Required"
        compliance_status = "Review Required" if high_risk_data > 0 else "Compliant"
        
        return {
            "total_records": total_records,
            "high_risk_data": high_risk_data,
            "compliance_status": compliance_status
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while generating DPDPA report: {str(e)}"
        )

@router.get("/dashboard-stats")
def get_dashboard_stats():
    """
    Returns an aggregated view of all dashboard analytics in a single response,
    reducing multiple round-trip API calls for the frontend.
    """
    if not check_db_connection():
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to connect to MongoDB Atlas"
        )
        
    try:
        # Fetch all records needed for analytics
        records = list(test_collection.find({}, {"_id": 0}))
        
        # 1. Total records
        total_records = len(records)
        
        # 2 & 3. Total Risk Score and Average Risk Score
        total_risk_score = sum(record.get("risk_score", 0) for record in records)
        average_risk_score = round(total_risk_score / total_records, 2) if total_records > 0 else 0
        
        # 4. PII Type Distribution
        pii_types = {}
        # 5. High Risk Records Count
        high_risk_records = 0
        
        for record in records:
            # Count PII types
            pii_type = record.get("type", "Unknown")
            pii_types[pii_type] = pii_types.get(pii_type, 0) + 1
            
            # Count high sensitivity records
            if record.get("sensitivity") == "High":
                high_risk_records += 1
                
        # 6. Compliance Status
        compliance_status = "Review Required" if high_risk_records > 0 else "Compliant"
        
        # Build the final combined analytic response
        return {
            "total_records": total_records,
            "total_risk_score": total_risk_score,
            "average_risk_score": average_risk_score,
            "pii_types": pii_types,
            "high_risk_records": high_risk_records,
            "compliance_status": compliance_status
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch dashboard data: {str(e)}"
        )
