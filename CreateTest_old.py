import sys, os
from PyQt5.QtWidgets import QApplication, QMessageBox

import files
import dbinteraction as db
import testWindow as testw
import taskWindow as task, Qtext_Amatch, Qtext_Aone, Qtext_Amany, Qimg_Amatch, Qimg_Aone, Qimg_Amany, Qaudio_Atmatch, Qaudio_Aone, Qaudio_Amany, EndCreate


class TaskController:

    def __init__(self, test, n, i, filename, score):
        self.testscore = score
        self.test = test
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
                self.CreateTaskWindow(n, i, filename)
            else:
                self.CreateTaskWindow(n, i, filename)
        self.task.show()

    def CreateTaskWindow(self, n, i, filename):
        self.task = task.ThisWindow(i, filename)
        self.task.switch_t_mch.connect(lambda: self.text_match(n, i, filename))
        self.task.switch_t_o.connect(lambda: self.text_one(n, i, filename))
        self.task.switch_t_m.connect(lambda: self.text_many(n, i, filename))
        self.task.switch_i_mch.connect(lambda: self.img_match(n, i, filename))
        self.task.switch_i_o.connect(lambda: self.img_one(n, i, filename))
        self.task.switch_i_m.connect(lambda: self.img_many(n, i, filename))
        self.task.switch_a_mch.connect(lambda: self.audio_match(n, i, filename))
        self.task.switch_a_o.connect(lambda: self.audio_one(n, i, filename))
        self.task.switch_a_m.connect(lambda: self.audio_many(n, i, filename))

    def text_match(self, n, i, filename):
        self.window = Qtext_Amatch.ThisWindow(n, i, filename)
        self.window.switch_tmch.connect(lambda: self.new(n, i, filename))
        self.task.close()
        self.window.show()

    def text_one(self, n, i, filename):
        self.window = Qtext_Aone.ThisWindow(n, i, filename)
        self.window.switch_to.connect(lambda: self.new(n, i, filename))
        self.task.close()
        self.window.show()

    def text_many(self, n, i, filename):
        self.window = Qtext_Amany.ThisWindow(n, i, filename)
        self.window.switch_tm.connect(lambda: self.new(n, i, filename))
        self.task.close()
        self.window.show()

    def img_match(self, n, i, filename):
        self.window = Qimg_Amatch.ThisWindow(n, i, filename)
        self.window.switch_imch.connect(lambda: self.new(n, i, filename))
        self.task.close()
        self.window.show()

    def img_one(self, n, i, filename):
        self.window = Qimg_Aone.ThisWindow(n, i, filename)
        self.window.switch_io.connect(lambda: self.new(n, i, filename))
        self.task.close()
        self.window.show()

    def img_many(self, n, i, filename):
        self.window = Qimg_Amany.ThisWindow(n, i, filename)
        self.window.switch_im.connect(lambda: self.new(n, i, filename))
        self.task.close()
        self.window.show()

    def audio_match(self, n, i, filename):
        self.window = Qaudio_Atmatch.ThisWindow(n, i, filename)
        self.window.switch_amch.connect(lambda: self.new(n, i, filename))
        self.task.close()
        self.window.show()

    def audio_one(self, n, i, filename):
        self.window = Qaudio_Aone.ThisWindow(n, i, filename)
        self.window.switch_ao.connect(lambda: self.new(n, i, filename))
        self.task.close()
        self.window.show()

    def audio_many(self, n, i, filename):
        self.window = Qaudio_Amany.ThisWindow(n, i, filename)
        self.window.switch_am.connect(lambda: self.new(n, i, filename))
        self.task.close()
        self.window.show()

    def new(self, n, i, filename):
        a = int(self.window.maxscore)
        self.testscore += a
        i = int(i)
        n = int(n)
        i += 1
        if i <= n:
            obj = TaskController(self.test, n, i, filename, self.testscore)
        elif i == n + 1:
            obj = TaskController(self.test, n, i, filename, self.testscore)


class TestController:

    def __init__(self, user_id):
        self.user_id = user_id
        self.testW = testw.ThisWindow(self.user_id)
        self.testW.switch_newtest.connect(lambda: self.Tasks())
        self.testW.show()

    def Tasks(self):
        self.testW.close()
        self.taskcontroller = TaskController(self, self.testW.questions, 1, f'testfiles/{self.testW.filename}', 0)


    def sendtest(self):
        try:
            f = files.File()
            fileid = f.post(self.testW.filename, f'testfiles/{self.testW.filename}', 'tests')
            conn = db.create_connection()
            query = f"UPDATE tests SET fileid='{fileid}' WHERE id={self.testW.n}"
            db.execute_query(conn, query, 'insert')
            path = os.getcwd()
            f = self.testW.filename.replace('/', '\\')
            os.remove(path + '\\' + f)
        except Exception:
            self.msgnofile = QMessageBox(self)
            self.msgnofile.critical(self, "Ошибка ", "Не удалось загрузить ваш файл.", QMessageBox.Ok)


if __name__=="__main__":
    app = QApplication(sys.argv)
    controller = TestController(1)
    sys.exit(app.exec_())
