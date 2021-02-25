import sys, base64
import logging
from cryptography.fernet import Fernet
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QApplication, QLineEdit, QPushButton, QMessageBox, QHBoxLayout
from PyQt5 import QtCore, QtGui, QtWidgets

import dbinteraction as db
import general_settings as gs


class ThisWindow(gs.SLWindow):
    switch_passed = QtCore.pyqtSignal()
    switch_register = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
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
        teacherstext = QLabel(
            "Регистрация преподавателей проводится администратором.\nДля подачи заявки напишите нам на email staceykarshakevich@gmail.com",
            self)
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
            user_login = self.login.text().strip()
            user_password = self.password.text().strip()

            if user_login == '':
                self.msgnum = QMessageBox(self)
                self.msgnum.critical(self, "Ошибка ", "Пожалуйста, укажите ваш логин.", QMessageBox.Ok)
            elif user_password == '':
                self.msgnum = QMessageBox(self)
                self.msgnum.critical(self, "Ошибка ", "Пожалуйста, укажите ваш пароль.", QMessageBox.Ok)
            else:
                conn = db.create_connection()
                result = db.execute_query(conn, "SELECT login FROM people")
                db_logins = [x[0] for x in result]
                login_permission = 0
                for login in db_logins:
                    if user_login == login:
                        login_permission = 1
                        query = f"SELECT id, password, confirmed FROM people WHERE login='{login}'"
                        result = db.execute_query(conn, query)[0]
                        self.user_id, bhashedpass, confirmed = result[0], result[1].encode('utf-8'), result[2]
                        break
                if login_permission == 0:
                    self.lmsg = QMessageBox(self)
                    self.lmsg.critical(self, "Ошибка ", "Данный логин не найден! Укажите его снова.", QMessageBox.Ok)
                else:
                    secret = user_login[::-1] + str(int(self.user_id) * 24 + int(self.user_id) * 57 + 13)
                    secret += ('y' * (32 - len(secret)))
                    bsecret = secret.encode("UTF-8")
                    cipher_key = base64.b64encode(bsecret)
                    cipher = Fernet(cipher_key)
                    decrypted_text = cipher.decrypt(bhashedpass)
                    basepassword = decrypted_text.decode('utf-8')
                    if user_password != basepassword:
                        self.pmsg = QMessageBox(self)
                        self.pmsg.critical(self, "Ошибка ", "Данный пароль не найден! Укажите его снова.",
                                           QMessageBox.Ok)
                    if user_login == login and user_password == basepassword:
                        if confirmed == 1:
                            logging.info('You are logged in!')
                            conn.close()
                            self.hide()
                            self.switch_passed.emit()
                        else:
                            self.msg = QMessageBox(self)
                            self.msg.critical(self, "Ошибка ",
                                              "Ваша учетная запись не подтверждена. Попробуйте авторизоваться позже.",
                                              QMessageBox.Ok)
        except Exception as e:
            self.show()
            self.msg = QMessageBox(None)
            self.msg.critical(None, "Ошибка ",
                              "Не удалось подключиться к базе данных. Попробуйте авторизоваться позже.",
                              QMessageBox.Ok)
            self.close()
            logging.error(e)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    import logging
    logging.basicConfig(filename='logs.log', encoding='utf-8', level=logging.DEBUG)
    myapp = ThisWindow()
    myapp.show()
    sys.exit(app.exec_())
