import time, sys
import threading

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import (QWidget, QApplication, QHBoxLayout, QPushButton)


def thread(my_func):
    """
    Запускает функцию в отдельном потоке
    """

    def wrapper(*args, **kwargs):
        my_thread = threading.Thread(target=my_func, args=args, kwargs=kwargs)
        my_thread.start()

    return wrapper


#thread
def processing(signal):
    """
    Эмулирует обработку (скачивание) каких-то данных
    """
    res = [i for i in 'hello']
    time.sleep(5)
    signal.emit(res)  # Посылаем сигнал в котором передаём полученные данные


class MyWidget(QWidget):
    my_signal = QtCore.pyqtSignal(list, name='my_signal')

    def __init__(self, parent=None):
        super(MyWidget, self).__init__(parent)
        self.mainLayout = QHBoxLayout()
        self.setLayout(self.mainLayout)

        self.button = QPushButton("Emit your signal!", self)
        self.mainLayout.addWidget(self.button)

        # При нажатии на кнопку запускаем обработку данных
        self.button.clicked.connect(lambda: processing(self.my_signal))

        # Обработчик сигнала
        self.my_signal.connect(self.mySignalHandler, QtCore.Qt.QueuedConnection)

    def mySignalHandler(self, data):  # Вызывается для обработки сигнала
        print(data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWidget()
    window.show()
    app.exec_()