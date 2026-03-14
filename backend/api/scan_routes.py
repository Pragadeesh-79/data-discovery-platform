"""
API Routes for data ingestion and dashboard analytics for the DPDPA platform.
"""

from fastapi import APIRouter, HTTPException, status, Query, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
import logging

# Import Pydantic models for request validation
# Import SQLAlchemy models for database operations
from models.pii_model import PIIRecordSchema, PIIRecord
from database.sqlite_db import get_db

router = APIRouter()
logger = logging.getLogger(__name__)

# =========================================================
# 1. SCAN INGESTION API
# =========================================================

@router.post("/scan-results")
def save_scan_result(record: PIIRecordSchema, db: Session = Depends(get_db)):
    """
    Endpoint to receive a single PII scan result and save it into SQLite.
    Checks for exact duplicates (by value & location) to prevent redundant data.
    """
    try:
        # Check if record exists (by value and location) - Upsert protection
        existing_record = db.query(PIIRecord).filter(
            PIIRecord.value == record.value,
            PIIRecord.location == record.location
        ).first()

        if existing_record:
            # Update existing record
            existing_record.type = record.type
            existing_record.source = record.source
            existing_record.owner = record.owner
            existing_record.sensitivity = record.sensitivity
            existing_record.risk_score = record.risk_score
            existing_record.detected_at = record.detected_at
        else:
            # Create new record
            new_record = PIIRecord(
                type=record.type,
                value=record.value,
                location=record.location,
                source=record.source,
                owner=record.owner,
                sensitivity=record.sensitivity,
                risk_score=record.risk_score,
                detected_at=record.detected_at
            )
            db.add(new_record)
        
        # Commit the transaction safely within the session
        db.commit()
        return {"message": "PII record stored successfully"}
        
    except Exception as e:
        db.rollback() 
        logger.error(f"Error saving to database: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while saving the record: {str(e)}"
        )

# =========================================================
# 2. INVENTORY API
# =========================================================

@router.get("/inventory")
def get_inventory(page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    """
    Returns detected PII records stored in SQLite with pagination.
    """
    try:
        # 1. Total records for pagination frontend calculation
        total_records = db.query(PIIRecord).count()
        
        # 2. Offset math
        skip = (page - 1) * limit
        
        # 3. Query limited subset
        records_db = db.query(PIIRecord).offset(skip).limit(limit).all()
        
        # Convert SQLAlchemy objects to dict form for JSON
        records = [
            {
                "type": r.type,
                "value": r.value,
                "location": r.location,
                "source": r.source,
                "owner": r.owner,
                "sensitivity": r.sensitivity,
                "risk_score": r.risk_score,
                "detected_at": r.detected_at.isoformat() if r.detected_at else None
            }
            for r in records_db
        ]
        
        return {
            "total_records": total_records,
            "page": page,
            "limit": limit,
            "data": records
        }
    except Exception as e:
        logger.error(f"Error fetching inventory: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# =========================================================
# 3. RISK SUMMARY API
# =========================================================

@router.get("/risk-summary")
def get_risk_summary(db: Session = Depends(get_db)):
    """
    Calculates total risk score and average across all database rows.
    """
    try:
        total_records = db.query(PIIRecord).count()
        
        # Use SQLAlchemy's sum function rather than loading all into Python
        total_risk_score = db.query(func.sum(PIIRecord.risk_score)).scalar() or 0
        
        # Prevent ZeroDivisionError organically
        average_risk_score = round(total_risk_score / total_records, 2) if total_records > 0 else 0
        
        return {
            "total_records": total_records,
            "total_risk_score": total_risk_score,
            "average_risk_score": average_risk_score
        }
    except Exception as e:
        logger.error(f"Error risk summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# =========================================================
# 4. PII TYPES API
# =========================================================

@router.get("/pii-types")
def get_pii_types(db: Session = Depends(get_db)):
    """
    Returns grouped counts for each PII type (e.g. Email: 4, PAN: 2).
    """
    try:
        # Uses SQL GROUP BY for best performance
        results = db.query(PIIRecord.type, func.count(PIIRecord.type)).group_by(PIIRecord.type).all()
        
        # Convert List of Tuples -> Dictionary format identical to original
        pii_counts = {item[0]: item[1] for item in results}
        return pii_counts
    except Exception as e:
        logger.error(f"Error pii types: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# =========================================================
# 5. DPDPA REPORT API
# =========================================================

@router.get("/dpdpa-report")
def get_dpdpa_report(db: Session = Depends(get_db)):
    """
    Summarizes total high risk data against compliance status codes.
    """
    try:
        total_records = db.query(PIIRecord).count()
        
        # Count all records explicitly defined as "High" Sensitivity
        high_risk_data = db.query(PIIRecord).filter(PIIRecord.sensitivity == "High").count()
        
        # Rule defined in documentation
        compliance_status = "Review Required" if high_risk_data > 0 else "Compliant"
        
        return {
            "total_records": total_records,
            "high_risk_data": high_risk_data,
            "compliance_status": compliance_status
        }
    except Exception as e:
        logger.error(f"Error dpdpa report: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# =========================================================
# 6. DASHBOARD STATS API (Aggregated)
# =========================================================

@router.get("/dashboard-stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    """
    Aggregated omni-endpoint powering the frontend to prevent round-trip chaining.
    Returns exactly matching MongoDB formatted dict structure but powered by SQLAlchemy.
    """
    try:
        total_records = db.query(PIIRecord).count()
        
        # Sum logic
        total_risk_score = db.query(func.sum(PIIRecord.risk_score)).scalar() or 0
        average_risk_score = round(total_risk_score / total_records, 2) if total_records > 0 else 0
        
        # PII Group By
        type_results = db.query(PIIRecord.type, func.count(PIIRecord.type)).group_by(PIIRecord.type).all()
        pii_types = {item[0]: item[1] for item in type_results}
        
        # Compliance logic
        high_risk_records = db.query(PIIRecord).filter(PIIRecord.sensitivity == "High").count()
        compliance_status = "Review Required" if high_risk_records > 0 else "Compliant"
        
        return {
            "total_records": total_records,
            "total_risk_score": total_risk_score,
            "average_risk_score": average_risk_score,
            "pii_types": pii_types,
            "high_risk_records": high_risk_records,
            "compliance_status": compliance_status
        }
    except Exception as e:
        logger.error(f"Error fetching dashboard data: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch dashboard data: {str(e)}")
