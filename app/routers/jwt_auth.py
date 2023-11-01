
from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.database.users import UserManager
from app.auth.auth import Token, create_access_token, verify_password
from app.database.models import User, UserDb
from app.config import Settings, get_settings

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


def authenticate_user(user_db: UserDb, password: str) -> User | None:
    if user_db is None:
        return None

    if not verify_password(password, user_db.hashed_password):
        return None

    return User(**dict(user_db))


@router.post("/login", response_model=Token)
async def login_for_access_token(
        settings: Annotated[Settings, Depends(get_settings)],
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    db_users: UserManager = UserManager(settings)
    user_db: UserDb | None = db_users.get_by_username(form_data.username)
    user: User | None = authenticate_user(user_db, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username and/or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return create_access_token(user)
