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
                    print("NEW DATA")
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
        # TODO database insert에서 잘못된 값 들어가는 버그 수정
        else:
            self.buy(data)

    def buy(self, data):
        print("BUY!!")
        transaction = Transaction(data['time'], CommandType.BUY, self.symbol, data['close'], 1)
        self.database.save_transaction(transaction)
        self.transaction_event.emit()

    def sell(self, data):
        print("SELL!!")
        transaction = Transaction(data['time'], CommandType.SELL, self.symbol, data['close'], 1)
        self.database.save_transaction(transaction)
        self.transaction_event.emit()
