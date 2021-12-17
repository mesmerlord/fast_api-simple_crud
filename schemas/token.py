from pydantic import BaseModel, Field

class LoginToken(BaseModel):
    access_token : str
    refresh_token : str

class RefreshToken(BaseModel):
    refresh_token : str
  