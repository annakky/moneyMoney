from strategy.Strategy import Strategy, Position
from strategy.rsi import calculate_latest_rsi, calculate_rsi

class RsiRange(Strategy):
    def __init__(self, period: int, low, high):
        super().__init__(period)
        self._period = period
        self._rsi = []
        self._low = low
        self._high = high
        self._subchart = None
        self._line = None

    def append_indicator(self, data):
        self._rsi.append(calculate_latest_rsi(self._data, self._period))

    def position(self) -> Position:
        if self._rsi[-1] is None:
            return Position.NONE

        if self._rsi[-1] < self._low:
            return Position.BUY
        elif self._rsi[-1] > self._high:
            return Position.SELL

        return Position.NONE

    def draw_indicator(self, chart):
        chart.resize(chart.width, chart.height - 0.2)

        if self._subchart is None:
            self._subchart = chart.create_subchart(position='bottom', width=1, height=0.2, sync=True)

        self._subchart.resize(1, 0.2)
        line = self._subchart.create_line(name='RSI', price_line=False, price_label=False, color='#FFFF00')
        line.set(calculate_rsi(chart.bars, self._period))

        line.horizontal_line(self._low)
        line.horizontal_line(self._high)
        self._line = line

    def clear_indicator(self, chart):
        chart.resize(chart.width, chart.height + 0.2)

        if self._subchart is None:
            return

        self._subchart.resize(0, 0)
        self._subchart.clear_horizontal_lines()
        self._line.delete()
