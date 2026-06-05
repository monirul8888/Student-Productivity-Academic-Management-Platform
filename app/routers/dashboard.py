from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.database import get_db
from app.models.course import Course
from app.models.assignment import Assignment
from app.utils.auth import get_current_user
from app.models.user import User

router = APIRouter()


@router.get("/summary")
def dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Count courses for this user
    total_courses = db.query(Course).filter(Course.user_id == current_user.id).count()

    # Count assignments for courses belonging to this user
    total_assignments = db.query(Assignment).join(Course).filter(
        Course.user_id == current_user.id
    ).count()

    completed_assignments = db.query(Assignment).join(Course).filter(
        Course.user_id == current_user.id,
        Assignment.status == "completed"
    ).count()

    pending_assignments = db.query(Assignment).join(Course).filter(
        Course.user_id == current_user.id,
        Assignment.status != "completed"
    ).count()

    today = datetime.now()
    week_later = today + timedelta(days=7)
    upcoming_deadlines = db.query(Assignment).join(Course).filter(
        Course.user_id == current_user.id,
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