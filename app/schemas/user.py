from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field, field_validator



class UserRegistration(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8)

    @field_validator("username", mode="before")
    @classmethod
    def normalize_username(cls, value: object) -> object:
        if isinstance(value, str):
            username = value.strip().lower()
            

            if any(ch.isspace() for ch in username):
                raise ValueError(
                    "Имя пользователя не должно содержать пробелы"
                )

            return username

        return value


class UserRead(BaseModel):
    id: UUID
    username: str
    created_at: datetime
