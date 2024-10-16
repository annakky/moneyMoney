from strategy.Strategy import Strategy, Position
from strategy.sma import calculate_latest_sma, calculate_sma

class Crossover(Strategy):
    def __init__(self, short_period: int, long_period: int):
        if short_period >= long_period:
            raise AttributeError("Short Period should smaller than Long Period.")

        super().__init__(long_period)
        self._short = short_period
        self._long = long_period
        self._short_sma = []
        self._long_sma = []

        self._short_line = None
        self._long_line = None

    def append_indicator(self, data):
        self._short_sma.append(calculate_latest_sma(self._data, self._short))
        self._long_sma.append(calculate_latest_sma(self._data, self._long))

    def position(self) -> Position:
        if self._long_sma[-1] is None or self._long_sma[-2] is None:
            return Position.NONE

        sma_short_before = self._short_sma[-2]
        sma_short_now = self._short_sma[-1]
        sma_long_before = self._long_sma[-2]
        sma_long_now = self._long_sma[-1]

        if sma_short_before == sma_long_before and self._long_sma[-3] is not None:
            sma_short_before = self._short_sma[-3]
            sma_long_before = self._long_sma[-3]

        if sma_short_before < sma_long_before and sma_short_now > sma_long_now:
            return Position.BUY

        elif sma_short_before > sma_long_before and sma_short_now < sma_long_now:
            return Position.SELL

        return Position.NONE

    def draw_indicator(self, chart):
        line_short = chart.create_line(name='SMA', price_line=False, price_label=False, color="#FFFF33")
        line_short.set(calculate_sma(chart.bars, self._short))
        self._short_line = line_short

        line_long = chart.create_line(name='SMA', price_line=False, price_label=False, color="#99FFFF")
        line_long.set(calculate_sma(chart.bars, self._long))
        self._long_line = line_long

    def clear_indicator(self, chart):
        if self._short_line is not None:
            self._short_line.delete()
            self._short_sma = []
            self._short_line = None
        if self._long_line is not None:
            self._long_line.delete()
            self._long_sma = []
            self._long_line = None
