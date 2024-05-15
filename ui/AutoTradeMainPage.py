from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QHeaderView, QTableWidgetItem

from autotrade.AutoTrader import AutoTrader
from autotrade.Database import Database
from ui.StrategyWidget import StrategyWidget

form_class = uic.loadUiType("static/autotrade-ui.ui")[0]

class AutoTradeMainPage(QWidget, form_class):
    def __init__(self, parent):
        super(AutoTradeMainPage, self).__init__(parent)
        self.setupUi(self)
        self.strategy_widget = StrategyWidget(self)

        self.body_layout.insertWidget(0, self.strategy_widget)
        self.transaction_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.trader = AutoTrader(self.strategy_widget.my_strategy, 'BTC/USDT', '1h')
        self.is_autotrade_start = False

        self.database = Database()
        self.update_transaction_table()

    def update_transaction_table(self):
        transactions = self.database.load_all_transaction()
        # TODO: INSERT TABLE DATA

    def push_trade_button(self):
        if self.is_autotrade_start:
            self.stop_autotrade()
        else:
            self.start_autotrade()

    def start_autotrade(self):
        self.is_autotrade_start = True
        self.autotrade_button.setText("중지")
        self.autotrade_button.setStyleSheet("background-color: rgba(200, 0, 0, 200);")

        self.trader.set_trader(self.strategy_widget.my_strategy, 'BTC/USDT', '1h')
        self.trader.run()

    def stop_autotrade(self):
        self.is_autotrade_start = False
        self.autotrade_button.setText("시작")
        self.autotrade_button.setStyleSheet("background-color: rgba(255, 255, 255, 255);")
