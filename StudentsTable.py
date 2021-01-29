import sys, os
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QGridLayout, QWidget, QTableWidget, QMessageBox, QTableWidgetItem, QCheckBox, QPushButton
from PyQt5.QtCore import Qt
import dbinteraction as db
import files


class MainWindow(QWidget):

    switch_tomenu = QtCore.pyqtSignal()
    switch_toresults = QtCore.pyqtSignal()

    def __init__(self):
        QWidget.__init__(self)
        self.initUI()

    def initUI(self):
        try:
            conn = db.create_connection()
            queryresult = db.execute_query(conn, "SELECT id, fio, confirmed, role FROM people")

            self.setFixedSize(800, 600)
            self.Center()
            pal = self.palette()
            pal.setColor(QtGui.QPalette.Normal, QtGui.QPalette.Window,
                         QtGui.QColor("#ffffff"))
            self.setPalette(pal)
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
            self.numstrings = 0
            self.studentsbefore = []
            for el in queryresult:
                role = el[3]
                if role == 2:
                    self.numstrings += 1
                    self.studentsbefore.append(el)
            self.table.setRowCount(self.numstrings)

            for el in queryresult:
                self.person_id = el[0]
                person = el[1]
                confirmed = el[2]
                role = el[3]
                # заполняем строку
                if role == 2:
                    self.table.setItem(i, 0, QTableWidgetItem(person))
                    self.checkbox = QCheckBox(self.table)
                    self.checkbox.setStyleSheet("margin-left:120%; margin-right:100%;")
                    if confirmed == 1:
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
            btn = QPushButton('Назад в меню')
            btn.setFixedSize(150, 25)
            grid_layout.addWidget(self.table, 0, 0)
            grid_layout.addWidget(btn, 1, 0)
            self.show()

            btn.clicked.connect(lambda: self.ChangeFlag())
            btn.clicked.connect(self.Remember)

        except Exception as e:
            print(e)
            self.setFixedSize(800, 600)
            self.Center()
            self.msg = QMessageBox(self)
            self.msg.critical(self, "Ошибка ", "Не удалось найти тесты. Повторите попытку позже.", QMessageBox.Ok)
            sys.exit()

    def ChangeFlag(self):
        self.tomenu = 1

    def WhichStudent(self):
        if self.numstrings != 0:
            for i in range(0, self.numstrings):
                button = self.table.cellWidget(i, 2)
                if button.isChecked():
                    print(self.studentsbefore[i][0])
                    self.person_id = self.studentsbefore[i][0]
                    self.switch_toresults.emit()
                    conn.close()
                    break

    def Center(self):
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
        x = (desktop.width() - self.frameSize().width()) // 2
        y = ((desktop.height() - self.frameSize().height()) // 2) - 30
        self.move(x, y)

    def Remember(self):
        try:
            conn = db.create_connection()
        except Exception as e:
            print(e)
            self.close()

        changed = []
        studentsafter = []
        for s in self.studentsbefore:
            studentsafter.append(list(s))
        if self.numstrings != 0:
            for i in range(0, self.numstrings):
                user = studentsafter[i]
                checkbox = self.table.cellWidget(i, 1)
                if checkbox.isChecked() is True and user[2] == 0:
                    user[2] = 1
                    changed.append(user)
                elif checkbox.isChecked() is False and user[2] == 1:
                    user[2] = 0
                    changed.append(user)
        if changed:
            for el in changed:
                query = (
                    "UPDATE people set confirmed={} WHERE id={}".format(el[2], el[0]))
                db.execute_query(conn, query, "insert")
                conn.commit()
        if self.tomenu == 1:
            conn.close()
            self.switch_tomenu.emit()
        else:
            self.WhichStudent()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())