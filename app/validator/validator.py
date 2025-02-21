from pathlib import Path

from app.exceptions.exceptions import ValidationException
from app.validator.allowed_extensions import AllowedExtensions


class Validator:
    async def validate(self, filename: str) -> None:
        await self._validate_file_extension(filename)

    @staticmethod
    async def _validate_file_extension(filename: str) -> None:
        suffix = Path(filename).suffix
        if suffix not in AllowedExtensions.to_list():
            raise ValidationException(
                detail=(
                    f"Extension: {suffix} is not allowed. "
                    f"Allowed extensions: {AllowedExtensions.to_list()}"
                ),
            )
