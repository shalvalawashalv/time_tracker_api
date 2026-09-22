from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exception import ActivityAlreadyExistError
from app.db.database import get_db
from app.schemas.activity import ActivityCreate, ActivityRead
from app.services.activity_service import (
    create_activity,
    get_activity,
    get_activities,
)



router = APIRouter(
    prefix="/activities",
    tags=["Activities"],
)


@router.get("/", response_model=list[ActivityRead])
async def get_activities_endpoint(
    db: AsyncSession = Depends(get_db),
):
    return await get_activities(db)


@router.get("/{activity_id}", response_model=ActivityRead)
async def get_activity_endpoint(
    activity_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    activity = await get_activity(db, activity_id)

    if activity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found",
        )
    
    return activity


@router.post("/", response_model=ActivityRead, status_code=status.HTTP_201_CREATED)
async def create_activity_endpoint(
    data: ActivityCreate,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await create_activity(db, data)
    except ActivityAlreadyExistError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Activity already exists",
        )
