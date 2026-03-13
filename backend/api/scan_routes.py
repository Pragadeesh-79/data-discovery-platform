"""
Routes for handling scan operations and result ingestion.
"""

from fastapi import APIRouter, HTTPException, status, UploadFile, File
import os
import shutil
from pydantic import BaseModel
from models.pii_model import PIIRecord
from database.mongo_client import pii_inventory, sample_data_sources, check_db_connection
import pymongo.errors
from detection.pii_detector import PIIDetector

router = APIRouter()

@router.get("/scan/local")
def scan_local_data():
    if not check_db_connection():
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to connect to MongoDB Atlas"
        )
        
    try:
        sources = list(sample_data_sources.find({}))
        detector = PIIDetector()
        
        all_results = []
        files_processed = 0
        
        for source in sources:
            file_name = source.get("file_name", "unknown")
            text_data = source.get("data", "")
            source_type = source.get("source_type", "unknown")
            
            result = detector.process_text(text_data, file_name, source_type)
            all_results.append(result)
            files_processed += 1
            
        return {
            "files_processed": files_processed,
            "results": all_results
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during scan: {str(e)}"
        )

@router.post("/scan/upload")
async def scan_uploaded_file(file: UploadFile = File(...)):
    if not check_db_connection():
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to connect to MongoDB Atlas"
        )

    upload_dir = os.path.join(os.path.dirname(__file__), "..", "uploads")
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        text_data = ""
        ext = file.filename.lower().split('.')[-1]
        
        if ext == "pdf":
            from parsers.pdf_parser import parse_pdf
            text_data = parse_pdf(file_path)
        elif ext == "csv":
            from parsers.csv_parser import parse_csv
            text_data = parse_csv(file_path)
        elif ext == "docx":
            from parsers.docx_parser import parse_docx
            text_data = parse_docx(file_path)
        elif ext in ["xls", "xlsx"]:
            from parsers.excel_parser import parse_excel
            text_data = parse_excel(file_path)
        else:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                text_data = f.read()
                
        if not text_data or not text_data.strip():
            raise ValueError("Parsed text is empty or file format is unsupported.")
            
        detector = PIIDetector()
        result = detector.process_text(text_data, file.filename, "uploaded")
        
        return result
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing the uploaded file: {str(e)}"
        )
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


@router.post("/scan-results")
def save_scan_result(record: PIIRecord):
    if not check_db_connection():
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to connect to MongoDB Atlas"
        )
        
    try:
        record_dict = record.model_dump() if hasattr(record, "model_dump") else record.dict()
        pii_inventory.insert_one(record_dict)
        return {"message": "PII record stored successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while saving the record: {str(e)}"
        )
