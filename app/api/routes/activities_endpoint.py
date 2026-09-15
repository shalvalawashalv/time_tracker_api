from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

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
def get_activities_endpoint(
    db: Session = Depends(get_db),
):
    return get_activities(db)


@router.get("/{activity_id}", response_model=ActivityRead)
def get_activity_endpoint(
    activity_id: UUID,
    db: Session = Depends(get_db),
):
    activity = get_activity(db, activity_id)

    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    return activity


@router.post("/", response_model=ActivityRead, status_code=status.HTTP_201_CREATED)
def create_activity_endpoint(
    data: ActivityCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_activity(db, data)
    except ActivityAlreadyExistError:
        raise HTTPException(status_code=409, detail="Activity already exists")
