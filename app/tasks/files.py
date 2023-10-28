import os

from datetime import datetime
from pathlib import Path

from fastapi import UploadFile
from fastapi.encoders import jsonable_encoder
from fit_galgo.galgo import FitGalgo
from fit_galgo.fit.models import FitModel
from couchbase.result import MutationResult

from app.models.files import FileUploadInfo, FilesUploadTask
from app.config import config
from app.database import get_collection


async def send_task_files(files: list[UploadFile]) -> FilesUploadTask:
    fit_files_folder: str = os.path.join(
        config["UPLOAD_FIT_FILES_FOLDER"],
        datetime.now().date().strftime("%Y%m%d")
    )
    Path(fit_files_folder).mkdir(parents=True, exist_ok=True)
    fut: FilesUploadTask = FilesUploadTask(files_info=[])

    for file in files:
        fit_file_path: str = os.path.join(fit_files_folder, file.filename)
        if not is_accepted_file(fit_file_path):
            fui: FileUploadInfo = FileUploadInfo(
                file_path=[file.filename],
                accepted=False,
                uuid=None,
                errors=["File extension not allowed"],
                zip_file_path=None
            )
        else:
            with open(fit_file_path, "wb") as file_object:
                chunk: bytes = await file.read(10_000)
                while chunk:
                    file_object.write(chunk)
                    chunk: bytes = await file.read(10_000)

            galgo: FitGalgo = FitGalgo(fit_file_path)
            model: FitModel = galgo.parse()

            id: str = f"{model.file_id.file_type}_{model.file_id.time_created}"
            collection = get_collection()
            result: MutationResult = collection.upsert(id, jsonable_encoder(model))

            fui: FileUploadInfo = FileUploadInfo(
                file_path=[file.filename],
                accepted=True,
                id=id,
                errors=[],
                zip_file_path=None
            )
        fut.files_info.append(fui)

    return fut


def is_accepted_file(filename: str) -> bool:
    return Path(filename).suffix.lower() in [".fit"]
