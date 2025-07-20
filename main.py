from fastapi import FastAPI, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import User, StudentChoice
from schemas import EmailSchema, VerifySchema, RoleResponse, StudentChoiceResponse, StudentChoiceBase, StudentChoiceUpdate
from verify_service import send_verification_code, verify_code
# from crud import get_user_by_email
import csv
import io
import sqlite3
import crud

from routers import programs
from routers import deadline_router

from fastapi.middleware.cors import CORSMiddleware
# import models
# import database
# from routers import programs, deadline_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

# для программ
# models.Base.metadata.create_all(bind=database.engine)
app.include_router(programs.router)

# для дедлайна
app.include_router(deadline_router.router)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------- AUTH ----------

@app.post("/send-code")
async def send_code(payload: EmailSchema, db: Session = Depends(get_db)):
    await send_verification_code(db, payload.email)
    return {"message": "Code sent"}

@app.post("/verify-code", response_model=RoleResponse)
def verify_user(payload: VerifySchema, db: Session = Depends(get_db)):
    verify_code(db, payload.email, payload.code)
    user = crud.get_user_by_email(db, payload.email)
    return {"role": user.role}

@app.get("/download-results")
def download_results():
    conn = sqlite3.connect('electives.db')  # Замени на свой файл БД
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM choice")  # Замени 'results' на свою таблицу

    output = io.StringIO()
    writer = csv.writer(output, delimiter=';')
    writer.writerow([desc[0] for desc in cursor.description])  # Заголовки

    for row in cursor.fetchall():
        safe_row = [value if value is not None else '.' for value in row]
        writer.writerow(safe_row)

    conn.close()

    return Response(
        content=output.getvalue(),
        media_type='text/csv',
        headers={
            'Content-Disposition': 'attachment; filename="results.csv"'
        }
    )
# ---------- STUDENT CHOICE ----------

@app.post("/student_choice/")
def create_choice(choice: StudentChoiceBase, db: Session = Depends(get_db)):
    db_choice = crud.get_student_choice(db, choice.email)
    if db_choice:
        raise HTTPException(status_code=400, detail="Student already exists.")
    return crud.create_student_choice(db, choice)

@app.get("/student_choice/{email}", response_model=StudentChoiceResponse)
def get_choice(email: str, db: Session = Depends(get_db)):
    choice = crud.get_student_choice(db, email)
    if not choice:
        raise HTTPException(status_code=404, detail="Student not found.")
    return choice

@app.put("/student_choice/update")
def update_choice(data: StudentChoiceUpdate, db: Session = Depends(get_db)):
    updated = crud.update_student_choice(db, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Student not found.")
    return updated


@app.get("/get-year/{email}")
def get_year(email: str, db: Session = Depends(get_db)):
    choice = db.query(StudentChoice).filter(StudentChoice.email == email).first()
    if not choice:
        raise HTTPException(status_code=404, detail="Student not found in choice table")
    return {"year": choice.year}
