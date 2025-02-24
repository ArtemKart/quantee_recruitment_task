from enum import StrEnum, auto


class AllowedExtensions(StrEnum):
    PNG = auto()
    JPG = auto()
    JPEG = auto()
    GIF = auto()
    SVG = auto()
    EXE = auto()
    ZIP = auto()
    INI = auto()
    YML = auto()
    YAML = auto()
    TXT = auto()

    def __str__(self) -> str:
        return f".{self.value}"

    @classmethod
    def to_list(cls) -> list[str]:
        return [str(extension) for extension in cls]
