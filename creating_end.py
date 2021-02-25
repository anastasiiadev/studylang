import sys
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QApplication, QPushButton, QLineEdit, QMessageBox
from PyQt5 import QtCore, QtGui

import general_settings as gs

TEXT_MARK = 'Оценка'
TEXT_MAX_TEST_SCORE = 'Максимальное количество баллов:'
TEXT_TIME = 'Время теста:'


class ThisWindow(gs.SLWindow):
    switch_end = QtCore.pyqtSignal()

    def __init__(self, score, filename):
        super().__init__()
        self.filename = filename
        self.maxscore = score
        self.initUI()

    def initUI(self):
        self.box = QVBoxLayout(self)
        self.text = QLabel("Сколько баллов нужно набрать пользователю, чтобы получить:", self)
        self.text.setFont(QtGui.QFont("Century Gothic", 14))
        self.text.adjustSize()
        self.five = QLabel("оценку 5?", self)
        self.five.setFont(QtGui.QFont("Century Gothic", 14))
        self.five.adjustSize()
        self.four = QLabel("оценку 4?", self)
        self.four.setFont(QtGui.QFont("Century Gothic", 14))
        self.four.adjustSize()
        self.three = QLabel("оценку 3?", self)
        self.three.setFont(QtGui.QFont("Century Gothic", 14))
        self.three.adjustSize()
        self.warnint = QLabel("Пожалуйста, указывайте целые числа.", self)
        self.warnint.setFont(QtGui.QFont("Century Gothic", 11))
        self.warnint.adjustSize()
        self.timetext = QLabel("Задайте максимальное время прохождения теста:", self)
        self.timetext.setFont(QtGui.QFont("Century Gothic", 14))
        self.timetext.adjustSize()
        self.minline = QLineEdit()
        self.mintext = QLabel("мин", self)
        self.mintext.setFont(QtGui.QFont("Century Gothic", 11))
        self.mintext.adjustSize()
        self.minline.setFixedSize(30, 25)
        self.secline = QLineEdit()
        self.sectext = QLabel("сек", self)
        self.sectext.setFont(QtGui.QFont("Century Gothic", 11))
        self.sectext.adjustSize()
        self.secline.setFixedSize(30, 25)
        self.fivescore = QLineEdit()
        self.fourscore = QLineEdit()
        self.threescore = QLineEdit()
        self.btn = QPushButton('ОК', self)
        self.btn.setFixedSize(140, 25)

        self.box.addStretch(2)
        self.box.addWidget(self.text, alignment=QtCore.Qt.AlignCenter)
        v1box = QHBoxLayout()
        v1box.addWidget(self.five, alignment=QtCore.Qt.AlignRight)
        v1box.addWidget(self.fivescore, alignment=QtCore.Qt.AlignLeft)
        v2box = QHBoxLayout()
        v2box.addWidget(self.four, alignment=QtCore.Qt.AlignRight)
        v2box.addWidget(self.fourscore, alignment=QtCore.Qt.AlignLeft)
        v3box = QHBoxLayout()
        v3box.addWidget(self.three, alignment=QtCore.Qt.AlignRight)
        v3box.addWidget(self.threescore, alignment=QtCore.Qt.AlignLeft)
        self.box.addStretch(1)
        self.box.addLayout(v1box)
        self.box.addSpacing(10)
        self.box.addLayout(v2box)
        self.box.addSpacing(10)
        self.box.addLayout(v3box)
        self.box.addStretch(1)
        self.box.addWidget(self.warnint, alignment=QtCore.Qt.AlignCenter)
        self.box.addStretch(1)
        timebox = QHBoxLayout()
        timebox.addStretch(1)
        timebox.addWidget(self.timetext)
        timebox.addWidget(self.minline)
        timebox.addWidget(self.mintext)
        timebox.addWidget(self.secline)
        timebox.addWidget(self.sectext)
        timebox.addStretch(1)
        self.box.addLayout(timebox)
        self.box.addStretch(1)
        self.box.addWidget(self.btn, alignment=QtCore.Qt.AlignCenter)
        self.box.addStretch(2)
        self.setLayout(self.box)
        self.show()

        self.btn.clicked.connect(self.Remember)

    def Remember(self):
        self.fivesc = self.fivescore.text()
        self.fivesc = self.fivesc.strip()
        self.foursc = self.fourscore.text()
        self.foursc = self.foursc.strip()
        self.threesc = self.threescore.text()
        self.threesc = self.threesc.strip()
        self.min = self.minline.text()
        self.min = self.min.strip()
        self.sec = self.secline.text()
        self.sec = self.sec.strip()

        if self.fivesc == '' or self.foursc == '' or self.threesc == '':
            self.msgnum = QMessageBox(self)
            self.msgnum.critical(self, "Ошибка ", "Пожалуйста, укажите баллы.", QMessageBox.Ok)
        elif self.min == '' or self.sec == '':
            self.msgnum = QMessageBox(self)
            self.msgnum.critical(self, "Ошибка ", "Введите максимальное время прохождения теста.", QMessageBox.Ok)
        else:
            try:
                self.fivesc = int(self.fivesc)
                self.foursc = int(self.foursc)
                self.threesc = int(self.threesc)
                self.min = int(self.min)
                self.sec = int(self.sec)
                if self.fivesc > self.maxscore or self.foursc > self.maxscore or self.threesc > self.maxscore:
                    self.msgnum = QMessageBox(self)
                    self.msgnum.critical(self, "Ошибка ",
                                         f"Максимальное количество баллов за тест - {self.maxscore}.",
                                         QMessageBox.Ok)
                else:
                    if self.fivesc < self.foursc:
                        self.msgnum = QMessageBox(self)
                        self.msgnum.critical(self, "Ошибка ",
                                             "Баллы для оценки 5 должны быть больше баллов для оценки 4.",
                                             QMessageBox.Ok)
                    elif self.fivesc < self.threesc:
                        self.msgnum = QMessageBox(self)
                        self.msgnum.critical(self, "Ошибка ",
                                             "Баллы для оценки 5 должны быть больше баллов для оценки 3.",
                                             QMessageBox.Ok)
                    elif self.foursc < self.threesc:
                        self.msgnum = QMessageBox(self)
                        self.msgnum.critical(self, "Ошибка ",
                                             "Баллы для оценки 4 должны быть больше баллов для оценки 3.",
                                             QMessageBox.Ok)
                    else:
                        with open(self.filename, 'a', encoding='utf-8') as file:
                            file.write(TEXT_MARK + ' 5:' + str(self.fivesc) + '\n')
                            file.write(TEXT_MARK + ' 4:' + str(self.foursc) + '\n')
                            file.write(TEXT_MARK + ' 3:' + str(self.threesc) + '\n')
                            file.write(TEXT_MAX_TEST_SCORE + str(self.maxscore) + '\n')
                            file.write(TEXT_TIME + str(self.min) + ' ' + str(self.sec) + '\n')
                            file.write('\n')
                        self.msgnum = QMessageBox(self)
                        self.msgnum.information(self, "Тест создан ", "Вы успешно создали тест!", QMessageBox.Close)
                        self.switch_end.emit()
            except Exception:
                self.msgnum = QMessageBox(self)
                self.msgnum.critical(self, "Ошибка ",
                                     "Необходимо указать целые числа. Проверьте введенные данные.",
                                     QMessageBox.Ok)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = ThisWindow(12, 'testfiles/Test1.txt')
    sys.exit(app.exec_())
