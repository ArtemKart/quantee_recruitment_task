from pydantic import BaseModel


class UploadResponse(BaseModel):
    status_code: int
    details: str
