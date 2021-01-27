import sys, datetime, mysql.connector, os
from ftplib import FTP
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QApplication, QLineEdit, QPushButton, QMessageBox)
from PyQt5 import QtCore, QtGui
from mysql.connector import errorcode


class ThisWindow(QWidget):

    switch_newtest = QtCore.pyqtSignal()

    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.initUI()

    def isInt(self, value):
        try:
            int(value)
            return True
        except ValueError:
            return False

    def Center(self):
        self.setWindowTitle("StudyLang")
        file = 'iconSL.jpg'
        path = os.getcwd()
        folder = path + '\\img\\'
        if os.path.exists(folder) is False:
            os.mkdir(folder)
        if os.path.exists(path + 'img/' + file) is False:
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
        self.setFixedSize(800, 600)
        self.Center()
        pal = self.palette()
        pal.setColor(QtGui.QPalette.Normal, QtGui.QPalette.Window,
                         QtGui.QColor("#ffffff"))
        self.setPalette(pal)

        self.box = QVBoxLayout(self)
        self.lname = QLabel("Укажите название теста:", self)
        self.lname.setFont(QtGui.QFont("Century Gothic", 15, QtGui.QFont.Bold))
        self.lname.adjustSize()
        self.name = QLineEdit(self)
        self.name.setFixedSize(400, 25)
        self.numlbl = QLabel("Введите количество вопросов в тесте:", self)
        self.numlbl.setFont(QtGui.QFont("Century Gothic", 15, QtGui.QFont.Bold))
        self.numlbl.adjustSize()
        self.num = QLineEdit(self)
        self.num.setFixedSize(40, 25)
        self.btn = QPushButton('Создать', self)
        self.box.addStretch(1)
        self.box.addWidget(self.lname, alignment=QtCore.Qt.AlignCenter)
        self.box.addWidget(self.name, alignment=QtCore.Qt.AlignCenter)
        self.box.addStretch(1)
        self.box.addWidget(self.numlbl, alignment=QtCore.Qt.AlignCenter)
        self.box.addWidget(self.num, alignment=QtCore.Qt.AlignCenter)
        self.box.addStretch(1)
        self.box.addWidget(self.btn, alignment=QtCore.Qt.AlignCenter)
        self.box.addStretch(2)
        self.setLayout(self.box)
        self.name.setFocus()

        self.btn.clicked.connect(self.Remember)


    def Remember(self):
        try:
            cnn = mysql.connector.connect(
                host='stacey789.beget.tech',
                database='stacey789_db',
                user='stacey789_db',
                password='StudyLang_user789',
                port=3306)
            print("It works!")
        except mysql.connector.Error as e:
            if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with username or password")
            elif e.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database doesn't exist")
            else:
                print(e)
        self.cursor = cnn.cursor()

        test_name = self.name.text()
        self.questions = self.num.text()

        flag = 0
        self.cursor.execute("SELECT testname FROM tests")
        result = self.cursor.fetchall()
        for el in result:
            el = str(el)
            el = el[2:(len(el) - 3)]
            if test_name == el:
                self.msgnum = QMessageBox(self)
                self.msgnum.critical(self, "Ошибка", "Тест с таким именем уже существует.", QMessageBox.Ok)
                flag = 1
                break

        if test_name == '':
            self.msg = QMessageBox(self)
            self.msg.critical(self, "Ошибка ", "Необходимо ввести название теста", QMessageBox.Ok)
        typeQuestions = self.isInt(self.questions)
        if self.questions == '' or typeQuestions is False:
            self.msgnum = QMessageBox(self)
            self.msgnum.critical(self, "Ошибка ", "Необходимо указать количество вопросов в тесте", QMessageBox.Ok)

        if test_name != '' and (self.questions != '' and typeQuestions is True) and flag == 0:
            now = datetime.datetime.now()
            date = now.strftime("%d-%m-%Y %H:%M")

            self.cursor.execute("SELECT max(id) FROM tests")
            result = self.cursor.fetchall()
            max = result[0][0]
            if max == None:
                self.n = 1
            else:
                self.n = int(max) + 1

            path = os.getcwd()
            folder = path + '\\testfiles\\'
            if os.path.exists(folder) is False:
                os.mkdir(folder)
            self.filename = "Test%s.txt" % self.n
            with open('testfiles/' + self.filename, 'w', encoding='utf-8') as file:
                file.write('Количество вопросов: %s\n' % self.questions)
                file.write('\n')

            self.cursor.execute("INSERT INTO tests (ID, TESTNAME, FILE_NAME, DATE) VALUES "
                           "({}, '{}', '{}', '{}')".format(self.n, test_name, self.filename, date))
            cnn.commit()

            self.cursor.execute("SELECT max(id) FROM work")
            result = self.cursor.fetchall()
            max = result[0][0]
            if max == None:
                id = 1
            else:
                id = int(max) + 1
            self.cursor.execute("INSERT INTO work (ID, PERSON_ID, TRIAL_OR_TEST_ID, MODE) VALUES "
                                "({}, '{}', '{}', '{}')".format(id, int(self.user_id), self.n, 1))
            cnn.commit()

            cnn.close()
            self.switch_newtest.emit()


if __name__=="__main__":
    app = QApplication(sys.argv)
    myapp = ThisWindow('1')
    myapp.switch_newtest.connect(lambda: print('done'))
    myapp.show()
    sys.exit(app.exec_())
