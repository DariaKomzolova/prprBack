from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from database import Base
from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    role = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ProgramDB(Base):
    __tablename__ = "Programs"
    name = Column(String, primary_key=True, index=True)
    tech = Column(Integer)
    hum = Column(Integer)

class Deadline(Base):
    __tablename__ = "deadline"

    id = Column(Integer, primary_key=True)
    start = Column(String, nullable=False)
    end = Column(String, nullable=False)

class StudentChoice(Base):
    __tablename__ = "choice"

    email = Column(String, primary_key=True, index=True)
    program = Column(String)
    tech1 = Column(String, nullable=True)
    tech2 = Column(String, nullable=True)
    tech3 = Column(String, nullable=True)
    tech4 = Column(String, nullable=True)
    tech5 = Column(String, nullable=True)
    hum1 = Column(String, nullable=True)
    hum2 = Column(String, nullable=True)
    hum3 = Column(String, nullable=True)
    hum4 = Column(String, nullable=True)
    hum5 = Column(String, nullable=True)


class VerificationCode(Base):
    __tablename__ = "verification_codes"

    email = Column(String, primary_key=True, index=True)
    code = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
