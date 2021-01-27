import sys, mysql.connector, datetime, os, threading, EndDo
from datetime import datetime, timedelta
from mysql.connector import errorcode
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QApplication, QPushButton, QLCDNumber, QFrame, QSizePolicy, QMessageBox)
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt, QTimer


class ThisWindow(QWidget):

    switch_end = QtCore.pyqtSignal()

    def __init__(self, test, score, marks):
        super().__init__()
        self.score = score
        self.testid = test
        self.marks = marks
        self.my_counter = 1
        self.initUI()

    def Center(self):
        self.setWindowTitle("StudyLang")
        ico = QtGui.QIcon("C:\Program Files\MySQL\MySQL Server 8.0\docs\S.jpg")
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


        self.label = QLabel("QLabel", self)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        #self.label.setStyleSheet("QLabel {background-color: pink; font-size: 50pt;}")

        #insert a score into DB
        '''
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
        cnn.commit()'''

        self.setFixedSize(800, 600)
        self.Center()
        pal = self.palette()
        pal.setColor(QtGui.QPalette.Normal, QtGui.QPalette.Window,
                         QtGui.QColor("#ffffff"))
        self.setPalette(pal)

        '''self.lcdNumber = QLCDNumber(self.centralwidget)
        self.lcdNumber.setGeometry(QtCore.QRect(30, 20, 251, 71))
        self.lcdNumber.setFrameShape(QFrame.Box)
        self.lcdNumber.setSegmentStyle(QLCDNumber.Filled)
        self.lcdNumber.setObjectName("lcdNumber")
        self.lcdNumber.setNumDigits(8)
        self.lcdNumber.display('00:00:60')'''

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

        self.second = QLabel("Всего хорошего!", self)
        self.second.setFont(QtGui.QFont("Century Gothic", 15))
        self.second.adjustSize()

        self.btn = QPushButton('До свидания!', self)
        self.btn.setFont(QtGui.QFont("Century Gothic", 10))
        self.btn.setMinimumWidth(150)
        self.btn.setMinimumHeight(30)
        self.box.addStretch(2)
        self.box.addWidget(self.label, alignment=QtCore.Qt.AlignLeft)
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

        '''timer = QTimer()
        timer.timeout.connect(self.local_button_handler)
        timer.start(5)'''
        self.show()
        m = 0
        s = 3
        self.begin = timedelta(minutes=m, seconds=s)
        self.foo()

        self.btn.clicked.connect(self.Remember)

    def Start_T(self):
        global count
        count = 0
        ##self.start_timer()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1000)
        self.begin = datetime.strptime(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S').split()[1]),
                                       '%H:%M:%S')

    def local_button_handler(self):
        self.label.setText("Qlabel" + " %d tick" % self.my_counter)
        self.my_counter += 1

    def Remember(self):
        self.switch_end.emit()
        self.close()

    def foo(self):
        #print(datetime.now())
        #self.label.setText("Qlabel" + " %d tick" % self.my_counter)
        #self.my_counter += 1
        if self.begin == timedelta(seconds=0):
            #self.msgnofile = QMessageBox(self)
            #self.msgnofile.critical(self, "Ошибка ", "Время вышло!", QMessageBox.Ok)
            self.close()
            newobj = EndDo.ThisWindow(61, 0, ['Оценки', '3', '0', '0', '3'])
            newobj.switch_end.connect(lambda: self.task.close())
            return
        self.begin = self.begin - timedelta(seconds=1)
        print(self.begin)
        threading.Timer(1, self.foo).start()


if __name__=="__main__":
    app = QApplication(sys.argv)
    myapp = ThisWindow(15, 7.0, ['Оценки', '8', '5', '3', '10'])
    sys.exit(app.exec_())
