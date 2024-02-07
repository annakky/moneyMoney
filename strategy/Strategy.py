from abc import ABCMeta, abstractmethod
from enum import Enum
from typing import List
import pandas
from pandas import DataFrame

class Position(Enum):
    BUY = 1
    NONE = 0
    SELL = -1

class Strategy(metaclass=ABCMeta):
    _data: DataFrame
    _min_size: int
    _indicators: List

    def __init__(self, min_size: int = 20):
        self._min_size = min_size
        self._data = pandas.DataFrame(columns=['time', 'open', 'high', 'low', 'close', 'volume'])

    def append_data(self, data: DataFrame):
        self._data = pandas.concat([self._data, data])
        self.append_indicator(data)

    @abstractmethod
    def append_indicator(self, data):
        pass

    @abstractmethod
    def position(self) -> Position:
        pass

    @abstractmethod
    def draw_indicator(self, chart):
        pass
