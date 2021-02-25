import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QApplication, QPushButton, QMessageBox, QCheckBox
from PyQt5 import QtGui, QtCore


MANY_VARIANTS = 'many'
ONE_VARIANT = 'one'


class AVariants(QWidget):

    do_task_end = QtCore.pyqtSignal()

    def __init__(self, type, i, answers, filename, rightanswers, maxscore):
        super().__init__()
        self.type = type
        self.n = i
        self.answers = answers
        self.filename = filename
        self.rightanswers = rightanswers
        self.maxscore = int(maxscore)
        self.score = 0
        self.initUI()

    def initUI(self):
        self.box = QVBoxLayout(self)
        if self.type == MANY_VARIANTS:
            self.message = QLabel("Выберите несколько правильных ответов.", self)
            self.message.setFixedSize(370, 25)
        else:
            self.message = QLabel("Выберите один правильный ответ.", self)
            self.message.setFixedSize(300, 25)
        self.message.setFont(QtGui.QFont("Century Gothic", 13))
        self.message.adjustSize()

        self.variants_number = len(self.answers)
        for x in range(1, self.variants_number + 1):
            exec(f"self.var{x} = QCheckBox(self.answers[{x - 1}])")
            exec(f"self.var{x}.setStyleSheet('font: 11pt Century Gothic;')")
        self.btn = QPushButton('OK', self)
        self.btn.setFixedSize(80, 25)
        self.box.addWidget(self.message, alignment=QtCore.Qt.AlignCenter)
        self.box.addSpacing(20)
        left = QVBoxLayout(self)
        if self.variants_number > 3:
            right = QVBoxLayout(self)
            left.addWidget(self.var1, alignment=QtCore.Qt.AlignLeft)
            left.addWidget(self.var2, alignment=QtCore.Qt.AlignLeft)
            right.addWidget(self.var4, alignment=QtCore.Qt.AlignLeft)
            if self.variants_number == 4:
                right.addWidget(self.var3, alignment=QtCore.Qt.AlignLeft)
            else:
                left.addWidget(self.var3, alignment=QtCore.Qt.AlignLeft)
                right.addWidget(self.var5, alignment=QtCore.Qt.AlignLeft)
        else:
            for x in range(1, self.variants_number + 1):
                exec(f"left.addWidget(self.var{x}, alignment=QtCore.Qt.AlignLeft)")
        horizontal = QHBoxLayout(self)
        horizontal.addStretch(1)
        horizontal.addLayout(left)
        if self.variants_number > 3:
            horizontal.addSpacing(10)
            horizontal.addLayout(right)
        horizontal.addStretch(1)
        self.box.addLayout(horizontal)
        self.box.addSpacing(20)
        self.box.addWidget(self.btn, alignment=QtCore.Qt.AlignCenter)
        self.setLayout(self.box)
        self.show()

        #self.btn.clicked.connect(self.WriteToFile)


    def WriteToFile(self):
        # проверка, что кнопка нажата
        user_answers = []
        for x in range(1, self.variants_number + 1):
            exec(f"if self.var{x}.isChecked() is True: user_answers.append(self.var{x}.text())")
        user_answers_number = len(user_answers)
        if self.type == MANY_VARIANTS and user_answers_number < 2:
            self.msgv1 = QMessageBox(self)
            self.msgv1.critical(self, "Ошибка ", "Пожалуйста, выберите два и более варианта ответов.", QMessageBox.Ok)
        elif self.type == ONE_VARIANT and (user_answers_number == 0 or user_answers_number > 1):
            self.msgv1 = QMessageBox(self)
            self.msgv1.critical(self, "Ошибка ", "Пожалуйста, выберите один ответ.", QMessageBox.Ok)
        else:
            # count a score
            if self.type == MANY_VARIANTS:
                point = self.maxscore / len(self.rightanswers)

                for el in user_answers:
                    if el in self.rightanswers:
                        self.score += point
                    elif len(user_answers) > len(self.rightanswers):
                        self.score -= point
                self.score = round(self.score, 1)
                ost = self.score % 1
                if ost == 0:
                    self.score = round(self.score)
                if self.score < 0:
                    self.score = 0
            else:
                if user_answers[0] == self.rightanswers:#is it safe???????????????????
                    self.score += self.maxscore

            with open(self.filename, 'a', encoding='utf-8') as file:
                file.write(f'Вопрос #{self.n}' + '\n')
                for el in user_answers:
                    file.write('Ответ:' + el + '\n')
                file.write(f'Баллы:{self.score}' + '\n')
                file.write('\n')
            self.do_task_end.emit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AVariants('one', 2, ['geg', 'kilol', 'mmmm'], 'answerfiles/Test1.txt', 'mmmm', '8')
    sys.exit(app.exec_())
