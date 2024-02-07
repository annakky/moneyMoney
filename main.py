import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from events.custom_chart import CustomChart
from strategy.Crossover import Crossover
from strategy.MyStrategy import MyStrategy

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QMainWindow()
    layout = QVBoxLayout()
    widget = QWidget()
    widget.setLayout(layout)

    window.resize(800, 500)
    layout.setContentsMargins(0, 0, 0, 0)

    chart = CustomChart(MyStrategy([Crossover(5, 20)], threshold=1))

    layout.addWidget(chart.get_webview())

    window.setCentralWidget(widget)
    window.show()

    sys.exit(app.exec_())
