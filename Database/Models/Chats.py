from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.types import ARRAY

from Database.Models import Base


class Chats(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_post = Column(Integer, nullable=True)
    id_channel = Column(String, nullable=True)
    link = Column(String, nullable=True)
    date = Column(DateTime, nullable=True)
    tags = Column(ARRAY(String), nullable=True)
    rating = Column(Integer, nullable=True)
    text = Column(String, nullable=True)
