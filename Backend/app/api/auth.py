from datetime import timedelta
from fastapi import APIRouter, HTTPException, status, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
from starlette.responses import RedirectResponse

from db.models import User
from core.security import create_access_token
from core.oauth import oauth

router = APIRouter(prefix="/api/auth", tags=["Authentication"])
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

class RegisterReq(BaseModel):
    username: str | None = None
    anonymous: bool = True
    password: str | None = None

class TokenResp(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str

@router.post("/register", response_model=TokenResp)
async def register(payload: RegisterReq):
    # This endpoint remains the same
    if not payload.anonymous and not payload.password:
        raise HTTPException(status_code=400, detail="Password required for non-anonymous users")
    if payload.username:
        existing = await User.find_one({"username": payload.username})
        if existing:
            raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = pwd_context.hash(payload.password) if payload.password else None
    user = User(
        username=payload.username,
        is_anonymous=payload.anonymous,
        hashed_password=hashed_password,
        provider="local"
    )
    await user.insert()
    token = create_access_token(subject=str(user.id), expires_delta=timedelta(days=30))
    return {"access_token": token, "token_type": "bearer", "user_id": str(user.id)}

@router.post("/token", response_model=TokenResp)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # This endpoint remains the same
    user = await User.find_one({"username": form_data.username})
    if not user or not user.hashed_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    try:
        if not pwd_context.verify(form_data.password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(subject=str(user.id), expires_delta=timedelta(days=30))
    return {"access_token": token, "token_type": "bearer", "user_id": str(user.id)}


# --- THIS IS THE FIXED FUNCTION ---
async def get_or_create_google_user(user_info: dict) -> User:
    """
    Finds a user by Google ID or email. Creates a new user if one doesn't exist.
    Crucially, it now saves or updates the profile picture URL in all cases.
    """
    # Case 1: User has logged in with Google before.
    user = await User.find_one({"google_id": user_info['sub']})
    if user:
        # Update their picture in case it has changed since their last login.
        user.profile_picture_url = user_info.get('picture')
        await user.save()
        return user

    # Case 2: User has a local account with the same email. Link it to Google.
    user = await User.find_one({"email": user_info['email']})
    if user:
        user.google_id = user_info['sub']
        user.provider = "google"
        user.profile_picture_url = user_info.get('picture') # <-- Add picture
        await user.save()
        return user

    # Case 3: This is a brand new user.
    new_user = User(
        email=user_info['email'],
        username=user_info.get('name'),
        google_id=user_info['sub'],
        provider="google",
        is_anonymous=False,
        profile_picture_url=user_info.get('picture') # <-- Add picture
    )
    await new_user.insert()
    return new_user

@router.get('/google/login')
async def google_login(request: Request):
    # This endpoint remains the same
    redirect_uri = request.url_for('google_auth_callback')
    return await oauth.google.authorize_redirect(request, str(redirect_uri))

@router.get('/google/auth')
async def google_auth_callback(request: Request):
    # This endpoint remains the same
    try:
        token_data = await oauth.google.authorize_access_token(request)
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Could not validate Google credentials: {e}")

    user_info = token_data.get('userinfo')
    if not user_info:
        raise HTTPException(status_code=401, detail="Could not fetch user info from Google.")

    user = await get_or_create_google_user(user_info)
    
    access_token = create_access_token(subject=str(user.id), expires_delta=timedelta(days=30))
    
    frontend_url = f"http://localhost:3000/auth/callback?token={access_token}&user_id={str(user.id)}"
    return RedirectResponse(url=frontend_url)

