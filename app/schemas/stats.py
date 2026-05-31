from pydantic import BaseModel

class ActivityStatsRead(BaseModel):
    activity_id: int
    activity_name: str
    total_second: int
    sessions_count: int