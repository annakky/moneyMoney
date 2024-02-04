from backtesting.lib import crossover
from pandas import DataFrame
from strategy.Strategy import Strategy, Position
from strategy.sma import calculate_sma, calculate_sma_list

class Crossover(Strategy):
    def init(self):
        pass

    def next(self):
        pass

    def __init__(self, data: DataFrame, short_period: int, long_period: int):
        # if short_period >= long_period:
        #     raise AttributeError("Short Period should smaller than Long Period.")
        # if len(data) < long_period:
        #     raise AttributeError("Data length should be bigger than Long Period.")

        super().__init__(data)
        self._short = short_period
        self._long = long_period

    def position(self) -> Position:
        sma_short = calculate_sma_list(self._data, self._short)
        sma_long = calculate_sma_list(self._data, self._long)

        sma_short_before = sma_short[-2]
        sma_short_now = sma_short[-1]
        sma_long_before = sma_long[-2]
        sma_long_now = sma_long[-1]

        if sma_short_before == sma_long_before:
            sma_short_before = sma_short[-3]
            sma_long_before = sma_long[-3]

        if sma_short_before < sma_long_before and sma_short_now > sma_long_now:
            return Position.BUY

        elif sma_short_before > sma_long_before and sma_short_now < sma_long_now:
            return Position.SELL

        return Position.NONE
