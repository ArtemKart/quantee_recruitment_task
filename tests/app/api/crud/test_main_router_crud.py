from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import aiofiles
import aiofiles.ospath
import pytest
from fastapi import FastAPI, Request
from httpx import ASGITransport, AsyncClient

from app.api.crud.main_router import read_files_from_db, upload_file, write_file_to_db
from app.exceptions.exceptions import DatabaseException
from tests.app.utils import validate_files_identicalness

fake_app = FastAPI()


@fake_app.post("/upload")
async def upload_endpoint(request: Request, file_path: str):
    await upload_file(request, Path(file_path))
    return {"message": "File uploaded successfully"}


@pytest.fixture
async def fake_client() -> AsyncClient:
    transport = ASGITransport(app=fake_app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client


async def test_upload_file_happy_path(
    fake_client: AsyncClient, test_txt_file: Path, tmp_path: Path
) -> None:
    file_path = tmp_path / test_txt_file.name
    async with aiofiles.open(test_txt_file, "rb") as f:
        response = await fake_client.post(f"/upload?file_path={file_path}", data=f)

        assert response.status_code == 200
        assert response.json() == {"message": "File uploaded successfully"}

    await validate_files_identicalness(
        tested_file_path=file_path, mock_file_path=test_txt_file
    )


async def test_upload_file_if_path_not_exists(
    fake_client: AsyncClient, test_txt_file: Path, tmp_path: Path
) -> None:
    file_path = tmp_path / "nonexistent_path"
    assert not await aiofiles.ospath.exists(file_path)

    async with aiofiles.open(test_txt_file, "rb") as f:
        response = await fake_client.post(f"/upload?file_path={file_path}", data=f)
        assert response.status_code == 200
        assert response.json() == {"message": "File uploaded successfully"}

    assert await aiofiles.ospath.exists(file_path)
    await validate_files_identicalness(
        tested_file_path=file_path, mock_file_path=test_txt_file
    )


async def test_write_file_to_db(mock_session: AsyncMock) -> None:
    mock_file_storage = AsyncMock()
    await write_file_to_db(obj=mock_file_storage, session=mock_session)

    mock_session.add.assert_called_once_with(mock_file_storage)
    mock_session.commit.assert_awaited_once()


async def test_write_file_to_db_error(mock_session: AsyncMock) -> None:
    mock_file_storage = AsyncMock()
    mock_session.commit.side_effect = DatabaseException(
        "An exception occurred while writing file metadata to the database:"
    )

    with pytest.raises(
        DatabaseException,
        match="An exception occurred while writing file metadata to the database:",
    ):
        await write_file_to_db(obj=mock_file_storage, session=mock_session)

    mock_session.add.assert_called_once_with(mock_file_storage)
    mock_session.commit.assert_awaited_once()


@pytest.mark.parametrize(
    "execute_return, expected",
    [
        (
            [
                {
                    "name": "file1.txt",
                    "size": 1024,
                    "path": "/path/to/file1.txt",
                    "date": "2025-02-24",
                },
                {
                    "name": "file2.txt",
                    "size": 2048,
                    "path": "/path/to/file2.txt",
                    "date": "2025-02-02",
                },
            ],
            [
                {
                    "name": "file1.txt",
                    "size": 1024,
                    "path": "/path/to/file1.txt",
                    "date": "2025-02-24",
                },
                {
                    "name": "file2.txt",
                    "size": 2048,
                    "path": "/path/to/file2.txt",
                    "date": "2025-02-02",
                },
            ],
        ),
        ([], []),
    ],
)
async def test_read_files_from_db(
    execute_return: list, expected: list, mock_session: AsyncMock
) -> None:
    mock_result = MagicMock()
    mock_result.mappings.return_value = execute_return
    mock_session.execute.return_value = mock_result
    result = await read_files_from_db(session=mock_session)

    assert result == expected
    mock_session.execute.assert_called_once()
