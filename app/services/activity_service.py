from uuid import UUID

from psycopg.errors import UniqueViolation
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.core.exception import ActivityAlreadyExistError
from app.db.models import Activity
from app.schemas.activity import ActivityCreate



async def get_activities(
    db: AsyncSession,
) -> list[Activity]:
    stmt = select(Activity)
    result = await db.scalars(stmt)
    activities = result.all()

    return list(activities)


async def get_activity(
    db: AsyncSession,
    activity_id: UUID,
) -> Activity | None:
    return await db.get(Activity, activity_id)


async def create_activity(
    db: AsyncSession,
    data: ActivityCreate,
) -> Activity:
    activity = Activity(name=data.name)
    db.add(activity)

    try:
        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        if (
            isinstance(exc.orig, UniqueViolation)
            and exc.orig.diag.constraint_name == "uq_activities_name"
        ):
            raise ActivityAlreadyExistError() from exc

        raise

    return activity
    