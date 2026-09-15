from sqlalchemy.orm import Session
from sqlalchemy import select, func

from app.db.models import Activity, TimeSession
from app.schemas.stats import ActivityStatsRead



def get_stats_by_activity(
    db: Session,
) -> list[ActivityStatsRead]:
    stmt = (
        select(
            Activity.id.label("activity_id"),
            Activity.name.label("activity_name"),
            func.sum(TimeSession.duration_seconds).label("total_seconds"),
            func.count(TimeSession.id).label("sessions_count"),
        )
        .join(TimeSession, TimeSession.activity_id == Activity.id)
        .where(TimeSession.ended_at.is_not(None))
        .group_by(Activity.id)
    )

    rows = db.execute(stmt).all()

    return [
        ActivityStatsRead(
            activity_id=row.activity_id,
            activity_name=row.activity_name,
            total_seconds=row.total_seconds,
            sessions_count=row.sessions_count,
        )
        for row in rows
    ]
