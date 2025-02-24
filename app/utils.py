import logging
import os
from pathlib import Path

from dotenv import load_dotenv

from app.exceptions.exceptions import ServiceException

logger = logging.getLogger(__name__)
load_dotenv()


def get_storage_root_dir(name: str = "STORAGE_ROOT_DIR") -> Path:
    path = os.getenv(name)
    if not path:
        raise ServiceException(f"Storage root dir variable: {name} is not set")
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path
