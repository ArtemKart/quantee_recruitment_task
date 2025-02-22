import logging
from typing import Optional
from urllib.parse import unquote

import aiofiles.ospath
from aiofiles.os import remove
from fastapi import APIRouter, Request
from starlette import status

from app import STORAGE_DIR
from app.api.crud.upload import upload_file, validate_file
from app.api.payload.upload import UploadResponse
from app.api.utils import to_megabytes
from app.exceptions.exceptions import ServiceException

logger = logging.getLogger(__name__)

upload_router = APIRouter()


@upload_router.post("/upload", response_model=Optional[UploadResponse])
async def upload(request: Request) -> Optional[UploadResponse]:
    file_name = unquote(request.headers["filename"])
    file_path = STORAGE_DIR / file_name
    try:
        # file_size = await to_megabytes(file_size=int(request.headers["content-length"]))
        await validate_file(file=file_name)
        await upload_file(r=request, file_name=file_name, file_path=file_path)
        return UploadResponse(
            status_code=status.HTTP_200_OK,
            details=f"File {file_name} uploaded successfully",
        )
    except Exception as e_info:
        if await aiofiles.ospath.exists(file_path):
            await remove(STORAGE_DIR / file_name)

        logger.error(f"While handling request, an exception occurred: {e_info}")
        raise ServiceException(
            detail=f"While handling request, an exception occurred: {e_info}"
        )
