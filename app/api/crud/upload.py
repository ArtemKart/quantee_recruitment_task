import logging
from pathlib import Path

import aiofiles
import aiofiles.os
import aiofiles.ospath
from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import database_session
from app.db import FileStorage
from app.exceptions.exceptions import DatabaseException, FileUploadException
from app.validator.validator import Validator

logger = logging.getLogger(__name__)


async def validate_file(file: Path) -> None:
    await Validator().validate(file)


async def upload_file(r: Request, file_path: Path) -> None:
    try:
        if not await aiofiles.ospath.exists(file_path.parent):
            await aiofiles.os.mkdir(file_path.parent)
            logger.info(
                f"Directory: {file_path.parent} does not exist. "
                f"Creating directory: {file_path.parent}"
            )
        async with aiofiles.open(file_path, "wb") as f:
            async for chunk in r.stream():
                await f.write(chunk)
    except Exception as e_info:
        logger.error(f"Exception occurred while uploading file: {e_info}")
        raise FileUploadException(
            detail=f"Exception occurred while uploading file: {e_info}"
        )


async def write_metadata(
    obj: FileStorage, session: AsyncSession = Depends(database_session)
) -> None:
    try:
        session.add(obj)
        await session.commit()
    except Exception as e_info:
        raise DatabaseException(
            f"Exception occurred during interaction with database: {e_info}"
        )
