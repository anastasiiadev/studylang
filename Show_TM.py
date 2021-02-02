import sys, os
import files
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QApplication, QCheckBox, QPushButton, QMessageBox)
from PyQt5 import QtCore, QtGui


class ThisWindow(QWidget):

    switch_tm = QtCore.pyqtSignal()

    def __init__(self, n, i, question, answers, filename, rightanswers, maxscore):
        super().__init__()
        self.num = n
        self.n = i
        self.answers = answers
        self.question = question
        self.filename = filename
        self.rightanswers = rightanswers
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
            f = files.File()
            f.get("1tdvwtNx2iQUEDPbpe7NsSl-djVe-_h9G", "img/iconSL.jpg")
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
        self.message = QLabel("Выберите несколько правильных ответов.", self)
        self.message.setFont(QtGui.QFont("Century Gothic", 13))
        self.message.adjustSize()
        self.message.setFixedSize(355, 25)
        self.var1 = QCheckBox(self.answers[0])
        self.var2 = QCheckBox(self.answers[1])
        self.var1.setStyleSheet('font: 11pt Century Gothic;')
        self.var2.setStyleSheet('font: 11pt Century Gothic;')
        if len(self.answers) == 3:
            self.var3 = QCheckBox(self.answers[2])
            self.var3.setStyleSheet('font: 11pt Century Gothic;')
        elif len(self.answers) == 4:
            self.var3 = QCheckBox(self.answers[2])
            self.var4 = QCheckBox(self.answers[3])
            self.var3.setStyleSheet('font: 11pt Century Gothic;')
            self.var4.setStyleSheet('font: 11pt Century Gothic;')
        elif len(self.answers) == 5:
            self.var3 = QCheckBox(self.answers[2])
            self.var4 = QCheckBox(self.answers[3])
            self.var5 = QCheckBox(self.answers[4])
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
            self.msgv1.critical(self, "Ошибка ", "Пожалуйста, выберите два и более варианта ответов.", QMessageBox.Ok)
        elif (len(self.answers) == 3 and (self.var1.isChecked() or self.var2.isChecked() or self.var3.isChecked()) is False):
            self.msgv1 = QMessageBox(self)
            self.msgv1.critical(self, "Ошибка ", "Пожалуйста, выберите два и более варианта ответов.", QMessageBox.Ok)
        elif (len(self.answers) == 4 and (self.var1.isChecked() or self.var2.isChecked() or self.var3.isChecked() or self.var4.isChecked()) is False):
            self.msgv1 = QMessageBox(self)
            self.msgv1.critical(self, "Ошибка ", "Пожалуйста, выберите два и более варианта ответов.", QMessageBox.Ok)
        elif (len(self.answers) == 5 and (self.var1.isChecked() or self.var2.isChecked() or self.var3.isChecked() or self.var4.isChecked() or self.var5.isChecked()) is False):
                self.msgv1 = QMessageBox(self)
                self.msgv1.critical(self, "Ошибка ", "Пожалуйста, выберите два и более варианта ответов.", QMessageBox.Ok)
        else:
            user_answers = []
            l = len(self.answers)
            if self.var1.isChecked():
                user_answers.append(self.var1.text())
            if self.var2.isChecked():
                 user_answers.append(self.var2.text())
            if l == 3:
                if self.var3.isChecked():
                    user_answers.append(self.var3.text())
            elif l == 4:
                if self.var3.isChecked():
                    user_answers.append(self.var3.text())
                if self.var4.isChecked():
                    user_answers.append(self.var4.text())
            elif l == 5:
                if self.var3.isChecked():
                    user_answers.append(self.var3.text())
                if self.var4.isChecked():
                    user_answers.append(self.var4.text())
                if self.var5.isChecked():
                    user_answers.append(self.var5.text())

            # count a score
            r = len(self.rightanswers)
            point = self.maxscore / r

            for el in user_answers:
                if el in self.rightanswers:
                    self.score += point
                else:
                    self.score -= point
            self.score = round(self.score, 1)
            ost = self.score % 1
            if ost == 0:
                self.score = round(self.score)
            if self.score < 0:
                self.score = 0

            with open(self.filename, 'a', encoding='utf-8') as file:
                file.write('Вопрос #%s' % self.num + '\n')
                for el in user_answers:
                    file.write('Ответ:' + el + '\n')
                file.write('Баллы:%s' % self.score + '\n')
                file.write('\n')
            self.rightanswers = ', '.join(self.rightanswers)
            self.switch_tm.emit()


if __name__=="__main__":
    app = QApplication(sys.argv)
    # [3, [1, 'Текст', 'Выбрать несколько правильных ответов', 'вопроссссссс', ['ййй', 'пппп', 'лллл', 'нннн'], ['лллл', 'нннн']], [3, 'Аудио', 'Выбрать несколько правильных ответов', 'как называется песня?', 'Pharrell Wiliams - Happy .mp3', ['happy', 'sad', 'pharrell williams - happy', 'pharrell williams - sad'], ['happy', 'pharrell williams - happy']], [2, 'Изображение', 'Выбрать один правильный ответ', 'кто это', '9DzD7wWyzpQ.jpg', ['суслик', 'белка', 'лось', 'мышь'], 'белка'], 'Конец теста']
    myapp = ThisWindow(3, 1, 'вопроссссссс', ['ййй', 'пппп', 'лллл', 'нннн'], 'answerfiles/Test3.txt', ['лллл', 'пппп', 'нннн'], 5)
    myapp.show()
    sys.exit(app.exec_())