from sqlalchemy.orm import Session
from models import User, Deadline, StudentChoice
import models
import schemas
from fastapi import FastAPI, Depends, HTTPException
from schemas import StudentChoiceBase, StudentChoiceUpdate


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_programs(db: Session):
    return db.query(models.ProgramDB).all()

def create_program(db: Session, program: schemas.Program):
    db_program = models.ProgramDB(**program.dict())
    db.add(db_program)
    db.commit()

def update_program(db: Session, name: str, program: schemas.Program):
    db_program = db.query(models.ProgramDB).filter(models.ProgramDB.name == name).first()
    if db_program:
        db_program.tech = program.tech
        db_program.hum = program.hum
        db.commit()
        return db_program
    return None

def delete_program(db: Session, name: str):
    db_program = db.query(models.ProgramDB).filter(models.ProgramDB.name == name).first()
    if db_program:
        db.delete(db_program)
        db.commit()
        return True
    return False

def set_deadline(db: Session, start: str, end: str):
    deadline = db.query(Deadline).filter(Deadline.id == 1).first()
    if deadline:
        deadline.start = start
        deadline.end = end
    else:
        deadline = Deadline(id=1, start=start, end=end)
        db.add(deadline)
    db.commit()

def get_deadline(db: Session):
    return db.query(Deadline).first()

def get_student_choice(db: Session, email: str):
    return db.query(StudentChoice).filter(StudentChoice.email == email).first()



def create_student_choice(db: Session, choice: StudentChoiceBase):
    db_choice = StudentChoice(email=choice.email, year=choice.year)
    db.add(db_choice)
    db.commit()
    db.refresh(db_choice)
    return db_choice

def update_student_choice(db, data):
    choice = db.query(StudentChoice).filter(StudentChoice.email == data.email).first()
    if not choice:
        return None

    choice.tech1 = data.tech1
    choice.tech2 = data.tech2
    choice.tech3 = data.tech3
    choice.tech4 = data.tech4
    choice.tech5 = data.tech5

    choice.hum1 = data.hum1
    choice.hum2 = data.hum2
    choice.hum3 = data.hum3
    choice.hum4 = data.hum4
    choice.hum5 = data.hum5

    db.commit()
    return choice
