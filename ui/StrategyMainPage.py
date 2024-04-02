from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from Chart import Chart
from ui.StrategyWidget import StrategyWidget

form_class = uic.loadUiType("static/strategy-main.ui")[0]

class StrategyMainPage(QWidget, form_class):
    def __init__(self, parent):
        super(StrategyMainPage, self).__init__(parent)
        self.setupUi(self)
        self.strategy_widget = StrategyWidget(self)

        self.chart = Chart(self.strategy_widget.my_strategy)
        self.body_layout.insertWidget(0, self.chart.get_webview())
        self.body_layout.insertWidget(1, self.strategy_widget)

    def set_datetime(self):
        string_format = 'yyyy-MM-dd hh:mm:ss'
        self.start = self.start_datetime_value.dateTime().toString(string_format)
        self.end = self.end_datetime_value.dateTime().toString(string_format)

    def redraw_chart(self):
        self.set_datetime()
        self.chart.set_datetime(self.start, self.end)
        self.strategy_widget.create_strategy()
        self.chart.set_strategy(self.strategy_widget.my_strategy)
        self.chart.draw()
