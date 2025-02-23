import logging
from pathlib import Path
from typing import Any

import aiofiles
import aiofiles.os
import aiofiles.ospath
from fastapi import Request
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import FileStorage
from app.exceptions.exceptions import DatabaseException, FileUploadException
from app.validator.validator import Validator

logger = logging.getLogger(__name__)


async def validate_file(file: Path) -> None:
    await Validator().validate(file)


async def upload_file(r: Request, file_path: Path) -> None:
    try:
        if not await aiofiles.ospath.exists(file_path.parent):
            await aiofiles.os.makedirs(file_path.parent)
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


async def write_file_to_db(obj: FileStorage, session: AsyncSession) -> None:
    try:
        session.add(obj)
        await session.commit()
    except Exception as e_info:
        logger.error(
            f"An exception occurred while writing "
            f"file metadata to the database: {e_info}"
        )
        raise DatabaseException(
            f"An exception occurred while writing "
            f"file metadata to the database: {e_info}"
        )


async def read_files_from_db(session: AsyncSession) -> list[dict[str, Any]] | None:
    try:
        stmt = text("SELECT * FROM public.filestorage")
        raw = await session.execute(stmt)
        return [dict(row) for row in raw.mappings()]
    except Exception as e_info:
        logger.error(
            f"An exception occurred while " f"fetching data from database: {e_info}"
        )
        raise DatabaseException(
            f"An exception occurred while " f"fetching data from database: {e_info}"
        )
