from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class PatientBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    age: int = Field(..., ge=0, le=130)
    gender: str = Field(..., min_length=1, max_length=32)
    diagnosis: str = Field(..., min_length=1, max_length=250)
    email: Optional[EmailStr] = None
    notes: Optional[str] = None

class PatientCreate(PatientBase):
    pass

class PatientUpdate(BaseModel):
    name: Optional[str]
    age: Optional[int]
    gender: Optional[str]
    diagnosis: Optional[str]
    email: Optional[EmailStr]
    notes: Optional[str]

class PatientInDB(PatientBase):
    id: str
    created_at: datetime

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    disabled: Optional[bool] = None
