import sys
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QApplication, QPushButton, QComboBox
from PyQt5 import QtCore, QtGui

import general_settings as gs


TEXT_QUESTION_NUMBER = 'Вопрос #'
TEXT_QUESTION_TYPE = 'Тип вопроса:'
TEXT_ANSWER_TYPE = 'Тип ответа:'
TEXT_TYPE_TEXT = 'Текст'
TEXT_TYPE_AUDIO = 'Аудио'
TEXT_TYPE_IMAGE = 'Изображение'
TEXT_TYPE_MANY_VARIANTS = 'Выбрать несколько правильных ответов'
TEXT_TYPE_ONE_VARIANT = 'Выбрать один правильный ответ'
TEXT_TYPE_MATCH = 'Установить соответствие'
AUDIO = 'audio'
IMAGE = 'image'
TEXT = 'text'
MANY_VARIANTS = 'many'
ONE_VARIANT = 'one'
MATCH = 'match'


class ThisWindow(gs.SLWindow):

    switch_type_task = QtCore.pyqtSignal(str, str)

    def __init__(self, n, testname):
        super().__init__()
        self.n = n
        self.testname = testname
        self.initUI()


    def initUI(self):
        self.box = QVBoxLayout(self)
        self.qnum = QLabel(f"Вопрос #{self.n}", self)
        self.qnum.setFont(QtGui.QFont("Century Gothic", 15, QtGui.QFont.Bold))
        self.qnum.adjustSize()
        self.qtype = QLabel("Выберите тип вопроса:", self)
        self.qtype.setFont(QtGui.QFont("Century Gothic", 15, QtGui.QFont.Bold))
        self.qtype.adjustSize()
        self.qbox = QComboBox(self)
        self.qbox.addItems(["Текст", "Изображение", "Аудио"])
        self.qbox.setFixedSize(100, 25)
        self.atype = QLabel("Выберите тип ответа:", self)
        self.atype.setFont(QtGui.QFont("Century Gothic", 15, QtGui.QFont.Bold))
        self.atype.adjustSize()
        self.abox = QComboBox(self)
        self.abox.addItems(["Установить соответствие", "Выбрать один правильный ответ", "Выбрать несколько правильных ответов"])
        self.abox.setFixedSize(300, 25)
        self.btn = QPushButton('OK', self)
        self.box.addStretch(1)
        self.box.addWidget(self.qnum, alignment=QtCore.Qt.AlignCenter)
        self.box.addWidget(self.qtype, alignment=QtCore.Qt.AlignCenter)
        self.box.addWidget(self.qbox, alignment=QtCore.Qt.AlignCenter)
        self.box.addStretch(1)
        self.box.addWidget(self.atype, alignment=QtCore.Qt.AlignCenter)
        self.box.addWidget(self.abox, alignment=QtCore.Qt.AlignCenter)
        self.box.addStretch(1)
        self.box.addWidget(self.btn, alignment=QtCore.Qt.AlignCenter)
        self.box.addStretch(2)
        self.setLayout(self.box)

        self.btn.clicked.connect(self.WriteToFile)


    def WriteToFile(self):
        self.qtype = self.qbox.currentText()
        self.atype = self.abox.currentText()
        with open(self.testname, 'a', encoding='utf-8') as file:
            file.write(TEXT_QUESTION_NUMBER + f'{self.n}\n')
            file.write(TEXT_QUESTION_TYPE + self.qtype + '\n')
            file.write(TEXT_ANSWER_TYPE + self.atype + '\n')

        if self.qtype == TEXT_TYPE_TEXT:
            question = TEXT
        elif self.qtype == TEXT_TYPE_IMAGE:
            question = IMAGE
        else:
            question = AUDIO

        if self.atype == TEXT_TYPE_MATCH:
            answer = MATCH
        elif self.atype == TEXT_TYPE_ONE_VARIANT:
            answer = ONE_VARIANT
        else:
            answer = MANY_VARIANTS

        self.switch_type_task.emit(question, answer)





if __name__=="__main__":
    app = QApplication(sys.argv)
    myapp = ThisWindow(2, 'files/Test1.txt')
    myapp.show()
    sys.exit(app.exec_())

