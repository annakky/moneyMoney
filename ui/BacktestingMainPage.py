from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QTableWidgetItem
from backtest.Tester import Tester
from ui.StrategyWidget import StrategyWidget

form_class = uic.loadUiType("static/backtesting-ui.ui")[0]

class BacktestingMainPage(QWidget, form_class):
    def __init__(self, parent):
        super(BacktestingMainPage, self).__init__(parent)
        self.setupUi(self)
        self.strategy_widget = StrategyWidget(self)

        self.body_layout.insertWidget(0, self.strategy_widget)
        self.tester = Tester()

    def run_backtesting(self):
        string_format = 'yyyy-MM-dd hh:mm:ss'
        start = self.start_value.dateTime().toString(string_format)
        end = self.end_value.dateTime().toString(string_format)
        symbol = 'BTC/USDT'
        timeframe = '1h'

        self.strategy_widget.create_strategy()
        result = self.tester.run(self.strategy_widget.my_strategy, start, end, symbol, timeframe)

        self.result_table.setItem(0, 1, QTableWidgetItem(str(result.get('Return [%]'))))
        self.result_table.setItem(1, 1, QTableWidgetItem(str(result.get('Win Rate [%]'))))
        self.result_table.setItem(2, 1, QTableWidgetItem(str(result.get('# Trades'))))
        self.result_table.setItem(3, 1, QTableWidgetItem(str(result.get('Buy & Hold Return [%]'))))
