import time

import pandas
from PyQt5 import uic
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QHeaderView, QGraphicsOpacityEffect
from backtest.Tester import Tester
from ui.LoadingWidget import LoadingWidget
from ui.StrategyWidget import StrategyWidget

form_class = uic.loadUiType("static/backtesting-ui.ui")[0]

class BacktestWorker(QThread):
    result_event = pyqtSignal(pandas.Series)

    def __init__(self, tester, strategy, start, end, symbol, timeframe):
        super().__init__()
        self._tester = tester
        self._strategy = strategy
        self._start = start
        self._end = end
        self._symbol = symbol
        self._timeframe = timeframe

    def run(self):
        result = self._tester.run(self._strategy, self._start, self._end, self._symbol, self._timeframe)
        self.result_event.emit(result)

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
        timeframe = self.timeframe_value.currentText()
        stop_loss = (100 + self.stoploss_value.value()) / 100

        self.backtesting_start()

        self.strategy_widget.create_strategy(stop_loss)
        self.worker_thread = BacktestWorker(self.tester, self.strategy_widget.my_strategy, start, end, symbol, timeframe)
        self.worker_thread.result_event.connect(self.update_table_widget)
        self.worker_thread.finished.connect(self.backtesting_finish)
        self.worker_thread.start()

    def backtesting_start(self):
        self.run_backtest_button.setEnabled(False)
        self.result_table.setStyleSheet("background-color: rgba(210, 210, 210, 150);")
        self.loading_widget = LoadingWidget(self.result_table)
        self.loading_widget.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.loading_widget.start()

    def backtesting_finish(self):
        self.run_backtest_button.setEnabled(True)
        self.loading_widget.deleteLater()
        self.result_table.setStyleSheet("background-color: white;")

    @pyqtSlot(pandas.Series)
    def update_table_widget(self, data: pandas.Series):
        self.update_table_widget_item(0, 1, str(data.get('Return [%]')))
        self.update_table_widget_item(1, 1, str(data.get('Win Rate [%]')))
        self.update_table_widget_item(2, 1, str(data.get('# Trades')))
        self.update_table_widget_item(3, 1, str(data.get('Buy & Hold Return [%]')))
        self.update_table_widget_item(4, 1, str(data.get('Best Trade [%]')))
        self.update_table_widget_item(5, 1, str(data.get('Worst Trade [%]')))

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
