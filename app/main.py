from fastapi import FastAPI, Depends
from .database import get_db, engine
from sqlalchemy.orm import Session

from . import models

app = FastAPI()
models.Base.metadata.create_all(bind = engine)


@app.get("/")
def home(db : Session = Depends(get_db) ):
    return {"msg" : "Welcome To Student Productivity & Academic Management Platform"}