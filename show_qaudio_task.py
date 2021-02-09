import sys, os
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QApplication, QPushButton, QMessageBox
from PyQt5 import QtGui, QtCore

import general_settings as gs
import files
import dbinteraction as db


class QAudio(gs.SLWindow):

    def __init__(self, n, i, question, audiofile):
        super().__init__()
        self.num = n
        self.n = i
        self.question = question
        self.audiofile = audiofile
        self.initUI()


    def initUI(self):
        box = QVBoxLayout(self)
        box.setContentsMargins(0, 30, 0, 30)
        self.qnum = QLabel("Вопрос #%s" % self.n, self)
        self.qnum.setFont(QtGui.QFont("Century Gothic", 15, QtGui.QFont.Bold))
        self.qnum.adjustSize()
        self.qtext = QLabel(self.question, self)
        self.qtext.setFont(QtGui.QFont("Century Gothic", 13))
        self.qtext.adjustSize()
        self.qtext.setWordWrap(True)
        if len(self.question) <= 50:
            self.qtext.setFixedSize(500, 50)
        else:
            self.qtext.setFixedSize(500, 150)
        self.qtext.setAlignment(QtCore.Qt.AlignCenter)
        self.audio = QPushButton('Прослушать аудиозапись', self)

        box.addStretch(1)
        box.addWidget(self.qnum, alignment=QtCore.Qt.AlignCenter)
        box.addSpacing(5)
        box.addWidget(self.qtext, alignment=QtCore.Qt.AlignCenter)
        box.addSpacing(15)
        box.addWidget(self.audio, alignment=QtCore.Qt.AlignCenter)
        box.addStretch(3)
        self.setLayout(box)
        self.show()

        self.audio.clicked.connect(self.RecordingPlay)


    def RecordingPlay(self):
        try:
            path = os.getcwd()
            folder = path + '\\audio\\'
            if os.path.exists(folder) is False:
                os.mkdir(folder)
            if os.path.exists(folder + self.audiofile) is False:
                conn = db.create_connection()
                fileid = db.execute_query(conn, f"SELECT fileid FROM audios WHERE filename='{self.audiofile}'")[0][0]
                f = files.File()
                f.get(fileid, f'audio/{self.audiofile}')

            os.startfile(folder + self.audiofile)
        except Exception:
            self.msgnofile = QMessageBox(self)
            self.msgnofile.critical(self, "Ошибка ", "Не удалось загрузить файл.", QMessageBox.Ok)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QAudio(3, 3, 'Listen to the recording. Tick true statements.', 'Bob Sinclar feat. Pitbull and DragonFly and Fatman Scoop - Rock The Boat.mp3')
    sys.exit(app.exec_())
