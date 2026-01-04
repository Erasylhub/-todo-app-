from pydantic import BaseModel, EmailStr
from typing import Optional


class UserReadSchema(BaseModel):
    username: str
    email: EmailStr

    class Config:
        from_attributes = True 
        
class UserCreateSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    
class UserUpdateSchema(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None