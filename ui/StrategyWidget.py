from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from strategy.Crossover import Crossover
from strategy.MyStrategy import MyStrategy
from strategy.RsiRange import RsiRange

form_class = uic.loadUiType("static/strategy-ui2.ui")[0]

class StrategyWidget(QWidget, form_class):
    def __init__(self, parent):
        super(StrategyWidget, self).__init__(parent)
        self.setupUi(self)

        self.my_strategy = MyStrategy([], 0)

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

        self.my_strategy = MyStrategy(strategies, self.threshold_value.value())
