import sys, os, base64
from cryptography.fernet import Fernet
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QApplication, QLineEdit, QPushButton, QMessageBox, QHBoxLayout)
from PyQt5 import QtCore, QtGui, QtWidgets

import dbinteraction as db
import general_settings as gs


class ThisWindow(gs.SLWindow):

    switch_register = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.box = QVBoxLayout(self)
        self.entertext = QLabel("Введите данные для регистрации:", self)
        self.entertext.setFont(QtGui.QFont("Century Gothic", 15))
        self.entertext.adjustSize()
        self.fiobox = QHBoxLayout(self)
        self.fiotext = QLabel("Ваше ФИО:", self)
        self.fiotext.setFont(QtGui.QFont("Century Gothic", 13))
        self.fiotext.adjustSize()
        self.fioline = QLineEdit(self)
        self.fioline.setFixedSize(200, 25)
        self.logbox = QHBoxLayout(self)
        self.logintext = QLabel("Логин:", self)
        self.logintext.setFont(QtGui.QFont("Century Gothic", 13))
        self.logintext.adjustSize()
        self.loginline = QLineEdit(self)
        self.loginline.setFixedSize(200, 25)
        self.pwbox = QHBoxLayout(self)
        self.pwtext = QLabel("Пароль:", self)
        self.pwtext.setFont(QtGui.QFont("Century Gothic", 13))
        self.pwtext.adjustSize()
        self.passwordline = QLineEdit(self)
        self.passwordline.setFixedSize(200, 25)
        self.pwbox2 = QHBoxLayout(self)
        self.pwtext2 = QLabel("Подтвердите пароль:", self)
        self.pwtext2.setFont(QtGui.QFont("Century Gothic", 13))
        self.pwtext2.adjustSize()
        self.passwordline2 = QLineEdit(self)
        self.passwordline2.setFixedSize(200, 25)
        self.btn = QPushButton("OK", self)
        self.box.addStretch(1)
        self.box.addWidget(self.entertext, alignment=QtCore.Qt.AlignCenter)
        self.box.addStretch(1)
        self.fiobox.addWidget(self.fiotext, alignment=QtCore.Qt.AlignRight)
        self.fiobox.addSpacing(20)
        self.fiobox.addWidget(self.fioline, alignment=QtCore.Qt.AlignLeft)
        self.logbox.addWidget(self.logintext, alignment=QtCore.Qt.AlignRight)
        self.logbox.addSpacing(20)
        self.logbox.addWidget(self.loginline, alignment=QtCore.Qt.AlignLeft)
        self.pwbox.addWidget(self.pwtext, alignment=QtCore.Qt.AlignRight)
        self.pwbox.addSpacing(20)
        self.pwbox.addWidget(self.passwordline, alignment=QtCore.Qt.AlignLeft)
        self.pwbox2.addWidget(self.pwtext2, alignment=QtCore.Qt.AlignRight)
        self.pwbox2.addSpacing(20)
        self.pwbox2.addWidget(self.passwordline2, alignment=QtCore.Qt.AlignLeft)
        self.box.addLayout(self.fiobox)
        self.box.addLayout(self.logbox)
        self.box.addLayout(self.pwbox)
        self.box.addLayout(self.pwbox2)
        self.box.addStretch(1)
        self.box.addWidget(self.btn, alignment=QtCore.Qt.AlignCenter)
        self.box.addStretch(2)
        self.setLayout(self.box)
        self.fioline.setFocus()
        self.show()

        self.btn.clicked.connect(self.Register)

    def Register(self):
        self.fio = self.fioline.text()
        self.fio = self.fio.strip()
        self.login = self.loginline.text()
        self.login = self.login.strip()
        self.password = self.passwordline.text()
        self.password = self.password.strip()
        self.password2 = self.passwordline2.text()
        self.password2 = self.password2.strip()

        if self.fio == '':
            self.msgnum = QMessageBox(self)
            self.msgnum.critical(self, "Ошибка ", "Пожалуйста, укажите ваше ФИО.", QMessageBox.Ok)
        elif self.login == '':
            self.msgnum = QMessageBox(self)
            self.msgnum.critical(self, "Ошибка ", "Пожалуйста, укажите ваш логин.", QMessageBox.Ok)
        elif self.password == '':
            self.msgnum = QMessageBox(self)
            self.msgnum.critical(self, "Ошибка ", "Пожалуйста, укажите ваш пароль.", QMessageBox.Ok)
        elif self.password2 == '':
            self.msgnum = QMessageBox(self)
            self.msgnum.critical(self, "Ошибка ", "Пожалуйста, подтвердите ваш пароль.", QMessageBox.Ok)
        else:
            if self.password != self.password2:
                self.msgnum = QMessageBox(self)
                self.msgnum.critical(self, "Ошибка ", "Указанные пароли не совпадают. Попробуйте их ввести еще раз.", QMessageBox.Ok)
            else:
                try:
                    # check if there is the same login
                    conn = db.create_connection()
                    result = db.execute_query(conn, "SELECT login FROM people")
                    logins = []
                    for el in result:
                        tmp = str(el)
                        length = len(tmp)
                        newLog = tmp[2:(length - 3)]
                        logins.append(newLog)
                    samelogin = 0
                    for el in logins:
                        if self.login == el:
                            samelogin = 1
                            break
                    if samelogin == 1:
                        self.msgnum = QMessageBox(self)
                        self.msgnum.critical(self, "Ошибка ", "Такой логин уже существует. Укажите, пожалуйста, другой.", QMessageBox.Ok)
                    else:
                        #get new id
                        result = db.execute_query(conn, "SELECT max(id) FROM people")
                        max = result[0][0]
                        if max == None:
                            self.n = 1
                        else:
                            self.n = int(max) + 1
                        # Шифруем пароль
                        # get key
                        s = self.login[::-1]+str(self.n * 24 + self.n * 57 + 13)
                        s = s + ('y' * (32 - len(s)))
                        b = s.encode("UTF-8")
                        cipher_key = base64.b64encode(b)
                        cipher = Fernet(cipher_key)
                        text = self.password.encode("UTF-8")
                        encrypted_text = cipher.encrypt(text)
                        hashedpass = encrypted_text.decode('utf-8')
                        if len(hashedpass) > 300:
                            self.msgnum = QMessageBox(self)
                            self.msgnum.critical(self, "Ошибка ",
                                                     "Пароль слишком длинный. Пожалуйста, введите пароль короче указанного.",
                                                     QMessageBox.Ok)
                        else:
                            query = (
                                "INSERT INTO people (ID, FIO, LOGIN, PASSWORD, ROLE, CONFIRMED) VALUES "
                                f"({self.n}, '{self.fio}', '{self.login}', {hashedpass}, 2, 0)")
                            db.execute_query(conn, query, "insert")
                            conn.commit()
                            conn.close()
                            self.hide()
                            self.switch_register.emit()
                except Exception as e:
                    print(e)
                    sys.exit(app.exec_())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = ThisWindow()
    myapp.show()
    sys.exit(app.exec_())
