import sys
from PyQt5.QtWidgets import QVBoxLayout,  QApplication
from PyQt5 import QtCore

import general_settings as gs
import show_qaudio_task, show_avariants_task


class ThisWindow(gs.SLWindow):

    switch_create_task_end = QtCore.pyqtSignal()

    def __init__(self, question_type, answer_type, n, i, question, audiofile, answers, filename, rightanswers, maxscore):
        super().__init__()
        self.question_type = question_type
        self.answer_type = answer_type
        self.num = n
        self.n = i
        self.answers = answers
        self.question = question
        self.audiofile = audiofile
        self.filename = filename
        self.rightanswers = rightanswers
        self.maxscore = int(maxscore)
        self.score = 0
        self.initUI()


    def initUI(self):
        self.mainbox = QVBoxLayout(self)

        #type of question check
        if self.question_type == 'audio':
            self.qcomponents = show_qaudio_task.QAudio(self.num, self.n, self.question, self.audiofile)
        elif self.question_type == 'image':
            self.qcomponents = show_qaudio_task.QImage(self.num, self.n, self.question, self.audiofile)
        else:
            self.qcomponents = show_qaudio_task.QText(self.num, self.n, self.question, self.audiofile)

        # type of answer check
        if self.answer_type == 'many':
            self.acomponents = show_avariants_task.AVariants('many', self.n, self.answers, self.filename, self.rightanswers, self.maxscore)
        elif self.answer_type == 'one':
            self.acomponents = show_avariants_task.AVariants('one', self.n, self.answers, self.filename, self.rightanswers, self.maxscore)
        else:
            self.acomponents = show_avariants_task.AMatch(self.n, self.answers, self.filename, self.rightanswers, self.maxscore)

        self.mainbox.addWidget(self.qcomponents)
        self.mainbox.addStretch(2)
        self.mainbox.addWidget(self.acomponents)
        self.setLayout(self.mainbox)

        self.acomponents.btn.clicked.connect(self.check)

    def check(self):
        self.acomponents.window_initialising.connect(lambda: self.switch_create_task_end.emit())
        if self.question_type in ('audio', 'image'):
            self.acomponents.WriteToFile()
        else:
            self.acomponents.WriteToFile()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = ThisWindow('audio', 'many', 3, 3, 'Listen to the recording. Tick true statements.',
                       'Bob Sinclar feat. Pitbull and DragonFly and Fatman Scoop - Rock The Boat.mp3',
                       ['The speaker is a journalist.', 'The speaker is a member of a rescue team.', 'There has been an earthquake.', 'There has been an avalanche.'],
                       'answerfiles/Test1.txt', ['The speaker is a member of a rescue team.', 'There has been an earthquake.'], '3')
    myapp.show()
    sys.exit(app.exec_())
