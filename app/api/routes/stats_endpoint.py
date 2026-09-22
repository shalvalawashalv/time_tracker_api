from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.stats import ActivityStatsRead
from app.services.stats_service import get_stats_by_activity



router = APIRouter(
    prefix="/stats",
    tags=["Stats"],
)


@router.get("/by-activity", response_model=list[ActivityStatsRead])
async def get_stats_by_activity_endpoint(
    db: AsyncSession = Depends(get_db),
) -> list[ActivityStatsRead]:
    return await get_stats_by_activity(db)
