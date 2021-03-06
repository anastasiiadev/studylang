import sys
import logging
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox, QVBoxLayout, QLabel, QApplication, QPushButton, QComboBox

import dbinteraction as db
import general_settings as gs


class ThisWindow(gs.SLWindow):

    """
    Открывается окно, с помощью которого, пользователь выбирает тест в выпаюдающем меню.
    Далее идентификатор выбранного теста сохраняется в атрибуте self.gettestid.
    """

    switch_choosetest = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.SelectFromDB()
        if self.status == 1:
            self.initUI()

    def SelectFromDB(self):

        """
        Функция подключается к БД и создает атрибуты объекта класса:
        self.tests_dict - словарь, в котором ключами являются идентификаторы всех тестов из БД,
            а значениями - имена тестов;
        self.testnames - список имен всех тестов из БД.
        """

        try:
            conn = db.create_connection()
            result = db.execute_query(conn, "SELECT id, testname FROM tests")
            if not result:
                self.show()
                self.msg = QMessageBox(None)
                self.msg.information(None, "Тесты отсутствуют", "В базе данных нет тестов. Попробуйте пройти тестирование позже.", QMessageBox.Ok)
                self.status = 0
                self.close()
                logging.info("Нет тестов в БД.")
            else:
                self.tests_dict = dict(result)
                self.testnames = list(self.tests_dict.values())
                self.status = 1
                conn.close()
        except Exception as e:
            self.show()
            logging.error(e)
            self.msg = QMessageBox(None)
            self.msg.critical(None, "Ошибка ", "Не удалось найти тесты. Повторите попытку позже.", QMessageBox.Ok)
            self.status = 0
            self.close()

    def initUI(self):
        self.box = QVBoxLayout(self)
        self.qtest = QLabel("Какой тест вы хотите пройти?", self)
        self.qtest.setFont(QtGui.QFont("Century Gothic", 15, QtGui.QFont.Bold))
        self.qtest.adjustSize()
        self.qbox = QComboBox(self)
        self.qbox.addItems(self.testnames)
        self.btn = QPushButton('OK', self)
        self.box.addStretch(2)
        self.box.addWidget(self.qtest, alignment=QtCore.Qt.AlignCenter)
        self.box.addWidget(self.qbox, alignment=QtCore.Qt.AlignCenter)
        self.box.addStretch(1)
        self.box.addWidget(self.btn, alignment=QtCore.Qt.AlignCenter)
        self.box.addStretch(2)
        self.setLayout(self.box)

        self.btn.clicked.connect(self.RememberTestId)

    def RememberTestId(self):

        """
        Функция создает атрибут self.gettestid - идентификатор, выбранного теста.
        """

        self.test = self.qbox.currentText()
        self.gettestid = self.get_key(self.tests_dict, self.test)
        self.switch_choosetest.emit()

    def get_key(self, dict, value):

        """
        :param dict: словарь
        :param value: значение
        :return: функция возвращает ключ для указанного значения
        """

        for k, v in dict.items():
            if v == value:
                return k



if __name__=="__main__":
    app = QApplication(sys.argv)
    logging.basicConfig(filename='logs.log', encoding='utf-8', level=logging.DEBUG)
    myapp = ThisWindow()
    myapp.show()
    sys.exit(app.exec_())


