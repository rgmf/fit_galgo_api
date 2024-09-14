from datetime import datetime, timedelta
from typing import Annotated

from pydantic import BaseModel
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt, JWTError

from app.database.models import User, UserDb
from app.database.users import UserManager
from app.config import Settings, get_settings

SECRET_KEY = get_settings().secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MIN = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


async def get_auth_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    settings: Annotated[Settings, Depends(get_settings)]
) -> User:
    db_users: UserManager = UserManager(settings)
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    token_data: TokenData = decode_token(token)
    if token_data is None or token_data.username is None:
        raise exception

    user_db: UserDb | None = db_users.get_by_username(token_data.username)
    if user_db is None:
        raise exception

    return User(**dict(user_db))


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password) -> str:
    return pwd_context.hash(password)


def create_access_token(user: User) -> Token:
    to_encode = {"sub": user.username}

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MIN)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": encoded_jwt, "token_type": "bearer"}


def decode_token(token: str) -> TokenData:
    try:
        payload: dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return TokenData(username=payload.get("sub"))
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
