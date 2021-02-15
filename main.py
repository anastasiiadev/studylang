import sys
import logging
from PyQt5.QtWidgets import QApplication

import AuthorisationWindow, Menu, RegistrationWindow, StudentsTable, StudentResults

class TestController:

    def __init__(self):
        logging.basicConfig(filename='logs.log', encoding='utf-8', level=logging.DEBUG)
        self.login = AuthorisationWindow.ThisWindow()
        self.login.switch_passed.connect(lambda: self.ShowMenu())
        self.login.switch_register.connect(lambda: self.Register())

    def ShowMenu(self):
        if hasattr(self, 'login'):
            self.login.close()
        if hasattr(self, 'studwin'):
            self.studwin.close()
        self.controller = Menu.ThisWindow(self.login.user_id)
        self.controller.switch_students.connect(lambda: self.StudentsTable())

    def Register(self):
        self.login.close()
        self.newwin = RegistrationWindow.ThisWindow()
        self.newwin.switch_register.connect(lambda: TestController())

    def StudentsTable(self):
        self.controller.close()
        self.studwin = StudentsTable.MainWindow()
        self.studwin.switch_tomenu.connect(lambda: self.ShowMenu())
        self.studwin.switch_toresults.connect(lambda: self.StudentResult(self.studwin.checked_person_id))

    def StudentResult(self, id):
        self.studwin.close()
        self.studres = StudentResults.MainWindow(id)
        self.studres.switch_tostudentstable.connect(lambda: self.From_Student_To_Students())

    def From_Student_To_Students(self):
        self.studres.close()
        self.studwin = StudentsTable.MainWindow()
        self.studwin.switch_tomenu.connect(lambda: self.ShowMenu())
        self.studwin.switch_toresults.connect(lambda: self.StudentResult(self.studwin.person_id))

if __name__=="__main__":
    app = QApplication(sys.argv)
    controller = TestController()
    sys.exit(app.exec_())
