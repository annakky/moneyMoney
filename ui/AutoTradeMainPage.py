from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QHeaderView, QTableWidgetItem
from autotrade.AutoTrader import AutoTrader
from autotrade.Database import Database
from autotrade.Transaction import Transaction
from ui.StrategyWidget import StrategyWidget

form_class = uic.loadUiType("static/autotrade-ui.ui")[0]

class AutoTradeMainPage(QWidget, form_class):
    def __init__(self, parent):
        super(AutoTradeMainPage, self).__init__(parent)
        self.setupUi(self)
        self.strategy_widget = StrategyWidget(self)

        self.body_layout.insertWidget(0, self.strategy_widget)
        self.transaction_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.trader = AutoTrader(self.strategy_widget.my_strategy, 'BTCUSDT', '1h')
        self.trader.transaction_event.connect(self.update_transaction_table)
        self.is_autotrade_start = False

        self.database = Database()
        self.update_transaction_table()

    def update_transaction_table(self):
        self.clear_transaction_table()

        transactions = self.database.load_all_transaction()
        for transaction in transactions:
            self.insert_transaction_table(transaction)

    def clear_transaction_table(self):
        row_count = self.transaction_table.rowCount()
        for i in range(0, row_count):
            self.transaction_table.removeRow(0)

    def insert_transaction_table(self, transaction: Transaction):
        row_count = self.transaction_table.rowCount()
        self.transaction_table.insertRow(row_count)

        date_item = QTableWidgetItem(str(transaction.date))
        command_item = QTableWidgetItem(transaction.command.value)
        symbol_item = QTableWidgetItem(transaction.symbol)
        price_item = QTableWidgetItem(str(transaction.price))
        volume_item = QTableWidgetItem(str(transaction.volume))

        self.transaction_table.setItem(row_count, 0, date_item)
        self.transaction_table.setItem(row_count, 1, command_item)
        self.transaction_table.setItem(row_count, 2, symbol_item)
        self.transaction_table.setItem(row_count, 3, price_item)
        self.transaction_table.setItem(row_count, 4, volume_item)

    def push_trade_button(self):
        if self.is_autotrade_start:
            self.stop_autotrade()
        else:
            self.start_autotrade()

    def start_autotrade(self):
        self.is_autotrade_start = True
        self.autotrade_button.setText("중지")
        self.autotrade_button.setStyleSheet("background-color: rgba(200, 0, 0, 200);")

        self.trader.set_trader(self.strategy_widget.my_strategy, 'BTCUSDT', '1m')
        self.trader.start()

    def stop_autotrade(self):
        self.is_autotrade_start = False
        self.autotrade_button.setText("시작")
        self.autotrade_button.setStyleSheet("background-color: rgba(255, 255, 255, 255);")

        self.trader.terminate()
        self.trader.wait()
