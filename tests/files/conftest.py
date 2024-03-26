import pytest

from pathlib import Path

from fastapi.testclient import TestClient

from app.database.files import COLLECTION_NAME
from app.database.models import User
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

    s: Settings = get_settings_override()
    p: Path = Path(s.upload_tmp_files_folder)
    assert p.is_dir()
    count_files: int = len([_ for _ in p.iterdir()])
    assert count_files == 0

    u = User(username="alice")
    for collection_name in set(COLLECTION_NAME.values()):
        FilesManager(get_settings_override(), u).drop(collection_name)
    UserManager(get_settings_override()).drop()
