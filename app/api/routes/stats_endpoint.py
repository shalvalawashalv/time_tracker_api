from fastapi import APIRouter, HTTPException

from app.core.exception import DataConsistencyError
from app.schemas.stats import ActivityStatsRead
from app.services.stats_service import get_stats_by_activity

router = APIRouter(
    prefix="/stats",
    tags=["Stats"]
)

@router.get("/by-activity", response_model=list[ActivityStatsRead])
def get_stats_by_activity_endpoint() -> list[ActivityStatsRead]:
    try:
        return get_stats_by_activity()
    except DataConsistencyError():
        raise HTTPException(status_code=500, detail="Internal data consistency erro")