from datetime import datetime
from enum import Enum

from pandas import DataFrame

class CommandType(Enum):
    BUY = "BUY"
    SELL = "SELL"

    @staticmethod
    def of(string: str):
        if string == "BUY":
            return CommandType.BUY
        elif string == "SELL":
            return CommandType.SELL

        raise ValueError("잘못된 enum value입니다.")

def timestamp_to_datetime(timestamp):
    dt_object = datetime.fromtimestamp(timestamp / 1000)
    return dt_object

class Transaction:
    def __init__(self, date: datetime, command: CommandType, symbol: str, price: float, volume: float):
        self.date = date
        self.command = command
        self.symbol = symbol
        self.price = price
        self.volume = volume

    @classmethod
    def from_timestamp(cls, timestamp: int, command: CommandType, symbol: str, price: float, volume: float):
        cls(timestamp_to_datetime(timestamp), command, symbol, price, volume)

    @staticmethod
    def from_dataframe(dataframe: DataFrame):
        transactions = []
        for index, row in dataframe.iterrows():
            date = datetime.fromisoformat(row['date'])
            command = CommandType.of(row['command'])
            symbol = row['symbol']
            price = float(row['price'])
            volume = float(row['volume'])
            transaction = Transaction(date, command, symbol, price, volume)
            transactions.append(transaction)

        return transactions
