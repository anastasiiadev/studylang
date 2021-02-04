import sys
import general_settings as gs
import qaudio, amany
from PyQt5.QtWidgets import QVBoxLayout,  QApplication
from PyQt5 import QtCore


class ThisWindow(gs.SLWindow):
    switch_am = QtCore.pyqtSignal()

    def __init__(self, n, i, filename):
        super().__init__()
        self.n = i
        self.filename = filename
        self.initUI()

    def initUI(self):
        self.mainbox = QVBoxLayout(self)
        self.qcomponents = qaudio.QAudio(self.n)
        self.acomponents = amany.AMany()
        self.mainbox.addWidget(self.qcomponents)
        self.mainbox.addStretch(1)
        self.mainbox.addWidget(self.acomponents)
        self.setLayout(self.mainbox)

        self.qcomponents.audiob.clicked.connect(self.qcomponents.showDialog)
        self.acomponents.btn.clicked.connect(self.check)

    def check(self):
        utext = self.qcomponents.utext.toPlainText()
        self.acomponents.WriteToFile(utext, self.filename, self.qcomponents.distribution, self.qcomponents.newfile)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = ThisWindow(1, 1, 'testfiles/Test1.txt')
    myapp.show()
    sys.exit(app.exec_())
