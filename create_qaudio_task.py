from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLabel, QPushButton, QFileDialog, QMessageBox
from PyQt5 import QtGui, QtCore
import os
import re


class QAudio(QWidget):

    """
    Виджет, реализующий часть окна создания задания типа "Аудио".
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
        self.qnum = QLabel("Вопрос #%s" % i, self)
        self.qnum.setFont(QtGui.QFont("Century Gothic", 15, QtGui.QFont.Bold))
        self.qnum.adjustSize()
        self.audiot = QLabel("Выберите аудиофайл в формате mp3 или wav(не превышающий 10 Mb):", self)
        self.audiot.setFont(QtGui.QFont("Century Gothic", 15))
        self.audiot.adjustSize()
        self.audio = QTextEdit(self)
        self.audio.setFixedSize(500, 25)
        self.audiob = QPushButton('Открыть файл', self)
        self.qtext = QLabel("Укажите текст вопроса:", self)
        self.qtext.setFont(QtGui.QFont("Century Gothic", 15))
        self.qtext.adjustSize()
        self.utext = QTextEdit(self)
        self.utext.setFixedSize(500, 50)

        self.box.addStretch(1)
        self.box.addWidget(self.qnum, alignment=QtCore.Qt.AlignCenter)
        self.box.addSpacing(10)
        self.box.addWidget(self.audiot, alignment=QtCore.Qt.AlignCenter)
        self.box.addSpacing(5)
        self.box.addWidget(self.audio, alignment=QtCore.Qt.AlignCenter)
        self.box.addSpacing(5)
        self.box.addWidget(self.audiob, alignment=QtCore.Qt.AlignCenter)
        self.box.addSpacing(20)
        self.box.addWidget(self.qtext, alignment=QtCore.Qt.AlignCenter)
        self.box.addSpacing(5)
        self.box.addWidget(self.utext, alignment=QtCore.Qt.AlignCenter)
        self.box.addSpacing(30)
        self.setLayout(self.box)

    def showDialog(self):

        """
        Атрибут self.distribution - путь до файла формата mp3 или wav.
        Выполняется проверка формата файла.
        В атрибут self.newfile сохраняется имя аудиофайла.
        """

        self.distribution = QFileDialog.getOpenFileName(self, 'Open file', '/home', "source File (*.mp3 *.wav)")[0]
        self.basename = os.path.basename(self.distribution)
        self.audio.setText(self.distribution)
        getformat = re.search(r'(?<=\.)\w+', self.distribution)
        self.format = getformat.group().lower()
        getfname = re.search(r'(?<=\/|\\)[ ,?!_()\]\[:;+#$%&*@\.\-\+\'\’\w]+(?=\.(mp3|wav|MP3|WAV))', self.distribution)
        self.fname = getfname.group()
        if self.format == 'mp3':
            self.newfile = f'{self.fname}.mp3'
        elif self.format == 'wav':
            self.newfile = f'{self.fname}.wav'
        else:
            self.msgformat = QMessageBox(self)
            self.msgformat.critical(self, "Ошибка ",
                                    "Пожалуйста, выберите другой файл соответствующий форматам mp3 или wav.",
                                    QMessageBox.Ok)
