from pydantic import BaseModel, computed_field


class FileUploadInfo(BaseModel):
    file_path: str
    accepted: bool
    id: str | None = None
    errors: list[str] = []
    zip_file_path: str | None = None


class FilesUploadTask(BaseModel):
    data: list[FileUploadInfo]

    @computed_field
    @property
    def count(self) -> int:
        return len(self.data)
