import sys
import os
import re
from ftplib import FTP
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QApplication, QTextEdit, QPushButton, QMessageBox,
                             QFileDialog)
from PyQt5 import QtCore, QtGui


class ThisWindow(QWidget):

    switch_imch = QtCore.pyqtSignal()

    def __init__(self, n, i, filename):
        super().__init__()
        self.n = i
        self.filename = filename
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
        self.qnum = QLabel("Вопрос #%s" % self.n, self)
        self.qnum.setFont(QtGui.QFont("Century Gothic", 15, QtGui.QFont.Bold))
        self.qnum.adjustSize()
        self.imgt = QLabel("Выберите изображение в формате jpg или png:", self)
        self.imgt.setFont(QtGui.QFont("Century Gothic", 15))
        self.imgt.adjustSize()
        self.img = QTextEdit(self)
        self.img.setFixedSize(500, 30)
        self.imgb = QPushButton('Открыть файл', self)
        self.qtext = QLabel("Укажите текст вопроса:", self)
        self.qtext.setFont(QtGui.QFont("Century Gothic", 15))
        self.qtext.adjustSize()
        self.utext = QTextEdit(self)
        self.utext.setFixedSize(500, 50)

        # new type
        self.message = QLabel(
            "Соответствий максимально может быть 5. Если вам нужно меньше, оставьте лишние поля пустыми.",
            self)
        self.message.setFont(QtGui.QFont("Century Gothic", 9))
        self.message.adjustSize()
        self.message.setFixedSize(700, 75)
        self.maxscoretext = QLabel("Укажите максимальное количество баллов за данное задание:")
        self.maxscoretext.setFont(QtGui.QFont("Century Gothic", 11))
        self.maxscoretext.adjustSize()
        self.maxsc = QLineEdit(self)
        self.maxsc.setFixedSize(25, 25)
        self.var1box = QHBoxLayout(self)
        self.var1t = QLabel("Введите первое соответствие:", self)
        self.var1t.setFont(QtGui.QFont("Century Gothic", 11))
        self.var1t.adjustSize()
        self.var1f = QLineEdit(self)
        self.var1s = QLineEdit(self)
        self.var1f.setFixedSize(250, 25)
        self.var1s.setFixedSize(250, 25)
        self.var2box = QHBoxLayout(self)
        self.var2t = QLabel("Введите второе соответствие:", self)
        self.var2t.setFont(QtGui.QFont("Century Gothic", 11))
        self.var2t.adjustSize()
        self.var2f = QLineEdit(self)
        self.var2s = QLineEdit(self)
        self.var2f.setFixedSize(250, 25)
        self.var2s.setFixedSize(250, 25)
        self.var3box = QHBoxLayout(self)
        self.var3t = QLabel("Введите третье соответствие:", self)
        self.var3t.setFont(QtGui.QFont("Century Gothic", 11))
        self.var3t.adjustSize()
        self.var3f = QLineEdit(self)
        self.var3s = QLineEdit(self)
        self.var3f.setFixedSize(250, 25)
        self.var3s.setFixedSize(250, 25)
        self.var4box = QHBoxLayout(self)
        self.var4t = QLabel("Введите четвертое соответствие:", self)
        self.var4t.setFont(QtGui.QFont("Century Gothic", 11))
        self.var4t.adjustSize()
        self.var4f = QLineEdit(self)
        self.var4s = QLineEdit(self)
        self.var4f.setFixedSize(250, 25)
        self.var4s.setFixedSize(250, 25)
        self.var5box = QHBoxLayout(self)
        self.var5t = QLabel("Введите пятое соответствие:", self)
        self.var5t.setFont(QtGui.QFont("Century Gothic", 11))
        self.var5t.adjustSize()
        self.var5f = QLineEdit(self)
        self.var5s = QLineEdit(self)
        self.var5f.setFixedSize(250, 25)
        self.var5s.setFixedSize(250, 25)

        self.btn = QPushButton('OK', self)
        self.box.addStretch(1)
        self.box.addWidget(self.qnum, alignment=QtCore.Qt.AlignCenter)
        self.box.addStretch(1)
        self.box.addWidget(self.imgt, alignment=QtCore.Qt.AlignCenter)
        self.box.addSpacing(5)
        self.box.addWidget(self.img, alignment=QtCore.Qt.AlignCenter)
        self.box.addSpacing(5)
        self.box.addWidget(self.imgb, alignment=QtCore.Qt.AlignCenter)
        self.box.addStretch(1)
        self.box.addWidget(self.qtext, alignment=QtCore.Qt.AlignCenter)
        self.box.addSpacing(5)
        self.box.addWidget(self.utext, alignment=QtCore.Qt.AlignCenter)
        self.box.addSpacing(50)

        self.var1box.addWidget(self.var1t, alignment=QtCore.Qt.AlignRight)
        self.var1box.addSpacing(10)
        self.var1box.addWidget(self.var1f, alignment=QtCore.Qt.AlignLeft)
        self.var1box.addSpacing(10)
        self.var1box.addWidget(self.var1s, alignment=QtCore.Qt.AlignLeft)
        self.box.addLayout(self.var1box)

        self.var2box.addWidget(self.var2t, alignment=QtCore.Qt.AlignRight)
        self.var2box.addSpacing(10)
        self.var2box.addWidget(self.var2f, alignment=QtCore.Qt.AlignLeft)
        self.var2box.addSpacing(10)
        self.var2box.addWidget(self.var2s, alignment=QtCore.Qt.AlignLeft)
        self.box.addLayout(self.var2box)

        self.var3box.addWidget(self.var3t, alignment=QtCore.Qt.AlignRight)
        self.var3box.addSpacing(10)
        self.var3box.addWidget(self.var3f, alignment=QtCore.Qt.AlignLeft)
        self.var3box.addSpacing(10)
        self.var3box.addWidget(self.var3s, alignment=QtCore.Qt.AlignLeft)
        self.box.addLayout(self.var3box)

        self.var4box.addWidget(self.var4t, alignment=QtCore.Qt.AlignRight)
        self.var4box.addSpacing(7)
        self.var4box.addWidget(self.var4f, alignment=QtCore.Qt.AlignLeft)
        self.var4box.addSpacing(10)
        self.var4box.addWidget(self.var4s, alignment=QtCore.Qt.AlignLeft)
        self.box.addLayout(self.var4box)

        self.var5box.addWidget(self.var5t, alignment=QtCore.Qt.AlignRight)
        self.var5box.addSpacing(10)
        self.var5box.addWidget(self.var5f, alignment=QtCore.Qt.AlignLeft)
        self.var5box.addSpacing(10)
        self.var5box.addWidget(self.var5s, alignment=QtCore.Qt.AlignLeft)
        self.box.addLayout(self.var5box)
        self.box.addWidget(self.message, alignment=QtCore.Qt.AlignCenter)
        scorebox = QHBoxLayout()
        scorebox.addStretch(1)
        scorebox.addWidget(self.maxscoretext, alignment=QtCore.Qt.AlignRight)
        scorebox.addSpacing(20)
        scorebox.addWidget(self.maxsc, alignment=QtCore.Qt.AlignLeft)
        scorebox.addStretch(1)
        self.box.addLayout(scorebox)
        self.box.addSpacing(20)
        self.box.addWidget(self.btn, alignment=QtCore.Qt.AlignCenter)
        self.box.addStretch(2)
        self.setLayout(self.box)

        self.imgb.clicked.connect(self.showDialog)
        self.btn.clicked.connect(self.WriteToFile)

    def WriteToFile(self):
        utext = self.utext.toPlainText()
        utext = utext.strip()
        var1f = self.var1f.text()
        var1f = var1f.strip()
        var1s = self.var1s.text()
        var1s = var1s.strip()
        var2f = self.var2f.text()
        var2f = var2f.strip()
        var2s = self.var2s.text()
        var2s = var2s.strip()
        var3f = self.var3f.text()
        var3f = var3f.strip()
        var3s = self.var3s.text()
        var3s = var3s.strip()
        var4f = self.var4f.text()
        var4f = var4f.strip()
        var4s = self.var4s.text()
        var4s = var4s.strip()
        var5f = self.var5f.text()
        var5f = var5f.strip()
        var5s = self.var5s.text()
        var5s = var5s.strip()
        self.maxscore = self.maxsc.text()
        self.maxscore = self.maxscore.strip()

        try:
            ftp = FTP()
            ftp.set_debuglevel(2)
            ftp.connect('stacey789.beget.tech', 21)
            ftp.login('stacey789_ftp', 'StudyLang456987')
            ftp.encoding = 'utf-8'
            ftp.cwd('/img')
            ftp.size(self.newfile)
            exist = 1
        except Exception:
            exist = 0
        if exist == 0 and utext != '' and self.maxscore != '':
            if self.flag == 1:
                self.msgexists = QMessageBox(self)
                self.msgexists.critical(self, "Ошибка ",
                                        "Нажмите кнопку 'Открыть файл' и переименуйте ваш файл, нажав на правую кнопку мыши.",
                                        QMessageBox.Ok)
            else:
                try:
                    fp = open(self.distribution, 'rb')
                    send = ftp.storbinary('STOR %s' % self.fname + '.' + self.format, fp, 1024)
                    fp.close()
                except Exception:
                    self.msgnofile = QMessageBox(self)
                    self.msgnofile.critical(self, "Ошибка ", "Не удалось загрузить ваш файл.", QMessageBox.Ok)
                if 'send' in locals():
                    with open(self.filename, 'a', encoding='utf-8') as file:
                        file.write('Вопрос:' + utext + '\n')
                        file.write('Имя файла:' + self.fname + '.' + self.format + '\n')
                        file.write('Соответствие1:' + var1f + ';' + var1s + '\n')
                        file.write('Соответствие2:' + var2f + ';' + var2s + '\n')
                        if var3f != '' or var3s != '':
                            file.write('Соответствие3:' + var3f + ';' + var3s + '\n')
                        if var4f != '' or var4s != '':
                            file.write('Соответствие4:' + var4f + ';' + var4s + '\n')
                        if var5f != '' or var5s != '':
                            file.write('Соответствие5:' + var5f + ';' + var5s + '\n')
                        file.write('Максимальный балл:' + self.maxscore + '\n')
                        file.write('\n')
                    self.hide()
                    self.switch_imch.emit()
        elif utext == '':
            self.msgnum = QMessageBox(self)
            self.msgnum.critical(self, "Ошибка ", "Пожалуйста, укажите ваш вопрос.", QMessageBox.Ok)
        elif self.maxscore == '':
            self.msgnum = QMessageBox(self)
            self.msgnum.critical(self, "Ошибка ", "Пожалуйста, введите максимальное количество баллов за задание.", QMessageBox.Ok)
        elif var1f == '' or var1s == '':
            self.msgv1 = QMessageBox(self)
            self.msgv1.critical(self, "Ошибка ", "Пожалуйста, укажите первое соответствие.", QMessageBox.Ok)
        elif var2f == '' or var2s == '':
            self.msgv2 = QMessageBox(self)
            self.msgv2.critical(self, "Ошибка ", "Пожалуйста, укажите второе соответствие.", QMessageBox.Ok)
        else:
            self.msgnofile = QMessageBox(self)
            self.msgnofile.critical(self, "Ошибка ", "Файл с таким имененем уже существует. Переименуйте ваш файл и откройте его заново.", QMessageBox.Ok)


    def showDialog(self):

        self.distribution = QFileDialog.getOpenFileName(self, 'Open file', '/home', "source File (*.jpg *.png)")[0]
        self.basename = os.path.basename(self.distribution)
        self.img.setText(self.distribution)
        getformat = re.search(r'(?<=\.)\w+', self.distribution)
        self.format = getformat.group()
        getfname = re.search(r'(?<=\/|\\)[ ,?!_():;+#$%&*@\-\+\'\’\w]+(?=\.)', self.distribution)
        self.fname = getfname.group()
        self.flag = 0
        if self.format == 'jpg':
            self.newfile = '{}.jpg'.format(self.fname)
        elif self.format == 'png':
            self.newfile = '{}.png'.format(self.fname)
        else:
            self.msgformat = QMessageBox(self)
            self.msgformat.critical(self, "Ошибка ", "Пожалуйста, выберите другой файл соответствующий форматам jpg или png.", QMessageBox.Ok)
        try:
            ftp = FTP()
            ftp.set_debuglevel(2)
            ftp.connect('stacey789.beget.tech', 21)
            ftp.login('stacey789_ftp', 'StudyLang456987')
            ftp.encoding = 'utf-8'
            ftp.cwd('/img')
            ftp.size(self.newfile)
            exist = 1
        except Exception:
            exist = 0
        if exist == 1:
            self.msgname = QMessageBox(self)
            self.msgname.critical(self, "Ошибка ",
                                  "Файл с таким имененем уже существует. Переименуйте ваш файл и откройте его заново",
                                  QMessageBox.Ok)
            self.flag = 1


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = ThisWindow(2, 2, 'files/Test15.txt')
    myapp.show()
    sys.exit(app.exec_())