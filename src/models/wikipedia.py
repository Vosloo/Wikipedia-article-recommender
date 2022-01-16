from sqlalchemy import Column, Text
from sqlalchemy.dialects.postgresql import UUID

from models.tables import DbBase


class Wikipedia(DbBase):
    __tablename__ = "wikipedia"

    id = Column(UUID, primary_key=True)
    url = Column(Text, nullable=False)
    raw_html = Column(Text, nullable=False)
    purified_html = Column(Text, nullable=False)
