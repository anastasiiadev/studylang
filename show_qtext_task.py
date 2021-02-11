import sys, os
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QApplication, QMessageBox
from PyQt5 import QtGui, QtCore

import general_settings as gs


class QText(gs.SLWindow):

    def __init__(self, i, question):
        super().__init__()
        self.n = i
        self.question = question
        self.initUI()

    def initUI(self):
        box = QVBoxLayout(self)
        box.setContentsMargins(0, 30, 0, 30)
        self.qnum = QLabel(f"Вопрос #{self.n}", self)
        self.qnum.setFont(QtGui.QFont("Century Gothic", 15, QtGui.QFont.Bold))
        self.qnum.adjustSize()
        self.qtext = QLabel(self.question, self)
        self.qtext.setFont(QtGui.QFont("Century Gothic", 13))
        self.qtext.adjustSize()
        self.qtext.setWordWrap(True)
        if len(self.question) <= 50:
            self.qtext.setFixedSize(500, 50)
        else:
            self.qtext.setFixedSize(500, 150)
        self.qtext.setAlignment(QtCore.Qt.AlignCenter)

        box.addStretch(1)
        box.addWidget(self.qnum, alignment=QtCore.Qt.AlignCenter)
        box.addSpacing(10)
        box.addWidget(self.qtext, alignment=QtCore.Qt.AlignCenter)
        box.addStretch(3)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QText(2, 1, 'What professions can you see in the picture?')
    sys.exit(app.exec_())