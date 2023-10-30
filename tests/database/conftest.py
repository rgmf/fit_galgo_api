import pytest

from app.config import Settings
from app.database.files import FilesManager
from app.database.database import COLLECTION_NAME


def get_settings_override() -> Settings:
    return Settings(
        mongodb_host="fit_galgo_mongodb_test",
        mongodb_port=27017,
        upload_files_folder="files",
        upload_fit_files_folder="files/fit"
    )


@pytest.fixture(scope="function")
def db_manager() -> Settings:
    yield FilesManager(get_settings_override())

    for collection_name in set(COLLECTION_NAME.values()):
        FilesManager(get_settings_override()).drop(collection_name)
