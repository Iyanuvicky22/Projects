# creating the endpoints for login and signup
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

router = APIRouter()


# * Creating endpoints for login and signup
# !Sample code for login and signup endpoints using FastAPI
# !Code will still be altered to fit the use case of the database and authentication system with jwt tokens
# Models for request validatio

class LoginRequest(BaseModel):
    username: str
    password: str

class SignupRequest(BaseModel):
    username: str
    password: str
    email: str


@router.post("/login")
def login(request: LoginRequest):
    if request.username == "username" and request.password == "password":
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@router.post("/signup")
def signup(request: SignupRequest):
    if request.username and request.password and request.email:
        return {"message": "Signup successful"}
    else:
        raise HTTPException(status_code=400, detail="Invalid signup details")