import sys
from PyQt5.QtWidgets import QVBoxLayout,  QApplication, QSizePolicy

import general_settings as gs
import show_qaudio_task, show_qimage_task, show_qtext_task
import show_avariants_task, show_amatch_task


TEXT_TYPE_AUDIO = 'Аудио'
TEXT_TYPE_IMAGE = 'Изображение'
TEXT_MANY_VARIANTS = 'Выбрать несколько правильных ответов'
TEXT_ONE_VARIANT = 'Выбрать один правильный ответ'
MANY_VARIANTS = 'many'
ONE_VARIANT = 'one'


class ThisWindow(gs.SLWindow):

    def __init__(self, filename, tasklist):
        super().__init__()
        self.tasklist = tasklist
        self.filename = filename
        self.question_type = tasklist[0]
        self.answer_type = tasklist[1]
        self.i = tasklist[2]
        self.question = tasklist[3]
        self.rightanswers = tasklist[4]
        self.maxscore = int(tasklist[5])
        self.score = 0
        self.initUI()

        # mediafile and variants are optional, depending on the task type



    def initUI(self):
        self.mainbox = QVBoxLayout(self)

        # type of question check
        if self.question_type == TEXT_TYPE_AUDIO:
            self.mediafile = self.tasklist[6]
            self.qcomponents = show_qaudio_task.QAudio(self.i, self.question, self.mediafile)
        elif self.question_type == TEXT_TYPE_IMAGE:
            self.mediafile = self.tasklist[6]
            self.qcomponents = show_qimage_task.QImage(self.i, self.question, self.mediafile)
        else:
            self.qcomponents = show_qtext_task.QText(self.i, self.question)

        # type of answer check
        if self.answer_type == TEXT_MANY_VARIANTS:
            if len(self.tasklist) == 8:
                self.variants = self.tasklist[7]
            else:
                self.variants = self.tasklist[6]
            self.acomponents = show_avariants_task.AVariants(MANY_VARIANTS, self.i, self.variants, self.filename, self.rightanswers, self.maxscore)
        elif self.answer_type == TEXT_ONE_VARIANT:
            if len(self.tasklist) == 8:
                self.variants = self.tasklist[7]
            else:
                self.variants = self.tasklist[6]
            self.acomponents = show_avariants_task.AVariants(ONE_VARIANT, self.i, self.variants, self.filename, self.rightanswers, self.maxscore)
        else:
            self.acomponents = show_amatch_task.AMatch(self.i, self.filename, self.rightanswers, self.maxscore)

        self.mainbox.addStretch()
        self.mainbox.addWidget(self.qcomponents)
        self.qcomponents.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.mainbox.addStretch()
        self.mainbox.addWidget(self.acomponents)
        self.acomponents.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.mainbox.addStretch()
        self.setLayout(self.mainbox)

        self.acomponents.btn.clicked.connect(self.acomponents.WriteToFile)
        self.acomponents.do_task_end.connect(lambda: self.close())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = ThisWindow('answerfiles/Test1.txt',
                       #['Текст', 'Установить соответствие', 2, 'names', {'Джоуи': 'Трибианни', 'Чендлер': 'Бинг'}, '6'])
                       ['Текст', 'Выбрать один правильный ответ', 1, 'hoow u doing?', 'ok', '3',
                        ['well', 'badly', 'ok']])
    myapp.show()
    myapp.acomponents.do_task_end.connect(lambda: print('signal'))
    sys.exit(app.exec_())
