import pytest

from datetime import datetime, timedelta

from fastapi.testclient import TestClient
from fit_galgo.fit.models import (
    FileId,
    HrvStatusSummary,
    HrvValue,
    Hrv
)

from app.database.files import COLLECTION_NAME
from app.main import app
from app.routers.jwt_auth import get_settings
from app.config import Settings
from app.database.files import FilesManager
from app.database.users import UserManager
from app.database.models import User, UserIn
from app.auth.auth import get_password_hash


def get_settings_override() -> Settings:
    return Settings(
        mongodb_host="fit_galgo_mongodb_test",
        mongodb_port=27017,
        upload_files_folder="files",
        upload_fit_files_folder="files/fit"
    )


def add_hrv_to_db_for_user(
        count: int, user: User, year: int, month: int, day: int
) -> FilesManager:
    """
    It creates count hrv.

    The first hrv was recorded today, the second one yesterday, and so on.
    """
    files_manager: FilesManager = FilesManager(get_settings_override(), user)

    for i in range(count):
        time_created: datetime = datetime.now() - timedelta(days=i)
        # time_created: datetime = datetime.now() - timedelta(days=i)
        file_id: FileId = FileId(
            type=68,
            time_created=time_created
        )
        summary: HrvStatusSummary = HrvStatusSummary(
            timestamp=time_created,
            weekly_average=10.0,
            last_night_average=10.0,
            last_night_5_min_high=10.0,
            baseline_low_upper=10.0,
            baseline_balanced_lower=10.0,
            baseline_balanced_upper=10.0,
            status=1
        )
        values: list[HrvValue] = [
            HrvValue(timestamp=time_created + timedelta(minutes=i))
            for i in range(5)
        ]
        hrv: Hrv = Hrv(
            fit_file_path="file_path.fit",
            file_id=file_id,
            summary=summary,
            values=values
        )

        files_manager.insert(hrv)

    return files_manager


@pytest.fixture(scope="function")
def testclient() -> TestClient:
    app.dependency_overrides[get_settings] = get_settings_override

    users_manager: UserManager = UserManager(get_settings_override())
    users_manager.insert(
        UserIn(
            username="alice",
            email="alice@alice.com",
            password=get_password_hash("alice")
        )
    )

    client = TestClient(app)
    response = client.post(
        "/auth/login",
        data={"username": "alice", "password": "alice"}
    )

    token = response.json()["access_token"]
    client.headers = {"Authorization": f"Bearer {token}"}

    fm1: FilesManager = add_hrv_to_db_for_user(10, User(username="alice"), 2020, 1, 1)
    fm2: FilesManager = add_hrv_to_db_for_user(5, User(username="bob"), 2021, 1, 1)

    yield client

    fm1.drop("hrv")
    fm2.drop("hrv")
    users_manager.drop()

    u = User(username="alice")
    u2 = User(username="bob")
    for collection_name in set(COLLECTION_NAME.values()):
        FilesManager(get_settings_override(), u).drop(collection_name)
        FilesManager(get_settings_override(), u2).drop(collection_name)
    UserManager(get_settings_override()).drop()
