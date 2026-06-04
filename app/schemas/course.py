from pydantic import BaseModel
from typing import Optional

class CourseCreate(BaseModel):
    name: str
    teacher: Optional[str] = None
    semester: Optional[str] = None
    credit: Optional[int] = None
    description: Optional[str] = None

class CourseResponse(BaseModel):
    id: int
    name: str
    teacher: Optional[str]
    semester: Optional[str]
    credit: Optional[int]
    description: Optional[str]

    class Config:
        from_attributes = True