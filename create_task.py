import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QVBoxLayout, QApplication

import create_amatch_task
import create_avariants_task
import create_qaudio_task
import create_qimage_task
import create_qtext_task
import general_settings as gs

AUDIO = 'audio'
IMAGE = 'image'
MANY_VARIANTS = 'many'
ONE_VARIANT = 'one'


class ThisWindow(gs.SLWindow):

    """
    Окно создания задания.
    """

    switch_create_task_end = QtCore.pyqtSignal()

    def __init__(self, i, filename, question, answer):

        """
        :param i: номер текущего задания
        :param filename: имя файла с тестом
        :param question: тип вопроса
        :param answer: тип ответа
        """

        super().__init__()
        self.n = i
        self.filename = filename
        self.question = question
        self.answer = answer
        self.initUI()

    def initUI(self):
        """
        В зависимости от типа вопроса и типа ответа вызываются соответстсвующие виджеты
            и компонуются в одном окне.
        """

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

        """
        Текст вопроса пользователя созраняется в переменной utext.
        Далее в зависимости от типа задания вызывается функция записи данных в файл с нужными аргументами.
        """

        utext = self.qcomponents.utext.toPlainText()
        self.acomponents.switch_task_end.connect(lambda: self.close_task_window())
        if self.question in (AUDIO, IMAGE):
            print('go to writetofile')
            self.acomponents.WriteToFile(utext, self.filename, self.qcomponents.distribution, self.qcomponents.newfile)
            print('step out from writetofile')
        else:
            self.acomponents.WriteToFile(utext, self.filename)

    def close_task_window(self):

        """
        Закрывается окно создания задания и издается сигнал.
        """

        print('before switch_create_task_end signal')
        self.close()
        self.switch_create_task_end.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = ThisWindow(1, 'testfiles/Test1.txt', 'image', 'match')
    myapp.show()
    sys.exit(app.exec_())