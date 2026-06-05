from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class AssignmentCreate(BaseModel):
    title: str
    deadline: datetime
    status: str = "pending"
    course_id: int


class AssignmentUpdate(BaseModel):
    title: Optional[str] = None
    deadline: Optional[datetime] = None
    status: Optional[str] = None


class AssignmentResponse(BaseModel):
    id: int
    title: str
    deadline: datetime
    status: str
    course_id: int

    model_config = ConfigDict(from_attributes=True)