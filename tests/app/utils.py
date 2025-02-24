from pathlib import Path

import aiofiles
import aiofiles.ospath


async def validate_files_identicalness(
    tested_file_path: Path, mock_file_path: Path
) -> None:
    async with aiofiles.open(tested_file_path, "rb") as tested_file:
        tested_content_file = await tested_file.read()
        async with aiofiles.open(mock_file_path, "rb") as mocked_file:
            mocked_content_file = await mocked_file.read()

            assert tested_content_file == mocked_content_file

            assert await aiofiles.ospath.getsize(
                tested_file_path
            ) == await aiofiles.ospath.getsize(mock_file_path)
