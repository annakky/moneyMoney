from PyQt5 import uic
from PyQt5.QtWidgets import QWidget


form_class = uic.loadUiType("redirection-button-ui.ui")[0]

class RedirectionButtonWidget(QWidget, form_class):
    def __init__(self, parent):
        super(RedirectionButtonWidget, self).__init__(parent)
        self.setupUi(self)

    def move_to_strategy_widget(self):
        self.window().stackedWidget.setCurrentIndex(0)

    def move_to_backtesting_widget(self):
        self.window().stackedWidget.setCurrentIndex(1)
