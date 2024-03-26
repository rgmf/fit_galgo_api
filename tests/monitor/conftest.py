import pytest

from datetime import datetime, timedelta

from fastapi.testclient import TestClient
from fit_galgo.fit.models import (
    FileId,
    MonitoringInfo,
    Monitoring,
    Monitor
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


def add_monitor_with_steps_to_db_for_user(
        count: int, user: User, year: int, month: int, day: int
) -> FilesManager:
    """
    It creates count monitor.

    The first monitor was recorded today, the second one yesterday, and so on.
    """
    files_manager: FilesManager = FilesManager(get_settings_override(), user)

    for i in range(count):
        # Daily log: one yes, one no
        if i % 2 == 0:
            time_created: datetime = (
                datetime(year, month, day, 0, 0, 0) + timedelta(days=i)
            )
        else:
            time_created: datetime = (
                datetime(year, month, day, 1, 1, 1) + timedelta(days=i)
            )
        # time_created: datetime = datetime.now() - timedelta(days=i)
        file_id: FileId = FileId(
            type="monitoring",
            time_created=time_created
        )
        monitoring_info: MonitoringInfo = MonitoringInfo(
            timestamp=time_created,
            resting_metabolic_rate=2000
        )
        monitoring: Monitoring = Monitoring(
            timestamp=time_created,
            steps=1000
        )
        monitor: Monitor = Monitor(
            fit_file_path="file_path.fit",
            file_id=file_id,
            monitoring_info=monitoring_info,
            monitorings=[monitoring]
        )

        files_manager.insert(monitor)

    return files_manager


def add_monitor_without_steps(
        count: int, user: User, year: int, month: int, day: int
) -> FilesManager:
    """
    It creates count monitor without steps.

    The first monitor was recorded today, the second one yesterday, and so on.
    """
    files_manager: FilesManager = FilesManager(get_settings_override(), user)

    for i in range(count):
        time_created: datetime = datetime(year, month, day, 0, 0, 0) - timedelta(days=i)
        file_id: FileId = FileId(
            type="monitoring",
            time_created=time_created
        )
        monitoring_info: MonitoringInfo = MonitoringInfo(
            timestamp=time_created,
            resting_metabolic_rate=2000
        )
        monitoring: Monitoring = Monitoring(
            timestamp=time_created
        )
        monitor: Monitor = Monitor(
            fit_file_path="file_path.fit",
            file_id=file_id,
            monitoring_info=monitoring_info,
            monitorings=[monitoring]
        )

        files_manager.insert(monitor)

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

    fm1: FilesManager = add_monitor_with_steps_to_db_for_user(
        10, User(username="alice"), 2020, 1, 1
    )
    fm2: FilesManager = add_monitor_with_steps_to_db_for_user(
        5, User(username="bob"), 2021, 1, 1
    )
    fm3: FilesManager = add_monitor_without_steps(
        5, User(username="alice"), 2022, 1, 1
    )

    yield client

    fm1.drop("monitoring")
    fm2.drop("monitoring")
    fm3.drop("monitoring")
    users_manager.drop()

    u = User(username="alice")
    u2 = User(username="bob")
    for collection_name in set(COLLECTION_NAME.values()):
        FilesManager(get_settings_override(), u).drop(collection_name)
        FilesManager(get_settings_override(), u2).drop(collection_name)
    UserManager(get_settings_override()).drop()
