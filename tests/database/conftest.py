import pytest

from app.config import Settings
from app.database.files import FilesManager
from app.database.files import COLLECTION_NAME
from app.database.models import User


def get_settings_override() -> Settings:
    return Settings(
        mongodb_host="fit_galgo_mongodb_test",
        mongodb_port=27017,
        upload_files_folder="files",
        upload_fit_files_folder="files/fit"
    )


@pytest.fixture(scope="function")
def db_manager() -> Settings:
    user: User = User(username="alice", email="alice@alice.com")
    yield FilesManager(get_settings_override(), user)

    for collection_name in set(COLLECTION_NAME.values()):
        FilesManager(get_settings_override(), user).drop(collection_name)
