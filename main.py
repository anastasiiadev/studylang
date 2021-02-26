import sys
import logging
from PyQt5.QtWidgets import QApplication

import authorisation_window
import menu
import registration_window
import student_results

import students_table

class TestController:

    def __init__(self):

        """
        Открывается окно авторизации, которое позволяет перейти к регистрации новых пользователей
        или авторизоваться и перейти в меню.
        """

        logging.basicConfig(filename='logs.log', encoding='utf-8', level=logging.DEBUG)
        self.login = authorisation_window.ThisWindow()
        self.login.switch_passed.connect(lambda: self.ShowMenu())
        self.login.switch_register.connect(lambda: self.Register())

    def ShowMenu(self):

        """
        Открывается окно меню. Открытые до этого окна закрываются.
        """

        if hasattr(self, 'login'):
            self.login.close()
        if hasattr(self, 'studwin'):
            self.studwin.close()
        self.controller = menu.ThisWindow(self.login.user_id)
        self.controller.switch_students.connect(lambda: self.StudentsTable())

    def Register(self):

        """
        Открывается окно регистрации. Окно авторизации закрывается.
        """

        self.login.close()
        self.newwin = registration_window.ThisWindow()
        self.newwin.switch_register.connect(lambda: TestController())

    def StudentsTable(self):

        """
        Открывается окно со списком учеников, в котором можно подтвердить или отменить регистрацию учетной записи.
        Открытые до этого окна закрываются.
        """

        if hasattr(self, 'controller'):
            self.controller.close()
        if hasattr(self, 'studres'):
            self.studres.close()
        self.studwin = students_table.MainWindow()
        self.studwin.switch_tomenu.connect(lambda: self.ShowMenu())
        self.studwin.switch_toresults.connect(lambda: self.StudentResult(self.studwin.checked_person_id))

    def StudentResult(self, id):
        """
        id - идентификатор пользователя в таблице people.
        Открывается окно с результами тестирований конкретного ученика. Окно со списком учеников закрывается.
        """
        self.studwin.close()
        self.studres = student_results.MainWindow(id)
        self.studres.switch_tostudentstable.connect(lambda: self.StudentsTable())


if __name__=="__main__":
    app = QApplication(sys.argv)
    controller = TestController()
    sys.exit(app.exec_())
