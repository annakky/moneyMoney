from typing import List

from strategy.Strategy import Strategy, Position

class MyStrategy:
    _strategies: List[Strategy]
    _positions: List[Position]
    _threshold: int

    def __init__(self, strategies: List[Strategy], threshold: int):
        self._strategies = strategies
        self._positions = [Position.NONE] * len(strategies)
        self._threshold = threshold

    def position(self):
        for i in range(0, len(self._strategies)):
            position = self._strategies[i].position()
            if position is not Position.NONE:
                self._positions[i] = position

        total = sum(position.value for position in self._positions)

        if abs(total) > self._threshold:
            if total > 0:
                return Position.BUY
            else:
                return Position.SELL
