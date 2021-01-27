import sys, os, mysql.connector
from mysql.connector import errorcode
from ftplib import FTP
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QGridLayout, QWidget, QTableWidget, QTableWidgetItem, QLabel, QPushButton
from PyQt5.QtCore import Qt


class MainWindow(QWidget):

    switch_tostudentstable = QtCore.pyqtSignal()

    def __init__(self, id):
        QWidget.__init__(self)
        self.id = id
        self.initUI()

    def initUI(self):
        try:
            self.cnn = mysql.connector.connect(
                host='stacey789.beget.tech',
                database='stacey789_db',
                user='stacey789_db',
                password='StudyLang_user789',
                port=3306)
            print('You have successfully connected to the Database.')
            self.cursor = self.cnn.cursor()

            query = "SELECT p.fio, tests.testname, t.date, t.score, t.mark " \
                    "FROM `people` as p, testing as t, tests, work as w " \
                    "WHERE p.id = w.person_id AND	w.trial_or_test_id = t.id AND tests.id = t.test_id AND w.mode = 2 AND p.id = {}".format(self.id)
            self.cursor.execute(query)
            queryresult = self.cursor.fetchall()

            self.setFixedSize(800, 600)
            self.Center()
            pal = self.palette()
            pal.setColor(QtGui.QPalette.Normal, QtGui.QPalette.Window,
                         QtGui.QColor("#ffffff"))
            self.setPalette(pal)

            grid_layout = QGridLayout()
            self.setLayout(grid_layout)
            self.table = QTableWidget(self)
            self.table.setColumnCount(5)
            self.table.setRowCount(len(queryresult))
            self.table.setHorizontalHeaderLabels(["Ученик", "Тест", "Дата и время", "Баллы", "Оценка"])

            # Устанавливаем выравнивание на заголовки
            for j in range(0, 5):
                self.table.horizontalHeaderItem(j).setTextAlignment(Qt.AlignCenter)

            i = 0
            for el in queryresult:
                # заполняем строку
                for k in range(0, 3):
                    self.table.setItem(i, k, QTableWidgetItem(el[k]))
                self.table.setItem(i, 3, QTableWidgetItem(str(el[3])))
                self.table.setItem(i, 4, QTableWidgetItem(str(el[4])))
                i += 1

            self.table.resizeRowsToContents()
            header = self.table.horizontalHeader()
            for i in range(0, 5):
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)

            btn = QPushButton('К таблице учеников')
            btn.setFixedSize(150, 25)
            grid_layout.addWidget(self.table, 0, 0)
            grid_layout.addWidget(btn, 1, 0)
            self.show()

            btn.clicked.connect(lambda: self.switch_tostudentstable.emit())

        except mysql.connector.Error as e:
            if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with username or password")
            elif e.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database doesn't exist")
            else:
                print(e)
            self.close()


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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow(2)
    mw.show()
    sys.exit(app.exec())