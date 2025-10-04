from fastapi import Depends, HTTPException, status
from core.security import oauth2_scheme, verify_token
from db.models import User


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    user_id = verify_token(token)
    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


async def get_moderator(user: User = Depends(get_current_user)) -> User:
    # For now, allow any authenticated user to access admin functions
    # In production, you'd check user.is_moderator or similar field
    return user