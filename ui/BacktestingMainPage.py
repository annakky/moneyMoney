from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QHeaderView
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
        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def run_backtesting(self):
        string_format = 'yyyy-MM-dd hh:mm:ss'
        start = self.start_value.dateTime().toString(string_format)
        end = self.end_value.dateTime().toString(string_format)
        symbol = 'BTC/USDT'
        timeframe = '1h'
        stop_loss = (100 + self.stoploss_value.value()) / 100

        self.strategy_widget.create_strategy(stop_loss)

        result = self.tester.run(self.strategy_widget.my_strategy, start, end, symbol, timeframe)
        self.update_table_widget_item(0, 1, str(result.get('Return [%]')))
        self.update_table_widget_item(1, 1, str(result.get('Win Rate [%]')))
        self.update_table_widget_item(2, 1, str(result.get('# Trades')))
        self.update_table_widget_item(3, 1, str(result.get('Buy & Hold Return [%]')))
        self.update_table_widget_item(4, 1, str(result.get('Best Trade [%]')))
        self.update_table_widget_item(5, 1, str(result.get('Worst Trade [%]')))

    def update_table_widget_item(self, row: int, column: int, data: str):
        if data == 'nan':
            item = QTableWidgetItem("결과없음")
            item.setTextAlignment(Qt.AlignCenter)
            self.result_table.setItem(row, column, item)
        else:
            item = QTableWidgetItem(self.process_value(data))
            item.setTextAlignment(Qt.AlignCenter)

            self.result_table.setItem(row, column, item)

    def process_value(self, value):
        float_value = float(value)
        if float_value.is_integer():
            return value
        else:
            return "{:.2f}".format(round(float_value, 2))
