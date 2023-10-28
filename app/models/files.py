from pydantic import BaseModel


class FileUploadInfo(BaseModel):
    file_path: list[str]
    accepted: bool
    id: str | None = None
    errors: list[str] = []
    zip_file_path: str | None = None


class FilesUploadTask(BaseModel):
    files_info: list[FileUploadInfo]
