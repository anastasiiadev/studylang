'''from PyQt5.QtWidgets import (QMainWindow, QApplication, QLabel, QWidget)
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QPainter, QBrush
from PyQt5.QtCore import Qt


class W(QMainWindow):
    def __init__(self, *args):
        super().__init__()
        #self.label1 = QLabel('Первая часть')
        #self.label1.move(100, 50)
        self.label = QLabel('Вторая часть')
        #self.label.move(150, 50)
        self.setCentralWidget(self.label)
        self.label.installEventFilter(self)
        #self.label.mousePressEvent = self.getPos

    def eventFilter(self, obj, e):
        if obj == self.label and e.type() == 2:
            self.label.setText('Clicked')

            def mouseMoveEvent(self, event):
                x = event.pos().x()
                y = event.pos().y()
                self.label.move(x, y)
        return super(QMainWindow, self).eventFilter(obj, e)

    def eventFilter(self, obj, e):
        if obj == self.label and e.type() == 3:
            self.x = e.pos().x()
            self.y = e.pos().y()
            self.clicked_label.move(self.x, self.y)
        return super(QMainWindow, self).eventFilter(obj, e)

    def mouseMoveEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()
        self.label.move(x, y)
    
    
    def mouseMoveEvent(self, event):
        print(event.pos())
    
    def getPos(self, event):
            self.x = event.pos().x()
            self.y = event.pos().y()

app = QApplication([])
w = W()
w.show()
app.exec_()'''

import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QDrag, QPixmap, QPainter
from PyQt5.QtCore import Qt, QMimeData
from PyQt5 import QtCore


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


class AppDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(800, 600)
        self.Center()

        self.mainbox = QVBoxLayout(self)
        self.abox = QHBoxLayout(self)
        self.firstpart = QVBoxLayout(self)
        lbl1 = QLabel('Russia', self)
        lbl2 = QLabel('UK', self)
        lbl3 = QLabel('France', self)
        self.firstpart.addStretch(2)
        self.firstpart.addWidget(lbl1, alignment=QtCore.Qt.AlignCenter)
        self.firstpart.addStretch(1)
        self.firstpart.addWidget(lbl2, alignment=QtCore.Qt.AlignCenter)
        self.firstpart.addStretch(1)
        self.firstpart.addWidget(lbl3, alignment=QtCore.Qt.AlignCenter)
        self.firstpart.addStretch(2)
        self.abox.addLayout(self.firstpart)
        #lbl_to_drag2.move(0, 20)

        self.placetoput = QVBoxLayout(self)
        lbl_to_drop1 = DropLabel('Перетащите ответ сюда', self)
        lbl_to_drop2 = DropLabel('Перетащите ответ сюда', self)
        lbl_to_drop3 = DropLabel('Перетащите ответ сюда', self)
        self.placetoput.addStretch(2)
        self.placetoput.addWidget(lbl_to_drop1, alignment=QtCore.Qt.AlignCenter)
        self.placetoput.addStretch(1)
        self.placetoput.addWidget(lbl_to_drop2, alignment=QtCore.Qt.AlignCenter)
        self.placetoput.addStretch(1)
        self.placetoput.addWidget(lbl_to_drop3, alignment=QtCore.Qt.AlignCenter)
        self.placetoput.addStretch(2)
        self.abox.addLayout(self.placetoput)

        self.secondpart = QVBoxLayout(self)
        lbl_to_drag = DragLabel('London', self)
        lbl_to_drag2 = DragLabel('Paris', self)
        lbl_to_drag3 = DragLabel('Moscow', self)
        self.secondpart.addStretch(2)
        self.secondpart.addWidget(lbl_to_drag, alignment=QtCore.Qt.AlignCenter)
        self.secondpart.addStretch(1)
        self.secondpart.addWidget(lbl_to_drag2, alignment=QtCore.Qt.AlignCenter)
        self.secondpart.addStretch(1)
        self.secondpart.addWidget(lbl_to_drag3, alignment=QtCore.Qt.AlignCenter)
        self.secondpart.addStretch(2)
        self.abox.addLayout(self.secondpart)
        self.mainbox.addLayout(self.abox)

        '''lbl_to_drop = DropLabel('Перетащите ответ сюда', self)
        lbl_to_drop.move(200, 70)'''

    def Center(self):
        self.setWindowTitle("StudyLang")
        '''file = 'iconSL.jpg'
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
        self.setWindowIcon(ico)'''
        desktop = QApplication.desktop()
        x = (desktop.width() - self.frameSize().width()) // 2
        y = ((desktop.height() - self.frameSize().height()) // 2) - 30
        self.move(x, y)


app = QApplication(sys.argv)

demo = AppDemo()
demo.show()

sys.exit(app.exec_())