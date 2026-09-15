from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.stats import ActivityStatsRead
from app.services.stats_service import get_stats_by_activity



router = APIRouter(
    prefix="/stats",
    tags=["Stats"],
)


@router.get("/by-activity", response_model=list[ActivityStatsRead])
def get_stats_by_activity_endpoint(
    db: Session = Depends(get_db),
) -> list[ActivityStatsRead]:
    return get_stats_by_activity(db)
