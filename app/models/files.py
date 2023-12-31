from pydantic import BaseModel, computed_field


class FileUploadInfo(BaseModel):
    filename: str
    accepted: bool
    id: str | None = None
    errors: list[str] = []
    zip_filename: str | None = None


class FilesUploadTask(BaseModel):
    data: list[FileUploadInfo]

    @computed_field
    @property
    def count(self) -> int:
        return len(self.data)
