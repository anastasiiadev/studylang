import sys, os, random
from ftplib import FTP
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QApplication, QTextEdit, QPushButton, QMessageBox)
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QDrag, QPixmap, QPainter
from PyQt5.QtCore import Qt, QMimeData


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
        event.acceptProposedAction()


class ThisWindow(QWidget):

    def __init__(self, d):
        super().__init__()
        self.dict = d
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
        self.setFixedSize(800, 600)
        self.Center()
        self.values = []
        for v in self.dict.values():
            self.values.append(v)
        print(self.values)
        random.shuffle(self.values)
        print(self.values)
        i = 1
        for el in self.values:
            exec('self.lbl_to_drag%s = DragLabel(el, self)' % i)
            i += 1
        i = 1
        for key in self.dict.keys():
            exec('self.lbl%s = QLabel(key, self)' % i)
            i += 1


        self.l = len(self.dict)
        self.mainbox = QVBoxLayout(self)
        self.abox = QHBoxLayout(self)
        self.firstpart = QVBoxLayout(self)
        self.firstpart.addStretch(2)
        self.firstpart.addWidget(self.lbl1, alignment=QtCore.Qt.AlignCenter)
        self.firstpart.addStretch(1)
        self.firstpart.addWidget(self.lbl2, alignment=QtCore.Qt.AlignCenter)
        if self.l == 3:
            self.firstpart.addStretch(1)
            self.firstpart.addWidget(self.lbl3, alignment=QtCore.Qt.AlignCenter)
        elif self.l == 4:
            self.firstpart.addStretch(1)
            self.firstpart.addWidget(self.lbl3, alignment=QtCore.Qt.AlignCenter)
            self.firstpart.addStretch(1)
            self.firstpart.addWidget(self.lbl4, alignment=QtCore.Qt.AlignCenter)
        elif self.l == 5:
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
        self.lbl_to_drop2 = DropLabel('Перетащите ответ сюда', self)
        self.placetoput.addStretch(2)
        self.placetoput.addWidget(self.lbl_to_drop1, alignment=QtCore.Qt.AlignCenter)
        self.placetoput.addStretch(1)
        self.placetoput.addWidget(self.lbl_to_drop2, alignment=QtCore.Qt.AlignCenter)
        if self.l == 3:
            self.lbl_to_drop3 = DropLabel('Перетащите ответ сюда', self)
            self.placetoput.addStretch(1)
            self.placetoput.addWidget(self.lbl_to_drop3, alignment=QtCore.Qt.AlignCenter)
        elif self.l == 4:
            self.lbl_to_drop3 = DropLabel('Перетащите ответ сюда', self)
            self.lbl_to_drop4 = DropLabel('Перетащите ответ сюда', self)
            self.placetoput.addStretch(1)
            self.placetoput.addWidget(self.lbl_to_drop3, alignment=QtCore.Qt.AlignCenter)
            self.placetoput.addStretch(1)
            self.placetoput.addWidget(self.lbl_to_drop4, alignment=QtCore.Qt.AlignCenter)
        elif self.l == 5:
            self.lbl_to_drop3 = DropLabel('Перетащите ответ сюда', self)
            self.lbl_to_drop4 = DropLabel('Перетащите ответ сюда', self)
            self.lbl_to_drop5 = DropLabel('Перетащите ответ сюда', self)
            self.placetoput.addStretch(1)
            self.placetoput.addWidget(self.lbl_to_drop3, alignment=QtCore.Qt.AlignCenter)
            self.placetoput.addStretch(1)
            self.placetoput.addWidget(self.lbl_to_drop4, alignment=QtCore.Qt.AlignCenter)
            self.placetoput.addStretch(1)
            self.placetoput.addWidget(self.lbl_to_drop5, alignment=QtCore.Qt.AlignCenter)
        self.placetoput.addStretch(2)
        self.abox.addLayout(self.placetoput)


        self.secondpart = QVBoxLayout(self)
        self.secondpart.addStretch(2)
        self.secondpart.addWidget(self.lbl_to_drag1, alignment=QtCore.Qt.AlignCenter)
        self.secondpart.addStretch(1)
        self.secondpart.addWidget(self.lbl_to_drag2, alignment=QtCore.Qt.AlignCenter)
        if self.l == 3:
            self.secondpart.addStretch(1)
            self.secondpart.addWidget(self.lbl_to_drag3, alignment=QtCore.Qt.AlignCenter)
        elif self.l == 4:
            self.secondpart.addStretch(1)
            self.secondpart.addWidget(self.lbl_to_drag3, alignment=QtCore.Qt.AlignCenter)
            self.secondpart.addStretch(1)
            self.secondpart.addWidget(self.lbl_to_drag4, alignment=QtCore.Qt.AlignCenter)
        elif self.l == 5:
            self.secondpart.addStretch(1)
            self.secondpart.addWidget(self.lbl_to_drag3, alignment=QtCore.Qt.AlignCenter)
            self.secondpart.addStretch(1)
            self.secondpart.addWidget(self.lbl_to_drag4, alignment=QtCore.Qt.AlignCenter)
            self.secondpart.addStretch(1)
            self.secondpart.addWidget(self.lbl_to_drag5, alignment=QtCore.Qt.AlignCenter)
        self.secondpart.addStretch(2)
        self.abox.addLayout(self.secondpart)
        self.mainbox.addLayout(self.abox)
        self.btn = QPushButton('OK', self)
        self.mainbox.addStretch(1)
        self.mainbox.addWidget(self.btn, alignment=QtCore.Qt.AlignCenter)
        self.mainbox.addStretch(2)

        self.btn.clicked.connect(self.WriteToFile)

    def WriteToFile(self):

        self.a1 = self.lbl_to_drop1.text()
        self.a2 = self.lbl_to_drop2.text()
        score = 0

        if self.l == 3:
            self.a3 = self.lbl_to_drop3.text()
            if self.a1 == 'Перетащите ответ сюда' or self.a2 == 'Перетащите ответ сюда' or self.a3 == 'Перетащите ответ сюда':
                self.msgnum = QMessageBox(self)
                self.msgnum.critical(self, "Ошибка ", "Пожалуйста, укажите ваш ответ.", QMessageBox.Ok)


if __name__=="__main__":
    app = QApplication(sys.argv)
    list = [3, [1, 'Текст', 'Установить соответствие', 'Укажите столицы стран', {'Германия':'Берлин', 'Италия':'Рим', 'Китай':'Пекин'}],
            [2, 'Изображение', 'Установить соответствие', 'Какого цвета?', 'рич.jpg', {'Человек':'черный', 'Фон':'оранжевый'}],
            [3, 'Аудио', 'Установить соответствие', 'Кто чья жена?', 'Beyonce - Partition.mp3', {'Бейонсе':'Джей Зи', 'Ким Кардашьян':'Кенью Уэст'}]]
    filename = 'Test2.txt'
    i = 1
    myapp = ThisWindow(list[1][4])
    myapp.show()
    sys.exit(app.exec_())