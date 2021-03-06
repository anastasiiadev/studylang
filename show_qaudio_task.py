import os
import sys
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication, QPushButton, QMessageBox

import dbinteraction as db
import files
import folder


class QAudio(QWidget):

    """
    Виджет, реализующий часть окна задания типа "Аудио".
    """

    def __init__(self, i, question, audiofile):

        """
        :param i: номер задания
        :param question: текст вопроса
        :param audiofile: название аудиофайла
        """

        super().__init__()
        self.n = i
        self.question = question
        self.audiofile = audiofile
        self.initUI()


    def initUI(self):

        """
        Настройка части виджета задания типа "Аудио".
        """

        self.box = QVBoxLayout(self)
        self.qnum = QLabel(f"Вопрос #{self.n}", self)
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
        self.audio.setFixedSize(170, 27)

        self.box.addSpacing(50)
        self.box.addWidget(self.qnum, alignment=QtCore.Qt.AlignCenter)
        self.box.addSpacing(10)
        self.box.addWidget(self.qtext, alignment=QtCore.Qt.AlignCenter)
        self.box.addSpacing(30)
        self.box.addWidget(self.audio, alignment=QtCore.Qt.AlignCenter)
        self.setLayout(self.box)
        self.show()

        self.audio.clicked.connect(self.RecordingPlay)


    def RecordingPlay(self):

        """
        Скачивание и воспроизведение аудиофайла.
        """

        try:
            audio_directory = folder.Making_Folder('\\audio\\')
            if os.path.exists(audio_directory.path_to_folder + self.audiofile) is False:
                conn = db.create_connection()
                fileid = db.execute_query(conn, f"SELECT fileid FROM audios WHERE filename='{self.audiofile}'")[0][0]
                f = files.File()
                f.get(fileid, f'audio/{self.audiofile}')
            os.startfile(audio_directory.path_to_folder + self.audiofile)
        except Exception:
            self.msgnofile = QMessageBox(self)
            self.msgnofile.critical(self, "Ошибка ", "Не удалось загрузить файл.", QMessageBox.Ok)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QAudio(3, 'Listen to the recording. Tick true statements.', 'Bob Sinclar feat. Pitbull and DragonFly and Fatman Scoop - Rock The Boat.mp3')
    sys.exit(app.exec_())
