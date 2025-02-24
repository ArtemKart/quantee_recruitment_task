import logging
from pathlib import Path

from app.exceptions.exceptions import ValidationException
from app.validator.allowed_extensions import AllowedExtensions

logger = logging.getLogger(__name__)


class Validator:
    def validate(self, file: Path) -> None:
        self._validate_file_extension(file)
        self._validate_if_file_already_exists(file)

    @staticmethod
    def _validate_file_extension(file: Path) -> None:
        if file.suffix not in AllowedExtensions.to_list():
            logger.error(
                f"Extension: {file.suffix} is not allowed. "
                f"Allowed extensions: {AllowedExtensions.to_list()}"
            )
            raise ValidationException(
                detail=(
                    f"Extension: {file.suffix} is not allowed. "
                    f"Allowed extensions: {AllowedExtensions.to_list()}"
                ),
            )

    @staticmethod
    def _validate_if_file_already_exists(file: Path) -> None:
        if file.exists():
            logger.error(f"File {file.name} already exists in the storage")
            raise ValidationException(
                detail=f"File {file.name} already exists in the storage"
            )
