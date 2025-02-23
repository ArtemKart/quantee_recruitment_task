async def to_megabytes(file_size: int) -> float:
    return file_size / (1024**2)


async def to_gigabytes(file_size: int) -> float:
    return file_size / (1024**3)
