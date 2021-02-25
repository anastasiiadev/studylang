import sys
import logging
from PyQt5.QtWidgets import QVBoxLayout,  QApplication
from PyQt5 import QtCore

import general_settings as gs
import create_qaudio_task, create_qimage_task, create_qtext_task
import create_avariants_task, create_amatch_task


AUDIO = 'audio'
IMAGE = 'image'
MANY_VARIANTS = 'many'
ONE_VARIANT = 'one'


class ThisWindow(gs.SLWindow):

    switch_create_task_end = QtCore.pyqtSignal()

    def __init__(self, i, filename, question, answer):
        super().__init__()
        self.n = i
        self.filename = filename
        self.question = question
        self.answer = answer
        self.initUI()

    def initUI(self):
        self.mainbox = QVBoxLayout(self)
        if self.question == AUDIO:
            self.qcomponents = create_qaudio_task.QAudio(self.n)
            self.qcomponents.audiob.clicked.connect(self.qcomponents.showDialog)
        elif self.question == IMAGE:
            self.qcomponents = create_qimage_task.QImage(self.n)
            self.qcomponents.imgb.clicked.connect(self.qcomponents.showDialog)
        else:
            self.qcomponents = create_qtext_task.QText(self.n)
        if self.answer == MANY_VARIANTS:
            self.acomponents = create_avariants_task.AVariants('many')
        elif self.answer == ONE_VARIANT:
            self.acomponents = create_avariants_task.AVariants('one')
        else:
            self.acomponents = create_amatch_task.AMatch()
        self.mainbox.addWidget(self.qcomponents)
        self.mainbox.addStretch(1)
        self.mainbox.addWidget(self.acomponents)
        self.setLayout(self.mainbox)

        self.acomponents.btn.clicked.connect(self.check)

    def check(self):
        utext = self.qcomponents.utext.toPlainText()
        self.acomponents.switch_task_end.connect(lambda: self.close_task_window())
        if self.question in (AUDIO, IMAGE):
            self.acomponents.WriteToFile(utext, self.filename, self.qcomponents.distribution, self.qcomponents.newfile)
        else:
            self.acomponents.WriteToFile(utext, self.filename)

    def close_task_window(self):
        self.close()
        self.switch_create_task_end.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = ThisWindow(1, 1, 'testfiles/Test1.txt', 'text', 'one')
    myapp.show()
    sys.exit(app.exec_())