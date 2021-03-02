import os
import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5 import QtGui

import files
import folder


class SLWindow(QWidget):

    """
    Класс представляет собой общие настройки для всех окон приложения.
    """

    def __init__(self):

        """
        Окно центрируется относительно размеров экрана,
        задается цветовая гамма.
        """

        super().__init__()
        self.set_icon_and_title()
        desktop = QApplication.desktop()
        x = ((desktop.width() - self.frameSize().width()) // 2) - 100
        y = ((desktop.height() - self.frameSize().height()) // 2) - 50
        self.move(x, y)
        self.setFixedSize(850, 650)
        pal = self.palette()
        pal.setColor(QtGui.QPalette.Normal, QtGui.QPalette.Window,
                     QtGui.QColor("#ffffff"))
        self.setPalette(pal)

    def set_icon_and_title(self):

        """
        Устанавливается заголовок окна и иконка приложения
            (если файла нет в папке, то он скачивается).
        """

        self.setWindowTitle("StudyLang")
        file = 'iconSL.jpg'
        img_directory = folder.Making_Folder('\\image\\')
        if os.path.exists(img_directory.path_to_folder + file) is False:
            f = files.File()
            f.get("1tdvwtNx2iQUEDPbpe7NsSl-djVe-_h9G", "image/iconSL.jpg")
        ico = QtGui.QIcon('image/iconSL.jpg')
        self.setWindowIcon(ico)

if __name__=="__main__":
    app = QApplication(sys.argv)
    myapp = SLWindow()
    myapp.show()
    sys.exit(app.exec_())
