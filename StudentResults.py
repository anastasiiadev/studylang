import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QGridLayout, QWidget, QTableWidget, QTableWidgetItem, QPushButton
from PyQt5.QtCore import Qt

import dbinteraction as db
import general_settings as gs


class MainWindow(gs.SLWindow):

    switch_tostudentstable = QtCore.pyqtSignal()

    def __init__(self, id):
        QWidget.__init__(self)
        self.id = id
        self.initUI()

    def initUI(self):
        try:
            conn = db.create_connection()
            query = ("SELECT p.fio, tests.testname, t.date, t.score, t.mark "
                     "FROM people as p, testing as t, tests, work as w "
                     "WHERE p.id = w.personid AND	w.trial_or_test_id = t.id AND tests.id = t.testid AND w.mode = 2 "
                     f"AND p.id = {self.id}")
            queryresult = db.execute_query(conn, query)
            conn.close()

            grid_layout = QGridLayout()
            self.setLayout(grid_layout)
            self.table = QTableWidget(self)
            self.table.setColumnCount(5)
            self.table.setRowCount(len(queryresult))
            self.table.setHorizontalHeaderLabels(["Ученик", "Тест", "Дата и время", "Баллы", "Оценка"])

            # Устанавливаем выравнивание на заголовки
            for j in range(0, 5):
                self.table.horizontalHeaderItem(j).setTextAlignment(Qt.AlignCenter)

            i = 0
            for el in queryresult:
                # заполняем строку
                for k in range(0, 3):
                    self.table.setItem(i, k, QTableWidgetItem(el[k]))
                self.table.setItem(i, 3, QTableWidgetItem(str(el[3])))
                self.table.setItem(i, 4, QTableWidgetItem(str(el[4])))
                i += 1

            self.table.resizeRowsToContents()
            header = self.table.horizontalHeader()
            for i in range(0, 5):
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)

            btn = QPushButton('К таблице учеников')
            btn.setFixedSize(150, 25)
            grid_layout.addWidget(self.table, 0, 0)
            grid_layout.addWidget(btn, 1, 0)
            self.show()

            btn.clicked.connect(lambda: self.switch_tostudentstable.emit())

        except Exception as e:
            print(e)
            print("ошибка")
            #надо придумать что будет если ошибка
            self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow(2)
    mw.show()
    sys.exit(app.exec())
