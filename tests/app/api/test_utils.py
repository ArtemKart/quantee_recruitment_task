from pathlib import Path
from unittest.mock import AsyncMock

from pytest_mock import MockerFixture

from app.api.utils import File


async def test_file_from_request(mocker: MockerFixture, tmp_path: Path) -> None:
    mocker.patch("app.api.utils.get_storage_root_dir", return_value=tmp_path)

    test_file_name = "test.txt"
    test_file_size = "1024"
    test_file_path = "uploads"

    mock_request = AsyncMock()
    mock_request.headers = {
        "filename": test_file_name,
        "filesize": test_file_size,
        "pathtosave": test_file_path,
    }

    file = await File.from_request(mock_request)

    assert isinstance(file, File)

    assert file.name == test_file_name
    assert isinstance(file.name, str)

    assert file.size == int(test_file_size)
    assert isinstance(file.size, int)

    assert file._path == Path(test_file_path)
    assert isinstance(file._path, Path)

    assert file.absolute_path == tmp_path / test_file_path / test_file_name
    assert isinstance(file.absolute_path, Path)
