import os
import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5 import QtGui

import files


class SLWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("StudyLang")
        file = 'iconSL.jpg'
        path = os.getcwd()
        folder = path + '\\img\\'
        if os.path.exists(folder) is False:
            os.mkdir(folder)
        if os.path.exists(folder + file) is False:
            f = files.File()
            f.get("1tdvwtNx2iQUEDPbpe7NsSl-djVe-_h9G", "img/iconSL.jpg")
        ico = QtGui.QIcon('img/iconSL.jpg')
        self.setWindowIcon(ico)
        desktop = QApplication.desktop()
        x = ((desktop.width() - self.frameSize().width()) // 2) - 100
        y = ((desktop.height() - self.frameSize().height()) // 2) - 50
        self.move(x, y)
        self.setFixedSize(850, 650)
        pal = self.palette()
        pal.setColor(QtGui.QPalette.Normal, QtGui.QPalette.Window,
                     QtGui.QColor("#ffffff"))
        self.setPalette(pal)

if __name__=="__main__":
    app = QApplication(sys.argv)
    myapp = SLWindow()
    myapp.show()
    sys.exit(app.exec_())
