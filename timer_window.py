import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QSizePolicy, QApplication
from PyQt5 import QtGui

import general_settings as gs


class Window(QWidget):
    def __init__(self, time):
        super().__init__()
        self.time = time
        gs.SLWindow.set_icon_and_title(self)
        self.move(50, 50)
        self.setFixedSize(250, 100)
        self.label = QLabel("Осталось  " + "{}".format(time), self)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QtGui.QFont("Century Gothic", 15))
        self.label.adjustSize()

        self.layout = QGridLayout()
        self.layout.addWidget(self.label, 0, 0)

        self.setLayout(self.layout)
        self.show()

    def local_button_handler(self, time):
        self.label.setText("Осталось  " + "{}".format(time))


if __name__=="__main__":
    app = QApplication(sys.argv)
    w = Window('00:21:00')
    sys.exit(app.exec_())
