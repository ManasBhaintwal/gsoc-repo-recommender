from fastapi import APIRouter, HTTPException, status, Depends, Header
from src.schemas import UserCreate, UserOut, UserLogin, TokenResponse
from services.users_db_ops import create_user, get_user_by_id, get_user_by_username, update_user
import bcrypt
from auth import create_access_token, decode_token

router = APIRouter(prefix="/user", tags=["User Profile"])

@router.post("/create", response_model=UserOut)
def register_user(payload: UserCreate):
    # check if username already exists
    existing = get_user_by_username(payload.username)
    if existing:
        raise HTTPException(status_code=400, detail="username already exists")
    user = create_user(
        username=payload.username,
        email=payload.email,
        password=payload.password,
        github_username=payload.github_username,
        languages=payload.languages,
        experience_level=payload.experience_level,
        interests=payload.interests
    )
    if not user:
        raise HTTPException(status_code=500, detail="failed to create user")
    return user


@router.post("/login", response_model=TokenResponse)
def login(payload: UserLogin):
    user = get_user_by_username(payload.username)
    if not user:
        raise HTTPException(status_code=401, detail="invalid credentials")
    password_hash = user.get("password_hash")
    if not password_hash or not bcrypt.checkpw(payload.password.encode('utf-8'), password_hash.encode('utf-8')):
        raise HTTPException(status_code=401, detail="invalid credentials")
    token = create_access_token({"sub": str(user["id"]), "username": user["username"]})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, authorization: str = Header(None)):
    # optional: verify token header "Authorization: Bearer <token>"
    # For now, we allow public read; add token checks if you want protected endpoints
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user


@router.patch("/{user_id}", response_model=UserOut)
def patch_user(user_id: int, payload: dict):
    # payload is a dict with allowed keys; you can validate with pydantic if desired
    allowed = {"email", "github_username", "languages", "experience_level", "interests"}
    updates = {k: v for k, v in payload.items() if k in allowed}
    if not updates:
        raise HTTPException(status_code=400, detail="no valid fields to update")
    user = update_user(user_id, **updates)
    if not user:
        raise HTTPException(status_code=404, detail="user not found or not updated")
    return user