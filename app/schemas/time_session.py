from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, ConfigDict



class TimeSessionRead(BaseModel):
    id: UUID
    activity_id: UUID
    started_at: datetime
    ended_at: datetime | None
    duration_seconds: int | None
    comment: str | None
    model_config = ConfigDict(from_attributes=True)


class TimeSessionStart(BaseModel):
    activity_id: UUID


class TimeSessionComment(BaseModel):
    comment: str
