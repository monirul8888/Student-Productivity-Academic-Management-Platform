from fastapi import FastAPI
from app.database import engine, Base  # Base from database.py
from app.routers import course, assignments, dashboard, auth # Include assignments router now

# Create all tables
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="StudyFlow SaaS",
    description="Student Productivity & Academic Management Platform",
    version="1.0.0"
)


# Include routers
app.include_router(course.router, prefix="/courses", tags=["Courses"])
app.include_router(assignments.router, prefix="/assignments", tags=["Assignments"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])

@app.get("/")
def home():
    return {"msg": "Welcome To Student Productivity & Academic Management Platform"}