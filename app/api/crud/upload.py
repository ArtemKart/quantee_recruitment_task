import aiofiles
from fastapi import Request

from app import STORAGE_DIR
from app.exceptions.exceptions import FileUploadException
from app.validator.validator import Validator


async def validate_file(file: str) -> None:
    await Validator().validate(file)


async def upload_file(r: Request, file_name: str) -> None:
    try:
        file_path = STORAGE_DIR / file_name
        async with aiofiles.open(file_path, "wb") as f:
            async for chunk in r.stream():
                await f.write(chunk)
    except Exception as e_info:
        raise FileUploadException(
            detail=f"Exception occurred while uploading file: {e_info}"
        )
