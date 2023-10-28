from fastapi import APIRouter, UploadFile, status

from app.models.files import FilesUploadTask
from app.tasks.files import send_task_files


router = APIRouter(
    prefix="/files",
    tags=["files"]
)


@router.post("/", response_model=FilesUploadTask, status_code=status.HTTP_200_OK)
async def post_files(files: list[UploadFile]) -> FilesUploadTask:
    fut: FilesUploadTask = await send_task_files(files)
    return fut
