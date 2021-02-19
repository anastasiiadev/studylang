from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox
from PyQt5 import QtGui, QtCore

import dbinteraction as db
import files


class AMatch(QWidget):

    switch_task_end = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.box = QVBoxLayout(self)
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
        self.scorebox = QHBoxLayout()
        self.scorebox.addStretch(1)
        self.scorebox.addWidget(self.maxscoretext, alignment=QtCore.Qt.AlignRight)
        self.scorebox.addSpacing(20)
        self.scorebox.addWidget(self.maxsc, alignment=QtCore.Qt.AlignLeft)
        self.scorebox.addStretch(1)
        self.box.addLayout(self.scorebox)
        self.box.addSpacing(20)
        self.box.addWidget(self.btn, alignment=QtCore.Qt.AlignCenter)
        self.box.addStretch(2)
        self.setLayout(self.box)

    def WriteToFile(self, userquestion, testfilename, distribution=None, mediafile=None):
        utext = userquestion.strip()
        var1f = self.var1f.text().strip()
        var1s = self.var1s.text().strip()
        var2f = self.var2f.text().strip()
        var2s = self.var2s.text().strip()
        var3f = self.var3f.text().strip()
        var3s = self.var3s.text().strip()
        var4f = self.var4f.text().strip()
        var4s = self.var4s.text().strip()
        var5f = self.var5f.text().strip()
        var5s = self.var5s.text().strip()
        self.maxscore = self.maxsc.text().strip()

        if mediafile is not None:
            if mediafile.split('.')[-1] in ('mp3', 'MP3', 'wav', 'WAV'):
                filetype = 'audio'
                table = 'audios'
            else:
                filetype = 'img'
                table = 'images'
            try:
                conn = db.create_connection()
                samefile = db.execute_query(conn, f"SELECT * FROM {table} WHERE filename='{mediafile}'")
            except Exception:
                samefile = []
            if samefile:
                self.msgnofile = QMessageBox(self)
                self.msgnofile.critical(self, "Ошибка ",
                                        "Файл с таким имененем уже существует. Переименуйте ваш файл и откройте его заново.",
                                        QMessageBox.Ok)
                permission = 'no'
            else:
                permission = 'yes'
        else:
            permission = 'yes'

        if permission == 'yes':
            if utext == '':
                self.msgnum = QMessageBox(self)
                self.msgnum.critical(self, "Ошибка ", "Пожалуйста, укажите ваш вопрос.", QMessageBox.Ok)
            elif self.maxscore == '':
                self.msgnum = QMessageBox(self)
                self.msgnum.critical(self, "Ошибка ",
                                     "Пожалуйста, введите максимальное количество баллов за задание.",
                                     QMessageBox.Ok)
            elif var1f == '' or var1s == '':
                self.msgv1 = QMessageBox(self)
                self.msgv1.critical(self, "Ошибка ", "Пожалуйста, укажите первый вариант ответа.", QMessageBox.Ok)
            elif var2f == '' or var2s == '':
                self.msgv2 = QMessageBox(self)
                self.msgv2.critical(self, "Ошибка ", "Пожалуйста, укажите второй вариант ответа.", QMessageBox.Ok)
            else:
                with open(testfilename, 'a', encoding='utf-8') as file:
                    if mediafile is not None:
                        try:
                            f = files.File()
                            fileid = f.post(mediafile, distribution, filetype)
                            whichid = db.execute_query(conn, f"SELECT max(id) FROM {table}")
                            max = whichid[0][0]
                            if max == None:
                                id = 1
                            else:
                                id = int(max) + 1
                            query = (f"INSERT INTO {table} (id, filename, fileid) "
                                     f"VALUES ({id}, '{mediafile}', '{fileid}')")
                            db.execute_query(conn, query, 'insert')
                        except Exception:
                            self.msgnofile = QMessageBox(self)
                            self.msgnofile.critical(self, "Ошибка ", "Не удалось загрузить ваш файл.",
                                                    QMessageBox.Ok)
                    file.write('Вопрос:' + utext + '\n')
                    if mediafile is not None:
                        file.write('Имя файла:' + mediafile + '\n')
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
                self.switch_task_end.emit()
