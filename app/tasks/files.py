import os

from datetime import datetime
from pathlib import Path

from fastapi import UploadFile
from fit_galgo.galgo import FitGalgo
from fit_galgo.fit.models import FitModel, FitError

from app.models.files import FileUploadInfo, FilesUploadTask
from app.database.files import FilesManager
from app.config import Settings
from app.database.models import User


async def send_task_files(
        files: list[UploadFile],
        zone: str | None,
        user: User,
        settings: Settings
) -> FilesUploadTask:
    fit_files_folder: str = os.path.join(
        settings.upload_fit_files_folder,
        datetime.now().date().strftime("%Y%m%d")
    )
    Path(fit_files_folder).mkdir(parents=True, exist_ok=True)
    fut: FilesUploadTask = FilesUploadTask(data=[])

    for file in files:
        fit_file_path: str = os.path.join(fit_files_folder, file.filename)
        if not is_accepted_file(fit_file_path):
            fui: FileUploadInfo = FileUploadInfo(
                file_path=file.filename,
                accepted=False,
                id=None,
                errors=["File extension not allowed"],
                zip_file_path=None
            )
        else:
            with open(fit_file_path, "wb") as file_object:
                chunk: bytes = await file.read(10_000)
                while chunk:
                    file_object.write(chunk)
                    chunk: bytes = await file.read(10_000)

            galgo: FitGalgo = FitGalgo(fit_file_path, zone)
            model: FitModel | FitError = galgo.parse()
            if isinstance(model, FitError):
                fui: FileUploadInfo = FileUploadInfo(
                    file_path=file.filename,
                    accepted=False,
                    id=None,
                    errors=[str(e) for e in model.errors],
                    zip_file_path=None
                )
            else:
                id: str | None = FilesManager(settings, user).insert(model)
                if not id:
                    fui: FileUploadInfo = FileUploadInfo(
                        file_path=file.filename,
                        accepted=False,
                        id=id,
                        errors=["The document already exists"],
                        zip_file_path=None
                    )
                else:
                    fui: FileUploadInfo = FileUploadInfo(
                        file_path=file.filename,
                        accepted=True,
                        id=id,
                        errors=[],
                        zip_file_path=None
                    )
        fut.data.append(fui)

    return fut


def is_accepted_file(filename: str) -> bool:
    return Path(filename).suffix.lower() in [".fit"]
