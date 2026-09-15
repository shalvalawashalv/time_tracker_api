from uuid import UUID

from pydantic import BaseModel



class ActivityStatsRead(BaseModel):
    activity_id: UUID
    activity_name: str
    total_seconds: int
    sessions_count: int
