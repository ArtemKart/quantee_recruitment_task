from datetime import datetime

from pydantic import BaseModel


class UploadResponse(BaseModel):
    status_code: int
    details: str


class FileInfoResponse(BaseModel):
    name: str
    size: int
    path: str
    date: datetime


class FileInfoListResponse(BaseModel):
    files_info: list[FileInfoResponse]
