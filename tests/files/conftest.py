import pytest

from fastapi.testclient import TestClient

from app.main import app
from app.routers.jwt_auth import get_settings
from app.config import Settings
from app.database.files import FilesManager
from app.database.users import UserManager
from app.database.models import UserIn
from app.auth.auth import get_password_hash


def get_settings_override() -> Settings:
    return Settings(
        mongodb_host="fit_galgo_mongodb_test",
        mongodb_port=27017,
        upload_files_folder="files",
        upload_fit_files_folder="files/fit"
    )


@pytest.fixture(scope="function")
def testclient() -> TestClient:
    app.dependency_overrides[get_settings] = get_settings_override

    user_in: UserIn = UserIn(
        username="alice",
        email="alice@alice.com",
        password=get_password_hash("alice")
    )
    user_manager: UserManager = UserManager(get_settings_override())
    user_manager.insert(user_in)

    client = TestClient(app)
    response = client.post(
        "/auth/login",
        data={"username": "alice", "password": "alice"}
    )

    token = response.json()["access_token"]
    client.headers = {"Authorization": f"Bearer {token}"}

    yield client

    FilesManager(get_settings_override(), user_in).drop("sleep")
    user_manager.drop()
