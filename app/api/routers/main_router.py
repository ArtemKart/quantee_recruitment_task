import logging
from typing import Optional

import aiofiles.os
import aiofiles.ospath
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.api.crud.main_router import (
    read_files_from_db,
    upload_file,
    validate_file,
    write_file_to_db,
)
from app.api.deps import database_session
from app.api.payload.main_router import (
    FileInfoListResponse,
    FileInfoResponse,
    UploadResponse,
)
from app.api.utils import File
from app.db import FileStorage
from app.exceptions.exceptions import ServiceException

logger = logging.getLogger(__name__)

main_router = APIRouter()


@main_router.post("/upload", response_model=Optional[UploadResponse])
async def upload(
    request: Request, session: AsyncSession = Depends(database_session)
) -> Optional[UploadResponse]:
    file = await File.from_request(r=request)

    try:
        await validate_file(file=file.absolute_path)
        await upload_file(r=request, file_path=file.absolute_path)
        file.uploaded = True
        storage_obj = FileStorage(
            name=file.name, size=file.size, path=str(file.absolute_path)
        )
        await write_file_to_db(obj=storage_obj, session=session)

        return UploadResponse(
            status_code=status.HTTP_200_OK,
            details=f"File {file.name} uploaded successfully",
        )

    except Exception as e_info:
        if await aiofiles.ospath.exists(file.absolute_path) and file.uploaded:
            await aiofiles.os.remove(file.absolute_path)
        raise ServiceException(
            detail=f"While handling request, an exception occurred: {e_info}"
        )


@main_router.get("/files", response_model=Optional[FileInfoListResponse])
async def files(
    _r: Request, session: AsyncSession = Depends(database_session)
) -> FileInfoListResponse:
    files_data = await read_files_from_db(session=session)
    return FileInfoListResponse(
        files_info=[FileInfoResponse(**data) for data in files_data]
    )
