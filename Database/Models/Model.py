from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.types import ARRAY

from Database.Models import Base


class Chats(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_post = Column(Integer, nullable=False)
    id_channel = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    text = Column(String, nullable=True)
    link = Column(String, nullable=False)