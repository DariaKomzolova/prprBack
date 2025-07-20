from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import database 
from crud import set_deadline, get_deadline

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/deadlines/set")
def set_deadline_api(data: dict, db: Session = Depends(get_db)):
    set_deadline(db, data["start"], data["end"])
    return {"message": "Deadline updated"}

@router.get("/deadlines/get")
def get_deadline_api(db: Session = Depends(get_db)):
    deadline = get_deadline(db)
    return {"start": deadline.start, "end": deadline.end} if deadline else {"start": None, "end": None}
