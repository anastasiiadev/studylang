import sys, datetime, os
import logging
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QApplication, QLineEdit, QPushButton, QMessageBox
from PyQt5 import QtCore, QtGui

import general_settings as gs
import dbinteraction as db


class ThisWindow(gs.SLWindow):
    switch_newtest = QtCore.pyqtSignal()

    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.initUI()

    def initUI(self):
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
            logging.error(e)

        test_name = self.name.text()
        self.questions = self.num.text()

        same_testname = 0
        result = db.execute_query(conn, f"SELECT * FROM tests WHERE testname='{test_name}'")
        if result:
            self.msg = QMessageBox(self)
            self.msg.critical(self, "Ошибка", "Тест с таким именем уже существует.", QMessageBox.Ok)
            same_testname = 1

        if test_name == '':
            self.msg = QMessageBox(self)
            self.msg.critical(self, "Ошибка ", "Необходимо ввести название теста", QMessageBox.Ok)
        try:
            self.questions = int(self.questions)
            questions_is_int = True
        except Exception:
            self.msg = QMessageBox(self)
            self.msg.critical(self, "Ошибка ", "Необходимо указать количество вопросов в тесте", QMessageBox.Ok)
            questions_is_int = False

        if test_name != '' and self.questions != '' and questions_is_int is True and same_testname == 0:
            now = datetime.datetime.now()
            date = now.strftime("%Y-%m-%d %H:%M")

            result = db.execute_query(conn, "SELECT max(id) FROM tests")
            test_max_id = result[0][0]
            if test_max_id == None:
                self.new_test_id = 1
            else:
                self.new_test_id = int(test_max_id) + 1

            path = os.getcwd()
            folder = path + '\\testfiles\\'
            if os.path.exists(folder) is False:
                os.mkdir(folder)
            self.filename = "Test%s.txt" % self.new_test_id
            with open('testfiles/' + self.filename, 'w', encoding='utf-8') as file:
                file.write(f'Количество вопросов:{self.questions}\n')
                file.write('\n')

            query = ("INSERT INTO tests (ID, TESTNAME, FILEID, DATE) VALUES "
                     f"({self.new_test_id}, '{test_name}', '{self.filename}', '{date}')")
            db.execute_query(conn, query, 'insert')
            conn.commit()

            result = db.execute_query(conn, "SELECT max(id) FROM work")
            work_max_id = result[0][0]
            if work_max_id == None:
                new_work_id = 1
            else:
                new_work_id = int(work_max_id) + 1
            query2 = ("INSERT INTO work (ID, PERSONID, TRIAL_OR_TEST_ID, MODE) VALUES "
                      f"({new_work_id}, '{int(self.user_id)}', '{self.new_test_id}', '{1}')")

            conn.commit()
            db.execute_query(conn, query2, 'insert')
            conn.close()
            self.switch_newtest.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    import logging
    logging.basicConfig(filename='logs.log', encoding='utf-8', level=logging.DEBUG)
    myapp = ThisWindow('1')
    myapp.show()
    sys.exit(app.exec_())
