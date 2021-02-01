import sys, datetime, os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QApplication, QLineEdit, QPushButton, QMessageBox)
from PyQt5 import QtCore, QtGui
import files
import dbinteraction as db


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
        if os.path.exists(folder + file) is False:
            f = files.File()
            f.get("1tdvwtNx2iQUEDPbpe7NsSl-djVe-_h9G", "img/iconSL.jpg")
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
            conn = db.create_connection()
        except Exception as e:
            print(e)

        test_name = self.name.text()
        self.questions = self.num.text()

        flag = 0
        result = db.execute_query(conn, "SELECT * FROM tests WHERE testname='{}'".format(test_name))
        print(result)
        if result:
            self.msgnum = QMessageBox(self)
            self.msgnum.critical(self, "Ошибка", "Тест с таким именем уже существует.", QMessageBox.Ok)
            flag = 1

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

            result = db.execute_query(conn, "SELECT max(id) FROM tests")
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

            query = ("INSERT INTO tests (ID, TESTNAME, FILEID, DATE) VALUES "
                     "({}, '{}', '{}', '{}')".format(self.n, test_name, self.filename, date))
            db.execute_query(conn, query, 'insert')
            conn.commit()

            result = db.execute_query(conn, "SELECT max(id) FROM work")
            max = result[0][0]
            if max == None:
                id = 1
            else:
                id = int(max) + 1
            query = ("INSERT INTO work (ID, PERSONID, TRIAL_OR_TEST_ID, MODE) VALUES "
                     "({}, '{}', '{}', '{}')".format(id, int(self.user_id), self.n, 1))
            conn.commit()

            conn.close()
            self.switch_newtest.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = ThisWindow('1')
    myapp.switch_newtest.connect(lambda: print('done'))
    myapp.show()
    sys.exit(app.exec_())
