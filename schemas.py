from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class EmployeeBase(BaseModel):
    name: str
    email: EmailStr
    department: Optional[str] = None
    role: Optional[str] = None

class EmployeeCreate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    id: int
    date_joined: datetime

    class Config:
        from_attributes = True

class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    department: Optional[str] = None
    role: Optional[str] = None

class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None