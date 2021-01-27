import sys

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QApplication, QPushButton)
from PyQt5 import QtCore, QtGui


class ThisWindow(QWidget):

    switch_end = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()

    def Center(self):
        self.setWindowTitle("StudyLang")
        ico = QtGui.QIcon("C:\Program Files\MySQL\MySQL Server 8.0\docs\S.jpg")
        self.setWindowIcon(ico)
        desktop = QApplication.desktop()
        x = (desktop.width() - self.frameSize().width()) // 2
        y = ((desktop.height() - self.frameSize().height()) // 2) - 30
        self.move(x, y)

    def initUI(self):
        self.setFixedSize(800, 600)
        self.Center()
        pal = self.palette()
        pal.setColor(QtGui.QPalette.Normal, QtGui.QPalette.Window,
                         QtGui.QColor("#ffffff"))
        self.setPalette(pal)

        self.box = QVBoxLayout(self)
        self.text = QLabel("Время вышло!", self)
        self.text.setFont(QtGui.QFont("Century Gothic", 15, QtGui.QFont.Bold))
        self.text.adjustSize()
        self.btn = QPushButton('ОK', self)
        self.box.addStretch(2)
        self.box.addWidget(self.text, alignment=QtCore.Qt.AlignCenter)
        self.box.addStretch(1)
        self.box.addWidget(self.btn, alignment=QtCore.Qt.AlignCenter)
        self.box.addStretch(2)
        self.setLayout(self.box)

        self.btn.clicked.connect(self.Remember)


    def Remember(self):
        self.switch_end.emit()
        self.close()


if __name__=="__main__":
    app = QApplication(sys.argv)
    myapp = ThisWindow()
    myapp.show()
    sys.exit(app.exec_())
