from sqlalchemy import BigInteger, Column, String

from app.db.base import Base


class FileStorage(Base):
    name = Column(String, nullable=False)
    size = Column(BigInteger, nullable=False)
    path = Column(String, nullable=False)
