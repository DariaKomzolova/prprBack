from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud
import schemas
import database

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/programs")
def read_programs(db: Session = Depends(get_db)):
    return crud.get_programs(db)

@router.post("/programs")
def create_program(program: schemas.Program, db: Session = Depends(get_db)):
    crud.create_program(db, program)
    return {"message": "Program created"}

@router.put("/programs/{name}")
def update_program(name: str, program: schemas.Program, db: Session = Depends(get_db)):
    result = crud.update_program(db, name, program)
    if not result:
        raise HTTPException(status_code=404, detail="Program not found")
    return {"message": "Program updated"}

@router.delete("/programs/{name}")
def delete_program(name: str, db: Session = Depends(get_db)):
    if not crud.delete_program(db, name):
        raise HTTPException(status_code=404, detail="Program not found")
    return {"message": "Program deleted"}
