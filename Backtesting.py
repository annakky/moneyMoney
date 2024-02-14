import pandas
from backtesting import Strategy, Backtest

from candle import get_bar_data
from strategy.Crossover import Crossover
from strategy.MyStrategy import MyStrategy
from strategy.RsiRange import RsiRange
from strategy.Strategy import Position

class TestStrategy(Strategy):
    def init(self):
        crossover = Crossover(5, 20)
        rsi = RsiRange(14)
        self._my_strategy = MyStrategy([crossover, rsi], 2)
        self._custom_index = 0

    def next(self):
        self._custom_index += 1
        data = self.data.df.iloc[[-1]]
        data.columns = data.columns.str.lower()
        self._my_strategy.append_data(data)

        position = self._my_strategy.position()

        if position is Position.BUY:
            self.buy()
        elif position is Position.SELL:
            self.sell()


start = '2021-01-01 00:00:00'
end = '2023-01-01 00:00:00'
df = get_bar_data('BTC/USDT', '1h', start, end)

df.columns = df.columns.str.capitalize()
df.index = pandas.DatetimeIndex(df['Time'])

bt = Backtest(df, TestStrategy, cash=1000000, commission=0.002)
result = bt.run()
print(result)
