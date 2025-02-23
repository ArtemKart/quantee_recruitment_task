from pathlib import Path
from typing import Self
from urllib.parse import unquote

from fastapi import Request

from app.utils import get_storage_root_dir


async def to_megabytes(file_size: int) -> float:
    return file_size / (1024**2)


async def to_gigabytes(file_size: int) -> float:
    return file_size / (1024**3)


class File:
    def __init__(self, name: str, size: int, path: Path, uploaded: bool = False):
        self.name = name
        self.size = size
        self._path = path
        self.absolute_path = None
        self.uploaded = uploaded

    @classmethod
    async def from_request(cls, r: Request) -> Self:
        file_name = unquote(r.headers["filename"])
        file_size = int(r.headers["file_size"])
        rel_path = Path(r.headers["path_to_save"])

        file = cls(name=file_name, size=file_size, path=rel_path)

        absolute_path = await get_storage_root_dir() / rel_path / file_name
        setattr(file, "absolute_path", absolute_path)

        return file
