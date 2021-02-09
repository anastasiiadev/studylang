import sys, os
from PyQt5.QtWidgets import QApplication, QMessageBox

import files
import dbinteraction as db
import create_task
import testWindow as testw
import taskWindow as task
import EndCreate


class TaskController:

    def __init__(self, test, n, i, filename, score):
        self.testscore = score
        self.test = test
        self.n = n
        self.i = i
        self.filename = filename
        n = int(n)
        i = int(i)
        if i > n:
            self.task = EndCreate.ThisWindow(self.testscore, filename)
            self.task.switch_end.connect(lambda: self.test.sendtest())
        else:
            if i == 1:
                path = os.getcwd()
                folder = path + '\\testfiles\\'
                if os.path.exists(folder) is False:
                    os.mkdir(folder)
            self.task = task.ThisWindow(self.i, self.filename)
            self.task.switch_type_task.connect(self.general)
        self.task.show()


    def general(self, q, a):
        self.window = create_task.ThisWindow(self.i, self.filename, q, a)
        self.window.switch_create_task_end.connect(lambda: self.new())
        self.task.close()
        self.window.show()

    def new(self):
        a = int(self.window.acomponents.maxscore)
        self.window.close()
        self.testscore += a
        i = int(self.i)
        n = int(self.n)
        i += 1
        obj = TestController.Create_New_Task(self.test, n, i, self.filename, self.testscore)


class TestController:

    def __init__(self, user_id):
        self.user_id = user_id
        self.testW = testw.ThisWindow(self.user_id)
        self.testW.switch_newtest.connect(lambda: self.TasksController())
        self.testW.show()

    def TasksController(self):
        self.testW.close()
        self.Create_New_Task(self.testW.questions, 1, f'testfiles/{self.testW.filename}', 0)

    def Create_New_Task(self, n, i, filename, score):
        self.taskcontroller = TaskController(self, n, i, filename, score)

    def sendtest(self):
        try:
            f = files.File()
            fileid = f.post(self.testW.filename, f'testfiles/{self.testW.filename}', 'tests')
            conn = db.create_connection()
            query = f"UPDATE tests SET fileid='{fileid}' WHERE id={self.testW.n}"
            db.execute_query(conn, query, 'insert')
        except Exception:
            self.msgnofile = QMessageBox(self)
            self.msgnofile.critical(self, "Ошибка ", "Не удалось загрузить ваш файл.", QMessageBox.Ok)
        path = os.getcwd()
        os.remove(path + '\\testfiles\\' + self.testW.filename)



if __name__=="__main__":
    app = QApplication(sys.argv)
    controller = TestController(1)
    sys.exit(app.exec_())
