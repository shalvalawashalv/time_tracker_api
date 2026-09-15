from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.exception import (
    ActivityNotFoundError,
    ActiveSessionAlreadyExistsError,
    SessionNotFoundError,
    SessionAlreadyStoppedError,
    SessionNotCompletedError,
)
from app.db.database import get_db
from app.schemas.time_session import (
    TimeSessionRead,
    TimeSessionStart,
    TimeSessionComment,
)
from app.services.time_session_service import (
    start_session,
    stop_session,
    get_session,
    get_sessions,
    patch_comment,
)



router = APIRouter(
    prefix="/sessions",
    tags=["Sessions"],
)


@router.post("/start", response_model=TimeSessionRead, status_code=status.HTTP_201_CREATED)
def start_session_endpoint(
    data: TimeSessionStart,
    db: Session = Depends(get_db),
):
    try:
        session = start_session(db, data)
    except ActivityNotFoundError:
        raise HTTPException(status_code=404, detail="Activity not found")
    except ActiveSessionAlreadyExistsError:
        raise HTTPException(status_code=409, detail="Active session already exists")
    
    return session


@router.post("/{session_id}/stop", response_model=TimeSessionRead)
def stop_session_endpoint(
    session_id: UUID,
    db: Session = Depends(get_db),
):
    try:
        session = stop_session(db, session_id)
    except SessionNotFoundError:
        raise HTTPException(status_code=404, detail="Session not found")
    except SessionAlreadyStoppedError:
        raise HTTPException(status_code=409, detail="Session is already stopped")
    
    return session


@router.get("/", response_model=list[TimeSessionRead])
def get_sessions_endpoint(
    activity_id: UUID | None = None,
    is_active: bool | None = None,
    db: Session = Depends(get_db),
):
    try:
        result = get_sessions(db, activity_id, is_active)
    except ActivityNotFoundError:
        raise HTTPException(status_code=404, detail="Activity not found")

    return result


@router.get("/{session_id}", response_model=TimeSessionRead)
def get_session_endpoint(
    session_id: UUID,
    db: Session = Depends(get_db),
):
    try:
        session = get_session(db, session_id)
    except SessionNotFoundError:
        raise HTTPException(status_code=404, detail="Session not found")

    return session


@router.patch("/{session_id}/comment", response_model=TimeSessionRead)
def patch_comment_endpoint(
    session_id: UUID,
    comment: TimeSessionComment,
    db: Session = Depends(get_db),
):
    try:
        session = patch_comment(db, session_id, comment.comment)
    except SessionNotFoundError:
        raise HTTPException(status_code=404, detail="Session not found")
    except SessionNotCompletedError:
        raise HTTPException(status_code=409, detail="Cannot update comment before session is stopped")
    
    return session
