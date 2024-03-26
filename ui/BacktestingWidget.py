from PyQt5 import uic
from PyQt5.QtWidgets import QWidget


form_class = uic.loadUiType("backtesting-ui.ui")[0]

class BacktestingWidget(QWidget, form_class):
    def __init__(self, parent):
        super(BacktestingWidget, self).__init__(parent)
        self.setupUi(self)

    def move_to_strategy_widget(self):
        self.parentWidget().setCurrentIndex(0)

    def move_to_backtesting_widget(self):
        pass
