import pytest

from fastapi.testclient import TestClient

from app.database.files import COLLECTION_NAME
from app.database.models import User
from app.database.files import FilesManager
from app.main import app
from app.database.users import UserManager
from app.database.models import UserIn
from app.auth.auth import get_password_hash
from app.routers.jwt_auth import get_settings
from app.config import Settings


def get_settings_override() -> Settings:
    return Settings(
        mongodb_host="fit_galgo_mongodb_test",
        mongodb_port=27017,
        upload_files_folder="files",
        upload_fit_files_folder="files/fit"
    )


@pytest.fixture(scope="function")
def db_test() -> UserManager:
    app.dependency_overrides[get_settings] = get_settings_override
    users_manager: UserManager = UserManager(get_settings_override())
    yield users_manager
    users_manager.drop()

    u = User(username="alice")
    for collection_name in set(COLLECTION_NAME.values()):
        FilesManager(get_settings_override(), u).drop(collection_name)
    UserManager(get_settings_override()).drop()


@pytest.fixture(scope="function")
def db_test_with_2_users(db_test) -> UserManager:
    db_test.insert(
        UserIn(
            username="alice",
            email="alice@alice.com",
            password=get_password_hash("alice")
        )
    )
    db_test.insert(
        UserIn(username="bob", email="bob@bob.com", password=get_password_hash("bob"))
    )
    return db_test


@pytest.fixture(scope="function")
def testclient_with_2_users(db_test_with_2_users) -> TestClient:
    client = TestClient(app)
    return client
