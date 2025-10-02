from datetime import timedelta
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext

from db.models import User
from core.security import create_access_token

# ------------------------------
# Router
# ------------------------------
router = APIRouter(prefix="/api/auth", tags=["Authentication"])

# ------------------------------
# Password hashing (Argon2)
# ------------------------------
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# ------------------------------
# Pydantic models
# ------------------------------
class RegisterReq(BaseModel):
    username: str | None = None
    anonymous: bool = True
    password: str | None = None

class TokenResp(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str

# ------------------------------
# Register endpoint
# ------------------------------
@router.post("/register", response_model=TokenResp)
async def register(payload: RegisterReq):
    # Require password for non-anonymous users
    if not payload.anonymous and not payload.password:
        raise HTTPException(status_code=400, detail="Password required for non-anonymous users")

    # Check if username exists
    existing = None
    if payload.username:
        existing = await User.find_one(User.username == payload.username)
        if existing:
            raise HTTPException(status_code=400, detail="Username already exists")

    # Hash password (Argon2)
    hashed_password = None
    if payload.password:
        hashed_password = pwd_context.hash(payload.password)

    # Create user
    user = User(
        username=payload.username,
        is_anonymous=payload.anonymous,
        hashed_password=hashed_password
    )
    await user.insert()

    # Generate JWT token
    token = create_access_token(subject=str(user.id), expires_delta=timedelta(days=30))
    return {"access_token": token, "token_type": "bearer", "user_id": str(user.id)}

# ------------------------------
# Login endpoint
# ------------------------------
@router.post("/token", response_model=TokenResp)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await User.find_one(User.username == form_data.username)
    if not user or not user.hashed_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # Verify password (Argon2)
    if not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # Generate JWT token
    token = create_access_token(subject=str(user.id), expires_delta=timedelta(days=30))
    return {"access_token": token, "token_type": "bearer", "user_id": str(user.id)}
