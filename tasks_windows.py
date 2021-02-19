import sys
from PyQt5.QtWidgets import QVBoxLayout,  QApplication, QSizePolicy
from PyQt5 import QtCore

import general_settings as gs
import show_qaudio_task, show_qimage_task, show_qtext_task
import show_avariants_task, show_amatch_task


class ThisWindow(gs.SLWindow):

    do_task_end = QtCore.pyqtSignal()

    def __init__(self, filename, question_type, answer_type, i, question, rightanswers, maxscore, mediafile=None, variants=None):
        super().__init__()
        self.question_type = question_type
        self.answer_type = answer_type
        self.n = i
        self.variants = variants
        self.question = question
        self.mediafile = mediafile
        self.filename = filename
        self.rightanswers = rightanswers
        self.maxscore = int(maxscore)
        self.score = 0
        self.initUI()


    def initUI(self):
        self.mainbox = QVBoxLayout(self)

        #type of question check
        if self.question_type == 'audio':
            self.qcomponents = show_qaudio_task.QAudio(self.n, self.question, self.mediafile)
        elif self.question_type == 'image':
            self.qcomponents = show_qimage_task.QImage(self.n, self.question, self.mediafile)
        else:
            self.qcomponents = show_qtext_task.QText(self.n, self.question)

        # type of answer check
        if self.answer_type == 'many':
            self.acomponents = show_avariants_task.AVariants('many', self.n, self.variants, self.filename, self.rightanswers, self.maxscore)
        elif self.answer_type == 'one':
            self.acomponents = show_avariants_task.AVariants('one', self.n, self.variants, self.filename, self.rightanswers, self.maxscore)
        else:
            self.acomponents = show_amatch_task.AMatch(self.n, self.filename, self.rightanswers, self.maxscore)

        self.mainbox.addStretch()
        self.mainbox.addWidget(self.qcomponents)
        self.qcomponents.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.mainbox.addStretch()
        self.mainbox.addWidget(self.acomponents)
        self.acomponents.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.mainbox.addStretch()
        self.setLayout(self.mainbox)

        self.acomponents.btn.clicked.connect(self.check)

    def check(self):
        self.acomponents.window_initialising.connect(lambda: self.close_task_window())
        self.acomponents.WriteToFile()

    def close_task_window(self):
        self.close()
        self.do_task_end.emit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = ThisWindow('image', 'many', 1, 'What professions can you see in the picture?',
                       'answerfiles/Test1.txt', ['The speaker is a member of a rescue team.', 'There has been an earthquake.'], '3',
                       'little-prince-illustration 350 высота.jpg',
                       ['The speaker is a journalist.', 'The speaker is a member of a rescue team.',
                        'There has been an earthquake.', 'There has been an avalanche.'],
                       )
    myapp.show()
    sys.exit(app.exec_())
