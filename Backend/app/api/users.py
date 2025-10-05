from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from typing import Optional

from .deps import get_current_user
from db.models import User

router = APIRouter(prefix="/api/users", tags=["Users"])

@router.get("/me")
async def get_current_user_details(current_user: User = Depends(get_current_user)):
    """
    Get all details for the currently authenticated user.
    This version manually creates the response to ensure stability.
    """
    # Manually create a dictionary with the user's data
    user_data = {
        "id": str(current_user.id),
        "username": current_user.username,
        "email": current_user.email,
        "provider": current_user.provider,
        "profile_picture_url": current_user.profile_picture_url,
    }
    # Return a direct JSONResponse to prevent data type errors
    return JSONResponse(content=user_data)

