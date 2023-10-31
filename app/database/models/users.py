from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserIn(User):
    password: str


class UserDb(User):
    hashed_password: str

    @staticmethod
    def from_database_dict(user_dict):
        user_dict["hashed_password"] = user_dict["password"]
        return UserDb(**user_dict)
