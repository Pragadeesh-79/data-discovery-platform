from fastapi import APIRouter, File, UploadFile, Depends
from sqlalchemy.orm import Session
import os
import shutil
from datetime import datetime
from database.sqlite_db import get_db
from models.pii_model import PIIRecord
from detection.pii_detector import PIIDetector
from parsers.csv_parser import parse_csv
from parsers.pdf_parser import parse_pdf
from parsers.docx_parser import parse_docx
from parsers.excel_parser import parse_excel

router = APIRouter()
detector = PIIDetector()

PARSERS = {
    '.csv': parse_csv,
    '.pdf': parse_pdf,
    '.docx': parse_docx,
    '.xlsx': parse_excel,
    '.xls': parse_excel
}

@router.post('/scan/upload')
async def scan_file_upload(file: UploadFile = File(...), db: Session = Depends(get_db)):
    print(f'File received: {file.filename}')
    temp_dir = 'temp_uploads'
    os.makedirs(temp_dir, exist_ok=True)
    file_path = os.path.join(temp_dir, file.filename)
    with open(file_path, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
    ext = os.path.splitext(file.filename)[1].lower()
    if ext in PARSERS:
        text = PARSERS[ext](file_path)
    else:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f_in:
                text = f_in.read()
        except:
            text = ''
    if os.path.exists(file_path):
        os.remove(file_path)
    if not text.strip():
        return {
            'filename': file.filename,
            'message': 'No text extracted or unsupported file format.',
            'detected_records': []
        }
    result = detector.process_text(text, file.filename, 'File Upload')
    entities = result.get('entities', [])
    print('Detected entities:', entities)
    db_records = []
    for ent in entities:
        sensitivity = ent.get('classification', 'Unknown')
        final_sensitivity = 'Medium'
        if sensitivity == 'Highly Sensitive':
            risk_score = 10
            final_sensitivity = 'High'
        elif sensitivity == 'Sensitive':
            risk_score = 8
            final_sensitivity = 'High'
        elif sensitivity == 'Personal':
            risk_score = 5
            final_sensitivity = 'Medium'
        else:
            risk_score = 1
            final_sensitivity = 'Low'
        record = PIIRecord(
            type=ent.get('entity_type', 'Unknown'),
            value=ent.get('value', ''),
            location=f'/uploads/{file.filename}',
            source='File Upload',
            owner='System User',
            sensitivity=final_sensitivity,
            risk_score=risk_score,
            detected_at=datetime.utcnow()
        )
        db.add(record)
        db_records.append(record)
        print('Saving record:', record)
    db.commit()
    return {
        'filename': file.filename,
        'message': f'Successfully processed {file.filename}',
        'records_found': len(db_records),
        'detected_records': [
            {
                'type': r.type,
                'value': '****' + r.value[-4:] if len(r.value) > 4 else '****',
                'location': r.location,
                'sensitivity': r.sensitivity,
                'risk_score': r.risk_score
            } for r in db_records
        ]
    }
