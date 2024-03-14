import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QSizePolicy, QVBoxLayout

from Chart import Chart
from strategy.Crossover import Crossover
from strategy.MyStrategy import MyStrategy
from strategy.RsiRange import RsiRange
from ui.StrategyWidget import StrategyWidget

form_class = uic.loadUiType("strategy-ui.ui")[0]

class MyMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.strategy_widget = StrategyWidget(self)
        self.setCentralWidget(self.strategy_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MyMainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
