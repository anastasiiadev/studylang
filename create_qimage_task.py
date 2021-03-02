from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLabel, QPushButton, QFileDialog, QMessageBox
from PyQt5 import QtGui, QtCore
import os
import re

class QImage(QWidget):

    """
    Виджет, реализующий часть окна создания задания типа "Изображение".
    Пользователю необходимо открыть диалоговое окно (объект класса QFileDialog)
        и выбрать файл, а также ввести текст вопроса.
    """

    def __init__(self, i):

        """
        :param i: номер задания
        """

        super().__init__()
        self.box = QVBoxLayout(self)
        self.box.setContentsMargins(0, 30, 0, 30)
        self.qnum = QLabel(f"Вопрос #{i}", self)
        self.qnum.setFont(QtGui.QFont("Century Gothic", 15, QtGui.QFont.Bold))
        self.qnum.adjustSize()
        self.imgt = QLabel("Выберите изображение в формате jpg или png(не превышающий 10 Mb):", self)
        self.imgt.setFont(QtGui.QFont("Century Gothic", 15))
        self.imgt.adjustSize()
        self.img = QTextEdit(self)
        self.img.setFixedSize(500, 25)
        self.imgb = QPushButton('Открыть файл', self)
        self.qtext = QLabel("Укажите текст вопроса:", self)
        self.qtext.setFont(QtGui.QFont("Century Gothic", 15))
        self.qtext.adjustSize()
        self.utext = QTextEdit(self)
        self.utext.setFixedSize(500, 50)

        self.box.addStretch(1)
        self.box.addWidget(self.qnum, alignment=QtCore.Qt.AlignCenter)
        self.box.addSpacing(10)
        self.box.addWidget(self.imgt, alignment=QtCore.Qt.AlignCenter)
        self.box.addSpacing(5)
        self.box.addWidget(self.img, alignment=QtCore.Qt.AlignCenter)
        self.box.addSpacing(5)
        self.box.addWidget(self.imgb, alignment=QtCore.Qt.AlignCenter)
        self.box.addSpacing(20)
        self.box.addWidget(self.qtext, alignment=QtCore.Qt.AlignCenter)
        self.box.addSpacing(5)
        self.box.addWidget(self.utext, alignment=QtCore.Qt.AlignCenter)
        self.box.addSpacing(30)
        self.setLayout(self.box)


    def showDialog(self):

        """
        Атрибут self.distribution - путь до файла формата jpg или png.
        Выполняется проверка формата файла.
        В атрибут self.newfile сохраняется имя файла изображения.
        """

        self.distribution = QFileDialog.getOpenFileName(self, 'Open file', '/home', "source File (*.jpg *.png)")[0]
        self.basename = os.path.basename(self.distribution)
        self.img.setText(self.distribution)
        getformat = re.search(r'(?<=\.)\w+', self.distribution)
        self.format = getformat.group()
        getfname = re.search(r'(?<=\/|\\)[ ,?!_()\]\[:;+#$%&*@\.\-\+\'\’\w]+(?=\.(jpg|png|JPG|PNG))', self.distribution)
        self.fname = getfname.group()
        if self.format == 'jpg':
            self.newfile = f'{self.fname}.jpg'
        elif self.format == 'png':
            self.newfile = f'{self.fname}.png'
        else:
            self.msgformat = QMessageBox(self)
            self.msgformat.critical(self, "Ошибка ",
                                    "Пожалуйста, выберите другой файл соответствующий форматам jpg или png.",
                                    QMessageBox.Ok)
