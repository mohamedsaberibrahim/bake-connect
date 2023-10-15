from pydantic import BaseModel, Field, EmailStr
from enum import Enum

class UserRole(Enum):
  MEMBER = 'member'
  BAKER = 'baker'

class UserBaseSchema(BaseModel):
    email: EmailStr
    name: str
    role: UserRole

class CreateUserSchema(UserBaseSchema):
    hashed_password: str = Field(alias="password")

class UserSchema(UserBaseSchema):
    id: int
    is_active: bool = Field(default=False)

    class Config:
        orm_mode = True

class UserLoginSchema(BaseModel):
    email: EmailStr = Field(alias="username")
    password: str 