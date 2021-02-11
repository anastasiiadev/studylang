import sys
from PyQt5.QtWidgets import QVBoxLayout,  QApplication
from PyQt5 import QtCore

import general_settings as gs
import show_qaudio_task, show_qimage_task, show_qtext_task
import show_avariants_task, show_amatch_task


class ThisWindow(gs.SLWindow):

    do_task_end = QtCore.pyqtSignal()

    def __init__(self, question_type, answer_type, i, question, filename, rightanswers, maxscore, mediafile=None, variants=None):
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


        self.mainbox.addWidget(self.qcomponents)
        if self.question_type == 'image':
            self.mainbox.addSpacing(280)
        else:
            self.mainbox.addSpacing(30)
        self.mainbox.addWidget(self.acomponents)
        self.setLayout(self.mainbox)

        self.acomponents.btn.clicked.connect(self.check)

    def check(self):
        self.acomponents.window_initialising.connect(lambda: self.do_task_end.emit())
        self.acomponents.WriteToFile()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = ThisWindow('text', 'match', 1, 'как кого звали?', 'answerfiles/Test4.txt', {'Рон': 'Уизли', 'Гермиона': 'Грейнжер', 'Гарри': 'Поттер'}, 6)
    myapp.show()
    sys.exit(app.exec_())
