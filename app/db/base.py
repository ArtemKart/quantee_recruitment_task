from sqlalchemy.ext.declarative import declarative_base, declared_attr


class Base(object):
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()  # type: ignore[attr-defined]


Base = declarative_base(cls=Base)  # type: ignore[misc]
