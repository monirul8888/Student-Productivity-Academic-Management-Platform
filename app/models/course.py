from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    teacher = Column(String, nullable=True)
    semester = Column(String, nullable=True)
    credit = Column(Integer, nullable=True)
    description = Column(String, nullable=True)

    assignments = relationship(
        "Assignment",
        back_populates="course",
        cascade="all, delete"
    )