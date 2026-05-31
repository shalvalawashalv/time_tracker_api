from datetime import datetime, timezone

from app.core.exception import ActivityNotFoundError, ActiveSessionAlreadyExistsError, SessionNotFoundError, SessionAlreadyStoppedError, SessionNotCompletedError
from app.schemas.time_session import TimeSession, TimeSessionStart
from app.services.activity_service import get_activity

sessions: dict[int, TimeSession] = {}
next_session_id: int = 1


def get_active_session() -> TimeSession | None:
    for session in sessions.values():
        if session.ended_at is None:
            return session
    
    return None


def get_sessions(activity_id: int | None = None, is_active: bool | None = None) -> list[TimeSession]:
    result = list(sessions.values())

    if activity_id is not None:
        activity = get_activity(activity_id)

        if activity is None:
            raise ActivityNotFoundError()
        result = [
            session 
            for session in result
            if session.activity_id == activity_id
            ]
    
    if is_active is not None:
        result = [
            session
            for session in result
            if (session.ended_at is None) == is_active
        ]

    return result
         

def get_session(session_id: int) -> TimeSession:
    session = sessions.get(session_id)
    if session is None:
        raise SessionNotFoundError()
    
    return session


def start_session(data: TimeSessionStart) -> TimeSession:
    global next_session_id

    if get_activity(data.activity_id) is None:
        raise ActivityNotFoundError()
    
    if get_active_session() is not None:
        raise ActiveSessionAlreadyExistsError()
    
    started_at = datetime.now(timezone.utc)

    session = TimeSession(
        id=next_session_id,
        activity_id=data.activity_id,
        started_at=started_at,
        ended_at=None,
        duration_seconds=None,
        comment=None
    )

    sessions[next_session_id] = session
    next_session_id += 1

    return session

def stop_session(session_id: int) -> TimeSession:
    session = sessions.get(session_id)

    if session is None:
        raise SessionNotFoundError()
    
    if session.ended_at is not None:
        raise SessionAlreadyStoppedError()
    
    ended_at = datetime.now(timezone.utc)
    duration_seconds = int((ended_at - session.started_at).total_seconds())

    session.ended_at = ended_at
    session.duration_seconds = duration_seconds
    
    return session


def patch_comment(session_id: int, comment: str) -> TimeSession:
    session = sessions.get(session_id)

    if session is None:
        raise SessionNotFoundError()
    
    if session.ended_at is None:
        raise SessionNotCompletedError()
    
    session.comment = comment
    
    return session
