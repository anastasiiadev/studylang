import datetime
import os
import random
import sys
import threading
from datetime import datetime, timedelta
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMessageBox

import dbinteraction as db
import doing_end
import files
import folder
import tasks_windows
import timer_window


TEXT_QUESTIONS_NUMBER = 'Количество вопросов:'
TEXT_QUESTION_NUMBER = 'Вопрос #'
TEXT_QUESTION_TYPE = 'Тип вопроса:'
TEXT_ANSWER_TYPE = 'Тип ответа:'
TEXT_TYPE_TEXT = 'Текст'
TEXT_TYPE_AUDIO = 'Аудио'
TEXT_TYPE_IMAGE = 'Изображение'
TEXT_TYPE_MANY_VARIANTS = 'Выбрать несколько правильных ответов'
TEXT_TYPE_ONE_VARIANT = 'Выбрать один правильный ответ'
TEXT_TYPE_MATCH = 'Установить соответствие'
TEXT_QUESTION = 'Вопрос:'
TEXT_MEDIAFILE = 'Имя файла:'
TEXT_MATCH = 'Соответствие'
TEXT_VARIANT = 'Вариант'
TEXT_RIGHT_ANSWERS = 'Правильные ответы:'
TEXT_RIGHT_ANSWER = 'Правильный ответ:'
TEXT_MAXSCORE = 'Максимальный балл:'
TEXT_MARKS = 'Оценки'
TEXT_MARK = 'Оценка'
TEXT_MAX_TEST_SCORE = 'Максимальное количество баллов:'
TEXT_TIME = 'Время теста:'



class Processor(QThread):
    signal = pyqtSignal()

    def __init__(self, m, s):
        super().__init__()
        self.begin = timedelta(minutes=m, seconds=s)
        self.timer_window = timer_window.Window(self.begin)
        self.run()

    def run(self):
        if self.begin == timedelta(seconds=0):
            self.timer_window.close()
            self.signal.emit()
            return
        self.begin = self.begin - timedelta(seconds=1)
        self.timer_window.local_button_handler(self.begin)
        self.thread = threading.Timer(1, self.run)
        self.thread.start()


class Show_Task:

    def __init__(self, controller, i):
        self.controller = controller
        current_task = self.controller.questions_list[i]
        if current_task[0] == TEXT_MARKS:
            self.controller.timer.thread.cancel()
            self.controller.timer.timer_window.close()
            with open(f'answerfiles/{self.controller.filename}', 'a', encoding='utf-8') as file:
                file.write(f'Общее количество баллов: {self.controller.wholescore}' + '\n')
            try:
                f = files.File()
                answerfileid = f.post(self.controller.filename, f'answerfiles/{self.controller.filename}', 'answers')
                conn = db.create_connection()
                query = f"UPDATE testing SET answerfileid='{answerfileid}' WHERE id={self.controller.answer_id}"
                db.execute_query(conn, query, 'insert')
                try:
                    self.controller.answer_directory.remove(self.controller.filename)
                except OSError as e:
                    logging.error("Failed with:", e.strerror)
            except Exception as ex:
                self.msg = QMessageBox(None)
                self.msg.critical(None, "Ошибка ", "Не удалось загрузить ваш файл на сервер.", QMessageBox.Ok)
                logging.error(ex)
            self.end_window = doing_end.ThisWindow(self.controller.answer_id, self.controller.wholescore, current_task)
            self.end_window.switch_end.connect(lambda: self.controller.end_testing())
            self.end_window.show()
        else:
            self.task_window = tasks_windows.ThisWindow(f'answerfiles/{self.controller.filename}', current_task)
            self.task_window.acomponents.do_task_end.connect(lambda: self.scoring(i))
            self.task_window.show()

    def scoring(self,  i):
        self.controller.wholescore += float(self.task_window.acomponents.score)
        self.controller.new(i)


class Show_Test_Controller:

    def __init__(self, testid, userid):
        self.test_id = testid
        self.user_id = userid
        self.answer_id = ''
        self.end = 0
        self.wholescore = 0
        try:
            self.insertToDB()
            test_directory = folder.Making_Folder('\\testfiles\\')
            self.testfile = f"Test{self.test_id}.txt"
            if os.path.exists(test_directory.path_to_folder + self.testfile) is False:
                try:
                    conn = db.create_connection()
                    tresult = db.execute_query(conn, f"SELECT fileid FROM tests WHERE id={self.test_id}")
                    if tresult:
                        f = files.File()
                        f.get(tresult[0][0], f'testfiles/{self.testfile}')
                except Exception as e:
                    self.msg = QMessageBox(None)
                    self.msg.critical(None, "Ошибка ", "Не удалось скачать файл теста. Повторите попытку позже.",
                                           QMessageBox.Ok)
                    logging.error(e)

            self.questions_list = self.read_from_file(self.testfile)
            self.questions_number = self.questions_list[0]
            self.minutes = int(self.questions_list[-1][0])
            self.seconds = int(self.questions_list[-1][1])
            test_directory.remove(self.testfile)
            self.timer = Processor(self.minutes, self.seconds)
            self.timer.signal.connect(lambda: self.timeout())
            self.new(0)
        except Exception as e:
            self.timer.timer_window.close()
            self.msg = QMessageBox(None)
            self.msg.critical(None, "Ошибка ", "Не удалось найти тест. Повторите попытку позже.", QMessageBox.Ok)
            logging.error(e)

    def new(self, i):
        if hasattr(self, 'task_object'):
            self.task_object.task_window.close()
        i += 1
        self.task_object = Show_Task(self, i)

    def end_testing(self):
        self.task_object.end_window.close()

    def timeout(self):
        self.msg = QMessageBox(None)
        self.msg.warning(None, "StudyLang", "Время вышло!", QMessageBox.Ok)
        self.new(self.questions_number)

    def insertToDB(self):
        try:
            conn = db.create_connection()
            max_testing_id = db.execute_query(conn, "SELECT max(id) FROM testing")[0][0]
            if max_testing_id == None:
                self.answer_id = '1'
            else:
                self.answer_id = str(int(max_testing_id) + 1)

            self.answer_directory = folder.Making_Folder('\\answerfiles\\')
            self.filename = f"Test{self.answer_id}.txt"
            now = datetime.now()
            date = now.strftime("%Y-%m-%d %H:%M")
            query = ("INSERT INTO testing (ID, TESTID, DATE, ANSWERFILEID) VALUES "
                     f"({self.answer_id}, '{self.test_id}', '{date}', '{self.filename}')")
            db.execute_query(conn, query, 'insert')
            conn.commit()

            max_work_id = db.execute_query(conn, "SELECT max(id) FROM work")[0][0]
            if max_work_id == None:
                new_work_id = 1
            else:
                new_work_id = int(max_work_id) + 1
            query = ("INSERT INTO work (ID, PERSONID, TRIAL_OR_TEST_ID, MODE) VALUES "
                     f"({new_work_id}, '{int(self.user_id)}', '{self.answer_id}', '2')")
            db.execute_query(conn, query, 'insert')
            conn.commit()
            conn.close()
        except Exception as e:
            logging.error(e)
            raise Exception

    def read_from_file(self, file):
        with open('testfiles/' + file, 'r', encoding='utf-8') as f:
            info = []
            lines = f.readlines()
            questionsnum = int(lines[0][20:].strip())
            info.append(questionsnum)
            i = 2
            variants, answers, marks, time = [], [], [], []
            dictmatch = {}
            img_or_audio, answer, score = '', '', ''
            while i < len(lines):
                item = []
                line = lines[i]
                if line.find(TEXT_MARK) != -1:
                    marks.append(TEXT_MARKS)
                    while line.find(TEXT_MAX_TEST_SCORE) == -1:
                        max_score = line[9:].strip()
                        marks.append(max_score)
                        i += 1
                        line = lines[i]
                    max_score = line[31:].strip()
                    marks.append(max_score)
                    i += 1
                    line = lines[i]
                    if line.find(TEXT_TIME) != -1:
                        time = line[12:].strip().split(' ')
                    break
                elif line.find(TEXT_QUESTION_NUMBER) != -1:
                    qnum = int(line[8:].strip())
                elif line.find(TEXT_QUESTION_TYPE) != -1:
                    qtype = line[12:].strip()
                elif line.find(TEXT_ANSWER_TYPE) != -1:
                    atype = line[11:].strip()
                elif line.find(TEXT_QUESTION) != -1:
                    q = line[7:].strip()
                elif line.find(TEXT_MEDIAFILE) != -1:
                    img_or_audio = line[10:].strip()
                elif line.find(TEXT_VARIANT + '1:') != -1:
                    v1 = line[9:].strip()
                    variants.append(v1)
                    i += 1
                    line = lines[i]
                    while line.find(TEXT_VARIANT) != -1:
                        v = lines[i][9:].strip()
                        variants.append(v)
                        i += 1
                        line = lines[i]
                elif line.find(TEXT_MATCH + '1:') != -1:
                    while line.find(TEXT_MATCH) != -1:
                        kend = line.find(';')
                        k = line[14:kend].strip()
                        v = line[kend + 1:].strip()
                        dictmatch.update({k: v})
                        i += 1
                        line = lines[i]
                if line.find(TEXT_MAXSCORE) != -1:
                    score = line[18:].strip()
                    i += 1
                    line = lines[i]
                if line.find(TEXT_RIGHT_ANSWER) != -1:
                    answer = line[17:].strip()
                if line.find(TEXT_RIGHT_ANSWERS) != -1:
                    ans = line[18:].strip()
                    answers = ans.split(', ')
                if line == '\n':
                    item.append(qtype)
                    item.append(atype)
                    item.append(qnum)
                    item.append(q)
                    if answer != '':
                        item.append(answer)
                    if answers:
                        item.append(answers)
                    if dictmatch:
                        item.append(dictmatch)
                    if score != '':
                        item.append(score)
                    if img_or_audio != '':
                        item.append(img_or_audio)
                    if variants:
                        item.append(variants)
                    info.append(item)
                    qtype, atype, qnum, q, answer, answers, img_or_audio = '', '', '', '', '', '', ''
                    dictmatch, variants = {}, []
                i += 1

            seq = [i for i in range(1, info[0] + 1)]
            random.shuffle(seq)
            randomed = [info[0]]
            for i in seq:
                randomed.append(info[i])
            if marks:
                randomed.append(marks)
            if time:
                randomed.append(time)
            return randomed


if __name__ == "__main__":
    app = QApplication(sys.argv)
    import logging
    logging.basicConfig(filename='logs.log', encoding='utf-8', level=logging.DEBUG)
    testid = '14'
    controller = Show_Test_Controller(testid, '1')
    sys.exit(app.exec_())
