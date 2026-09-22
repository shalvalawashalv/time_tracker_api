from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exception import UserAlreadyExistsError
from app.db.database import get_db
from app.schemas.user import UserRegistration, UserRead
from app.services.auth_service import registration



router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def registration_endpoint(
    data: UserRegistration,
    db: AsyncSession = Depends(get_db),
    ) -> UserRead:
    try:
        return await registration(db, data)
    except UserAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists",
        )
