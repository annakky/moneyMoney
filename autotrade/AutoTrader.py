from datetime import datetime, timedelta
from binance import AsyncClient, BinanceSocketManager
from pandas import DataFrame
from autotrade.Database import Database
from autotrade.Transaction import Transaction, CommandType
from candle import get_bar_data
from strategy.MyStrategy import MyStrategy
from strategy.Strategy import Position

class AutoTrader:
    def __init__(self, strategy: MyStrategy, symbol, timeframe):
        self.strategy = strategy
        self.symbol = symbol
        self.timeframe = timeframe
        self.database = Database()

    def set_trader(self, strategy: MyStrategy, symbol, timeframe):
        self.strategy = strategy
        self.symbol = symbol
        self.timeframe = timeframe

    async def run(self):
        client = await AsyncClient.create()
        socket_manager = BinanceSocketManager(client)
        self.set_past_data()

        socket = socket_manager.kline_socket(self.symbol, interval=self.timeframe)

        async with socket:
            while True:
                response = await socket.recv()
                close_time = response['k']['T']
                event_time = response['E']

                if event_time > close_time:
                    self.new_data(response)

    def set_past_data(self):
        end = datetime.now()
        start = end - timedelta(days=365)
        data = get_bar_data(self.symbol, self.timeframe, str(start), str(end))

        for i in range(0, len(data)):
            d = data.iloc[[i]]
            self.strategy.append_data(d)

    def new_data(self, response):
        data = DataFrame({
            'time': [datetime.fromtimestamp(response['k']['t'] / 1000)],
            'open': [response['k']['o']],
            'high': [response['k']['h']],
            'low': [response['k']['l']],
            'close': [response['k']['c']],
            'volume': [response['k']['v']]
        })
        self.strategy.append_data(data)

        position = self.strategy.position()
        if position is Position.BUY:
            self.buy(data)
        elif position is Position.SELL:
            self.sell(data)

    def buy(self, data):
        print("BUY!!")
        transaction = Transaction(data['time'], CommandType.BUY, self.symbol, data['close'], 1)
        self.database.save_transaction(transaction)

    def sell(self, data):
        print("SELL!!")
        transaction = Transaction(data['time'], CommandType.SELL, self.symbol, data['close'], 1)
        self.database.save_transaction(transaction)
