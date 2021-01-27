import sys, os
from ftplib import FTP
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QApplication, QRadioButton, QPushButton, QMessageBox)
from PyQt5 import QtCore, QtGui


class ThisWindow(QWidget):

    switch_to = QtCore.pyqtSignal()

    def __init__(self, n, i, question, answers, filename, rightanswer, maxscore):
        super().__init__()
        self.num = n
        self.n = i
        self.answers = answers
        self.question = question
        self.filename = filename
        self.rightanswer = rightanswer
        self.maxscore = int(maxscore)
        self.score = 0
        self.initUI()


    def Center(self):
        self.setWindowTitle("StudyLang")
        file = 'iconSL.jpg'
        path = os.getcwd()
        folder = path + '\\img\\'
        if os.path.exists(folder) is False:
            os.mkdir(folder)
        if os.path.exists(folder + file) is False:
            ftp = FTP()
            ftp.set_debuglevel(2)
            ftp.connect('stacey789.beget.tech', 21)
            ftp.login('stacey789_ftp', 'StudyLang456987')
            ftp.cwd('/img')
            ftp.retrbinary("RETR " + file, open(folder + file, 'wb').write)
            ftp.close()
        ico = QtGui.QIcon('img/iconSL.jpg')
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
        self.box.setContentsMargins(0, 30, 0, 30)
        self.qnum = QLabel("Вопрос #%s." % self.n, self)
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
        self.message = QLabel("Выберите один правильный ответ.", self)
        self.message.setFont(QtGui.QFont("Century Gothic", 13))
        self.message.adjustSize()
        self.message.setFixedSize(300, 25)
        self.var1 = QRadioButton(self.answers[0])
        self.var2 = QRadioButton(self.answers[1])
        self.var1.setStyleSheet('font: 11pt Century Gothic;')
        self.var2.setStyleSheet('font: 11pt Century Gothic;')
        if len(self.answers) == 3:
            self.var3 = QRadioButton(self.answers[2])
            self.var3.setStyleSheet('font: 11pt Century Gothic;')
        elif len(self.answers) == 4:
            self.var3 = QRadioButton(self.answers[2])
            self.var4 = QRadioButton(self.answers[3])
            self.var3.setStyleSheet('font: 11pt Century Gothic;')
            self.var4.setStyleSheet('font: 11pt Century Gothic;')
        elif len(self.answers) == 5:
            self.var3 = QRadioButton(self.answers[2])
            self.var4 = QRadioButton(self.answers[3])
            self.var5 = QRadioButton(self.answers[4])
            self.var3.setStyleSheet('font: 11pt Century Gothic;')
            self.var4.setStyleSheet('font: 11pt Century Gothic;')
            self.var5.setStyleSheet('font: 11pt Century Gothic;')
        self.btn = QPushButton('OK', self)
        self.box.addStretch(1)
        self.box.addWidget(self.qnum, alignment=QtCore.Qt.AlignCenter)
        self.box.addSpacing(10)
        self.box.addWidget(self.qtext, alignment=QtCore.Qt.AlignCenter)
        self.box.addSpacing(50)
        self.box.addWidget(self.message, alignment=QtCore.Qt.AlignCenter)
        self.box.addSpacing(20)
        self.left = QVBoxLayout(self)
        horizontal = QHBoxLayout(self)
        if len(self.answers) == 2:
            self.left.addWidget(self.var1, alignment=QtCore.Qt.AlignLeft)
            self.left.addWidget(self.var2, alignment=QtCore.Qt.AlignLeft)
        elif len(self.answers) == 3:
            self.left.addWidget(self.var1, alignment=QtCore.Qt.AlignLeft)
            self.left.addWidget(self.var2, alignment=QtCore.Qt.AlignLeft)
            self.left.addWidget(self.var3, alignment=QtCore.Qt.AlignLeft)
        elif len(self.answers) == 4:
            self.left.addWidget(self.var1, alignment=QtCore.Qt.AlignLeft)
            self.left.addWidget(self.var2, alignment=QtCore.Qt.AlignLeft)
            self.left.addWidget(self.var3, alignment=QtCore.Qt.AlignLeft)
            self.left.addWidget(self.var4, alignment=QtCore.Qt.AlignLeft)
        elif len(self.answers) == 5:
            self.left.addWidget(self.var1, alignment=QtCore.Qt.AlignLeft)
            self.left.addWidget(self.var2, alignment=QtCore.Qt.AlignLeft)
            self.left.addWidget(self.var3, alignment=QtCore.Qt.AlignLeft)
            self.left.addWidget(self.var4, alignment=QtCore.Qt.AlignLeft)
            self.left.addWidget(self.var5, alignment=QtCore.Qt.AlignLeft)
        horizontal.addStretch(1)
        horizontal.addLayout(self.left)
        horizontal.addStretch(1)
        self.box.addLayout(horizontal)
        self.box.addSpacing(60)
        self.box.addWidget(self.btn, alignment=QtCore.Qt.AlignCenter)
        self.box.addStretch(1)
        self.setLayout(self.box)

        self.btn.clicked.connect(self.WriteToFile)

    def WriteToFile(self):
        #проверка, что кнопка нажата
        if (len(self.answers) == 2 and (self.var1.isChecked() or self.var2.isChecked()) is False):
            self.msgv1 = QMessageBox(self)
            self.msgv1.critical(self, "Ошибка ", "Пожалуйста, выберите один ответ.", QMessageBox.Ok)
        elif (len(self.answers) == 3 and (self.var1.isChecked() or self.var2.isChecked() or self.var3.isChecked()) is False):
            self.msgv1 = QMessageBox(self)
            self.msgv1.critical(self, "Ошибка ", "Пожалуйста, выберите один ответ.", QMessageBox.Ok)
        elif (len(self.answers) == 4 and (self.var1.isChecked() or self.var2.isChecked() or self.var3.isChecked() or self.var4.isChecked()) is False):
            self.msgv1 = QMessageBox(self)
            self.msgv1.critical(self, "Ошибка ", "Пожалуйста, выберите один ответ.", QMessageBox.Ok)
        elif (len(self.answers) == 5 and (self.var1.isChecked() or self.var2.isChecked() or self.var3.isChecked() or self.var4.isChecked() or self.var5.isChecked()) is False):
                self.msgv1 = QMessageBox(self)
                self.msgv1.critical(self, "Ошибка ", "Пожалуйста, выберите один ответ.", QMessageBox.Ok)
        else:
            if self.var1.isChecked():
                pressed = self.var1.text()
            elif self.var2.isChecked():
                pressed = self.var2.text()
            if len(self.answers) == 3:
                if self.var3.isChecked():
                    pressed = self.var3.text()
            elif len(self.answers) == 4:
                if self.var3.isChecked():
                    pressed = self.var3.text()
                elif self.var4.isChecked():
                    pressed = self.var4.text()
            elif len(self.answers) == 5:
                if self.var3.isChecked():
                    pressed = self.var3.text()
                elif self.var4.isChecked():
                    pressed = self.var4.text()
                elif self.var5.isChecked():
                    pressed = self.var5.text()

            # count a score
            if pressed == self.rightanswer:
                self.score += self.maxscore

            with open(self.filename, 'a', encoding='utf-8') as file:
                file.write('Вопрос #%s' % self.num + '\n')
                file.write('Ответ:' + pressed + '\n')
                file.write('Баллы:%s' % self.score + '\n')
                file.write('\n')
            self.switch_to.emit()


if __name__=="__main__":
    app = QApplication(sys.argv)
    #myapp = ThisWindow(2, 1, 'Сколько будет 2*2?', ['4', '6', '8'], 'answerfiles/Test2.txt')
    myapp = ThisWindow(3, 3, 'Кто главный извращенец мира?', ['Ганибал Лектор', 'Фредди Крюгер', 'Ганибал Лектор', 'Фредди Крюгер'], 'answerfiles/Test2.txt')
    myapp.show()
    sys.exit(app.exec_())
