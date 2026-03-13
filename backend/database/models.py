from typing import Optional
from pydantic import BaseModel, Field

class EncryptedPIIRecord(BaseModel):
    """
    Data model for storing encrypted sensitive information into the database.
    Requires text to be processed before storage to meet DPDPA compliance.
    """
    file_name: str
    source: str
    entity_type: str
    encrypted_value: str
    classification: str
    timestamp: str

class SampleDataSource(BaseModel):
    """
    Data model representing a simulated data source loaded into MongoDB
    for detection analysis.
    """
    source_type: str
    file_name: str
    data: str
