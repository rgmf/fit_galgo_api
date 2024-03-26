import os

from datetime import datetime
from pathlib import Path
from zipfile import ZipFile

from fastapi import UploadFile
from fit_galgo.galgo import FitGalgo
from fit_galgo.fit.models import FitModel, FitError

from app.models.files import FileUploadInfo, FilesUploadTask
from app.database.files import FilesManager
from app.config import Settings
from app.database.models import User

ACCEPTED_FILES = [".fit"]


def is_accepted_file(filename: str) -> bool:
    return Path(filename).suffix.lower() in ACCEPTED_FILES


def is_zip_file(filename: str) -> bool:
    return Path(filename).suffix.lower() == ".zip"


async def process_fit_file(
        fit_file_path: str,
        zone: str | None,
        user: User,
        settings: Settings,
        zip_file_path: str | None = None
) -> FileUploadInfo:
    galgo: FitGalgo = FitGalgo(fit_file_path, zone)
    model: FitModel | FitError = galgo.parse()
    zip_file_path = os.path.basename(zip_file_path) if zip_file_path else None
    if isinstance(model, FitError):
        fui: FileUploadInfo = FileUploadInfo(
            filename=os.path.basename(fit_file_path),
            accepted=False,
            id=None,
            errors=[str(e) for e in model.errors],
            zip_filename=zip_file_path
        )
    else:
        id: str | None = FilesManager(settings, user).insert(model)
        if not id:
            fui: FileUploadInfo = FileUploadInfo(
                filename=os.path.basename(fit_file_path),
                accepted=False,
                id=id,
                errors=["The document already exists"],
                zip_filename=zip_file_path
            )
        else:
            fui: FileUploadInfo = FileUploadInfo(
                filename=os.path.basename(fit_file_path),
                accepted=True,
                id=id,
                errors=[],
                zip_filename=zip_file_path
            )

    return fui


async def send_task_files(
        files: list[UploadFile],
        zone: str | None,
        user: User,
        settings: Settings
) -> FilesUploadTask:
    fut: FilesUploadTask = FilesUploadTask(data=[])

    for file in files:
        # Write the file into tmp folder
        tmp_files_folder: str = settings.upload_tmp_files_folder
        Path(tmp_files_folder).mkdir(parents=True, exist_ok=True)
        tmp_file_path: str = os.path.join(tmp_files_folder, file.filename)

        with open(tmp_file_path, "wb") as file_object:
            chunk: bytes = await file.read(10_000)
            while chunk:
                file_object.write(chunk)
                chunk: bytes = await file.read(10_000)

        # Depends on the type of file...
        if is_accepted_file(tmp_file_path):
            # Move tmp file to the destination folder
            dst_path: str = os.path.join(
                settings.upload_fit_files_folder,
                datetime.now().date().strftime("%Y%m%d")
            )
            Path(dst_path).mkdir(parents=True, exist_ok=True)
            dst_file_path = Path(tmp_file_path).rename(Path(os.path.join(dst_path, file.filename)))
            # Process file
            fui: FileUploadInfo = await process_fit_file(
                fit_file_path=dst_file_path.as_posix(),
                zone=zone,
                user=user,
                settings=settings
            )
            fut.data.append(fui)
        elif is_zip_file(tmp_file_path):
            # Move tmp file to the destination folder
            dst_zip_path: str = os.path.join(
                settings.upload_zip_files_folder,
                datetime.now().date().strftime("%Y%m%d")
            )
            Path(dst_zip_path).mkdir(parents=True, exist_ok=True)
            dst_zipfile_path = Path(tmp_file_path).rename(Path(os.path.join(dst_zip_path, file.filename)))
            # Process zip file
            with ZipFile(dst_zipfile_path.as_posix()) as zipfile:
                for filename in [f for f in zipfile.namelist() if is_accepted_file(f)]:
                    with zipfile.open(filename) as file_in_zip:
                        tmp_fit_file_path: str = os.path.join(
                            tmp_files_folder, file_in_zip.name
                        )
                        with open(tmp_fit_file_path, "wb") as fo:
                            chunk: bytes = file_in_zip.read(10_000)
                            while chunk:
                                fo.write(chunk)
                                chunk: bytes = file_in_zip.read(10_000)

                        # Move tmp file to the destination folder
                        dst_path: str = os.path.join(
                            settings.upload_fit_files_folder,
                            datetime.now().date().strftime("%Y%m%d")
                        )
                        Path(dst_path).mkdir(parents=True, exist_ok=True)
                        dst_file_path = Path(tmp_fit_file_path).rename(Path(os.path.join(dst_path, filename)))
                        # Process file
                        fui: FileUploadInfo = await process_fit_file(
                            fit_file_path=dst_file_path.as_posix(),
                            zip_file_path=dst_zipfile_path,
                            zone=zone,
                            user=user,
                            settings=settings
                        )
                        fut.data.append(fui)
        else:
            fui: FileUploadInfo = FileUploadInfo(
                filename=file.filename,
                accepted=False,
                id=None,
                errors=["File extension not allowed"],
                zip_filename=None
            )
            fut.data.append(fui)
            Path(tmp_file_path).unlink()

    return fut
