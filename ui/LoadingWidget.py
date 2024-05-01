from PyQt5.QtCore import QByteArray, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QWidget
from PyQt5 import uic

form_class = uic.loadUiType("static/loading.ui")[0]

class LoadingWidget(QWidget, form_class):
    def __init__(self, parent):
        super(LoadingWidget, self).__init__(parent)
        self.setupUi(self)
        self.center()
        self.show()

        self.movie = QMovie("static/loading.gif", QByteArray(), self)
        self.movie.setCacheMode(QMovie.CacheAll)

        self.label.setMovie(self.movie)

        self.setWindowFlags(Qt.FramelessWindowHint)

    def center(self):
        size = self.size()
        ph = self.parent().geometry().height()
        pw = self.parent().geometry().width()
        self.move(int(pw / 2 - size.width() / 2), int(ph / 2 - size.height() / 2))

    def start(self):
        self.movie.start()
