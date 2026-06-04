from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

url = "postgresql://postgres:1234@localhost/studyflow_db"

engine = create_engine(url)
sessionLocal = sessionmaker(autocommit = False, autoflush=False,  bind=engine )

Base = declarative_base()



def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()