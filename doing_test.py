import sys, datetime, random, os, threading, logging
from datetime import datetime, timedelta
from PyQt5.QtWidgets import QApplication, QMessageBox, QWidget
from PyQt5.QtCore import QThread, pyqtSignal

import tasks_windows
import timer_window
import doing_end
import files
import dbinteraction as db
import general_settings as gs


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
        threading.Timer(1, self.run).start()


class Showtask(gs.SLWindow):

    def __init__(self, controller, testid, user_id):
        super().__init__()
        self.controller = controller
        self.testid = testid
        self.user_id = user_id
        self.wholescore = 0
        self.answer_id = ''
        self.end = 0
        try:
            self.insertToDB()
            path = os.getcwd()
            folder = path + '\\testfiles\\'
            if os.path.exists(folder) is False:
                os.mkdir(folder)
            self.testfile = f"Test{self.testid}.txt"
            if os.path.exists(folder + self.testfile) is False:
                try:
                    conn = db.create_connection()
                    tresult = db.execute_query(conn, f"SELECT fileid FROM tests WHERE id={self.testid}")
                    if tresult:
                        f = files.File()
                        f.get(tresult[0][0], f'testfiles/{self.testfile}')
                except Exception:
                    self.task.msg = QMessageBox(self)
                    self.task.msg.critical(self, "Ошибка ", "Не удалось скачать файл теста. Повторите попытку позже.",
                                      QMessageBox.Ok)

            self.questions_list = self.read_from_file(self.testfile)
            self.questions_number = self.questions_list[0]
            self.minutes = int(self.questions_list[-1][0])
            self.seconds = int(self.questions_list[-1][1])
            i = 0
            path = os.getcwd()
            f = self.testfile.replace('/', '\\')
            os.remove(path + '\\testfiles\\' + f)
            self.timer = Processor(self.minutes, self.seconds)
            self.timer.signal.connect(lambda: self.timeout())
            self.new(i)
        except Exception:
            self.msg = QMessageBox(self)
            self.msg.critical(self, "Ошибка ", "Не удалось найти тест. Повторите попытку позже.", QMessageBox.Ok)

    def timeout(self):
        self.msg = QMessageBox(self.task)
        self.msg.warning(self.task, "StudyLang", "Время вышло!", QMessageBox.Ok)
        self.task.close()
        self.show_task(self.questions_number + 1)

    def show_task(self, i):
        current_task = self.questions_list[i]
        if (len(current_task) == 5 and current_task[0] == 'Оценки'):
            self.timer.timer_window.close()
            with open(f'answerfiles/{self.filename}', 'a', encoding='utf-8') as file:
                file.write(f'Общее количество баллов: {self.wholescore}' + '\n')
            try:
                f = files.File()
                answerfileid = f.post(self.filename, f'answerfiles/{self.filename}', 'answers')
                conn = db.create_connection()
                query = f"UPDATE testing SET answerfileid='{answerfileid}' WHERE id={self.answer_id}"
                db.execute_query(conn, query, 'insert')
                path = os.getcwd()
                try:
                    os.remove(path + '\\answerfiles\\' + self.filename)
                except OSError as e:
                    logging.error("Failed with:", e.strerror)
            except Exception:
                self.msg = QMessageBox(self)
                self.msg.critical(self, "Ошибка ", "Не удалось загрузить ваш файл на сервер.", QMessageBox.Ok)
            self.task = doing_end.ThisWindow(self.answer_id, self.wholescore, current_task)
            self.task.switch_end.connect(lambda: self.controller.end_testing(self.task))

        #elements order in ifo: i, question_type, answer_type, question, mediafile, [variants], rightanswer, score (mediafile and variants are optional)
        #arguments in showtaskWindow: self, question_type, answer_type, i, question, rightanswers, maxscore, mediafile=None, variants=None
        elif current_task[0] == 'Текст' and current_task[1] == 'Установить соответствие':
            self.task = tasks_windows.ThisWindow(f'answerfiles/{self.filename}', 'text', 'match', *current_task[2:])
            self.task.do_task_end.connect(lambda: self.show_score(self.task.acomponents.score, i))
        elif current_task[0] == 'Текст' and current_task[1] == 'Выбрать один правильный ответ':
            self.task = tasks_windows.ThisWindow(f'answerfiles/{self.filename}', 'text', 'one', *current_task[2:6],
                                                 variants=current_task[6])
            self.task.do_task_end.connect(lambda: self.show_score(self.task.acomponents.score, i))
        elif current_task[0] == 'Текст' and current_task[1] == 'Выбрать несколько правильных ответов':
            self.task = tasks_windows.ThisWindow(f'answerfiles/{self.filename}', 'text', 'many', *current_task[2:6],
                                                 variants=current_task[6])
            self.task.do_task_end.connect(lambda: self.show_score(self.task.acomponents.score, i))
        elif current_task[0] == 'Изображение' and current_task[1] == 'Установить соответствие':
            self.task = tasks_windows.ThisWindow(f'answerfiles/{self.filename}', 'image', 'match', *current_task[2:])
            self.task.do_task_end.connect(lambda: self.show_score(self.task.acomponents.score, i))
        elif current_task[0] == 'Изображение' and current_task[1] == 'Выбрать один правильный ответ':
            self.task = tasks_windows.ThisWindow(f'answerfiles/{self.filename}', 'image', 'one', *current_task[2:])
            self.task.do_task_end.connect(lambda: self.show_score(self.task.acomponents.score, i))
        elif current_task[0] == 'Изображение' and current_task[1] == 'Выбрать несколько правильных ответов':
            self.task = tasks_windows.ThisWindow(f'answerfiles/{self.filename}', 'image', 'many', *current_task[2:])
            self.task.do_task_end.connect(lambda: self.show_score(self.task.acomponents.score, i))
        elif current_task[0] == 'Аудио' and current_task[1] == 'Установить соответствие':
            self.task = tasks_windows.ThisWindow(f'answerfiles/{self.filename}', 'audio', 'match', *current_task[2:])
            self.task.do_task_end.connect(lambda: self.show_score(self.task.acomponents.score, i))
        elif current_task[0] == 'Аудио' and current_task[1] == 'Выбрать один правильный ответ':
            self.task = tasks_windows.ThisWindow(f'answerfiles/{self.filename}', 'audio', 'one', *current_task[2:])
            self.task.do_task_end.connect(lambda: self.show_score(self.task.acomponents.score, i))
        elif current_task[0] == 'Аудио' and current_task[1] == 'Выбрать несколько правильных ответов':
            self.task = tasks_windows.ThisWindow(f'answerfiles/{self.filename}', 'audio', 'many', *current_task[2:])
            self.task.do_task_end.connect(lambda: self.show_score(self.task.acomponents.score, i))
        self.task.show()

    def new(self, i):
        i += 1
        if hasattr(self, 'task'):
            self.task.close()
        Showtask.show_task(self, i)

    def show_score(self, score, i):
        p = float(score)
        self.wholescore += p
        self.task.close()
        self.new(i)

    def insertToDB(self):
        try:
            conn = db.create_connection()
            max_testing_id = db.execute_query(conn, "SELECT max(id) FROM testing")[0][0]
            if max_testing_id == None:
                self.answer_id = '1'
            else:
                self.answer_id = str(int(max_testing_id) + 1)

            path = os.getcwd()
            folder = path + '\\answerfiles\\'
            if os.path.exists(folder) is False:
                os.mkdir(folder)
            self.filename = f"Test{self.answer_id}.txt"
            now = datetime.now()
            date = now.strftime("%Y-%m-%d %H:%M")
            query = ("INSERT INTO testing (ID, TESTID, DATE, ANSWERFILEID) VALUES "
                     f"({self.answer_id}, '{self.testid}', '{date}', '{self.filename}')")
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
                if line.find('Оценка') != -1:
                    marks.append('Оценки')
                    while line.find('Максимальное количество баллов:') == -1:
                        max_score = line[9:].strip()
                        marks.append(max_score)
                        i += 1
                        line = lines[i]
                    max_score = line[31:].strip()
                    marks.append(max_score)
                    i += 1
                    line = lines[i]
                    if line.find('Время теста:') != -1:
                        time = line[12:].strip().split(' ')
                    break
                elif line.find('Вопрос #') != -1:
                    qnum = int(line[8:].strip())
                elif line.find('Тип вопроса:') != -1:
                    qtype = line[12:].strip()
                elif line.find('Тип ответа:') != -1:
                    atype = line[11:].strip()
                elif line.find('Вопрос:') != -1:
                    q = line[7:].strip()
                elif line.find('Имя файла:') != -1:
                    img_or_audio = line[10:].strip()
                elif line.find('Вариант1:') != -1:
                    v1 = line[9:].strip()
                    variants.append(v1)
                    i += 1
                    line = lines[i]
                    while line.find('Вариант') != -1:
                        v = lines[i][9:].strip()
                        variants.append(v)
                        i += 1
                        line = lines[i]
                elif line.find('Соответствие1:') != -1:
                    while line.find('Соответствие') != -1:
                        kend = line.find(';')
                        k = line[14:kend].strip()
                        v = line[kend + 1:].strip()
                        dictmatch.update({k: v})
                        i += 1
                        line = lines[i]
                if line.find('Максимальный балл:') != -1:
                    score = line[18:].strip()
                    i += 1
                    line = lines[i]
                if line.find('Правильный ответ:') != -1:
                    answer = line[17:].strip()
                if line.find('Правильные ответы:') != -1:
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

class Show_task_Controller:

    def __init__(self, testid, userid):
        Showtask(self, testid, userid)

    def end_testing(self, window):
        window.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    import logging
    logging.basicConfig(filename='logs.log', encoding='utf-8', level=logging.DEBUG)
    testid = '14'
    #test = Showtask(testid, '1')
    controller = Show_task_Controller(testid, '1')
    sys.exit(app.exec_())
