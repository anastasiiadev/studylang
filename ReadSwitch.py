import sys, datetime, random, os, threading, TimerWindow
from datetime import datetime, timedelta
from PyQt5.QtWidgets import QApplication, QMessageBox, QWidget
from PyQt5.QtCore import QThread, pyqtSignal

import Show_TMCH, Show_TO, Show_TM, Show_IMCH, Show_IO, Show_IM, Show_AMCH, Show_AO, Show_AM, EndDo
import files
import dbinteraction as db


class Processor(QThread):
    signal = pyqtSignal()

    def __init__(self, m, s):
        super().__init__()
        self.begin = timedelta(minutes=m, seconds=s)
        self.window = TimerWindow.Window(self.begin)
        self.run()

    def run(self):
        if self.begin == timedelta(seconds=0):
            self.window.close()
            self.signal.emit()
            return
        self.begin = self.begin - timedelta(seconds=1)
        self.window.local_button_handler(self.begin)
        threading.Timer(1, self.run).start()


class Showtask:

    def __init__(self, testid, user_id):
        self.testid = testid
        self.task = QWidget()
        self.user_id = user_id
        self.wholescore = 0
        self.answerid = ''
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
                    self.msg = QMessageBox(self)
                    self.msg.critical(self, "Ошибка ", "Не удалось скачать файл теста. Повторите попытку позже.",
                                      QMessageBox.Ok)

                info = self.read_from_file(self.testfile)
                self.list = info
                print(*self.list)
                self.n = self.list[0]
                self.m = int(self.list[-1][0])
                self.s = int(self.list[-1][1])
                i = 0
                path = os.getcwd()
                f = self.testfile.replace('/', '\\')
                os.remove(path + '\\testfiles\\' + f)
                self.processor = Processor(self.m, self.s)
                self.processor.signal.connect(lambda: self.timeout())
                self.new(i)
        except Exception:
            self.msg = QMessageBox(self)
            self.msg.critical(self, "Ошибка ", "Не удалось найти тест. Повторите попытку позже.", QMessageBox.Ok)

    def timeout(self):
        self.msg = QMessageBox(self.task)
        self.msg.warning(self.task, "StudyLang", "Время вышло!", QMessageBox.Ok)
        self.task.close()
        self.show_task(self.n + 1)

    def show_task(self, i):
        el = self.list[i]
        if (len(el) == 5 and el[0] == 'Оценки'):
            with open(f'answerfiles/{self.filename}', 'a', encoding='utf-8') as file:
                file.write(f'Общее количество баллов: {self.wholescore}' + '\n')
            file.close()
            try:
                f = files.File()
                answerfileid = f.post(self.filename, f'answerfiles/{self.filename}', 'answers')
                conn = db.create_connection()
                query = f"UPDATE testing SET answerfileid='{answerfileid}' WHERE id={self.answerid}"
                db.execute_query(conn, query, 'insert')
                path = os.getcwd()
                try:
                    os.remove(path + '\\answerfiles\\' + self.filename)
                except OSError as e:
                    print("Failed with:", e.strerror)
            except Exception:
                self.msgnofile = QMessageBox(self)
                self.msgnofile.critical(self, "Ошибка ", "Не удалось загрузить ваш файл на сервер.", QMessageBox.Ok)
            self.task = EndDo.ThisWindow(self.answerid, self.wholescore, el)
            self.task.switch_end.connect(lambda: self.task.close())
            self.processor.window.close()
        elif el[1] == 'Текст' and el[2] == 'Установить соответствие':
            self.task = Show_TMCH.ThisWindow(el[0], i, el[3], 'answerfiles/{}'.format(self.filename), el[4], el[5])
            self.task.switch_tmch.connect(lambda: self.show_score(self.task.score, i))
        elif el[1] == 'Текст' and el[2] == 'Выбрать один правильный ответ':
            self.task = Show_TO.ThisWindow(el[0], i, el[3], el[4], 'answerfiles/{}'.format(self.filename), el[5], el[6])
            self.task.switch_to.connect(lambda: self.show_score(self.task.score, i))
        elif el[1] == 'Текст' and el[2] == 'Выбрать несколько правильных ответов':
            self.task = Show_TM.ThisWindow(el[0], i, el[3], el[4], 'answerfiles/{}'.format(self.filename), el[5], el[6])
            self.task.switch_tm.connect(lambda: self.show_score(self.task.score, i))
        elif el[1] == 'Изображение' and el[2] == 'Установить соответствие':
            self.task = Show_IMCH.ThisWindow(el[0], i, el[3], el[4], 'answerfiles/{}'.format(self.filename), el[5],
                                             el[6])
            self.task.switch_imch.connect(lambda: self.show_score(self.task.score, i))
        elif el[1] == 'Изображение' and el[2] == 'Выбрать один правильный ответ':
            self.task = Show_IO.ThisWindow(el[0], i, el[3], el[4], el[5], 'answerfiles/{}'.format(self.filename), el[6],
                                           el[7])
            self.task.switch_io.connect(lambda: self.show_score(self.task.score, i))
        elif el[1] == 'Изображение' and el[2] == 'Выбрать несколько правильных ответов':
            self.task = Show_IM.ThisWindow(el[0], i, el[3], el[4], el[5], 'answerfiles/{}'.format(self.filename), el[6],
                                           el[7])
            self.task.switch_im.connect(lambda: self.show_score(self.task.score, i))
        elif el[1] == 'Аудио' and el[2] == 'Установить соответствие':
            self.task = Show_AMCH.ThisWindow(el[0], i, el[3], el[4], 'answerfiles/{}'.format(self.filename), el[5],
                                             el[6])
            self.task.switch_amch.connect(lambda: self.show_score(self.task.score, i))
        elif el[1] == 'Аудио' and el[2] == 'Выбрать один правильный ответ':
            self.task = Show_AO.ThisWindow(el[0], i, el[3], el[4], el[5], 'answerfiles/{}'.format(self.filename), el[6],
                                           el[7])
            self.task.switch_ao.connect(lambda: self.show_score(self.task.score, i))
        elif el[1] == 'Аудио' and el[2] == 'Выбрать несколько правильных ответов':
            self.task = Show_AM.ThisWindow(el[0], i, el[3], el[4], el[5], 'answerfiles/{}'.format(self.filename), el[6],
                                           el[7])
            self.task.switch_am.connect(lambda: self.show_score(self.task.score, i))
        self.task.show()

    def new(self, i):
        i += 1
        if hasattr(self, 'task'):
            self.task.close()
        obj = Showtask.show_task(self, i)

    def show_score(self, score, i):
        p = float(score)
        self.wholescore += p
        self.task.close()
        self.new(i)

    def insertToDB(self):
        try:
            conn = db.create_connection()
            result = db.execute_query(conn, "SELECT max(id) FROM testing")
            max = result[0][0]
            if max == None:
                n = 1
            else:
                n = int(max) + 1
            self.answerid = str(n)

            path = os.getcwd()
            folder = path + '\\answerfiles\\'
            if os.path.exists(folder) is False:
                os.mkdir(folder)
            self.filename = f"Test{n}.txt"
            now = datetime.now()
            date = now.strftime("%d-%m-%Y %H:%M")
            query = ("INSERT INTO testing (ID, TESTID, DATE, ANSWERFILEID) VALUES "
                     f"({n}, '{self.testid}', '{date}', '{self.filename}')")
            db.execute_query(conn, query, 'insert')
            conn.commit()

            result = db.execute_query(conn, "SELECT max(id) FROM work")
            max = result[0][0]
            if max == None:
                id = 1
            else:
                id = int(max) + 1
            query = ("INSERT INTO work (ID, PERSONID, TRIAL_OR_TEST_ID, MODE) VALUES "
                     f"({id}, '{int(self.user_id)}', '{n}', '2')")
            db.execute_query(conn, query, 'insert')
            conn.commit()
            conn.close()
        except Exception as e:
            print(e)
            raise Exception


    def read_from_file(self, file):
        with open('testfiles/' + file, 'r', encoding='utf-8') as f:
            info = []
            lines = f.readlines()
            questionsnum = int(lines[0][21:].strip())
            info.append(questionsnum)
            i = 2
            variants = []
            dictmatch = {}
            img_or_audio = ''
            answer = ''
            answers = []
            marks = []
            score = ''
            time = []
            while i < len(lines):
                item = []
                a = lines[i]
                if a.find('Оценка') != -1:
                    marks.append('Оценки')
                    while a.find('Максимальное количество баллов:') == -1:
                        m = a[9:].strip()
                        marks.append(m)
                        i += 1
                        a = lines[i]
                    m = a[31:].strip()
                    marks.append(m)
                    i += 1
                    a = lines[i]
                    if a.find('Время теста:') != -1:
                        t = a[12:].strip()
                        time = t.split(' ')
                    break
                elif a.find('Вопрос #') != -1:
                    qnum = int(a[8:].strip())
                elif a.find('Тип вопроса:') != -1:
                    qtype = a[12:].strip()
                elif a.find('Тип ответа:') != -1:
                    atype = a[11:].strip()
                elif a.find('Вопрос:') != -1:
                    q = a[7:].strip()
                elif a.find('Имя файла:') != -1:
                    img_or_audio = a[10:].strip()
                elif a.find('Вариант1:') != -1:
                    v1 = a[9:].strip()
                    variants.append(v1)
                    i += 1
                    a = lines[i]
                    while a.find('Вариант') != -1:
                        v = lines[i][9:].strip()
                        variants.append(v)
                        i += 1
                        a = lines[i]
                elif a.find('Соответствие1:') != -1:
                    kend = a.find(';')
                    k = a[14:kend].strip()
                    v = a[kend + 1:].strip()
                    dictmatch.update({k: v})
                    i += 1
                    a = lines[i]
                    while a.find('Соответствие') != -1:
                        kend = a.find(';')
                        k = a[14:kend].strip()
                        v = a[kend + 1:].strip()
                        dictmatch.update({k: v})
                        i += 1
                        a = lines[i]
                if a.find('Максимальный балл:') != -1:
                    score = a[18:].strip()
                    i += 1
                    a = lines[i]
                if a.find('Правильный ответ:') != -1:
                    answer = a[17:].strip()
                if a.find('Правильные ответы:') != -1:
                    ans = a[18:].strip()
                    answers = ans.split(', ')
                if a == '\n':
                    item.append(qnum)
                    item.append(qtype)
                    item.append(atype)
                    item.append(q)
                    if img_or_audio != '':
                        item.append(img_or_audio)
                    if variants:
                        item.append(variants)
                    if dictmatch:
                        item.append(dictmatch)
                    if answer != '':
                        item.append(answer)
                    if answers:
                        item.append(answers)
                    if score != '':
                        item.append(score)
                    info.append(item)
                    qnum, qtype, atype, q, img_or_audio, variants, dictmatch, answer, answers = '', '', '', '', '', [], {}, '', []
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
    testid = '1'
    test = Showtask(testid, '1')
    sys.exit(app.exec_())
