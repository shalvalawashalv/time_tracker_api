from pydantic import BaseModel
from datetime import datetime

class TimeSession(BaseModel):
    id: int
    activity_id: int
    started_at: datetime
    ended_at: datetime | None
    duration_second: int | None
    comment: str | None

class TimeSessionStart(BaseModel):
    activity_id: int

class TimeSessionComment(BaseModel):
    comment: str