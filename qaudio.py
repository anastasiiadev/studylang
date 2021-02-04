from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLabel, QPushButton, QFileDialog, QMessageBox
from PyQt5 import QtGui, QtCore
import os
import re
import dbinteraction as db


class QAudio(QWidget):

    def __init__(self, i):
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
        self.distribution = QFileDialog.getOpenFileName(self, 'Open file', '/home', "source File (*.mp3 *.wav)")[0]
        self.basename = os.path.basename(self.distribution)
        self.audio.setText(self.distribution)
        getformat = re.search(r'(?<=\.)\w+', self.distribution)
        self.format = getformat.group().lower()
        getfname = re.search(r'(?<=\/|\\)[ ,?!_()\]\[:;+#$%&*@\.\-\+\'\’\w]+(?=\.(mp3|wav|MP3|WAV))', self.distribution)
        self.fname = getfname.group()
        if self.format == 'mp3':
            self.newfile = '{}.mp3'.format(self.fname)
        elif self.format == 'wav':
            self.newfile = '{}.wav'.format(self.fname)
        else:
            self.msgformat = QMessageBox(self)
            self.msgformat.critical(self, "Ошибка ",
                                    "Пожалуйста, выберите другой файл соответствующий форматам mp3 или wav.",
                                    QMessageBox.Ok)
