from pydantic import BaseModel, Field

class ActivityCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)

class ActivityRead(BaseModel):
    id: int
    name: str

class Activity(BaseModel):
    id: int
    name: str