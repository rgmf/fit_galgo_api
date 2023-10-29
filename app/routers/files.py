from functools import lru_cache
from typing import Annotated

from fastapi import APIRouter, UploadFile, status, Depends

from app.models.files import FilesUploadTask
from app.tasks.files import send_task_files
from app.config import Settings

router = APIRouter(
    prefix="/files",
    tags=["files"]
)


@lru_cache
def get_settings():
    return Settings()


@router.post("/", response_model=FilesUploadTask, status_code=status.HTTP_200_OK)
async def post_files(
        files: list[UploadFile],
        settings: Annotated[Settings, Depends(get_settings)]
) -> FilesUploadTask:
    fut: FilesUploadTask = await send_task_files(files, settings)
    return fut
