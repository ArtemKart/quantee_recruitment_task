import logging
from pathlib import Path
from typing import Self
from urllib.parse import unquote

from fastapi import Request

from app.exceptions.exceptions import RequestException
from app.utils import get_storage_root_dir

logger = logging.getLogger(__name__)


class File:
    def __init__(
        self,
        name: str,
        size: int,
        path: Path,
        absolute_path: Path,
        uploaded: bool = False,
    ):
        self.name = name
        self.size = size
        self._path = path
        self.absolute_path = absolute_path
        self.uploaded = uploaded

    @classmethod
    async def from_request(cls, r: Request) -> Self:
        try:
            file_name = unquote(r.headers["filename"])
            file_size = int(r.headers["filesize"])
            rel_path = Path(r.headers["pathtosave"])
            absolute_path = await get_storage_root_dir() / rel_path / file_name

            return cls(
                name=file_name,
                size=file_size,
                path=rel_path,
                absolute_path=absolute_path,
            )

        except Exception as e_info:
            logger.error(f"Exception occurred while handling the request: {e_info}")
            raise RequestException(
                f"Exception occurred while handling the request: {e_info}"
            )
