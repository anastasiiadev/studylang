import sys
import random
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QApplication, QPushButton, QMessageBox, QCheckBox
from PyQt5 import QtGui, QtCore

import general_settings as gs


class DragLabel(QLabel):
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
        else:
            drag = QDrag(self)

            mimedata = QMimeData()
            mimedata.setText(self.text())

            drag.setMimeData(mimedata)

            # creating the dragging effect
            pixmap = QPixmap(self.size())  # label size

            painter = QPainter(pixmap)
            painter.drawPixmap(self.rect(), self.grab())
            painter.end()

            drag.setPixmap(pixmap)
            drag.setHotSpot(event.pos())
            drag.exec_(Qt.CopyAction | Qt.MoveAction)

class DropLabel(QLabel):
    def __init__(self, label, parent):
        super().__init__(label, parent)

        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        pos = event.pos()
        text = event.mimeData().text()
        self.setText(text)
        self.setFont(QtGui.QFont("Century Gothic", 11, QtGui.QFont.Bold))
        event.acceptProposedAction()


class ThisWindow(gs.SLWindow):

    window_initialising = QtCore.pyqtSignal()

    def __init__(self, i, filename, d, maxscore):
        super().__init__()
        self.n = i
        self.filename = filename
        self.dict = d
        self.rightanswers = ''
        self.maxscore = int(maxscore)
        self.score = 0
        self.initUI()


    def initUI(self):
        # new type
        self.values = []
        for v in self.dict.values():
            self.values.append(v)
        random.shuffle(self.values)
        i = 1
        for el in self.values:
            exec(f'self.lbl_to_drag{i} = DragLabel(el, self)')
            i += 1
        i = 1
        for key in self.dict.keys():
            exec(f'self.lbl{i} = QLabel(key, self)')
            i += 1

        self.matches_number = len(self.dict)
        self.mainbox = QVBoxLayout(self)
        self.abox = QHBoxLayout(self)
        self.firstpart = QVBoxLayout(self)
        self.lbl1.setFont(QtGui.QFont("Century Gothic", 11, QtGui.QFont.Bold))
        self.lbl1.adjustSize()
        self.lbl2.setFont(QtGui.QFont("Century Gothic", 11, QtGui.QFont.Bold))
        self.lbl2.adjustSize()
        self.firstpart.addStretch(2)
        self.firstpart.addWidget(self.lbl1, alignment=QtCore.Qt.AlignCenter)
        self.firstpart.addStretch(1)
        self.firstpart.addWidget(self.lbl2, alignment=QtCore.Qt.AlignCenter)
        if self.matches_number == 3:
            self.lbl3.setFont(QtGui.QFont("Century Gothic", 11, QtGui.QFont.Bold))
            self.lbl3.adjustSize()
            self.firstpart.addStretch(1)
            self.firstpart.addWidget(self.lbl3, alignment=QtCore.Qt.AlignCenter)
        elif self.matches_number == 4:
            self.lbl3.setFont(QtGui.QFont("Century Gothic", 11, QtGui.QFont.Bold))
            self.lbl3.adjustSize()
            self.lbl4.setFont(QtGui.QFont("Century Gothic", 11, QtGui.QFont.Bold))
            self.lbl4.adjustSize()
            self.firstpart.addStretch(1)
            self.firstpart.addWidget(self.lbl3, alignment=QtCore.Qt.AlignCenter)
            self.firstpart.addStretch(1)
            self.firstpart.addWidget(self.lbl4, alignment=QtCore.Qt.AlignCenter)
        elif self.matches_number == 5:
            self.lbl3.setFont(QtGui.QFont("Century Gothic", 11, QtGui.QFont.Bold))
            self.lbl3.adjustSize()
            self.lbl4.setFont(QtGui.QFont("Century Gothic", 11, QtGui.QFont.Bold))
            self.lbl4.adjustSize()
            self.lbl5.setFont(QtGui.QFont("Century Gothic", 11, QtGui.QFont.Bold))
            self.lbl5.adjustSize()
            self.firstpart.addStretch(1)
            self.firstpart.addWidget(self.lbl3, alignment=QtCore.Qt.AlignCenter)
            self.firstpart.addStretch(1)
            self.firstpart.addWidget(self.lbl4, alignment=QtCore.Qt.AlignCenter)
            self.firstpart.addStretch(1)
            self.firstpart.addWidget(self.lbl5, alignment=QtCore.Qt.AlignCenter)
        self.firstpart.addStretch(2)
        self.abox.addLayout(self.firstpart)

        self.placetoput = QVBoxLayout(self)
        self.lbl_to_drop1 = DropLabel('Перетащите ответ сюда', self)
        self.lbl_to_drop1.setFont(QtGui.QFont("Century Gothic", 11))
        self.lbl_to_drop1.adjustSize()
        self.lbl_to_drop2 = DropLabel('Перетащите ответ сюда', self)
        self.lbl_to_drop2.setFont(QtGui.QFont("Century Gothic", 11))
        self.lbl_to_drop2.adjustSize()
        self.placetoput.addStretch(2)
        self.placetoput.addWidget(self.lbl_to_drop1, alignment=QtCore.Qt.AlignCenter)
        self.placetoput.addStretch(1)
        self.placetoput.addWidget(self.lbl_to_drop2, alignment=QtCore.Qt.AlignCenter)
        if self.matches_number == 3:
            self.lbl_to_drop3 = DropLabel('Перетащите ответ сюда', self)
            self.lbl_to_drop3.setFont(QtGui.QFont("Century Gothic", 11))
            self.lbl_to_drop3.adjustSize()
            self.placetoput.addStretch(1)
            self.placetoput.addWidget(self.lbl_to_drop3, alignment=QtCore.Qt.AlignCenter)
        elif self.matches_number == 4:
            self.lbl_to_drop3 = DropLabel('Перетащите ответ сюда', self)
            self.lbl_to_drop4 = DropLabel('Перетащите ответ сюда', self)
            self.lbl_to_drop3.setFont(QtGui.QFont("Century Gothic", 11))
            self.lbl_to_drop3.adjustSize()
            self.lbl_to_drop4.setFont(QtGui.QFont("Century Gothic", 11))
            self.lbl_to_drop4.adjustSize()
            self.placetoput.addStretch(1)
            self.placetoput.addWidget(self.lbl_to_drop3, alignment=QtCore.Qt.AlignCenter)
            self.placetoput.addStretch(1)
            self.placetoput.addWidget(self.lbl_to_drop4, alignment=QtCore.Qt.AlignCenter)
        elif self.matches_number == 5:
            self.lbl_to_drop3 = DropLabel('Перетащите ответ сюда', self)
            self.lbl_to_drop4 = DropLabel('Перетащите ответ сюда', self)
            self.lbl_to_drop5 = DropLabel('Перетащите ответ сюда', self)
            self.lbl_to_drop3.setFont(QtGui.QFont("Century Gothic", 11))
            self.lbl_to_drop3.adjustSize()
            self.lbl_to_drop4.setFont(QtGui.QFont("Century Gothic", 11))
            self.lbl_to_drop4.adjustSize()
            self.lbl_to_drop5.setFont(QtGui.QFont("Century Gothic", 11))
            self.lbl_to_drop5.adjustSize()
            self.placetoput.addStretch(1)
            self.placetoput.addWidget(self.lbl_to_drop3, alignment=QtCore.Qt.AlignCenter)
            self.placetoput.addStretch(1)
            self.placetoput.addWidget(self.lbl_to_drop4, alignment=QtCore.Qt.AlignCenter)
            self.placetoput.addStretch(1)
            self.placetoput.addWidget(self.lbl_to_drop5, alignment=QtCore.Qt.AlignCenter)
        self.placetoput.addStretch(2)
        self.abox.addLayout(self.placetoput)

        self.secondpart = QVBoxLayout(self)
        self.lbl_to_drag1.setFont(QtGui.QFont("Century Gothic", 11))
        self.lbl_to_drag1.adjustSize()
        self.lbl_to_drag2.setFont(QtGui.QFont("Century Gothic", 11))
        self.lbl_to_drag2.adjustSize()
        self.secondpart.addStretch(2)
        self.secondpart.addWidget(self.lbl_to_drag1, alignment=QtCore.Qt.AlignCenter)
        self.secondpart.addStretch(1)
        self.secondpart.addWidget(self.lbl_to_drag2, alignment=QtCore.Qt.AlignCenter)
        if self.matches_number == 3:
            self.lbl_to_drag3.setFont(QtGui.QFont("Century Gothic", 11))
            self.lbl_to_drag3.adjustSize()
            self.secondpart.addStretch(2)
            self.secondpart.addWidget(self.lbl_to_drag3, alignment=QtCore.Qt.AlignCenter)
        elif self.matches_number == 4:
            self.lbl_to_drag3.setFont(QtGui.QFont("Century Gothic", 11))
            self.lbl_to_drag3.adjustSize()
            self.lbl_to_drag4.setFont(QtGui.QFont("Century Gothic", 11))
            self.lbl_to_drag4.adjustSize()
            self.secondpart.addStretch(2)
            self.secondpart.addWidget(self.lbl_to_drag3, alignment=QtCore.Qt.AlignCenter)
            self.secondpart.addStretch(2)
            self.secondpart.addWidget(self.lbl_to_drag4, alignment=QtCore.Qt.AlignCenter)
        elif self.matches_number == 5:
            self.lbl_to_drag3.setFont(QtGui.QFont("Century Gothic", 11))
            self.lbl_to_drag3.adjustSize()
            self.lbl_to_drag4.setFont(QtGui.QFont("Century Gothic", 11))
            self.lbl_to_drag4.adjustSize()
            self.lbl_to_drag5.setFont(QtGui.QFont("Century Gothic", 11))
            self.lbl_to_drag5.adjustSize()
            self.secondpart.addStretch(2)
            self.secondpart.addWidget(self.lbl_to_drag3, alignment=QtCore.Qt.AlignCenter)
            self.secondpart.addStretch(2)
            self.secondpart.addWidget(self.lbl_to_drag4, alignment=QtCore.Qt.AlignCenter)
            self.secondpart.addStretch(2)
            self.secondpart.addWidget(self.lbl_to_drag5, alignment=QtCore.Qt.AlignCenter)
        self.secondpart.addStretch(2)
        self.abox.addLayout(self.secondpart)
        self.mainbox.addLayout(self.abox)
        self.btn = QPushButton('OK', self)
        self.mainbox.addStretch(1)
        self.mainbox.addWidget(self.btn, alignment=QtCore.Qt.AlignCenter)
        self.mainbox.addStretch(2)
        self.setLayout(self.mainbox)
        self.btn.clicked.connect(self.WriteToFile)


    def WriteToFile(self):
        self.a1 = self.lbl_to_drop1.text()
        self.a2 = self.lbl_to_drop2.text()
        firstpart1 = self.lbl1.text()
        firstpart2 = self.lbl2.text()

        error = 0
        point = self.maxscore / self.l
        if self.matches_number == 2:
            if self.a1 == 'Перетащите ответ сюда' or self.a2 == 'Перетащите ответ сюда':
                self.msgnum = QMessageBox(self)
                self.msgnum.critical(self, "Ошибка ", "Пожалуйста, укажите ваш ответ.", QMessageBox.Ok)
                error = 1
        elif self.matches_number == 3:
            self.a3 = self.lbl_to_drop3.text()
            firstpart3 = self.lbl3.text()
            if self.a1 == 'Перетащите ответ сюда' or self.a2 == 'Перетащите ответ сюда' or self.a3 == 'Перетащите ответ сюда':
                self.msgnum = QMessageBox(self)
                self.msgnum.critical(self, "Ошибка ", "Пожалуйста, укажите ваш ответ.", QMessageBox.Ok)
                error = 1
        elif self.matches_number == 4:
            self.a3 = self.lbl_to_drop3.text()
            self.a4 = self.lbl_to_drop4.text()
            firstpart3 = self.lbl3.text()
            firstpart4 = self.lbl4.text()
            if self.a1 == 'Перетащите ответ сюда' or self.a2 == 'Перетащите ответ сюда' or self.a3 == 'Перетащите ответ сюда' or self.a4 == 'Перетащите ответ сюда':
                self.msgnum = QMessageBox(self)
                self.msgnum.critical(self, "Ошибка ", "Пожалуйста, укажите ваш ответ.", QMessageBox.Ok)
                error = 1
        elif self.matches_number == 5:
            self.a3 = self.lbl_to_drop3.text()
            self.a4 = self.lbl_to_drop4.text()
            self.a5 = self.lbl_to_drop5.text()
            firstpart3 = self.lbl3.text()
            firstpart4 = self.lbl4.text()
            firstpart5 = self.lbl5.text()
            if self.a1 == 'Перетащите ответ сюда' or self.a2 == 'Перетащите ответ сюда' or self.a3 == 'Перетащите ответ сюда' or self.a4 == 'Перетащите ответ сюда' or self.a5 == 'Перетащите ответ сюда':
                self.msgnum = QMessageBox(self)
                self.msgnum.critical(self, "Ошибка ", "Пожалуйста, укажите ваш ответ.", QMessageBox.Ok)
                error = 1
        if error == 0:
            with open(self.filename, 'a', encoding='utf-8') as file:
                file.write('Вопрос #%s' % self.num + '\n')
                file.write('Ответ:\n')
                file.write('Соответствие1:' + firstpart1 + ' - ' + self.a1 + '\n')
                file.write('Соответствие2:' + firstpart2 + ' - ' + self.a2 + '\n')
                if firstpart1 in self.dict and self.a1 == self.dict[firstpart1]:
                    self.score += point
                if firstpart2 in self.dict and self.a2 == self.dict[firstpart2]:
                    self.score += point
                if self.matches_number == 3:
                    file.write('Соответствие3:' + firstpart3 + ' - ' + self.a3 + '\n')
                    if firstpart3 in self.dict and self.a3 == self.dict[firstpart3]:
                        self.score += point
                elif self.matches_number == 4:
                    file.write('Соответствие3:' + firstpart3 + ' - ' + self.a3 + '\n')
                    if firstpart3 in self.dict and self.a3 == self.dict[firstpart3]:
                        self.score += point
                    file.write('Соответствие4:' + firstpart4 + ' - ' + self.a4 + '\n')
                    if firstpart4 in self.dict and self.a4 == self.dict[firstpart4]:
                        self.score += point
                elif self.matches_number == 5:
                    file.write('Соответствие3:' + firstpart3 + ' - ' + self.a3 + '\n')
                    if firstpart3 in self.dict and self.a3 == self.dict[firstpart3]:
                        self.score += point
                    file.write('Соответствие4:' + firstpart4 + ' - ' + self.a4 + '\n')
                    if firstpart4 in self.dict and self.a4 == self.dict[firstpart4]:
                        self.score += point
                    file.write('Соответствие5:' + firstpart5 + ' - ' + self.a5 + '\n')
                    if firstpart5 in self.dict and self.a5 == self.dict[firstpart5]:
                        self.score += point
                self.score = round(self.score, 1)
                ost = self.score % 1
                if ost == 0:
                    self.score = round(self.score)
                file.write('Баллы: ' + str(self.score) + '\n')
                file.write('\n')
            self.switch_amch.emit()


if __name__=="__main__":
    app = QApplication(sys.argv)
    myapp = ThisWindow(3, 'answerfiles/Test2.txt', {'Бейонсе':'Джей Зи', 'Ким Кардашьян':'Кенью Уэст'}, 2)
    myapp.show()
    sys.exit(app.exec_())
