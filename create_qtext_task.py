from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLabel
from PyQt5 import QtGui, QtCore


class QText(QWidget):

    def __init__(self, i):
        super().__init__()
        self.box = QVBoxLayout(self)
        self.box.setContentsMargins(0, 30, 0, 30)
        self.qnum = QLabel(f"Вопрос #{i}", self)
        self.qnum.setFont(QtGui.QFont("Century Gothic", 15, QtGui.QFont.Bold))
        self.qnum.adjustSize()
        self.qtext = QLabel("Текст вопроса:", self)
        self.qtext.setFont(QtGui.QFont("Century Gothic", 15))
        self.qtext.adjustSize()
        self.utext = QTextEdit(self)
        self.utext.setFixedSize(500, 90)

        self.box.addStretch(2)
        self.box.addWidget(self.qnum, alignment=QtCore.Qt.AlignCenter)
        self.box.addSpacing(10)
        self.box.addWidget(self.qtext, alignment=QtCore.Qt.AlignCenter)
        self.box.addSpacing(5)
        self.box.addWidget(self.utext, alignment=QtCore.Qt.AlignCenter)
        self.box.addSpacing(50)
        self.setLayout(self.box)
