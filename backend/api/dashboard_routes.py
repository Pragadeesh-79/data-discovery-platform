from fastapi import APIRouter
from database.mongo_client import pii_inventory

router = APIRouter()

@router.get("/dashboard-stats")
def get_dashboard_stats():
    # Number of unique files
    unique_files = len(pii_inventory.distinct("file_name"))
    
    # Total PII records detected
    total_pii = pii_inventory.count_documents({})
    
    # Total High Risk records
    high_risk_count = pii_inventory.count_documents({"classification": {"$in": ["Highly Sensitive", "Strict", "High"]}})
    
    return {
        "files_scanned": unique_files,
        "pii_detected": total_pii,
        "high_risk": high_risk_count
    }
