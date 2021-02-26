import sys, os
import logging
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets

import testing
import creating_test
import dbinteraction as db
import files
import general_settings as gs
import folder


class ThisWindow(gs.SLWindow):

    switch_students = QtCore.pyqtSignal()

    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.role = self.define_role(user_id)
        if hasattr(self, 'role'):
            self.initUI()


    def define_role(self, user_id):
        try:
            conn = db.create_connection()
            result = db.execute_query(conn, f"SELECT role FROM people WHERE id={user_id}")
            if result:
                role = result[0][0]
            else:
                self.show()
                self.msg = QMessageBox(None)
                self.msg.critical(None, "Ошибка ", "Не удалось найти пользователя в базе данных.", QMessageBox.Ok)
                self.close()
            conn.close()
            return role
        except Exception as e:
            self.msg = QMessageBox(None)
            self.msg.critical(None, "Ошибка ", "Не удалось подключиться к базе данных. Повторите попытку позже.", QMessageBox.Ok)
            logging.error(e)


    def initUI(self):
        self.box = QVBoxLayout(self)
        self.mainbox = QVBoxLayout(self)
        self.do = QPushButton("Пройти тест", self)
        self.do.setFixedSize(150, 30)
        self.do.setStyleSheet('font: 11pt Century Gothic;')
        self.guide_box = QHBoxLayout(self)
        guide_button = QPushButton(self)
        file = 'question.jpg'
        img_directory = folder.Making_Folder('\\img\\')
        if os.path.exists(img_directory.path_to_folder + file) is False:
            f = files.File()
            f.get("1jgRj4273tHow-e8JJ8btM4jl6rG20t1U", "img/question.jpg")
        ico = QtGui.QIcon('img/question.jpg')
        guide_button.setIcon(ico)
        guide_button.setIconSize(QtCore.QSize(25, 25))
        self.guide_box.addWidget(guide_button, alignment=QtCore.Qt.AlignRight)
        self.guide_box.addSpacing(20)
        if self.role == 1:
            self.text = QLabel("Что вы хотите сделать?", self)
            self.text.setFont(QtGui.QFont("Century Gothic", 15, QtGui.QFont.Bold))
            self.text.adjustSize()
            self.hbox = QHBoxLayout(self)
            self.create = QPushButton("Создать тест", self)
            self.create.setFixedSize(150, 30)
            self.create.setStyleSheet('font: 11pt Century Gothic;')
            self.mainbox.addStretch(2)
            self.mainbox.addWidget(self.text, alignment=QtCore.Qt.AlignCenter)
            self.mainbox.addStretch(1)
            self.hbox.addStretch(1)
            self.hbox.addWidget(self.create, alignment=QtCore.Qt.AlignCenter)
            self.hbox.addStretch(1)
            self.hbox.addWidget(self.do, alignment=QtCore.Qt.AlignCenter)
            self.hbox.addStretch(1)
            self.seestudents = QPushButton("Посмотреть информацию об учениках", self)
            self.seestudents.setFixedSize(400, 30)
            self.seestudents.setStyleSheet('font: 11pt Century Gothic;')
            self.mainbox.addLayout(self.hbox)
            self.mainbox.addStretch(1)
            self.mainbox.addWidget(self.seestudents, alignment=QtCore.Qt.AlignCenter)
            self.mainbox.addStretch(2)
        else:
            self.mainbox.addStretch(2)
            self.mainbox.addWidget(self.do, alignment=QtCore.Qt.AlignCenter)
            self.mainbox.addStretch(2)
        self.box.addLayout(self.guide_box)
        self.box.addLayout(self.mainbox)
        self.show()

        if self.role == 1:
            self.create.clicked.connect(self.SwitchMode1)
            guide_button.clicked.connect(self.teachers_guide)
            self.seestudents.clicked.connect(lambda: self.switch_students.emit())
        else:
            guide_button.clicked.connect(self.students_guide)
        self.do.clicked.connect(self.SwitchMode2)

    def students_guide(self):
        o = QMessageBox(self)
        o.about(self, "Руководство пользователя", "Вам будет предложен список доступных тестов, выбрав один из "
                                                  "которых, вы приступите к тестированию. Вам необходимо ответить на "
                                                  "вопросы содержащие текст, а также изображения и аудиофайлы. В "
                                                  "зависимости от типа задания нужно выбрать один или несколько "
                                                  "правильных ответов или установить соответствие. Закончив тест, "
                                                  "вы узнаете, сколько баллов вы набрали, и свою оценку.")

    def teachers_guide(self):
        o = QMessageBox(self)
        o.about(self, "Руководство пользователя", "Вам доступно два режима работы с программой: создание тестов и "
                                                  "прохождение тестов.\n\nВ режиме создания тестов вам нужно указать "
                                                  "название вашего теста и количество вопросов. Далее для каждого "
                                                  "вопроса необходимо выбрать его тип: текствый вопрос, "
                                                  "текст и картинка, текст и аудиофайл. Также вам следует выбрать тип "
                                                  "ответа: один правильный ответ среди нескольких вариантов, "
                                                  "несколько правильных ответов из нескольких вариантов или "
                                                  "установление соответствий. За каждое задание вам необходимо "
                                                  "определить максимальный балл, который получит ученик в случае "
                                                  "успешного ответа. В конце вам нужно указать, сколько баллов должен "
                                                  "набрать ученик, чтобы получить оценку 5, 4, 3. Результаты "
                                                  "тестирований вы можете посмотреть в меню, нажав на кнопку "
                                                  "«Посмотреть информацию об учениках» и выбрав нужного вам "
                                                  "обучающегося. Также на сервере сохраняются файлы с подробными "
                                                  "ответами учеников.\n\nВ режиме прохождения теста вам будет "
                                                  "предложен список доступных тестов, выбрав один из которых, "
                                                  "вы приступите к тестированию. Вам необходимо ответить на вопросы "
                                                  "содержащие текст, а также изображения и аудиофайлы. В зависимости "
                                                  "от типа задания нужно выбрать один или несколько правильных "
                                                  "ответов или установить соответствие. Закончив тест, вы узнаете, "
                                                  "сколько баллов вы набрали, и свою оценку.")

    def SwitchMode1(self):
        self.close()
        creating_test.TestController(self.user_id)

    def SwitchMode2(self):
        self.close()
        testing.Controller(self.user_id)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    import logging
    logging.basicConfig(filename='logs.log', encoding='utf-8', level=logging.DEBUG)
    myapp = ThisWindow('1')
    myapp.show()
    sys.exit(app.exec_())

