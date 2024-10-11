import asyncio
from datetime import datetime, timedelta
from PyQt5.QtCore import QThread, pyqtSignal
from binance import AsyncClient, BinanceSocketManager
from pandas import DataFrame
from autotrade.Database import Database
from autotrade.Transaction import Transaction, CommandType
from candle import get_bar_data
from strategy.MyStrategy import MyStrategy
from strategy.Strategy import Position

class AutoTrader(QThread):
    transaction_event = pyqtSignal()

    def __init__(self, strategy: MyStrategy, symbol, timeframe):
        super().__init__()
        self.strategy = strategy
        self.symbol = symbol
        self.timeframe = timeframe
        self.database = Database()

    def set_trader(self, strategy: MyStrategy, symbol, timeframe):
        self.strategy = strategy
        self.symbol = symbol
        self.timeframe = timeframe

    def run(self):
        asyncio.run(self.auto_trade())

    async def auto_trade(self):
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
        start = end - timedelta(days=1)
        data = get_bar_data(self.symbol, self.timeframe, str(start), str(end))

        for i in range(0, len(data)):
            d = data.iloc[[i]]
            self.strategy.append_data(d)

    def new_data(self, response):
        data = DataFrame({
            'time': [response['k']['t']],
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
        transaction = Transaction(datetime.now(), CommandType.BUY, self.symbol, data['close'][0], 1)
        self.database.save_transaction(transaction)
        self.transaction_event.emit()

    def sell(self, data):
        transaction = Transaction(data['time'], CommandType.SELL, self.symbol, data['close'][0], 1)
        self.database.save_transaction(transaction)
        self.transaction_event.emit()
