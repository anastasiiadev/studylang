import sys
import mysql.connector
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QApplication, QTextEdit)
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from mysql.connector import errorcode


try:
    cnn = mysql.connector.connect(
        user='root',
        password='Studydb789',
        host='localhost',
        port = 3306,
        database='studylang')
    print("It works!")
except mysql.connector.Error as e:
    if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with username ot password")
    elif e.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database doesn't exist")
    else:
        print(e)

cursor = cnn.cursor()



class Picture(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.resize(500, 350)
        self.setWindowTitle('Question - Image')
        self.move(self.width() * -2, 0)
        pal = self.palette()
        pal.setColor(QtGui.QPalette.Normal, QtGui.QPalette.Window,
                     QtGui.QColor("#ffffff"))
        self.setPalette(pal)

        #Question
        Qbox = QVBoxLayout(self)
        pixmap = QPixmap('img/S.jpg')
        lbl = QLabel(self)
        lbl.setPixmap(pixmap)
        label = QtWidgets.QLabel("What's in the picture?")
        Qbox.addWidget(label)
        Qbox.addWidget(lbl)

        #Answer
        Abox = QVBoxLayout(self)
        labAnsw = QtWidgets.QLabel("Please enter your answer:")
        Text = QTextEdit()
        Qbox.addWidget(labAnsw)
        Qbox.addWidget(Text)
        self.setLayout(Qbox)
        self.setLayout(Abox)
        self.show()



if __name__ == '__main__':
    query = "SELECT filename FROM tests WHERE id = 1"
    cursor.execute(query)
    result = cursor.fetchall()
    # Преобразуем
    tmp = str(result)
    length = len(tmp)
    file = tmp[3:(length - 4)]

    f = open(file, 'r')
    pict = f.readline()

    app = QApplication(sys.argv)
    window = Picture()
    window.setWindowTitle("Study Lang")
    ico = QtGui.QIcon("img\S.jpg")
    window.setWindowIcon(ico)
    app.setWindowIcon(ico)
    desktop = QtWidgets.QApplication.desktop()
    x = (desktop.width() - window.frameSize().width()) // 2
    y = (desktop.height() - window.frameSize().height()) // 2
    window.move(x, y)
    sys.exit(app.exec_())
