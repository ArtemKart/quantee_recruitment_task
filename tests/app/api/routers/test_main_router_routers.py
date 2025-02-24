from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock
from urllib.parse import quote

import pytest
from pytest_mock import MockerFixture
from starlette.testclient import TestClient


def test_upload_endpoint(
    client: TestClient, test_txt_file: Path, mocker: MockerFixture, tmp_path: Path
) -> None:
    mocker.patch("app.api.utils.get_storage_root_dir", return_value=Path(tmp_path))
    test_headers = {
        "filename": quote(test_txt_file.name),
        "pathtosave": "text_files",
        "filesize": "1000",
    }
    with open(test_txt_file, "rb") as f:
        r = client.post(url="/upload", data=f, headers=test_headers)

    assert r.status_code == 200
    assert (
        r.json()["details"] == f"File {quote(test_txt_file.name)} uploaded successfully"
    )


@pytest.mark.parametrize(
    "mock_value, expected_value",
    [
        (
            [
                {
                    "name": "file1.txt",
                    "size": 1024,
                    "path": "/path/to/file1.txt",
                    "date": "2025-02-24T00:00:00",
                },
            ],
            [
                {
                    "name": "file1.txt",
                    "size": 1024,
                    "path": "/path/to/file1.txt",
                    "date": "2025-02-24T00:00:00",
                },
            ],
        ),
        ([], []),
    ],
)
def test_file_endpoint(
    client: TestClient,
    mock_session: AsyncMock,
    mock_value: dict[list[Any]],
    expected_value: dict[list[Any]],
) -> None:
    mock_result = MagicMock()
    mock_result.mappings.return_value = mock_value
    mock_session.execute.return_value = mock_result

    r = client.get("/files")

    assert r.status_code == 200
    assert r.json() == {"files_info": expected_value}
