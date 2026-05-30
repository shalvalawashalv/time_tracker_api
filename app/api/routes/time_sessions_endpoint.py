from fastapi import APIRouter, HTTPException, status

from app.core.exception import ActivityNotFoundError, ActiveSessionAlreadyExistsError, SessionNotFoundError, SessionAlreadyStoppedError, SessionNotCompletedError
from app.schemas.time_session import TimeSession, TimeSessionStart, TimeSessionComment
from app.services.time_session_service import start_session, stop_session, get_session, get_sessions, patch_comment


router = APIRouter(
    prefix="/sessions",
    tags=["Sessions"],
)


@router.post("/start", response_model=TimeSession, status_code=status.HTTP_201_CREATED)
def start_session_endpoint(data: TimeSessionStart):
    try:
        session = start_session(data)
    except ActivityNotFoundError:
        raise HTTPException(status_code=404, detail="Activity not found")
    except ActiveSessionAlreadyExistsError:
        raise HTTPException(status_code=409, detail="Active session already exists")
    
    return session

@router.post("/{session_id}/stop", response_model=TimeSession)
def stop_session_endpoint(session_id: int):
    try:
        session = stop_session(session_id)
    except SessionNotFoundError:
        raise HTTPException(status_code=404, detail="Session not found")
    except SessionAlreadyStoppedError:
        raise HTTPException(status_code=409, detail="Session is already stopped")
    
    return session


@router.get("/", response_model=list[TimeSession])
def get_sessions_endpoint(
    activity_id: int | None = None,
    is_active: bool | None = None,
    ):

    try:
        result = get_sessions(activity_id, is_active)
    except ActivityNotFoundError:
        raise HTTPException(status_code=404, detail="Activity not found")

    return result

@router.get("/{session_id}", response_model=TimeSession)
def get_session_endpoint(session_id: int):
    try:
        session = get_session(session_id)
    except SessionNotFoundError:
        raise HTTPException(status_code=404, detail="Session not found")

    return session


@router.patch("/{session_id}/comment", response_model=TimeSession)
def patch_comment_endpoint(session_id: int, comment: TimeSessionComment):
    try:
        session = patch_comment(session_id, comment.comment)
    except SessionNotFoundError:
        raise HTTPException(status_code=404, detail="Session not found")
    except SessionNotCompletedError:
        raise HTTPException(status_code=409, detail="Cannot update comment before session is stopped")
    
    return session
