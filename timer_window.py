import sys, threading, os
from ftplib import FTP
from datetime import datetime, timedelta
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QGridLayout, QSizePolicy, QApplication, QMessageBox
from PyQt5 import QtGui


class Window(QWidget):
    def __init__(self, time):
        self.time = time

        QWidget.__init__(self)
        self.Center()
        self.label = QLabel("Осталось  " + "{}".format(time), self)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QtGui.QFont("Century Gothic", 15))
        self.label.adjustSize()

        self.layout = QGridLayout()
        self.layout.addWidget(self.label, 0, 0)

        self.setLayout(self.layout)
        self.show()

    def local_button_handler(self, time):
        self.label.setText("Осталось  " + "{}".format(time))

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
        self.move(50, 50)

if __name__=="__main__":
    app = QApplication(sys.argv)
    w = Window('00:00:08')
    sys.exit(app.exec_())
