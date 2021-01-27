import sys

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QApplication, QPushButton)
from PyQt5 import QtCore, QtGui


class ThisWindow(QWidget):

    switch_end = QtCore.pyqtSignal()

    def __init__(self, answer, score, quantity):
        super().__init__()
        self.answer = answer
        self.score = score
        self.quantity = quantity
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
        if self.quantity == 'many':
            self.right = QLabel("Правильные ответы:", self)
        else:
            self.right = QLabel("Правильный ответ:", self)
        self.right.setFont(QtGui.QFont("Century Gothic", 15, QtGui.QFont.Bold))
        self.right.adjustSize()
        self.answerlab = QLabel(self.answer, self)
        self.answerlab.setFont(QtGui.QFont("Century Gothic", 13))
        self.answerlab.adjustSize()
        self.scorenum = QLabel("Ваш балл:", self)
        self.scorenum.setFont(QtGui.QFont("Century Gothic", 15, QtGui.QFont.Bold))
        self.scorenum.adjustSize()
        self.scorelab = QLabel('%s' % self.score, self)
        self.scorelab.setFont(QtGui.QFont("Century Gothic", 13))
        self.scorelab.adjustSize()
        self.btn = QPushButton('ОK', self)
        self.box.addStretch(2)
        self.box.addWidget(self.right, alignment=QtCore.Qt.AlignCenter)
        self.box.addWidget(self.answerlab, alignment=QtCore.Qt.AlignCenter)
        self.box.addStretch(1)
        self.box.addWidget(self.scorenum, alignment=QtCore.Qt.AlignCenter)
        self.box.addWidget(self.scorelab, alignment=QtCore.Qt.AlignCenter)
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
    myapp = ThisWindow("Зебра", 1)
    myapp.show()
    sys.exit(app.exec_())
