import os
from pathlib import Path

import pytest

from app.exceptions.exceptions import ServiceException
from app.utils import get_storage_root_dir


@pytest.fixture
def env_name() -> str:
    return "DUMMY_ENV"


def test_get_storage_root_dir_happy_path(env_name: str, tmp_path: Path) -> None:
    os.environ[env_name] = str(tmp_path)
    get_storage_root_dir(name=env_name)


def test_get_storage_root_dir_env_not_set(env_name: str) -> None:
    os.environ.pop(env_name, None)
    assert not os.getenv(env_name)
    expected_msg = f"Storage root dir variable: {env_name} is not set"
    with pytest.raises(ServiceException) as e_info:
        get_storage_root_dir(name=env_name)
    assert e_info.value.detail == expected_msg


def test_get_storage_root_dir_should_create_dir(env_name: str, tmp_path: Path) -> None:
    os.environ[env_name] = str(tmp_path / "dummy/path")
    assert not (tmp_path / "dummy/path").exists()
    get_storage_root_dir(name=env_name)
    assert (tmp_path / "dummy/path").exists()
