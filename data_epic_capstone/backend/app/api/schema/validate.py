from pydantic import BaseModel, Field
from typing import Optional

class LoginRequest(BaseModel):
    username: str
    password: str=Field(min_length=4, max_length=8)

class SignupRequest(BaseModel):
    username: str
    password: str=Field(min_length=4, max_length=8)
    email: str
class agentRequest(BaseModel):
    id: int
    name: str
    category: Optional[str] = None
    trending: Optional[bool] = True 

