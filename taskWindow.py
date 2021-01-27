import sys, os
from ftplib import FTP
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QApplication, QPushButton, QComboBox)
from PyQt5 import QtCore, QtGui


class ThisWindow(QWidget):

    switch_t_mch = QtCore.pyqtSignal()
    switch_t_o = QtCore.pyqtSignal()
    switch_t_m = QtCore.pyqtSignal()
    switch_i_mch = QtCore.pyqtSignal()
    switch_i_o = QtCore.pyqtSignal()
    switch_i_m = QtCore.pyqtSignal()
    switch_a_mch = QtCore.pyqtSignal()
    switch_a_o = QtCore.pyqtSignal()
    switch_a_m = QtCore.pyqtSignal()

    def __init__(self, n, testname):
        super().__init__()
        self.n = n
        self.testname = testname
        self.initUI()


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
        self.qnum = QLabel("Вопрос #%s" % self.n, self)
        self.qnum.setFont(QtGui.QFont("Century Gothic", 15, QtGui.QFont.Bold))
        self.qnum.adjustSize()
        self.qtype = QLabel("Выберите тип вопроса:", self)
        self.qtype.setFont(QtGui.QFont("Century Gothic", 15, QtGui.QFont.Bold))
        self.qtype.adjustSize()
        self.qbox = QComboBox(self)
        self.qbox.addItems(["Текст", "Изображение", "Аудио"])
        self.qbox.setFixedSize(100, 25)
        self.atype = QLabel("Выберите тип ответа:", self)
        self.atype.setFont(QtGui.QFont("Century Gothic", 15, QtGui.QFont.Bold))
        self.atype.adjustSize()
        self.abox = QComboBox(self)
        self.abox.addItems(["Установить соответствие", "Выбрать один правильный ответ", "Выбрать несколько правильных ответов"])
        self.abox.setFixedSize(300, 25)
        self.btn = QPushButton('OK', self)
        self.box.addStretch(1)
        self.box.addWidget(self.qnum, alignment=QtCore.Qt.AlignCenter)
        self.box.addWidget(self.qtype, alignment=QtCore.Qt.AlignCenter)
        self.box.addWidget(self.qbox, alignment=QtCore.Qt.AlignCenter)
        self.box.addStretch(1)
        self.box.addWidget(self.atype, alignment=QtCore.Qt.AlignCenter)
        self.box.addWidget(self.abox, alignment=QtCore.Qt.AlignCenter)
        self.box.addStretch(1)
        self.box.addWidget(self.btn, alignment=QtCore.Qt.AlignCenter)
        self.box.addStretch(2)
        self.setLayout(self.box)

        self.btn.clicked.connect(self.WriteToFile)


    def WriteToFile(self):
        self.qtype = self.qbox.currentText()
        self.atype = self.abox.currentText()
        with open(self.testname, 'a', encoding='utf-8') as file:
            file.write('Вопрос #%s\n' % self.n)
            file.write('Тип вопроса:' + self.qtype + '\n')
            file.write('Тип ответа:' + self.atype + '\n')

        if self.qtype == 'Текст' and self.atype == 'Установить соответствие':
            self.switch_t_mch.emit()
        elif self.qtype == 'Текст' and self.atype == 'Выбрать один правильный ответ':
            self.switch_t_o.emit()
        elif self.qtype == 'Текст' and self.atype == 'Выбрать несколько правильных ответов':
            self.switch_t_m.emit()
        elif self.qtype == 'Изображение' and self.atype == 'Установить соответствие':
            self.switch_i_mch.emit()
        elif self.qtype == 'Изображение' and self.atype == 'Выбрать один правильный ответ':
            self.switch_i_o.emit()
        elif self.qtype == 'Изображение' and self.atype == 'Выбрать несколько правильных ответов':
            self.switch_i_m.emit()
        elif self.qtype == 'Аудио' and self.atype == 'Установить соответствие':
            self.switch_a_mch.emit()
        elif self.qtype == 'Аудио' and self.atype == 'Выбрать один правильный ответ':
            self.switch_a_o.emit()
        elif self.qtype == 'Аудио' and self.atype == 'Выбрать несколько правильных ответов':
            self.switch_a_m.emit()


if __name__=="__main__":
    app = QApplication(sys.argv)
    myapp = ThisWindow(2, 'files/Test1.txt')
    myapp.show()
    sys.exit(app.exec_())

