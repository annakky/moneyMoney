from abc import ABCMeta, abstractmethod
from enum import Enum
from pandas import DataFrame

class Position(Enum):
    BUY = 1
    NONE = 0
    SELL = -1

class Strategy(metaclass=ABCMeta):
    def __init__(self, data: DataFrame):
        self._data = data

    @abstractmethod
    def position(self) -> Position:
        pass
