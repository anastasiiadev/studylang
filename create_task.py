import sys
from PyQt5.QtWidgets import QVBoxLayout,  QApplication
from PyQt5 import QtCore

import general_settings as gs
import qaudio, qimage, qtext
import avariants, amatch


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
        if self.question == 'audio':
            self.qcomponents = qaudio.QAudio(self.n)
            self.qcomponents.audiob.clicked.connect(self.qcomponents.showDialog)
        elif self.question == 'image':
            self.qcomponents = qimage.QImage(self.n)
            self.qcomponents.imgb.clicked.connect(self.qcomponents.showDialog)
        else:
            self.qcomponents = qtext.QText(self.n)
        if self.answer == 'many':
            self.acomponents = avariants.AVariants('many')
        elif self.answer == 'one':
            self.acomponents = avariants.AVariants('one')
        else:
            self.acomponents = amatch.AMatch()
        self.mainbox.addWidget(self.qcomponents)
        self.mainbox.addStretch(1)
        self.mainbox.addWidget(self.acomponents)
        self.setLayout(self.mainbox)

        self.acomponents.btn.clicked.connect(self.check)

    def check(self):
        utext = self.qcomponents.utext.toPlainText()
        self.acomponents.switch_task_end.connect(lambda: self.switch_create_task_end.emit())
        if self.question in ('audio', 'image'):
            self.acomponents.WriteToFile(utext, self.filename, self.qcomponents.distribution, self.qcomponents.newfile)
        else:
            self.acomponents.WriteToFile(utext, self.filename)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = ThisWindow(1, 1, 'testfiles/Test1.txt', 'text', 'one')
    myapp.show()
    sys.exit(app.exec_())