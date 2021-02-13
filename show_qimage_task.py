import sys, os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication, QMessageBox
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QPixmap

import files
import dbinteraction as db


class QImage(QWidget):

    def __init__(self, i, question, image):
        super().__init__()
        self.n = i
        self.question = question
        self.image = image
        self.initUI()

    def initUI(self):
        self.box = QVBoxLayout(self)
        self.qnum = QLabel(f"Вопрос #{self.n}", self)
        self.qnum.setFont(QtGui.QFont("Century Gothic", 15, QtGui.QFont.Bold))
        self.qnum.adjustSize()
        self.qtext = QLabel(self.question, self)
        self.qtext.setFont(QtGui.QFont("Century Gothic", 13))
        self.qtext.adjustSize()
        self.qtext.setWordWrap(True)
        if len(self.question) <= 50:
            self.qtext.setFixedSize(500, 50)
        else:
            self.qtext.setFixedSize(500, 150)
        self.qtext.setAlignment(QtCore.Qt.AlignCenter)
        try:
            path = os.getcwd()
            folder = path + '\\img\\'
            if os.path.exists(folder + self.image) is False:
                conn = db.create_connection()
                fileid = db.execute_query(conn,
                                          f"SELECT fileid FROM images WHERE filename='{self.image}'")[0][0]
                f = files.File()
                f.get(fileid, f'img/{self.image}')
        except Exception:
            self.msgnofile = QMessageBox(self)
            self.msgnofile.critical(self, "Ошибка ", "Не удалось загрузить файл.", QMessageBox.Ok)
            self.close()
        prepixmap = QPixmap(folder + self.image)
        width = prepixmap.width()
        height = prepixmap.height()
        if height > 330:
            pixmap = prepixmap.scaledToHeight(300, mode=0)
        elif width <= 650:
            pixmap = prepixmap
        elif width > 650:
            pixmap = prepixmap.scaledToWidth(650, mode=0)
        lbl = QLabel(self)
        lbl.setPixmap(pixmap)

        self.box.addWidget(self.qnum, alignment=QtCore.Qt.AlignCenter)
        self.box.addSpacing(5)
        self.box.addWidget(self.qtext, alignment=QtCore.Qt.AlignCenter)
        self.box.addSpacing(5)
        self.box.addWidget(lbl, alignment=QtCore.Qt.AlignCenter)
        self.setLayout(self.box)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QImage(1, 'What professions can you see in the picture?', 'little-prince-illustration 350 высота.jpg')
    sys.exit(app.exec_())
