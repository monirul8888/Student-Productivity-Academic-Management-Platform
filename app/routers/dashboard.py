from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.database import get_db
from app.models.course import Course
from app.models.assignment import Assignment
# If auth ready, import get_current_user

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/summary")
def dashboard_summary(db: Session = Depends(get_db)):
    total_courses = db.query(Course).count()
    total_assignments = db.query(Assignment).count()
    completed_assignments = db.query(Assignment).filter(Assignment.status == "completed").count()
    pending_assignments = db.query(Assignment).filter(Assignment.status != "completed").count()

    today = datetime.now()
    week_later = today + timedelta(days=7)
    upcoming_deadlines = db.query(Assignment).filter(
        Assignment.deadline >= today,
        Assignment.deadline <= week_later
    ).count()

    return {
        "total_courses": total_courses,
        "total_assignments": total_assignments,
        "completed_assignments": completed_assignments,
        "pending_assignments": pending_assignments,
        "upcoming_deadlines_this_week": upcoming_deadlines
    }