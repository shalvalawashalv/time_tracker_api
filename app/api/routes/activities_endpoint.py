from fastapi import APIRouter, status, HTTPException

from app.schemas.activity import ActivityCreate, ActivityRead
from app.services.activity_service import create_activity, get_activity, get_activities


router = APIRouter(
    prefix="/activities",
    tags=["Activities"],
)


@router.get("/", response_model=list[ActivityRead])
def get_activities_endpoint():
    activities = get_activities()
    
    return activities

@router.get("/{activity_id}", response_model=ActivityRead)
def get_activity_endpoint(activity_id: int):
    activity = get_activity(activity_id)

    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    return activity


@router.post("/", response_model=ActivityRead, status_code=status.HTTP_201_CREATED)
def create_activity_endpoint(data: ActivityCreate):
    return create_activity(data)