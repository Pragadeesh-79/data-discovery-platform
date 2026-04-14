from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database.sqlite_db import get_db
from models.pii_model import PIIRecord

router = APIRouter()

@router.get("/dashboard-stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    # Number of unique file locations scanned
    unique_files = db.query(func.count(func.distinct(PIIRecord.location))).scalar() or 0

    # Total PII records detected
    total_pii = db.query(PIIRecord).count()

    # Total High Risk records
    high_risk_count = db.query(PIIRecord).filter(
        PIIRecord.sensitivity.in_(["High"])
    ).count()

    return {
        "files_scanned": unique_files,
        "pii_detected": total_pii,
        "high_risk": high_risk_count
    }
