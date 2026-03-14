# 🛡️ DPDPA Data Discovery Platform

*This project was built during a 24-hour hackathon.*

## 1️⃣ Problem Statement

Organizations store vast amounts of unstructured and structured data across formats like PDFs, Excel sheets, CSV files, and Word documents. This data often contains sensitive Personally Identifiable Information (PII). Under regulations like India\'s **Digital Personal Data Protection Act (DPDPA)**, organizations must identify, classify, and protect personal data. Failing to do so can lead to severe penalties, non-compliance, and loss of customer trust. Manual discovery of PII across scattered enterprise data sources is time-consuming, prone to human error, and virtually impossible at scale.

## 2️⃣ Solution Overview

The **DPDPA Data Discovery Platform** is an automated scanning and classification system designed to help organizations discover sensitive personal data within their files. 

The platform automatically:
- **Scans** uploaded documents (CSV, PDF, Excel, Word).
- **Detects** sensitive PII (Aadhaar, PAN, Emails, Phone numbers, Names) using a robust regex-based engine.
- **Classifies** the sensitivity of the data and assigns a corresponding risk score.
- **Stores** findings in a centralized data inventory database.
- **Visualizes** analytics via an intuitive dashboard.
- **Generates** compliance reports aligned with DPDPA guidelines.

## 3️⃣ System Architecture

The platform follows a streamlined data processing pipeline:

`	ext
User Uploads File
       ↓
Frontend Scanner (HTML/JS)
       ↓
FastAPI Backend
       ↓
Parser Engine (CSV, PDF, Docx, Excel extractors)
       ↓
PII Detection Engine (Regex-based pattern matching)
       ↓
Classification Engine (Sensitivity & Risk Assignment)
       ↓
SQLite Database (Data Inventory)
       ↓
Dashboard Analytics (Visualization & Reporting)
`

## 4️⃣ Key Features

- **Automated PII Detection**: Rapidly identifies personal data stored in multi-format documents.
- **Regex-based Scanning Engine**: Highly accurate pattern matching for Indian-specific and standard PII.
- **Risk Scoring System**: Automatically assigns quantitative risk severity based on the type of data detected.
- **Data Inventory Tracking**: Maintains a structured log of all discovered PII, its location, and owner.
- **DPDPA Compliance Reporting**: Exportable reports tailored to audit and regulatory requirements.
- **Dashboard Visualization**: At-a-glance metrics covering risk distributions, data locations, and total PII records.
- **File Upload Scanning**: Easy drop-in interface for quick document analysis.
- **Real-time Analytics**: Instant feedback and score adjustment upon scanning new files.

## 5️⃣ Folder Structure

`	ext
data-discovery-platform/
│
├── backend/
│   ├── api/             # FastAPI route handlers
│   ├── detection/       # Regex rules and PII detectors
│   ├── parsers/         # Document parsers for CSV, PDF, etc.
│   ├── classification/  # Risk and sensitivity classifiers
│   ├── models/          # Data schemas 
│   ├── database/        # SQLite connection and setup
│   └── main.py          # FastAPI application entry point
│
├── frontend/
│   ├── index.html       # Dashboard view
│   ├── scan.html        # File upload and scanning interface
│   ├── css/             # Stylesheets (Bootstrap & custom)
│   └── js/              # Vanilla JS logic and API integration
│
├── data_sources/        # Sample datasets and directories
│
└── requirements.txt     # Python dependencies
`

## 6️⃣ Installation Guide

Follow these steps to run the platform locally:

### 1. Install Dependencies

Ensure you have Python 3.8+ installed, then run:

`ash
pip install -r requirements.txt
`

### 2. Run the Backend

Navigate to the backend directory and start the FastAPI server using Uvicorn:

`ash
cd backend
python -m uvicorn main:app --reload
`
*The backend will be available at http://localhost:8000*

### 3. Open the Frontend

You can run the frontend by serving the rontend folder using any static server, such as **VS Code Live Server**, or simply by opening index.html directly in your web browser.

## 7️⃣ API Endpoints

The backend provides a set of RESTful APIs to interface with the core engines:

- **POST /scan/upload**: Accepts a file upload, parses the text, scans for PII, classifies it, stores records in the DB, and returns the findings.
- **POST /scan-results**: Submits raw scan findings (from local/client scanning) into the database.
- **GET /inventory**: Retrieves the list of all detected PII records stored in the data inventory.
- **GET /risk-summary**: Returns aggregated risk scores and overall classification metrics for the organization.
- **GET /pii-types**: Provides a breakdown of the detected PII by its specific type (e.g., Aadhaar vs. Email).
- **GET /dpdpa-report**: Generates a consolidated compliance report structured for DPDPA requirements.
- **GET /dashboard-stats**: Fetches KPI statistics like total files scanned, total PII found, and high-risk alerts for the main dashboard.

## 8️⃣ Risk Scoring System

The classification engine evaluates the sensitivity of detected data and assigns a risk score. This helps prioritize data protection efforts.

| Data Type | Example | Risk Score | Sensitivity |
|-----------|---------|------------|-------------|
| **Aadhaar** | XXXX-XXXX-XXXX | **10** | Highly Sensitive |
| **PAN** | ABCDE1234F | **8** | Sensitive |
| **Phone** | +91-9876543210 | **4** | Personal |
| **Email** | user@domain.com | **3** | Personal |
| **Name** | John Doe | **1** | Low |

## 9️⃣ Dashboard Features

The analytical frontend dashboard offers:
- **Total PII Records**: A high-level count of total sensitive entities discovered.
- **Risk Score Summary**: An aggregated gauge of the organization\'s overall data risk health.
- **PII Distribution Charts**: Visual breakdowns of data types found across the system.
- **Compliance Status**: A quick indicator of DPDPA alignment based on current data holdings.

## 🔟 Future Improvements

While this is a functional hackathon prototype, future enhancements could include:
- **AI NLP Detection**: Incorporating Machine Learning (like SpaCy or Transformers) to detect context-based PII beyond predefined regex patterns.
- **Cloud Storage Scanning**: Connecting directly to AWS S3, Azure Blob, or Google Drive for continuous scanning.
- **Enterprise Integrations**: Connecting with Active Directory, Jira, or Outlook.
- **Authentication**: Admin login pages and secure token-based API access.
- **Role-based Access Control (RBAC)**: Providing different views for Data Protection Officers (DPOs), Admins, and regular users.

## 📝 License

This project is licensed under the **MIT License**.
