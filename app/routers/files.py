from typing import Annotated

from fastapi import APIRouter, UploadFile, status, Depends, Form

from app.models.files import FilesUploadTask
from app.tasks.files import send_task_files
from app.config import Settings, get_settings
from app.database.models import User
from app.auth.auth import get_auth_user


router = APIRouter(
    prefix="/files",
    tags=["files"]
)


@router.post("/", response_model=FilesUploadTask, status_code=status.HTTP_200_OK)
async def upload_files(
        files: list[UploadFile],
        settings: Annotated[Settings, Depends(get_settings)],
        user: Annotated[User, Depends(get_auth_user)],
        zone: Annotated[
            str | None,
            Form(description="IANA time zone name where FIT file was recorded")
        ] = None
) -> FilesUploadTask:
    fut: FilesUploadTask = await send_task_files(files, zone, user, settings)
    return fut
