import sys, mysql.connector, os
from ftplib import FTP
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMessageBox, QWidget, QVBoxLayout, QLabel, QApplication, QPushButton, QComboBox
from mysql.connector import errorcode

class ThisWindow(QWidget):

    switch_choosetest = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.SelectFromDB()
        if self.status == 1:
            self.initUI()


    def SelectFromDB(self):
        try:
            cnn = mysql.connector.connect(
                host='stacey789.beget.tech',
                database='stacey789_db',
                user='stacey789_db',
                password='StudyLang_user789',
                port=3306)
            self.cursor = cnn.cursor()

            self.cursor.execute("SELECT id, testname FROM tests")
            result = self.cursor.fetchall()
            if not result:
                self.msg = QMessageBox(self)
                self.msg.critical(self, "Ошибка ", "Не удалось найти тесты. Повторите попытку позже.", QMessageBox.Ok)
                self.status = 0
            else:
                self.d = dict(result)
                self.testnames = list(self.d.values())
                self.status = 1
                cnn.close()
        except mysql.connector.Error as e:
            if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                text = "Something is wrong with username or password"
            elif e.errno == errorcode.ER_BAD_DB_ERROR:
                text = "Database doesn't exist"
            else:
                text = e
            self.setFixedSize(800, 600)
            self.Center()
            self.msg = QMessageBox(self)
            self.msg.critical(self, "Ошибка ", "Не удалось найти тесты. Повторите попытку позже.", QMessageBox.Ok)
            sys.exit()
            self.status = 0


    def initUI(self):
        self.setFixedSize(800, 600)
        self.Center()
        pal = self.palette()
        pal.setColor(QtGui.QPalette.Normal, QtGui.QPalette.Window,
                     QtGui.QColor("#ffffff"))
        self.setPalette(pal)

        self.box = QVBoxLayout(self)
        self.qtest = QLabel("Какой тест вы хотите пройти?", self)
        self.qtest.setFont(QtGui.QFont("Century Gothic", 15, QtGui.QFont.Bold))
        self.qtest.adjustSize()
        self.qbox = QComboBox(self)
        self.qbox.addItems(self.testnames)
        #self.qbox.setFixedSize(300, 25)
        self.btn = QPushButton('OK', self)
        self.box.addStretch(2)
        self.box.addWidget(self.qtest, alignment=QtCore.Qt.AlignCenter)
        self.box.addWidget(self.qbox, alignment=QtCore.Qt.AlignCenter)
        self.box.addStretch(1)
        self.box.addWidget(self.btn, alignment=QtCore.Qt.AlignCenter)
        self.box.addStretch(2)
        self.setLayout(self.box)

        self.btn.clicked.connect(self.RememberTestId)

    def RememberTestId(self):
        self.test = self.qbox.currentText()
        self.gettestid = self.get_key(self.d, self.test)
        self.switch_choosetest.emit()


    def get_key(self, d, value):
        for k, v in d.items():
            if v == value:
                return k

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



if __name__=="__main__":
    app = QApplication(sys.argv)
    myapp = ThisWindow()
    myapp.show()
    sys.exit(app.exec_())


