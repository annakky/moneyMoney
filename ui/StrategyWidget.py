from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QWidget, QBoxLayout, QVBoxLayout, QGridLayout
from Chart import Chart
from strategy.Crossover import Crossover
from strategy.MyStrategy import MyStrategy
from strategy.RsiRange import RsiRange

form_class = uic.loadUiType("strategy-ui2.ui")[0]

class StrategyWidget(QWidget, form_class):
    def __init__(self, parent):
        super(StrategyWidget, self).__init__(parent)
        self.setupUi(self)

        self.my_strategy = MyStrategy([], 0)
        self.chart = Chart(self.my_strategy)
        self.body_layout.insertWidget(0, self.chart.get_webview())

    def create_strategy(self):
        strategies = []
        if self.rsi_checkbox.isChecked():
            period = self.rsi_period_value.value()
            low = self.rsi_low_value.value()
            high = self.rsi_high_value.value()
            strategies.append(RsiRange(period=period, low=low, high=high))

        if self.crossover_checkbox.isChecked():
            short = self.crossover_short_value.value()
            long = self.crossover_long_value.value()
            strategies.append(Crossover(short, long))

        self.chart.clear_all()
        self.my_strategy = MyStrategy(strategies, self.threshold_value.value())

        self.redraw_chart()

    def set_datetime(self):
        string_format = 'yyyy-MM-dd hh:mm:ss'
        self.start = self.start_datetime_value.dateTime().toString(string_format)
        self.end = self.end_datetime_value.dateTime().toString(string_format)

    def redraw_chart(self):
        self.set_datetime()
        self.chart.set_datetime(self.start, self.end)
        self.chart.set_strategy(self.my_strategy)
        self.chart.draw()
