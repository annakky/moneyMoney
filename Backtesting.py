from backtesting import Strategy, Backtest

from candle import get_bar_data, get_bar_data_for_bt
from strategy.Crossover import Crossover
from strategy.MyStrategy import MyStrategy
from strategy.Strategy import Position

class TestStrategy(Strategy):
    def init(self):
        self._my_strategy = MyStrategy([Crossover(5, 20)], 1)
        self._custom_index = 0
        self._my_data = self._data.df

    def next(self):
        data = self._my_data.iloc[self._custom_index]
        self._my_strategy.append_data(data)
        self._custom_index += 1

        position = self._my_strategy.position()

        if position is Position.BUY:
            self.buy()
        elif position is Position.SELL:
            self.sell()


start = '2022-10-01 00:00:00'
end = '2023-01-01 00:00:00'
ddd = get_bar_data_for_bt('BTC/USDT', '1h', start, end)

bt = Backtest(ddd, TestStrategy, cash=1000000, commission=0.002)
result = bt.run()
print(result)
