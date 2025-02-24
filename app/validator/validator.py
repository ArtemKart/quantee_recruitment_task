import logging
from pathlib import Path

import aiofiles.ospath

from app.exceptions.exceptions import ValidationException
from app.validator.allowed_extensions import AllowedExtensions

logger = logging.getLogger(__name__)


class Validator:
    async def validate(self, file: Path) -> None:
        await self._validate_file_extension(file)
        await self._validate_if_file_already_exists(file)

    @staticmethod
    async def _validate_file_extension(file: Path) -> None:
        if file.suffix not in await AllowedExtensions.to_list():
            logger.error(
                f"Extension: {file.suffix} is not allowed. "
                f"Allowed extensions: {await AllowedExtensions.to_list()}"
            )
            raise ValidationException(
                detail=(
                    f"Extension: {file.suffix} is not allowed. "
                    f"Allowed extensions: {await AllowedExtensions.to_list()}"
                ),
            )

    @staticmethod
    async def _validate_if_file_already_exists(file: Path) -> None:
        if await aiofiles.ospath.exists(file):
            logger.error(f"File {file.name} already exists in the storage")
            raise ValidationException(
                detail=f"File {file.name} already exists in the storage"
            )
