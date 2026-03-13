"""
Pydantic data models for the application.
"""

from typing import Literal
from datetime import datetime
from pydantic import BaseModel, Field

class PIIRecord(BaseModel):
    """
    Pydantic model representing a single detected PII 
    (Personally Identifiable Information) record.

    Validates automatic JSON parsing and incoming data format 
    before it reaches the database.
    """
    type: str          # The type of PII (e.g., 'PAN', 'Aadhaar', 'Email')
    value: str         # The actual extracted data value (e.g., 'ABCDE1234F')
    location: str      # Where it was found (e.g., 'finance/data.xlsx' or a DB table)
    source: str        # The source medium (e.g., 'local_folder', 'email', 'database')
    owner: str         # The owner or department (e.g., 'Finance', 'HR')
    sensitivity: Literal["Low", "Medium", "High"]   # The sensitivity level (must be exact match)
    risk_score: int    # Calculated numeric risk score based on the data type
    detected_at: datetime = Field(default_factory=datetime.utcnow) # Automatically set when data was discovered

