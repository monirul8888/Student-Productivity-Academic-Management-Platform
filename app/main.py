from fastapi import FastAPI
from app.database import engine, Base  # Import Base from database.py
from app.routers import course
# Import other routers later: assignment, exam, note, auth

# Create all tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="StudyFlow SaaS",
    description="Student Productivity & Academic Management Platform",
    version="1.0.0"
)

# Include routers
app.include_router(course.router, prefix="/courses", tags=["Courses"])
# app.include_router(assignment.router, prefix="/assignments", tags=["Assignments"])
# app.include_router(exam.router, prefix="/exams", tags=["Exams"])
# app.include_router(note.router, prefix="/notes", tags=["Notes"])
# app.include_router(auth.router, prefix="/auth", tags=["Authentication"])

@app.get("/")
def home():
    return {"msg": "Welcome To Student Productivity & Academic Management Platform"}