from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.course import Course
from app.schemas.course import CourseCreate, CourseResponse
from app.utils.auth import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/", response_model=CourseResponse)
def create_course(
    course: CourseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_course = Course(
        name=course.name,
        teacher=course.teacher,
        semester=course.semester,
        credit=course.credit,
        description=course.description,
        user_id=current_user.id  # link course to user
    )

    db.add(db_course)
    db.commit()
    db.refresh(db_course)

    return db_course


@router.get("/", response_model=list[CourseResponse])
def get_courses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # only return courses for this user
    courses = db.query(Course).filter(Course.user_id == current_user.id).all()
    return courses


@router.get("/{course_id}", response_model=CourseResponse)
def get_single_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    course = db.query(Course).filter(
        Course.id == course_id,
        Course.user_id == current_user.id  # user can only access own courses
    ).first()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    return course