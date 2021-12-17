
from pydantic import BaseModel, Field

## Models

class UserSignup(BaseModel):
    username : str = Field(..., example="test_username")
    password : str = Field(..., example="strong_password_1234")
    name : str = Field(..., example="John Smith")
    class Config:
        orm_mode = True

class UserCreated(BaseModel):
    username : str = Field(..., example="test_username")
    name : str = Field(..., example="John")
    id : int = Field(..., example=1)
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    username : str = Field(..., example="test_username")
    password : str = Field(..., example="strong_password_1234")
    class Config:
        orm_mode = True

