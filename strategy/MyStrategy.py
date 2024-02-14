from typing import List
from pandas import DataFrame

from strategy.Strategy import Strategy, Position

class MyStrategy:
    _strategies: List[Strategy]
    _positions: List[Position]
    _threshold: int

    def __init__(self, strategies: List[Strategy], threshold: int):
        self._strategies = strategies
        self._positions = [Position.NONE] * len(strategies)
        self._threshold = threshold
        self._position = Position.NONE
        self._is_position_calculated = False

    def draw_indicators(self, chart):
        for strategy in self._strategies:
            strategy.draw_indicator(chart)

    def clear_indicators(self, chart):
        for strategy in self._strategies:
            strategy.clear_indicator(chart)

    def append_data(self, data: DataFrame):
        self._is_position_calculated = False
        for s in self._strategies:
            s.append_data(data)

    def position(self):
        if self._is_position_calculated is True:
            return self._position

        for i in range(0, len(self._strategies)):
            self._positions[i] = self._strategies[i].position()

        self._is_position_calculated = True
        total = sum(position.value for position in self._positions)

        if abs(total) >= self._threshold:
            if total > 0 and self._position is not Position.BUY:
                self._position = Position.BUY
                return Position.BUY
            elif total < 0 and self._position is not Position.SELL:
                self._position = Position.SELL
                return Position.SELL

        self._position = Position.NONE
        return Position.NONE
