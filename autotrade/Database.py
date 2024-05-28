import os
import pandas as pd
from autotrade.Transaction import Transaction, CommandType

class Database:
    FILE_NAME = "/moneyMoney/transaction.csv"
    DIR_NAME = "/moneyMoney"
    headers = ['date', 'command', 'symbol', 'price', 'volume']

    def save_transaction(self, transaction: Transaction):
        data = {
            'date': [transaction.date],
            'command': [transaction.command.value],
            'symbol': [transaction.symbol],
            'price': [transaction.price],
            'volume': [transaction.volume],
        }
        df = pd.DataFrame(data)

        if not os.path.exists(self.DIR_NAME):
            os.mkdir(self.DIR_NAME)
            df.to_csv(self.FILE_NAME, header=True, index=False)
        else:
            df.to_csv(self.FILE_NAME, mode='a', header=False, index=False)

    def save_transactions(self, transactions: [Transaction]):
        data = {
            'date': [transaction.date for transaction in transactions],
            'command': [transaction.command.value for transaction in transactions],
            'symbol': [transaction.symbol for transaction in transactions],
            'price': [transaction.price for transaction in transactions],
            'volume': [transaction.volume for transaction in transactions],
        }
        df = pd.DataFrame(data)

        if not os.path.exists(self.DIR_NAME):
            os.mkdir(self.DIR_NAME)
            df.to_csv(self.FILE_NAME, header=True, index=False)
        else:
            df.to_csv(self.FILE_NAME, mode='a', header=False, index=False)

    # TODO file 없을 때 에러 수정
    def load_all_transaction(self):
        df = pd.read_csv(self.FILE_NAME)
        return Transaction.from_dataframe(df)


# db = Database()
# data = [
#     Transaction.from_timestamp(1715776245, CommandType.BUY, 'BTC', 11.1, 1.1),
#     Transaction.from_timestamp(1715776245, CommandType.BUY, 'BTC', 22.2, 222),
#     Transaction.from_timestamp(1715776245, CommandType.SELL, 'BTC', 33.3, 333)
# ]
# result = db.load_all_transaction()
# for r in result:
#     print(r.date, r.command)
