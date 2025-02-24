import logging
import os
from pathlib import Path

import aiofiles.os
import aiofiles.ospath
from dotenv import load_dotenv
from fastapi.concurrency import run_in_threadpool

from app.exceptions.exceptions import ServiceException

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
load_dotenv()


def get_env(name: str) -> str | None:
    return os.getenv(name)


async def get_storage_root_dir(name: str = "STORAGE_ROOT_DIR") -> Path:
    path = Path(await run_in_threadpool(get_env, name))
    if not path:
        raise ServiceException("Storage root dir variable is not set")
    if not await aiofiles.ospath.exists(path):
        logger.info(f"Storage root dir: {path} does not exist. Creating...")
        await aiofiles.os.makedirs(path)
    return Path(path)
