from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .Chats import *  # noqa
from .WebResources import WebResources