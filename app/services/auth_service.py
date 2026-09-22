from uuid import UUID
from asyncio import to_thread

from psycopg.errors import UniqueViolation
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exception import UserAlreadyExistsError
from app.core.security import hash_password, verify_password
from app.db.models import User
from app.schemas.user import UserRegistration



async def registration(
        db: AsyncSession,
        data: UserRegistration
    ) -> User:
    stmt = select(User).where(User.username == data.username)
    result = await db.execute(stmt)
    existing_user = result.scalar_one_or_none()

    if existing_user is not None:
        raise UserAlreadyExistsError(data.username)

    password_hash = await to_thread(hash_password, data.password)

    user = User(
        username=data.username,
        password_hash=password_hash,
    )

    db.add(user)
    try:
        await db.commit()
    except IntegrityError as exc:
        await db.rollback()

        if (
            isinstance(exc.orig, UniqueViolation)
            and exc.orig.diag.constraint_name == "uq_users_username"
        ):
            raise UserAlreadyExistsError(data.username) from exc

        raise


    await db.refresh(user)

    return user
