import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from custom_chart import CustomChart
from strategy.Crossover import Crossover
from strategy.MyStrategy import MyStrategy
from strategy.RsiRange import RsiRange

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QMainWindow()
    layout = QVBoxLayout()
    widget = QWidget()
    widget.setLayout(layout)

    window.resize(800, 500)
    layout.setContentsMargins(0, 0, 0, 0)

    crossover = Crossover(5, 20)
    rsi = RsiRange(14)
    chart = CustomChart(MyStrategy([crossover, rsi], threshold=2))

    layout.addWidget(chart.get_webview())

    window.setCentralWidget(widget)
    window.show()

    sys.exit(app.exec_())
