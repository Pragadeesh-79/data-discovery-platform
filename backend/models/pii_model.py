"""
Database models and Pydantic schemas for the application.
"""

from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database.sqlite_db import Base

# We import BaseModel to optionally keep Pydantic API validation in the same file if needed.
from pydantic import BaseModel, Field
from typing import Literal

# =========================================================
# SQLALCHEMY DATABASE MODEL
# =========================================================

class PIIRecord(Base):
    """
    SQLAlchemy model that represents the 'pii_records' table in the SQLite database.
    This stores all the sensitive data we detect from scanning files.
    """
    
    # 1. Define the exact name of the table in SQLite
    __tablename__ = "pii_records"

    # 2. Primary Key: A unique ID for every single record inserted
    # 'index=True' makes searching by ID much faster
    id = Column(Integer, primary_key=True, index=True)

    # 3. Type of PII Detected (e.g., 'Email', 'Phone', 'PAN', 'Aadhaar')
    type = Column(String)

    # 4. The actual raw sensitive data extracted (e.g., 'ABCDE1234F')
    value = Column(String)

    # 5. Where the data was found (e.g., 'finance/data.xlsx' or 'marketing/leads.csv')
    location = Column(String)

    # 6. The source medium (e.g., 'local_folder', 'database', 'email_attachment')
    source = Column(String)

    # 7. Department or team who owns this data (e.g., 'Finance', 'HR')
    owner = Column(String)

    # 8. Classification level of the data (e.g., 'Low', 'Medium', 'High')
    sensitivity = Column(String)

    # 9. Numerical risk value used to calculate global enterprise risk
    risk_score = Column(Integer)

    # 10. Auto-Timestamp: Automatically saves the exact moment this PII was found
    # 'default=datetime.utcnow' ensures we don't have to pass this manually in Python
    detected_at = Column(DateTime, default=datetime.utcnow)


# =========================================================
# PYDANTIC MODEL (For API Request Validation)
# =========================================================
# (Keeping this so the FastAPI /scan-results endpoint still accepts JSON safely)
class PIIRecordSchema(BaseModel):
    type: str
    value: str
    location: str
    source: str
    owner: str
    sensitivity: Literal["Low", "Medium", "High"]
    risk_score: int
    detected_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True

