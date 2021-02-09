import sys
import taskWindow as task, Qtext_Amatch, Qtext_Aone, Qimg_Amatch, Qimg_Aone, Qaudio_Atmatch, Qaudio_Aone
from PyQt5.QtWidgets import QApplication


class Controller:

    def __init__(self, n, i, filename):
        self.show_task(n, i, filename)

    def show_task(self, n, i, filename):
        self.task = task.ThisWindow(i, 'files/{}'.format(filename))
        self.task.switch_t_mch.connect(lambda: self.text_match(n, i, filename))
        self.task.switch_t_v.connect(lambda: self.text_var(n, i, filename))
        self.task.switch_i_mch.connect(lambda: self.img_match(n, i, filename))
        self.task.switch_i_v.connect(lambda: self.img_var(n, i, filename))
        self.task.switch_a_mch.connect(lambda: self.audio_match(n, i, filename))
        self.task.switch_a_v.connect(lambda: self.audio_var(n, i, filename))
        self.task.show()

    def text_match(self, n, i, filename):
        self.window = Qtext_Amatch.ThisWindow(n, i, 'files/{}'.format(filename))
        self.window.switch_tmch.connect(lambda: self.new(n, i, filename))
        self.task.close()
        self.window.show()

    def text_var(self, n, i, filename):
        self.window = Qtext_Aone.ThisWindow(n, i, 'files/{}'.format(filename))
        self.window.switch_tv.connect(lambda: self.new(n, i, filename))
        self.task.close()
        self.window.show()

    def img_match(self, n, i, filename):
        self.window = Qimg_Amatch.ThisWindow(n, i, 'files/{}'.format(filename))
        self.window.switch_imch.connect(lambda: self.new(n, i, filename))
        self.task.close()
        self.window.show()

    def img_var(self, n, i, filename):
        self.window = Qimg_Aone.ThisWindow(n, i, 'files/{}'.format(filename))
        self.window.switch_iv.connect(lambda: self.new(n, i, filename))
        self.task.close()
        self.window.show()

    def audio_match(self, n, i, filename):
        self.window = Qaudio_Atmatch.ThisWindow(n, i, 'files/{}'.format(filename))
        self.window.switch_amch.connect(lambda: self.new(n, i, filename))
        self.task.close()
        self.window.show()

    def audio_var(self, n, i, filename):
        self.window = Qaudio_Aone.ThisWindow(n, i, 'files/{}'.format(filename))
        self.window.switch_av.connect(lambda: self.new(n, i, filename))
        self.task.close()
        self.window.show()

    def new(self, n, i, filename):
        i += 1
        if i <= n:
            obj = Controller(n, i, filename)
        else:
            sys.exit(app.exec_())


if __name__=="__main__":
    app = QApplication(sys.argv)
    filename = 'Test1.txt'
    n = 2
    controller = Controller(n, 1, filename)

