from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.types import ARRAY

from Database.Models import Base


class WebResources(Base):
    __tablename__ = "webresources"

    id = Column(Integer, primary_key=True, autoincrement=True)
    resource = Column(String, nullable=True)
    link = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    tags = Column(ARRAY(String), nullable=True)
    rating = Column(Integer, nullable=True)
    text = Column(String, nullable=True)
