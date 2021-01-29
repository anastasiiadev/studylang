import sys, os, base64
from cryptography.fernet import Fernet
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QApplication, QLineEdit, QPushButton, QMessageBox, QHBoxLayout)
from PyQt5 import QtCore, QtGui, QtWidgets
import dbinteraction as db
import files


class ThisWindow(QWidget):

    switch_passed = QtCore.pyqtSignal()
    switch_register = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()

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
        self.setFixedSize(850, 650)
        self.Center()
        pal = self.palette()
        pal.setColor(QtGui.QPalette.Normal, QtGui.QPalette.Window,
                         QtGui.QColor("#ffffff"))
        self.setPalette(pal)

        self.box = QVBoxLayout(self)
        self.welcome = QLabel("Добро пожаловать в StudyLang!", self)
        self.welcome.setFont(QtGui.QFont("Century Gothic", 15, QtGui.QFont.Bold))
        self.welcome.adjustSize()
        self.authorise = QLabel("Пожалуйста, авторизуйтесь.", self)
        self.authorise.setFont(QtGui.QFont("Century Gothic", 15))
        self.authorise.adjustSize()
        self.logbox = QHBoxLayout(self)
        self.logintext = QLabel("Логин:", self)
        self.logintext.setFont(QtGui.QFont("Century Gothic", 13))
        self.logintext.adjustSize()
        self.login = QLineEdit(self)
        self.login.setFixedSize(200, 25)
        self.pwbox = QHBoxLayout(self)
        self.pwtext = QLabel("Пароль:", self)
        self.pwtext.setFont(QtGui.QFont("Century Gothic", 13))
        self.pwtext.adjustSize()
        self.password = QLineEdit(self)
        self.password.setFixedSize(200, 25)
        self.btn = QPushButton("OK", self)
        self.regbox = QVBoxLayout(self)
        regtext = QLabel("Нет учетной записи?", self)
        regtext.setFont(QtGui.QFont("Century Gothic", 13))
        regtext.adjustSize()
        self.regbtn = QPushButton("Зарегистрироваться", self)
        self.regbtn.setFixedSize(200, 25)
        teacherstext = QLabel("Регистрация преподавателей проводится администратором.\nДля подачи заявки напишите нам на email staceykarshakevich@gmail.com", self)
        teacherstext.setFont(QtGui.QFont("Century Gothic", 11))
        teacherstext.setWordWrap(True)
        teacherstext.adjustSize()
        teacherstext.setAlignment(QtCore.Qt.AlignCenter)
        teacherstext.setFixedSize(650, 100)
        self.box.addStretch(1)
        self.box.addWidget(self.welcome, alignment=QtCore.Qt.AlignCenter)
        self.box.addStretch(1)
        self.box.addWidget(self.authorise, alignment=QtCore.Qt.AlignCenter)
        self.logbox.addWidget(self.logintext, alignment=QtCore.Qt.AlignRight)
        self.logbox.addSpacing(20)
        self.logbox.addWidget(self.login, alignment=QtCore.Qt.AlignLeft)
        self.pwbox.addWidget(self.pwtext, alignment=QtCore.Qt.AlignRight)
        self.pwbox.addSpacing(20)
        self.pwbox.addWidget(self.password, alignment=QtCore.Qt.AlignLeft)
        self.regbox.addWidget(regtext, alignment=QtCore.Qt.AlignCenter)
        self.regbox.addSpacing(10)
        self.regbox.addWidget(self.regbtn, alignment=QtCore.Qt.AlignCenter)
        self.regbox.addWidget(teacherstext, alignment=QtCore.Qt.AlignCenter)
        self.box.addLayout(self.logbox)
        self.box.addLayout(self.pwbox)
        self.box.addSpacing(30)
        self.box.addWidget(self.btn, alignment=QtCore.Qt.AlignCenter)
        self.box.addStretch(1)
        self.box.addLayout(self.regbox)
        self.box.addStretch(2)
        self.setLayout(self.box)
        self.login.setFocus()
        self.show()

        self.btn.clicked.connect(self.Autorise)
        self.regbtn.clicked.connect(lambda: self.switch_register.emit())

    def Autorise(self):
        try:
            login = self.login.text()
            login = login.strip()
            password = self.password.text()
            password = password.strip()

            if login == '':
                self.msgnum = QMessageBox(self)
                self.msgnum.critical(self, "Ошибка ", "Пожалуйста, укажите ваш логин.", QMessageBox.Ok)
            elif password == '':
                self.msgnum = QMessageBox(self)
                self.msgnum.critical(self, "Ошибка ", "Пожалуйста, укажите ваш пароль.", QMessageBox.Ok)
            else:
                conn = db.create_connection()
                result = db.execute_query(conn, "SELECT login FROM people")
                logins = []
                for el in result:
                    tmp = str(el)
                    length = len(tmp)
                    newLog = tmp[2:(length - 3)]
                    logins.append(newLog)

                flag = 0
                for el in logins:
                    if login == el:
                        flag = 1
                        query = "SELECT id FROM people WHERE login='{}'".format(login)
                        result = db.execute_query(conn, query)
                        # Преобразуем id
                        tmp = str(result)
                        length = len(tmp)
                        a = tmp[2:(length - 3)]
                        self.user_id = a
                        query = "SELECT password, confirmed FROM people WHERE login='{}'".format(login)
                        result = db.execute_query(conn, query)
                        # Преобразуем пароль
                        tmp = str(result)
                        length = len(tmp)
                        hashedpass = tmp[3:(length - 4)]
                        bhashedpass = hashedpass.encode('utf-8')
                        #Проверяем, есть ли подтверждение
                        confirmed = result[0][1]
                        break
                if flag == 0:
                    self.lmsg = QMessageBox(self)
                    self.lmsg.critical(self, "Ошибка ", "Данный логин не найден! Укажите его снова.", QMessageBox.Ok)
                else:
                    s = login[::-1] + str(int(self.user_id) * 24 + int(self.user_id) * 57 + 13)
                    s = s + ('y' * (32 - len(s)))
                    b = s.encode("UTF-8")
                    cipher_key = base64.b64encode(b)
                    cipher = Fernet(cipher_key)
                    decrypted_text = cipher.decrypt(bhashedpass)
                    basepassword = decrypted_text.decode('utf-8')
                    if password != basepassword:
                        self.pmsg = QMessageBox(self)
                        self.pmsg.critical(self, "Ошибка ", "Данный пароль не найден! Укажите его снова.",
                                           QMessageBox.Ok)
                    if login == el and password == basepassword:
                        if confirmed == 1:
                            print('You are logged in!')
                            conn.close()
                            self.hide()
                            self.switch_passed.emit()
                        else:
                            self.pmsg = QMessageBox(self)
                            self.pmsg.critical(self, "Ошибка ", "Ваша учетная запись не подтверждена. Попробуйте авторизоваться позже.", QMessageBox.Ok)
        except Exeception as e:
            print(e)
            self.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = ThisWindow()
    myapp.show()
    sys.exit(app.exec_())
