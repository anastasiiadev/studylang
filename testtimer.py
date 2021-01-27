import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTime, QTimer
from PyQt5.QtWidgets import QApplication, QLCDNumber
import design
from datetime import datetime, timedelta


class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow, QLCDNumber):
    def __init__(self, parent=None):
        super(ExampleApp, self).__init__(parent)
        self.setupUi(self)
        self.pushButton_3.clicked.connect(self.Start_T)
        self.pushButton_2.clicked.connect(self.Stop_T)
        self.pushButton.clicked.connect(self.Reset_T)
        # self.t = StringVar()
        self.lcdNumber.setNumDigits(8)
        self.lcdNumber.display('00:00:00')

    def Start_T(self):
        global count
        count = 0
        ##self.start_timer()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1000)
        self.begin = datetime.strptime(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S').split()[1]),
                                       '%H:%M:%S')

    def Stop_T(self):
        count = 1
        self.timer.stop()

    def Reset_T(self):
        self.lcdNumber.display('00:00:00')
        self.timer.stop()

    def start_timer(self):
        self.timer()

    def showTime(self):
        if self.begin == datetime.strptime(str('00:00:00'), '%H:%M:%S'):
            self.timer.stop()
            return
        self.begin = self.begin - timedelta(seconds=1)
        self.lcdNumber.display(str(self.begin).split()[1])


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()