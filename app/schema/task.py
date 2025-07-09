from pydantic import BaseModel, Field


class Task(BaseModel):
    id: int
    name: str
    pomodoro_count: int
    category_id: int = Field(exclude=True)
