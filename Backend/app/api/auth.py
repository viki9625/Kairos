from datetime import timedelta
from fastapi import APIRouter, HTTPException, status, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
from starlette.responses import RedirectResponse # Ensure this is imported

from db.models import User
from core.security import create_access_token
from core.oauth import oauth

# (Your existing router, pwd_context, and Pydantic models remain the same)
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

# (Your existing /register and /token endpoints remain the same)
@router.post("/register", response_model=TokenResp)
async def register(payload: RegisterReq):
    if not payload.anonymous and not payload.password:
        raise HTTPException(status_code=400, detail="Password required for non-anonymous users")
    if payload.username:
        existing = await User.find_one(User.username == payload.username)
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
    user = await User.find_one(User.username == form_data.username)
    if not user or not user.hashed_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    try:
        if not pwd_context.verify(form_data.password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(subject=str(user.id), expires_delta=timedelta(days=30))
    return {"access_token": token, "token_type": "bearer", "user_id": str(user.id)}


# --- Google OAuth2 Endpoints ---

async def get_or_create_google_user(user_info: dict) -> User:
    user = await User.find_one(User.google_id == user_info['sub'])
    if user: return user
    user = await User.find_one(User.email == user_info['email'])
    if user:
        user.google_id = user_info['sub']
        user.provider = "google"
        await user.save()
        return user
    new_user = User(
        email=user_info['email'],
        username=user_info.get('name'),
        google_id=user_info['sub'],
        provider="google",
        is_anonymous=False,
    )
    await new_user.insert()
    return new_user

@router.get('/google/login')
async def google_login(request: Request):
    """Redirects the user to Google's authentication page."""
    redirect_uri = request.url_for('google_auth_callback')
    return await oauth.google.authorize_redirect(request, str(redirect_uri))


# --- THIS IS THE FIXED FUNCTION ---
@router.get('/google/auth')
async def google_auth_callback(request: Request):
    """Handles the callback from Google and REDIRECTS to the frontend."""
    try:
        token_data = await oauth.google.authorize_access_token(request)
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Could not validate Google credentials: {e}")

    user_info = token_data.get('userinfo')
    if not user_info:
        raise HTTPException(status_code=401, detail="Could not fetch user info from Google.")

    user = await get_or_create_google_user(user_info)
    
    access_token = create_access_token(subject=str(user.id), expires_delta=timedelta(days=30))
    
    # Instead of returning JSON, we now build a URL and redirect the user's browser.
    frontend_url = f"http://localhost:3000/auth/callback?token={access_token}&user_id={str(user.id)}"
    return RedirectResponse(url=frontend_url)

