from pydantic import BaseModel
from typing import Optional

class EmailSchema(BaseModel):
    email: str

class VerifySchema(BaseModel):
    email: str
    code: str

class RoleResponse(BaseModel):
    role: str

class Program(BaseModel):
    name: str
    tech: int
    hum: int
class StudentChoiceBase(BaseModel):
    email: str
    program: str

    class Config:
        from_attributes = True

class StudentChoiceUpdate(BaseModel):
    email: str
    tech1: Optional[str] = None
    tech2: Optional[str] = None
    tech3: Optional[str] = None
    tech4: Optional[str] = None
    tech5: Optional[str] = None

    hum1: Optional[str] = None
    hum2: Optional[str] = None
    hum3: Optional[str] = None
    hum4: Optional[str] = None
    hum5: Optional[str] = None

class StudentChoiceResponse(BaseModel):
    email: str
    program: str
    tech1: Optional[str] = "-"
    tech2: Optional[str] = "-"
    tech3: Optional[str] = "-"
    tech4: Optional[str] = "-"
    tech5: Optional[str] = "-"
    hum1: Optional[str] = "-"
    hum2: Optional[str] = "-"
    hum3: Optional[str] = "-"
    hum4: Optional[str] = "-"
    hum5: Optional[str] = "-"

    class Config:
        from_attributes = True
