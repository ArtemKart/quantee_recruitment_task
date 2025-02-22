from typing import Optional
from urllib.parse import unquote

from fastapi import APIRouter, Request

from app.api.crud.upload import upload_file, validate_file
from app.api.payload.upload import UploadResponse
from app.exceptions.exceptions import ServiceException

upload_router = APIRouter()


@upload_router.post("/upload", response_model=Optional[UploadResponse])
async def upload(request: Request) -> Optional[UploadResponse]:
    try:
        file_name = unquote(request.headers["filename"])
        await validate_file(file=file_name)
        await upload_file(r=request, file_name=file_name)
        return UploadResponse(
            status_code=200, detail=f"File {file_name} uploaded successfully"
        )
    except Exception as e_info:
        raise ServiceException(
            detail=f"While handling request, an exception occurred: {e_info}"
        )
