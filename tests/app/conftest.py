from pathlib import Path
from typing import Generator
from unittest.mock import AsyncMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.testclient import TestClient

from app.api.deps import database_session
from app.api.main import app
from tests import get_resources


@pytest.fixture()
def test_txt_file() -> Path:
    return get_resources("test_upload_file.txt")


@pytest.fixture
def mock_session() -> Generator[AsyncMock, None, None]:
    yield AsyncMock(spec=AsyncSession)


@pytest.fixture
def client(mock_session: AsyncMock) -> Generator[TestClient, None, None]:
    app.dependency_overrides[database_session] = lambda: mock_session
    yield TestClient(app)
