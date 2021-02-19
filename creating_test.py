import sys, os
import logging
from PyQt5.QtWidgets import QApplication, QMessageBox

import files
import dbinteraction as db
import create_task
import test_window
import type_task_window
import creating_end


class TaskController:

    def __init__(self, test, n, i, filename, score):
        self.testscore = score
        self.test = test
        self.n = int(n)
        self.i = int(i)
        self.filename = filename
        if self.i > self.n:
            self.end_window = creating_end.ThisWindow(self.testscore, filename)
            self.end_window.switch_end.connect(lambda: self.test.sendtest(self.end_window))
            self.end_window.show()
        else:
            if self.i == 1:
                path = os.getcwd()
                folder = path + '\\testfiles\\'
                if os.path.exists(folder) is False:
                    os.mkdir(folder)
            self.type_task = type_task_window.ThisWindow(self.i, self.filename)
            self.type_task.switch_type_task.connect(self.general)
            self.type_task.show()


    def general(self, q, a):
        self.task = create_task.ThisWindow(self.i, self.filename, q, a)
        self.task.switch_create_task_end.connect(self.new)
        self.type_task.close()
        self.task.show()

    def new(self):
        self.task.close()
        self.testscore += int(self.task.acomponents.maxscore)
        TestController.create_new_task(self.test, self.n, self.i + 1, self.filename, self.testscore)


class TestController:

    def __init__(self, user_id):
        self.user_id = user_id
        self.test_window = test_window.ThisWindow(self.user_id)
        self.test_window.switch_newtest.connect(lambda: self.tasks_controller())
        self.test_window.show()

    def tasks_controller(self):
        self.test_window.close()
        self.create_new_task(self.test_window.questions, 1, f'testfiles/{self.test_window.filename}', 0)

    def create_new_task(self, n, i, filename, score):
        self.taskcontroller = TaskController(self, n, i, filename, score)

    def sendtest(self, window):
        try:
            f = files.File()
            fileid = f.post(self.test_window.filename, f'testfiles/{self.test_window.filename}', 'tests')
            conn = db.create_connection()
            query = f"UPDATE tests SET fileid='{fileid}' WHERE id={self.test_window.new_test_id}"
            db.execute_query(conn, query, 'insert')
        except Exception:
            self.msgnofile = QMessageBox(self)
            self.msgnofile.critical(self, "Ошибка ", "Не удалось загрузить ваш файл.", QMessageBox.Ok)
        path = os.getcwd()
        os.remove(path + '\\testfiles\\' + self.test_window.filename)
        window.close()


if __name__=="__main__":
    app = QApplication(sys.argv)
    import logging
    logging.basicConfig(filename='logs.log', encoding='utf-8', level=logging.DEBUG)
    controller = TestController(1)
    sys.exit(app.exec_())
