from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.assignment import Assignment
from app.models.course import Course
from app.schemas.assignment import AssignmentCreate, AssignmentUpdate, AssignmentResponse
from app.utils.auth import get_current_user
from app.models.user import User

router = APIRouter()


# Create assignment
@router.post("/", response_model=AssignmentResponse)
def create_assignment(
    data: AssignmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verify the course exists and belongs to the current user
    course = db.query(Course).filter(
        Course.id == data.course_id,
        Course.user_id == current_user.id
    ).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found or not owned by user")

    assignment = Assignment(
        title=data.title,
        deadline=data.deadline,
        status=data.status,
        course_id=data.course_id
    )

    db.add(assignment)
    db.commit()
    db.refresh(assignment)

    return assignment


# List all assignments of the current user
@router.get("/", response_model=list[AssignmentResponse])
def get_assignments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    assignments = db.query(Assignment).join(Course).filter(
        Course.user_id == current_user.id
    ).all()
    return assignments


# Update assignment
@router.put("/{assignment_id}", response_model=AssignmentResponse)
def update_assignment(
    assignment_id: int,
    data: AssignmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    assignment = db.query(Assignment).join(Course).filter(
        Assignment.id == assignment_id,
        Course.user_id == current_user.id
    ).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found or not owned by user")

    if data.title is not None:
        assignment.title = data.title
    if data.deadline is not None:
        assignment.deadline = data.deadline
    if data.status is not None:
        assignment.status = data.status

    db.commit()
    db.refresh(assignment)

    return assignment


# Delete assignment
@router.delete("/{assignment_id}")
def delete_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    assignment = db.query(Assignment).join(Course).filter(
        Assignment.id == assignment_id,
        Course.user_id == current_user.id
    ).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found or not owned by user")

    db.delete(assignment)
    db.commit()

    return {"message": "Assignment deleted successfully"}