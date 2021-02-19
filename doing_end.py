import sys
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QApplication, QPushButton
from PyQt5 import QtCore, QtGui

import dbinteraction as db
import general_settings as gs


class ThisWindow(gs.SLWindow):

    switch_end = QtCore.pyqtSignal()

    def __init__(self, test, score, marks):
        super().__init__()
        self.score = score
        self.testid = test
        self.marks = marks
        self.initUI()

    def initUI(self):
        #define a mark
        if self.score >= int(self.marks[1]):
            self.mark = 5
        elif self.score >= int(self.marks[2]):
            self.mark = 4
        elif self.score >= int(self.marks[3]):
            self.mark = 3
        else:
            self.mark = 2

        #insert a score into DB
        try:
            conn = db.create_connection()
            db.execute_query(conn, f"UPDATE testing set score={self.score}, mark={self.mark} WHERE id={self.testid}", 'insert')
            conn.commit()
            conn.close()
        except Exception as e:
            print(e)

        self.box = QVBoxLayout(self)
        self.first = QLabel("Спасибо за прохождение теста!", self)
        self.first.setFont(QtGui.QFont("Century Gothic", 15))
        self.first.adjustSize()

        ed = self.score % 10
        doli = ed % 1
        if doli == 0:
            self.score = round(self.score)
        if doli < 1 and doli != 0:
            text = 'балла'
        else:
            if ed >= 5 or ed == 0 or self.score in (10, 11, 12, 13, 14):
                text = 'баллов'
            elif ed == 1:
                text = 'балл'
            else:
                text = 'балла'
        self.showscore = QLabel(f"Вы набрали {self.score} " + text + f' из {self.marks[4]}!', self)
        self.showscore.setFont(QtGui.QFont("Century Gothic", 15, QtGui.QFont.Bold))
        self.showscore.adjustSize()

        self.umark = QLabel(f"Ваша оценка - {self.mark}!", self)
        self.umark.setFont(QtGui.QFont("Century Gothic", 15, QtGui.QFont.Bold))
        self.umark.adjustSize()

        if self.mark == 2:
            self.second = QLabel("Вам нужно еще позаниматься, и тогда все получится!", self)
        elif self.mark == 3:
            self.second = QLabel("Неплохо, но вы можете еще лучше!", self)
        else:
            self.second = QLabel("Всего хорошего!", self)
        self.second.setFont(QtGui.QFont("Century Gothic", 15))
        self.second.adjustSize()

        self.btn = QPushButton('До свидания!', self)
        self.btn.setFont(QtGui.QFont("Century Gothic", 10))
        self.btn.setMinimumWidth(150)
        self.btn.setMinimumHeight(30)
        self.box.addStretch(2)
        self.box.addWidget(self.first, alignment=QtCore.Qt.AlignCenter)
        self.box.addStretch(1)
        self.box.addWidget(self.showscore, alignment=QtCore.Qt.AlignCenter)
        self.box.addStretch(1)
        self.box.addWidget(self.umark, alignment=QtCore.Qt.AlignCenter)
        self.box.addStretch(1)
        self.box.addWidget(self.second, alignment=QtCore.Qt.AlignCenter)
        self.box.addStretch(1)
        self.box.addWidget(self.btn, alignment=QtCore.Qt.AlignCenter)
        self.box.addStretch(2)
        self.setLayout(self.box)

        self.btn.clicked.connect(self.Remember)


    def Remember(self):
        self.switch_end.emit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = ThisWindow(28, 16.0, ['Оценки', '3', '3', '3', '11'])
    sys.exit(app.exec_())
