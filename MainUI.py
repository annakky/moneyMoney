import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QVBoxLayout, QWidget
from ui.AutoTradeMainPage import AutoTradeMainPage
from ui.BacktestingMainPage import BacktestingMainPage
from ui.RedirectionButtonWidget import RedirectionButtonWidget
from ui.StrategyMainPage import StrategyMainPage

form_class = uic.loadUiType("static/strategy-ui.ui")[0]

class MyMainWindow(QMainWindow, form_class):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        # 중앙 위젯 생성
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)

        # 중앙 위젯에 레이아웃 설정
        self.central_layout = QVBoxLayout(self.centralWidget)

        # Stacked Widget 생성
        self.stackedWidget = QStackedWidget(self.centralWidget)
        self.central_layout.addWidget(self.stackedWidget)

        # 전략 메인 페이지 추가
        self.strategy_main_page = StrategyMainPage(self)
        self.stackedWidget.addWidget(self.strategy_main_page)

        # 백테스팅 위젯 추가
        self.backtesting_widget = BacktestingMainPage(self)
        self.stackedWidget.addWidget(self.backtesting_widget)

        # 자동매매 위젯 추가
        self.autotrade_widget = AutoTradeMainPage(self)
        self.stackedWidget.addWidget(self.autotrade_widget)

        # 버튼 추가
        self.button_widget = RedirectionButtonWidget(self)
        self.central_layout.addWidget(self.button_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MyMainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
