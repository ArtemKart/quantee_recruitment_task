import shutil
from pathlib import Path

import pytest

from app.exceptions.exceptions import ValidationException
from app.validator.validator import Validator


@pytest.mark.parametrize(
    "file, exception_msg",
    [
        (
            "/dummy_path/dummy_file.txt",
            None,
        ),
        (
            "/dummy_path/dummy_file.101",
            (
                "Extension: .101 is not allowed. Allowed extensions: "
                "['.png', '.jpg', '.jpeg', '.gif', '.svg', '.exe', "
                "'.zip', '.ini', '.yml', '.yaml', '.txt']"
            ),
        ),
    ],
    ids=["happy_path", "error_expected"],
)
async def test_validate_file_extension(file: str, exception_msg: str | None) -> None:
    if not exception_msg:
        await Validator()._validate_file_extension(Path(file))
    else:
        with pytest.raises(ValidationException) as e_info:
            await Validator()._validate_file_extension(Path(file))
        assert exception_msg == e_info.value.detail


async def test_validate_if_file_already_exists(
    test_txt_file: Path, tmp_path: Path
) -> None:
    file = tmp_path / test_txt_file.name
    assert not file.exists()
    shutil.copy(test_txt_file, tmp_path)
    assert file.exists()

    exception_msg = f"File {file.name} already exists in the storage"
    with pytest.raises(ValidationException) as e_info:
        await Validator()._validate_if_file_already_exists(file)
    assert exception_msg == e_info.value.detail
