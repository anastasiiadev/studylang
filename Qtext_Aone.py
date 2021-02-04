import sys, os
import files
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QCheckBox, QApplication, QTextEdit, QLineEdit, QPushButton, QMessageBox, QHBoxLayout)
from PyQt5 import QtCore, QtGui


class ThisWindow(QWidget):

    switch_to = QtCore.pyqtSignal()

    def __init__(self, n, i, filename):
        super().__init__()
        self.n = i
        self.filename = filename
        self.initUI()


    # def Center(self):
    #     self.setWindowTitle("StudyLang")
    #     file = 'iconSL.jpg'
    #     path = os.getcwd()
    #     folder = path + '\\img\\'
    #     if os.path.exists(folder) is False:
    #         os.mkdir(folder)
    #     if os.path.exists(folder + file) is False:
    #         f = files.File()
    #         f.get("1tdvwtNx2iQUEDPbpe7NsSl-djVe-_h9G", "img/iconSL.jpg")
    #     ico = QtGui.QIcon('img/iconSL.jpg')
    #     self.setWindowIcon(ico)
    #     desktop = QApplication.desktop()
    #     x = (desktop.width() - self.frameSize().width()) // 2
    #     y = ((desktop.height() - self.frameSize().height()) // 2) - 30
    #     self.move(x, y)


    def initUI(self):
        self.setFixedSize(850, 650)
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
        self.qtext = QLabel("Текст вопроса:", self)
        self.qtext.setFont(QtGui.QFont("Century Gothic", 15))
        self.qtext.adjustSize()
        self.utext = QTextEdit(self)
        self.utext.setFixedSize(500, 90)
        self.message = QLabel("Вариантов ответа максимально может быть 5. Если вам нужно меньше, оставьте соответствующие поля пустыми.", self)
        self.message.setFont(QtGui.QFont("Century Gothic", 9))
        self.message.adjustSize()
        self.message.setFixedSize(700, 20)
        self.message2 = QLabel("Поставьте галочку ✔ напротив правильного ответа.", self)
        self.message2.setFont(QtGui.QFont("Century Gothic", 9))
        self.message2.adjustSize()
        self.message2.setFixedSize(700, 20)
        self.maxscoretext = QLabel("Укажите максимальное количество баллов за данное задание:")
        self.maxscoretext.setFont(QtGui.QFont("Century Gothic", 11))
        self.maxscoretext.adjustSize()
        self.maxsc = QLineEdit(self)
        self.maxsc.setFixedSize(25, 25)

        self.variants = QHBoxLayout(self)
        self.texts = QVBoxLayout(self)
        self.input = QVBoxLayout(self)
        self.checkboxes = QVBoxLayout(self)
        self.var1t = QLabel("Введите первый вариант ответа:", self)
        self.var1t.setFont(QtGui.QFont("Century Gothic", 13))
        self.var1t.adjustSize()
        self.var1 = QLineEdit(self)
        self.var1.setFixedSize(350, 25)
        self.ch1 = QCheckBox()
        self.var2t = QLabel("Введите второй вариант ответа:", self)
        self.var2t.setFont(QtGui.QFont("Century Gothic", 13))
        self.var2t.adjustSize()
        self.var2 = QLineEdit(self)
        self.var2.setFixedSize(350, 25)
        self.ch2 = QCheckBox()
        self.var3t = QLabel("Введите третий вариант ответа:", self)
        self.var3t.setFont(QtGui.QFont("Century Gothic", 13))
        self.var3t.adjustSize()
        self.var3 = QLineEdit(self)
        self.var3.setFixedSize(350, 25)
        self.ch3 = QCheckBox()
        self.var4t = QLabel("Введите четвертый вариант ответа:", self)
        self.var4t.setFont(QtGui.QFont("Century Gothic", 13))
        self.var4t.adjustSize()
        self.var4 = QLineEdit(self)
        self.var4.setFixedSize(350, 25)
        self.ch4 = QCheckBox()
        self.var5t = QLabel("Введите пятый вариант ответа:", self)
        self.var5t.setFont(QtGui.QFont("Century Gothic", 13))
        self.var5t.adjustSize()
        self.var5 = QLineEdit(self)
        self.var5.setFixedSize(350, 25)
        self.ch5 = QCheckBox()
        self.btn = QPushButton('OK', self)

        self.box.addStretch(2)
        self.box.addWidget(self.qnum, alignment=QtCore.Qt.AlignCenter)
        self.box.addSpacing(10)
        self.box.addWidget(self.qtext, alignment=QtCore.Qt.AlignCenter)
        self.box.addSpacing(5)
        self.box.addWidget(self.utext, alignment=QtCore.Qt.AlignCenter)
        self.box.addSpacing(50)

        self.texts.addWidget(self.var1t, alignment=QtCore.Qt.AlignRight)
        self.texts.addWidget(self.var2t, alignment=QtCore.Qt.AlignRight)
        self.texts.addWidget(self.var3t, alignment=QtCore.Qt.AlignRight)
        self.texts.addWidget(self.var4t, alignment=QtCore.Qt.AlignRight)
        self.texts.addWidget(self.var5t, alignment=QtCore.Qt.AlignRight)

        self.input.addWidget(self.var1)
        self.input.addSpacing(2)
        self.input.addWidget(self.var2)
        self.input.addSpacing(2)
        self.input.addWidget(self.var3)
        self.input.addSpacing(2)
        self.input.addWidget(self.var4)
        self.input.addSpacing(2)
        self.input.addWidget(self.var5)

        self.checkboxes.addSpacing(6)
        self.checkboxes.addWidget(self.ch1)
        self.checkboxes.addSpacing(9)
        self.checkboxes.addWidget(self.ch2)
        self.checkboxes.addSpacing(9)
        self.checkboxes.addWidget(self.ch3)
        self.checkboxes.addSpacing(9)
        self.checkboxes.addWidget(self.ch4)
        self.checkboxes.addSpacing(9)
        self.checkboxes.addWidget(self.ch5)

        self.variants.addSpacing(40)
        self.variants.addLayout(self.texts)
        self.variants.addLayout(self.input)
        self.variants.addLayout(self.checkboxes)
        self.variants.addSpacing(25)
        self.box.addLayout(self.variants)

        self.box.addSpacing(10)
        message = QVBoxLayout()
        message.addWidget(self.message, alignment=QtCore.Qt.AlignCenter)
        message.addWidget(self.message2, alignment=QtCore.Qt.AlignCenter)
        scorebox = QHBoxLayout()
        scorebox.addStretch(1)
        scorebox.addWidget(self.maxscoretext, alignment=QtCore.Qt.AlignRight)
        scorebox.addSpacing(20)
        scorebox.addWidget(self.maxsc, alignment=QtCore.Qt.AlignLeft)
        scorebox.addStretch(1)
        message.addLayout(scorebox)
        self.box.addLayout(message)
        self.box.addSpacing(20)
        self.box.addWidget(self.btn, alignment=QtCore.Qt.AlignCenter)
        self.box.addStretch(2)
        self.setLayout(self.box)

        self.btn.clicked.connect(self.WriteToFile)

    def WriteToFile(self):
        utext = self.utext.toPlainText()
        utext = utext.strip()
        var1 = self.var1.text()
        var1 = var1.strip()
        var2 = self.var2.text()
        var2 = var2.strip()
        var3 = self.var3.text()
        var3 = var3.strip()
        var4 = self.var4.text()
        var4 = var4.strip()
        var5 = self.var5.text()
        var5 = var5.strip()
        self.maxscore = self.maxsc.text()
        self.maxscore =  self.maxscore.strip()

        # проверка, что кнопка нажата
        numch = 0
        answer = 0
        if self.ch1.isChecked() is True:
            numch += 1
            answer = var1
        if self.ch2.isChecked() is True:
            numch += 1
            answer = var2
        if self.ch3.isChecked() is True:
            numch += 1
            answer = var3
        if self.ch4.isChecked() is True:
            numch += 1
            answer = var4
        if self.ch5.isChecked() is True:
            numch += 1
            answer = var5
        if numch == 0:
            self.msgv1 = QMessageBox(self)
            self.msgv1.critical(self, "Ошибка ", "Пожалуйста, укажите правильный ответ, отметив его галочкой.",
                                QMessageBox.Ok)
        elif numch > 1:
            self.msgv1 = QMessageBox(self)
            self.msgv1.critical(self, "Ошибка ", "Пожалуйста, укажите только один правильный ответ.", QMessageBox.Ok)
        else:
            if utext == '':
                self.msgnum = QMessageBox(self)
                self.msgnum.critical(self, "Ошибка ", "Пожалуйста, укажите ваш вопрос.", QMessageBox.Ok)
            elif self.maxscore == '':
                self.msgnum = QMessageBox(self)
                self.msgnum.critical(self, "Ошибка ", "Пожалуйста, введите максимальное количество баллов за задание.", QMessageBox.Ok)
            elif var1 == '':
                self.msgv1 = QMessageBox(self)
                self.msgv1.critical(self, "Ошибка ", "Пожалуйста, укажите первый вариант ответа.", QMessageBox.Ok)
            elif var2 == '':
                self.msgv2 = QMessageBox(self)
                self.msgv2.critical(self, "Ошибка ", "Пожалуйста, укажите второй вариант ответа.", QMessageBox.Ok)
            else:
                with open(self.filename, 'a', encoding='utf-8') as file:
                    file.write('Вопрос:' + utext + '\n')
                    file.write('Вариант1:' + var1 + '\n')
                    file.write('Вариант2:' + var2 + '\n')
                    if var3 != '':
                        file.write('Вариант3:' + var3 + '\n')
                    if var4 != '':
                        file.write('Вариант4:' + var4 + '\n')
                    if var5 != '':
                        file.write('Вариант5:' + var5 + '\n')
                    file.write('Правильный ответ:' + answer + '\n')
                    file.write('Максимальный балл:' + self.maxscore + '\n')
                    file.write('\n')
                self.hide()
                self.switch_to.emit()


if __name__=="__main__":
    app = QApplication(sys.argv)
    myapp = ThisWindow(2, 1, 'testfiles/Test1.txt')
    myapp.show()
    sys.exit(app.exec_())

