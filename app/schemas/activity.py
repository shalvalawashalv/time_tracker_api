from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict, field_validator



class ActivityCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)

    @field_validator("name", mode="before")
    @classmethod
    def strip_name(cls, value: object) -> object:
        if isinstance(value, str):
            return value.strip()
        return value


class ActivityRead(BaseModel):
    id: UUID
    name: str
    model_config = ConfigDict(from_attributes=True)
