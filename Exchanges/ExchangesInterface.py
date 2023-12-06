import datetime
from abc import ABCMeta
from abc import abstractmethod
from typing import Any
from typing import List
from typing import Optional
from typing import Union
from enum import Enum


class MOEXTimePeriods(Enum):
    ONE_MINUTE = '1m'
    TEN_MINUTES = '10m'
    ONE_HOUR = '1h'
    ONE_DAY = 'D'
    ONE_WEEK = 'W'
    ONE_MONTH = 'M'
    ONE_QUARTER = 'Q'

# print(MOEXTimePeriods.ONE_HOUR)


class ExchangesInterface(object):
    apiKeys: list[str] | None
    __metaclass__ = ABCMeta

    @property
    def modules(self):
        return self.__function_groups.keys()

    @property
    def exchangeName(self):
        return self._exchangeName

    @exchangeName.setter
    def exchangeName(self, value):
        self._exchangeName = value

    @abstractmethod
    def __init__(self, apiKeys: Optional[List[str]]):
        self.apiKeys = apiKeys

    __function_groups = {"key": ["value"]}

