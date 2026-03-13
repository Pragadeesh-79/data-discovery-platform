from fastapi import APIRouter, HTTPException
from reporting.heatmap_report import generate_heatmap_data
import logging

# Set up logging
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/reports/heatmap")
def get_heatmap_data():
    """
    Endpoint to retrieve aggregated sensitive data counts by source folder.
    This data powers the Heatmap Dashboard.
    """
    try:
        heatmap_data = generate_heatmap_data()
        return heatmap_data
    except Exception as e:
        logger.error(f"Error generating heatmap data: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate heatmap data: {str(e)}"
        )
