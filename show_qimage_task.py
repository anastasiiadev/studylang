import os
import sys

from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication, QMessageBox

import dbinteraction as db
import files
import folder


class QImage(QWidget):

    """
    Виджет, реализующий часть окна задания типа "Изображение".
    """

    def __init__(self, i, question, image):

        """
        :param i: номер задания
        :param question: текст вопроса
        :param image: название файла с картинкой
        """

        super().__init__()
        self.n = i
        self.question = question
        self.image = image
        self.initUI()

    def initUI(self):

        """
        Настройка части виджета задания типа "Изображение".
        """

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
            image_directory = folder.Making_Folder('\\image\\')
            if os.path.exists(image_directory.path_to_folder + self.image) is False:
                conn = db.create_connection()
                fileid = db.execute_query(conn,
                                          f"SELECT fileid FROM images WHERE filename='{self.image}'")[0][0]
                f = files.File()
                f.get(fileid, f'image/{self.image}')
        except Exception:
            self.msgnofile = QMessageBox(None)
            self.msgnofile.critical(None, "Ошибка ", "Не удалось загрузить файл.", QMessageBox.Ok)
            self.close()
        prepixmap = QPixmap(image_directory.path_to_folder + self.image)
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
    window = QImage(1, 'What professions can you see in the picture?', 'cover3.jpg')
    sys.exit(app.exec_())
