from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.database.models import User
from app.auth.auth import get_auth_user

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/me", response_model=User, status_code=status.HTTP_200_OK)
async def read_users_me(current_user: Annotated[User, Depends(get_auth_user)]):
    return current_user
