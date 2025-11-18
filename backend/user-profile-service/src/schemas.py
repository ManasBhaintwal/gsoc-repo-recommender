# schemas.py
from typing import List, Optional
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: Optional[str] = None
    password: str
    github_username: Optional[str] = None
    languages: Optional[List[str]] = []
    experience_level: Optional[str] = None
    interests: Optional[List[str]] = []

class UserOut(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    github_username: Optional[str] = None
    languages: Optional[List[str]] = []
    experience_level: Optional[str] = None
    interests: Optional[List[str]] = []
    created_at: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
