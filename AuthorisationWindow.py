import sys, mysql.connector, os, base64
from cryptography.fernet import Fernet
from ftplib import FTP
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QApplication, QLineEdit, QPushButton, QMessageBox, QHBoxLayout)
from PyQt5 import QtCore, QtGui, QtWidgets
from mysql.connector import errorcode


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
            self.cnn = mysql.connector.connect(
                host='stacey789.beget.tech',
                database='stacey789_db',
                user='stacey789_db',
                password='StudyLang_user789',
                port=3306)
            print('You have successfully connected to the Database.')
            self.cursor = self.cnn.cursor()

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
                query = "SELECT login FROM people"
                self.cursor.execute(query)
                result = self.cursor.fetchall()
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
                        self.cursor.execute(query)
                        result = self.cursor.fetchall()
                        # Преобразуем id
                        tmp = str(result)
                        length = len(tmp)
                        a = tmp[2:(length - 3)]
                        self.user_id = a
                        query = "SELECT password, confirmed FROM people WHERE login='{}'".format(login)
                        self.cursor.execute(query)
                        result = self.cursor.fetchall()
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
                            self.cnn.close()
                            self.hide()
                            self.switch_passed.emit()
                        else:
                            self.pmsg = QMessageBox(self)
                            self.pmsg.critical(self, "Ошибка ", "Ваша учетная запись не подтверждена. Попробуйте авторизоваться позже.", QMessageBox.Ok)
        except mysql.connector.Error as e:
            if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with username or password")
            elif e.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database doesn't exist")
            else:
                print(e)
            self.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = ThisWindow()
    myapp.show()
    sys.exit(app.exec_())
