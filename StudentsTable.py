import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QGridLayout, QTableWidget, QMessageBox, QTableWidgetItem, QCheckBox, QPushButton
from PyQt5.QtCore import Qt

import dbinteraction as db
import general_settings as gs


class MainWindow(gs.SLWindow):

    switch_tomenu = QtCore.pyqtSignal()
    switch_toresults = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        try:
            conn = db.create_connection()
            self.students_info = db.execute_query(conn, "SELECT id, fio, confirmed FROM people WHERE role='2'")
            self.tomenu = 0

            grid_layout = QGridLayout()
            self.setLayout(grid_layout)
            self.table = QTableWidget(self)
            self.table.setColumnCount(3)
            self.table.setHorizontalHeaderLabels(["Ученик", "Подтверждение регистрации", "Результаты тестов"])

            # Устанавливаем выравнивание на заголовки
            self.table.horizontalHeaderItem(0).setTextAlignment(Qt.AlignCenter)
            self.table.horizontalHeaderItem(1).setTextAlignment(Qt.AlignCenter)
            self.table.horizontalHeaderItem(2).setTextAlignment(Qt.AlignCenter)

            i = 0
            self.numstrings = len(self.students_info)
            self.table.setRowCount(self.numstrings)

            for student in self.students_info:
                # заполняем строку
                self.table.setItem(i, 0, QTableWidgetItem(student[1]))
                self.checkbox = QCheckBox(self.table)
                self.checkbox.setStyleSheet("margin-left:120%; margin-right:100%;")
                if student[2] == 1:
                    self.checkbox.setCheckState(2)
                else:
                    self.checkbox.setCheckState(0)
                self.table.setCellWidget(i, 1, self.checkbox)
                self.results = QPushButton('Посмотреть')
                self.results.setFixedSize(200, 25)
                self.results.setCheckable(True)
                self.results.setStyleSheet("margin-left:70%; margin-right:10%;")
                self.results.clicked.connect(lambda: self.Remember())
                self.table.setCellWidget(i, 2, self.results)
                i += 1

            self.table.resizeRowsToContents()
            header = self.table.horizontalHeader()
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
            header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
            btn_menu = QPushButton('Назад в меню')
            btn_menu.setFixedSize(150, 25)
            grid_layout.addWidget(self.table, 0, 0)
            grid_layout.addWidget(btn_menu, 1, 0)
            self.show()

            btn_menu.clicked.connect(lambda: self.ChangeFlag())
            btn_menu.clicked.connect(self.Remember)

        except Exception as e:
            logging.error(e)
            self.show()
            self.msg = QMessageBox(self)
            self.msg.critical(self, "Ошибка ", "Не удалось найти информацию о студентах. Повторите попытку позже.", QMessageBox.Ok)
            self.close()
            sys.exit()

    def ChangeFlag(self):
        self.tomenu = 1

    def WhichStudent(self):
        if self.numstrings != 0:
            for i in range(0, self.numstrings):
                button = self.table.cellWidget(i, 2)
                if button.isChecked():
                    self.checked_person_id = self.students_info[i][0]
                    self.switch_toresults.emit()
                    break

    def Remember(self):
        try:
            conn = db.create_connection()
            changed = []
            for i in range(0, self.numstrings):
                user = list(self.students_info[i])
                checkbox = self.table.cellWidget(i, 1)
                if checkbox.isChecked() is True and user[2] == 0:
                    user[2] = 1
                    changed.append(user)
                elif checkbox.isChecked() is False and user[2] == 1:
                    user[2] = 0
                    changed.append(user)
            for student in changed:
                query = (
                    f"UPDATE people set confirmed={student[2]} WHERE id={student[0]}")
                db.execute_query(conn, query, "insert")
                conn.commit()
            if self.tomenu == 1:
                conn.close()
                self.switch_tomenu.emit()
            else:
                self.WhichStudent()
        except Exception as e:
            logging.error(e)
            self.msg = QMessageBox(self)
            self.msg.critical(self, "Ошибка ", "Не удалось подключиться к базе данных. Повторите попытку позже.",
                              QMessageBox.Ok)
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    import logging
    logging.basicConfig(filename='logs.log', encoding='utf-8', level=logging.DEBUG)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())
