from app.schemas.time_session import TimeSession, TimeSessionStart, TimeSessionComment
from app.core.exception  import ActivityNotFoundError, ActiveSessionAlreadyExistsError, SessionNotFoundError, SessionAlreadyStoppedError, SessionNotCompletedError
from app.services.activity_service import get_activity
from datetime import datetime, timezone

sessions: dict[int, TimeSession] = {}
next_session_id = 1


def get_activity_session():
    for session in sessions:
        if session["ended_at"] is None:
            return session
    
    return None


def start_session(data: TimeSessionStart) -> TimeSession:
    global next_session_id

    if get_activity(data.activity_id) is None:
        raise ActivityNotFoundError
    
    if get_activity_session() is not None:
        raise ActiveSessionAlreadyExistsError
    
    started_at = datetime.now(timezone.utc)

    session = TimeSession(
        id=next_session_id,
        activity_id=data.activity_id,
        started_at=started_at,
        ended_at=None,
        duration_second=None,
        comment=None
    )

    sessions[next_session_id] = session
    next_session_id += 1

    return session

def stop_session(session_id: int) -> TimeSession:
    session = sessions.get(session_id)

    if session is None:
        raise SessionNotFoundError
    
    if session["ended_at"] is not None:
        raise SessionAlreadyStoppedError
    
    ended_at = datetime.now(timezone.utc)
    duration_seconds = int((ended_at - session["started_at"]).total_seconds())

    session["ended_at"] = ended_at
    session["duration_seconds"] = duration_seconds
    
    return session


def get_sessions() -> list[TimeSession]:
    return list(sessions.values())

def get_session(session_id: int) -> TimeSession:
    session = sessions.get(session_id)
    if session is None:
        raise SessionNotFoundError
    
    return session


def patch_comment(session_id: int, comment: str):
    session = sessions.get(session_id)

    if session is None:
        raise SessionNotFoundError
    
    if get_activity_session() is not None:
        raise SessionNotCompletedError
    
    session["comment"] = comment
    
    return session