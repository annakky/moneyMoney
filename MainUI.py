import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy, QStackedWidget, QVBoxLayout, QGridLayout
from ui.BacktestingWidget import BacktestingWidget
from ui.StrategyWidget import StrategyWidget

class MyMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)

        self.stackedWidget = QStackedWidget(self)
        self.strategy_widget = StrategyWidget(self)
        self.backtestingWidget = BacktestingWidget(self)

        self.stackedWidget.addWidget(self.strategy_widget)
        self.stackedWidget.addWidget(self.backtestingWidget)
        self.setCentralWidget(self.stackedWidget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MyMainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
