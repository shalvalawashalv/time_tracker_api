from app.schemas.stats import ActivityStatsRead
from app.core.exception import DataConsistencyError
from app.services.time_session_service import get_sessions
from app.services.activity_service import get_activity

def get_stats_by_activity() -> list[ActivityStatsRead]:
    stats_by_activity_id = {}
    
    for session in get_sessions():
        if session.ended_at is None:
            continue

        activity_id = session.activity_id

        if activity_id not in stats_by_activity_id:
            stats_by_activity_id[activity_id] = {
                "total_seconds": 0,
                "sessions_count": 0,
            }

        stats_by_activity_id[activity_id]["total_seconds"] += session.duration_seconds
        stats_by_activity_id[activity_id]["sessions_count"] += 1

    result = []
    for activity_id, stats in stats_by_activity_id.items():
        activity = get_activity(activity_id)
        if activity is None:
            raise DataConsistencyError()

        activity_name = activity.name
        total_seconds = stats["total_seconds"]
        sessions_count = stats["sessions_count"]

        result.append(
            ActivityStatsRead(
                activity_id=activity_id,
                activity_name=activity_name,
                total_seconds=total_seconds,
                sessions_count=sessions_count,
            )
        )

    return result