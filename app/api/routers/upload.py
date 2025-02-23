import logging
from pathlib import Path
from typing import Optional
from urllib.parse import unquote

import aiofiles.os
import aiofiles.ospath
from fastapi import APIRouter, Request
from starlette import status

from app.api.crud.upload import upload_file, validate_file, write_metadata
from app.api.payload.upload import UploadResponse
from app.db import FileStorage
from app.exceptions.exceptions import ServiceException
from app.utils import get_storage_root_dir

logger = logging.getLogger(__name__)

upload_router = APIRouter()


@upload_router.post("/upload", response_model=Optional[UploadResponse])
async def upload(request: Request) -> Optional[UploadResponse]:
    storage_root_dir = await get_storage_root_dir()
    file_path = request.headers["path_to_save"]
    file_name = unquote(request.headers["filename"])
    file: Path = storage_root_dir / file_path / file_name
    file_size = int(request.headers["file_size"])

    try:
        await validate_file(file=file)
        await upload_file(r=request, file_path=file)

        storage_obj = FileStorage(name=file.name, size=file_size, path=file.parent)
        await write_metadata(obj=storage_obj)

        return UploadResponse(
            status_code=status.HTTP_200_OK,
            details=f"File {file_name} uploaded successfully",
        )

    except Exception as e_info:
        if await aiofiles.ospath.exists(file):
            await aiofiles.os.remove(file)
        raise ServiceException(
            detail=f"While handling request, an exception occurred: {e_info}"
        )
