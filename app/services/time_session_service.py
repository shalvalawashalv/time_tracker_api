from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exception import (
    ActivityNotFoundError,
    ActiveSessionAlreadyExistsError,
    SessionNotFoundError,
    SessionAlreadyStoppedError,
    SessionNotCompletedError,
)
from app.db.models import TimeSession
from app.schemas.time_session import TimeSessionStart
from app.services.activity_service import get_activity



def get_sessions(
    db: Session,
    activity_id: UUID | None = None,
    is_active: bool | None = None,
) -> list[TimeSession]:
    stmt = select(TimeSession)

    if activity_id is not None:
        if get_activity(db, activity_id) is None:
            raise ActivityNotFoundError()

        stmt = stmt.where(TimeSession.activity_id == activity_id)

    if is_active is True:
        stmt = stmt.where(TimeSession.ended_at.is_(None))
    elif is_active is False:
        stmt = stmt.where(TimeSession.ended_at.is_not(None))

    return list(db.scalars(stmt).all())


def get_session(
    db: Session,
    session_id: UUID,
) -> TimeSession:
    session = db.get(TimeSession, session_id)

    if session is None:
        raise SessionNotFoundError()
    
    return session


def start_session(
    db: Session,
    data: TimeSessionStart,
) -> TimeSession:
    if get_activity(db, data.activity_id) is None:
        raise ActivityNotFoundError()
    
    if get_sessions(db, is_active=True):
        raise ActiveSessionAlreadyExistsError()

    session = TimeSession(activity_id=data.activity_id)

    db.add(session)
    db.commit()

    return session


def stop_session(
    db: Session,
    session_id: UUID,
) -> TimeSession:
    session = db.get(TimeSession, session_id)

    if session is None:
        raise SessionNotFoundError()
    
    if session.ended_at is not None:
        raise SessionAlreadyStoppedError()
    
    ended_at = datetime.now(timezone.utc)
    duration_seconds = int((ended_at - session.started_at).total_seconds())

    session.ended_at = ended_at
    session.duration_seconds = duration_seconds

    db.commit()
    
    return session


def patch_comment(
    db: Session,
    session_id: UUID,
    comment: str,
) -> TimeSession:
    session = db.get(TimeSession, session_id)

    if session is None:
        raise SessionNotFoundError()
    
    if session.ended_at is None:
        raise SessionNotCompletedError()
    
    session.comment = comment
    db.commit()
    
    return session
