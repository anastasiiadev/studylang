from PyQt5.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QHBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox
from PyQt5 import QtGui, QtCore
import dbinteraction as db
import files


class AMany(QWidget):

    def __init__(self):
        super().__init__()
        self.generalbox = QVBoxLayout(self)
        self.variants = QHBoxLayout(self)
        self.texts = QVBoxLayout(self)
        self.input = QVBoxLayout(self)
        self.checkboxes = QVBoxLayout(self)
        self.var1t = QLabel("Введите первый вариант ответа:", self)
        self.var1t.setFont(QtGui.QFont("Century Gothic", 12))
        self.var1t.adjustSize()
        self.var1 = QLineEdit(self)
        self.var1.setFixedSize(350, 25)
        self.ch1 = QCheckBox()
        self.var2t = QLabel("Введите второй вариант ответа:", self)
        self.var2t.setFont(QtGui.QFont("Century Gothic", 12))
        self.var2t.adjustSize()
        self.var2 = QLineEdit(self)
        self.var2.setFixedSize(350, 25)
        self.ch2 = QCheckBox()
        self.var3t = QLabel("Введите третий вариант ответа:", self)
        self.var3t.setFont(QtGui.QFont("Century Gothic", 12))
        self.var3t.adjustSize()
        self.var3 = QLineEdit(self)
        self.var3.setFixedSize(350, 25)
        self.ch3 = QCheckBox()
        self.var4t = QLabel("Введите четвертый вариант ответа:", self)
        self.var4t.setFont(QtGui.QFont("Century Gothic", 12))
        self.var4t.adjustSize()
        self.var4 = QLineEdit(self)
        self.var4.setFixedSize(350, 25)
        self.ch4 = QCheckBox()
        self.var5t = QLabel("Введите пятый вариант ответа:", self)
        self.var5t.setFont(QtGui.QFont("Century Gothic", 12))
        self.var5t.adjustSize()
        self.var5 = QLineEdit(self)
        self.var5.setFixedSize(350, 25)
        self.ch5 = QCheckBox()

        self.texts.addWidget(self.var1t, alignment=QtCore.Qt.AlignRight)
        self.texts.addWidget(self.var2t, alignment=QtCore.Qt.AlignRight)
        self.texts.addWidget(self.var3t, alignment=QtCore.Qt.AlignRight)
        self.texts.addWidget(self.var4t, alignment=QtCore.Qt.AlignRight)
        self.texts.addWidget(self.var5t, alignment=QtCore.Qt.AlignRight)

        self.input.addWidget(self.var1)
        self.input.addSpacing(2)
        self.input.addWidget(self.var2)
        self.input.addSpacing(2)
        self.input.addWidget(self.var3)
        self.input.addSpacing(2)
        self.input.addWidget(self.var4)
        self.input.addSpacing(2)
        self.input.addWidget(self.var5)

        self.checkboxes.addSpacing(6)
        self.checkboxes.addWidget(self.ch1)
        self.checkboxes.addSpacing(9)
        self.checkboxes.addWidget(self.ch2)
        self.checkboxes.addSpacing(9)
        self.checkboxes.addWidget(self.ch3)
        self.checkboxes.addSpacing(9)
        self.checkboxes.addWidget(self.ch4)
        self.checkboxes.addSpacing(9)
        self.checkboxes.addWidget(self.ch5)

        self.variants.addSpacing(20)
        self.variants.addLayout(self.texts)
        self.variants.addLayout(self.input)
        self.variants.addLayout(self.checkboxes)
        self.variants.addSpacing(20)

        self.message = QLabel(
            "Вариантов ответа максимально может быть 5. Если вам нужно меньше, оставьте соответствующие поля пустыми.",
            self)
        self.message.setFont(QtGui.QFont("Century Gothic", 9))
        self.message.adjustSize()
        self.message.setFixedSize(700, 20)
        self.message2 = QLabel("Поставьте галочку ✔ напротив правильных ответов.", self)
        self.message2.setFont(QtGui.QFont("Century Gothic", 9))
        self.message2.adjustSize()
        self.message2.setFixedSize(700, 20)
        self.maxscoretext = QLabel("Укажите максимальное количество баллов за данное задание:")
        self.maxscoretext.setFont(QtGui.QFont("Century Gothic", 11))
        self.maxscoretext.adjustSize()
        self.maxsc = QLineEdit(self)
        self.maxsc.setFixedSize(25, 25)
        self.messagebox = QVBoxLayout(self)
        self.messagebox.addWidget(self.message, alignment=QtCore.Qt.AlignCenter)
        self.messagebox.addWidget(self.message2, alignment=QtCore.Qt.AlignCenter)
        self.scorebox = QHBoxLayout(self)
        self.scorebox.addStretch(1)
        self.scorebox.addWidget(self.maxscoretext, alignment=QtCore.Qt.AlignRight)
        self.scorebox.addSpacing(20)
        self.scorebox.addWidget(self.maxsc, alignment=QtCore.Qt.AlignLeft)
        self.scorebox.addStretch(1)
        self.messagebox.addLayout(self.scorebox)

        self.generalbox.addLayout(self.variants)
        self.generalbox.addStretch(1)
        self.generalbox.addLayout(self.messagebox)
        self.btn = QPushButton('OK', self)
        self.btn.setFixedSize(100, 25)
        self.generalbox.addWidget(self.btn, alignment=QtCore.Qt.AlignCenter)
        self.setLayout(self.generalbox)

    def WriteToFile(self, userquestion, testfilename, distribution, mediafile=None):
        utext = userquestion.strip()
        var1 = self.var1.text()
        var1 = var1.strip()
        var2 = self.var2.text()
        var2 = var2.strip()
        var3 = self.var3.text()
        var3 = var3.strip()
        var4 = self.var4.text()
        var4 = var4.strip()
        var5 = self.var5.text()
        var5 = var5.strip()
        self.maxscore = self.maxsc.text()
        self.maxscore = self.maxscore.strip()

        # проверка, что кнопка нажата
        numch = 0
        answer = []
        if self.ch1.isChecked() is True:
            numch += 1
            answer.append(var1)
        if self.ch2.isChecked() is True:
            numch += 1
            answer.append(var2)
        if self.ch3.isChecked() is True:
            numch += 1
            answer.append(var3)
        if self.ch4.isChecked() is True:
            numch += 1
            answer.append(var4)
        if self.ch5.isChecked() is True:
            numch += 1
            answer.append(var5)
        if numch == 0:
            self.msgv1 = QMessageBox(self)
            self.msgv1.critical(self, "Ошибка ", "Пожалуйста, укажите правильные ответы, отметив их галочкой.",
                                QMessageBox.Ok)
        elif numch == 1:
            self.msgv1 = QMessageBox(self)
            self.msgv1.critical(self, "Ошибка ", "Пожалуйста, укажите более одного правильного ответа.", QMessageBox.Ok)
        else:
            a = ', '
            a = a.join(answer)
            if mediafile is not None:
                try:
                    conn = db.create_connection()
                    samefile = db.execute_query(conn, "SELECT * FROM audios WHERE filename='{}'".format(mediafile))
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
                elif var1 == '':
                    self.msgv1 = QMessageBox(self)
                    self.msgv1.critical(self, "Ошибка ", "Пожалуйста, укажите первый вариант ответа.", QMessageBox.Ok)
                elif var2 == '':
                    self.msgv2 = QMessageBox(self)
                    self.msgv2.critical(self, "Ошибка ", "Пожалуйста, укажите второй вариант ответа.", QMessageBox.Ok)
                else:
                    with open(testfilename, 'a', encoding='utf-8') as file:
                        if mediafile is not None:
                            try:
                                f = files.File()
                                fileid = f.post(mediafile, distribution, 'audio')
                                whichid = db.execute_query(conn, "SELECT max(id) FROM audios")
                                max = whichid[0][0]
                                if max == None:
                                    n = 1
                                else:
                                    n = int(max) + 1
                                query = ("INSERT INTO audios (id, filename, fileid) "
                                         "VALUES ({}, '{}', '{}')".format(n, mediafile, fileid))
                                db.execute_query(conn, query, 'insert')
                            except Exception:
                                self.msgnofile = QMessageBox(self)
                                self.msgnofile.critical(self, "Ошибка ", "Не удалось загрузить ваш файл.",
                                                        QMessageBox.Ok)
                        file.write('Вопрос:' + utext + '\n')
                        if mediafile is not None:
                            file.write('Имя файла:' + mediafile + '\n')
                        file.write('Вариант1:' + var1 + '\n')
                        file.write('Вариант2:' + var2 + '\n')
                        if var3 != '':
                            file.write('Вариант3:' + var3 + '\n')
                        if var4 != '':
                            file.write('Вариант4:' + var4 + '\n')
                        if var5 != '':
                            file.write('Вариант5:' + var5 + '\n')
                        file.write('Правильные ответы:' + a + '\n')
                        file.write('Максимальный балл:' + self.maxscore + '\n')
                        file.write('\n')
                    self.hide()
                    self.switch_tm.emit()
