from typing import Final

__version__ = "0.0.1"


_api_version: Final[str] = "1"
_api_prefix: Final[str] = f"/api/v{_api_version}"


def get_api_prefix() -> str:
    return _api_prefix


def get_api_version() -> str:
    return _api_version
