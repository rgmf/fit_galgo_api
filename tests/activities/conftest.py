import pytest

from datetime import datetime, timedelta

from fastapi.testclient import TestClient
from fit_galgo.fit.models import (
    FileId,
    Session,
    Activity
)

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


def add_activities_to_db_for_user(count: int, user: User) -> FilesManager:
    """
    It creates count activities.

    The first activity was recorded today, the second one yesterday, and so on.
    """
    files_manager: FilesManager = FilesManager(get_settings_override(), user)

    for i in range(count):
        time_created: datetime = datetime.now() - timedelta(days=i)
        file_id: FileId = FileId(
            type="activity",
            time_created=time_created
        )
        session: Session = Session(
            message_index=0,
            timestamp=time_created,
            start_time=time_created,
            total_elapsed_time=60.0,
            total_timer_time=60.0,
            sport="cycling",
            sub_sport="road cycling"
        )
        activity: Activity = Activity(
            fit_file_path="file_path.fit",
            file_id=file_id,
            session=session
        )

        files_manager.insert(activity)

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

    fm1: FilesManager = add_activities_to_db_for_user(10, User(username="alice"))
    fm2: FilesManager = add_activities_to_db_for_user(5, User(username="bob"))

    yield client

    fm1.drop("activity")
    fm2.drop("activity")
    users_manager.drop()
