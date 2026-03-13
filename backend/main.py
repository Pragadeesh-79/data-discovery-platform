"""
DPDPA Data Discovery Platform - Backend
This is the main entry point for the FastAPI application.

This prototype is built to scan enterprise data sources, detect personal data (PII),
calculate risk scores, and generate DPDPA compliance reports.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import our scan routes router from the api module
from api.scan_routes import router as scan_router

# Initialize the FastAPI app
# Title and version will appear in the automatically generated Swagger UI API documentation
app = FastAPI(
    title="DPDPA Data Discovery Platform API",
    description="Backend API for scanning data sources, detecting PII, risk scoring, and compliance reporting.",
    version="1.0"
)

# Configure CORS (Cross-Origin Resource Sharing)
# This is required so our frontend (running on a different port/domain) can talk to this backend API.
# Using ["*"] allows all origins, which is good for local development and hackathons.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# ---------------------------------------------------------
# Register API Routers
# ---------------------------------------------------------

# Include all routes defined in api/scan_routes.py
app.include_router(scan_router)

# ---------------------------------------------------------
# API Endpoints
# ---------------------------------------------------------

@app.get("/")
async def root():
    """
    Health check endpoint.
    A simple GET request to the root URL to verify the server is running.
    """
    return {
        "message": "DPDPA Data Discovery Backend Running"
    }


@app.get("/status")
async def get_status():
    """
    Test endpoint for system status.
    Returns the operational status and current version of the API.
    """
    return {
        "status": "Backend API is running",
        "version": "1.0"
    }
