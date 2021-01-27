import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
    QTextEdit, QApplication, QHBoxLayout, QVBoxLayout, )


class Text_Text(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        Question = QLabel('Задание:')
        Answer = QLabel('Ваш ответ:')

        QuestionEdit = QTextEdit(data)
        AnswerEdit = QLineEdit()

        vboxQ = QVBoxLayout()
        vboxQ.addWidget(Question)
        vboxQ.addStretch(1)
        hboxQ = QHBoxLayout()
        hboxQ.addLayout(vboxQ)
        hboxQ.addWidget(QuestionEdit)

        vboxA = QVBoxLayout()
        vboxA.addWidget(Answer)
        vboxA.addStretch(1)
        hboxA = QHBoxLayout()
        hboxA.addLayout(vboxA)
        hboxA.addWidget(AnswerEdit)

        vbox = QVBoxLayout()
        vbox.addLayout(hboxQ)
        vbox.addLayout(hboxA)

        self.setLayout(vbox)

        self.setGeometry(500, 500, 500, 300)
        self.setWindowTitle('StudyLang')
        self.show()



if __name__ == '__main__':

    app = QApplication(sys.argv)

    f = open('files/QuestionText.txt', 'r')
    #predata = f.readlines()
    predata = 'Nastya is testing'
    data = ''.join(predata)

    ex = Text_Text()
    sys.exit(app.exec_())