import pytest

from datetime import datetime, timedelta

from fastapi.testclient import TestClient
from fit_galgo.fit.models import (
    FileId,
    SleepAssessment,
    SleepLevel,
    Sleep
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


def add_sleep_to_db_for_user(count: int, user: User) -> FilesManager:
    """
    It creates count sleep.

    The first sleep was recorded today, the second one yesterday, and so on.
    """
    files_manager: FilesManager = FilesManager(get_settings_override(), user)

    for i in range(count):
        time_created: datetime = datetime.now() - timedelta(days=i)
        file_id: FileId = FileId(
            type=49,
            time_created=time_created
        )
        assessment: SleepAssessment = SleepAssessment(
            combined_awake_score=10,
            awake_time_score=10,
            awakenings_count_score=10,
            deep_sleep_score=10,
            sleep_duration_score=10,
            light_sleep_score=10,
            overall_sleep_score=10,
            sleep_quality_score=10,
            sleep_recovery_score=10,
            rem_sleep_score=10,
            sleep_restlessness_score=10,
            awakenings_count=10,
            interruptions_score=10,
            average_stress_during_sleep=10.5
        )
        levels: list[SleepLevel] = [
            SleepLevel(
                timestamp=time_created + timedelta(minutes=1),
                sleep_level=3
            ) for _ in range(5)
        ]
        sleep: Sleep = Sleep(
            fit_file_path="file_path.fit",
            file_id=file_id,
            assessment=assessment,
            levels=levels
        )

        files_manager.insert(sleep)

    return files_manager


def add_sleep_to_db_with_two_dates(user: User) -> FilesManager:
    """
    Cretes a sleep with two dates: 20101010 and 20101011.
    """
    time_created: datetime = datetime(2010, 10, 10, 23, 50, 0)

    files_manager: FilesManager = FilesManager(get_settings_override(), user)
    file_id: FileId = FileId(
        type=49,
        time_created=time_created
    )
    assessment: SleepAssessment = SleepAssessment(
        combined_awake_score=10,
        awake_time_score=10,
        awakenings_count_score=10,
        deep_sleep_score=10,
        sleep_duration_score=10,
        light_sleep_score=10,
        overall_sleep_score=10,
        sleep_quality_score=10,
        sleep_recovery_score=10,
        rem_sleep_score=10,
        sleep_restlessness_score=10,
        awakenings_count=10,
        interruptions_score=10,
        average_stress_during_sleep=10.5
    )
    levels: list[SleepLevel] = [
        SleepLevel(
            timestamp=time_created + timedelta(minutes=i * 10),
            sleep_level=3
        ) for i in range(5)
    ]
    sleep: Sleep = Sleep(
        fit_file_path="file_path.fit",
        file_id=file_id,
        assessment=assessment,
        levels=levels
    )

    files_manager.insert(sleep)

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

    fm1: FilesManager = add_sleep_to_db_for_user(10, User(username="alice"))
    fm2: FilesManager = add_sleep_to_db_for_user(5, User(username="bob"))
    fm3: FilesManager = add_sleep_to_db_with_two_dates(User(username="alice"))

    yield client

    fm1.drop("sleep")
    fm2.drop("sleep")
    fm3.drop("sleep")
    users_manager.drop()

    u = User(username="alice")
    u2 = User(username="bob")
    for collection_name in set(COLLECTION_NAME.values()):
        FilesManager(get_settings_override(), u).drop(collection_name)
        FilesManager(get_settings_override(), u2).drop(collection_name)
    UserManager(get_settings_override()).drop()
