import sys, mysql.connector, os
from mysql.connector import errorcode
from ftplib import FTP
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QApplication, QPushButton)
from PyQt5 import QtCore, QtGui


class ThisWindow(QWidget):

    switch_end = QtCore.pyqtSignal()

    def __init__(self, test, score, marks):
        super().__init__()
        self.score = score
        self.testid = test
        self.marks = marks
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
            cnn = mysql.connector.connect(
                host='stacey789.beget.tech',
                database='stacey789_db',
                user='stacey789_db',
                password='StudyLang_user789',
                port=3306)
        except mysql.connector.Error as e:
            if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with username or password")
            elif e.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database doesn't exist")
            else:
                print(e)
        self.cursor = cnn.cursor()
        self.cursor.execute("UPDATE testing set score={}, mark={} WHERE id={}".format(self.score, self.mark, self.testid))
        cnn.commit()
        cnn.close()

        self.setFixedSize(800, 600)
        self.Center()
        pal = self.palette()
        pal.setColor(QtGui.QPalette.Normal, QtGui.QPalette.Window,
                         QtGui.QColor("#ffffff"))
        self.setPalette(pal)

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
            if ed == 1:
                text = 'балл'
            elif ed >= 5 or ed == 0 or self.score in (10, 11, 12, 13, 14):
                text = 'баллов'
            else:
                text = 'балла'
        self.showscore = QLabel("Вы набрали %s " % self.score + text + ' из %s!' % self.marks[4], self)
        self.showscore.setFont(QtGui.QFont("Century Gothic", 15, QtGui.QFont.Bold))
        self.showscore.adjustSize()

        self.umark = QLabel("Ваша оценка - {}!".format(self.mark), self)
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
        self.show()

        self.btn.clicked.connect(self.Remember)


    def Remember(self):
        self.switch_end.emit()
        self.close()


if __name__=="__main__":
    app = QApplication(sys.argv)
    #myapp = ThisWindow(15, 7.0, ['Оценки', '8', '5', '3', '10'])
    myapp = ThisWindow(10, 0, ['Оценки', '8', '5', '3', '9'])
    sys.exit(app.exec_())
