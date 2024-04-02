import pandas
from backtesting import Backtest, Strategy
from candle import get_bar_data
from strategy import MyStrategy
from strategy.Strategy import Position

class Tester:
    def __init__(self):
        pass

    def run(self, strategy: MyStrategy, start, end, symbol, timeframe):
        class TestingStrategy(Strategy):
            def init(self):
                self._my_strategy = strategy
                self._custom_index = 0

                self.size = self._my_strategy.position_size
                self.sl = self._my_strategy.stop_loss

            def next(self):
                self._custom_index += 1
                data = self.data.df.iloc[[-1]]
                data.columns = data.columns.str.lower()
                self._my_strategy.append_data(data)

                price = self.data.Close[-1]

                position = self._my_strategy.position()

                if position is Position.BUY:
                    self.buy(size=self.size, sl=price * self.sl)
                elif position is Position.SELL:
                    self.sell()

        data = get_bar_data(symbol, timeframe, start, end)
        data.columns = data.columns.str.capitalize()
        data.index = pandas.DatetimeIndex(data['Time'])

        backtesting = Backtest(data, TestingStrategy, cash=1000000, commission=0.005)
        result = backtesting.run()

        print(result)
        print(result.get('Return [%]'))
        return result
