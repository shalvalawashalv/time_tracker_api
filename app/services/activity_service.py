from uuid import UUID

from psycopg.errors import UniqueViolation
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.core.exception import ActivityAlreadyExistError
from app.db.models import Activity
from app.schemas.activity import ActivityCreate



def create_activity(
    db: Session,
    data: ActivityCreate,
) -> Activity:
    activity = Activity(name=data.name)
    db.add(activity)

    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        if (
            isinstance(exc.orig, UniqueViolation)
            and exc.orig.diag.constraint_name == "uq_activities_name"
        ):
            raise ActivityAlreadyExistError() from exc

        raise

    return activity


def get_activities(
    db: Session,
) -> list[Activity]:
    stmt = select(Activity)
    activities = db.scalars(stmt).all()

    return list(activities)


def get_activity(
    db: Session,
    activity_id: UUID,
) -> Activity | None:
    return db.get(Activity, activity_id)
