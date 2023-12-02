from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .Model import *  # noqa