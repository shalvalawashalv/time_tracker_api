from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

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


@router.get("/", response_model=list[TimeSessionRead])
async def get_sessions_endpoint(
    activity_id: UUID | None = None,
    is_active: bool | None = None,
    db: AsyncSession = Depends(get_db),
):
    try:
        result = await get_sessions(db, activity_id, is_active)
    except ActivityNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found",
        )

    return result


@router.get("/{session_id}", response_model=TimeSessionRead)
async def get_session_endpoint(
    session_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    try:
        session = await get_session(db, session_id)
    except SessionNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found",
        )

    return session


@router.post("/start", response_model=TimeSessionRead, status_code=status.HTTP_201_CREATED)
async def start_session_endpoint(
    data: TimeSessionStart,
    db: AsyncSession = Depends(get_db),
):
    try:
        session = await start_session(db, data)
    except ActivityNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found",
        )
    except ActiveSessionAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Active session already exists",
        )
    
    return session


@router.post("/{session_id}/stop", response_model=TimeSessionRead)
async def stop_session_endpoint(
    session_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    try:
        session = await stop_session(db, session_id)
    except SessionNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found",
        )
    except SessionAlreadyStoppedError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Session is already stopped",
        )
    
    return session


@router.patch("/{session_id}/comment", response_model=TimeSessionRead)
async def patch_comment_endpoint(
    session_id: UUID,
    comment: TimeSessionComment,
    db: AsyncSession = Depends(get_db),
):
    try:
        session = await patch_comment(db, session_id, comment.comment)
    except SessionNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found",
        )
    except SessionNotCompletedError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot update comment before session is stopped",
        )
    
    return session
