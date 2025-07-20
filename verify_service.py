import random
from fastapi import HTTPException
from fastapi_mail import MessageSchema
from sqlalchemy.sql import func
from mail_config import fast_mail
from crud import get_user_by_email
from models import VerificationCode

async def send_verification_code(db, email: str):
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    code = str(random.randint(100000, 999999))

    # Сохраняем код в БД (если уже есть — обновляем)
    existing = db.query(VerificationCode).filter(VerificationCode.email == email).first()
    if existing:
        existing.code = code
        existing.created_at = func.now()
    else:
        new_code = VerificationCode(email=email, code=code)
        db.add(new_code)

    db.commit()

    print(f"[INFO] Отправляю код {code} на {email}")

    message = MessageSchema(
        subject="Your verification code",
        recipients=[email],
        body=f"Your verification code is: {code}",
        subtype="plain"
    )

    await fast_mail.send_message(message)
    print(f"[INFO] Письмо отправлено через SMTP")


def verify_code(db, email: str, code: str):
    record = db.query(VerificationCode).filter(VerificationCode.email == email).first()
    if not record or record.code != code:
        raise HTTPException(status_code=400, detail="Invalid code")
