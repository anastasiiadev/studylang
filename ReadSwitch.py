import sys, mysql.connector, datetime, random, os, threading, TimerWindow
from datetime import datetime, timedelta
import Show_TMCH, Show_TO, Show_TM, Show_IMCH, Show_IO, Show_IM, Show_AMCH, Show_AO, Show_AM, EndDo
from PyQt5.QtWidgets import QApplication, QMessageBox, QWidget
from PyQt5.QtCore import QThread, pyqtSignal
from mysql.connector import errorcode
from ftplib import FTP


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
        self.task = QWidget()
        self.user_id = user_id
        self.wholescore = 0
        self.testid = ''
        self.end = 0
        rows = self.insertToDB(testid)
        if rows == 1:
            path = os.getcwd()
            folder = path + '\\testfiles\\'
            if os.path.exists(folder) is False:
                os.mkdir(folder)
            self.testfile = "Test{}.txt".format(testid)
            if os.path.exists(folder + self.testfile) is False:
                try:
                    ftp = FTP()
                    ftp.set_debuglevel(2)
                    ftp.connect('stacey789.beget.tech', 21)
                    ftp.login('stacey789_ftp', 'StudyLang456987')
                    ftp.encoding = 'utf-8'
                    ftp.cwd('/testfiles')
                    download = ftp.retrbinary("RETR " + self.testfile, open(folder + self.testfile, 'wb').write)
                    ftp.close()
                except Exception:
                    self.msg = QMessageBox(self)
                    self.msg.critical(self, "Ошибка ", "Не удалось скачать файл теста. Повторите попытку позже.",
                                      QMessageBox.Ok)
            else:
                download = 'File is already in the directory'
            if 'download' in locals():
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
        else:
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
            with open('answerfiles/{}'.format(self.filename), 'a', encoding='utf-8') as file:
                file.write('Общее количество баллов: %s' % self.wholescore + '\n')
            file.close()
            try:
                ftp = FTP()
                ftp.set_debuglevel(2)
                ftp.connect('stacey789.beget.tech', 21)
                ftp.login('stacey789_ftp', 'StudyLang456987')
                ftp.encoding = 'utf-8'
                ftp.cwd('/answerfiles')
                fp = open('answerfiles/{}'.format(self.filename), 'rb')
                send = ftp.storbinary('STOR %s' % self.filename, fp, 1024)
                fp.close()
            except Exception:
                self.msgnofile = QMessageBox(self)
                self.msgnofile.critical(self, "Ошибка ", "Не удалось загрузить ваш файл.", QMessageBox.Ok)
            if 'send' in locals():
                path = os.getcwd()
                try:
                    os.remove(path + '\\answerfiles\\' + self.filename)
                except OSError as e:
                    print("Failed with:", e.strerror)
            self.task = EndDo.ThisWindow(self.testid, self.wholescore, el)
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
            self.task = Show_IMCH.ThisWindow(el[0], i, el[3], el[4], 'answerfiles/{}'.format(self.filename), el[5], el[6])
            self.task.switch_imch.connect(lambda: self.show_score(self.task.score, i))
        elif el[1] == 'Изображение' and el[2] == 'Выбрать один правильный ответ':
            self.task = Show_IO.ThisWindow(el[0], i, el[3], el[4], el[5], 'answerfiles/{}'.format(self.filename), el[6], el[7])
            self.task.switch_io.connect(lambda: self.show_score(self.task.score, i))
        elif el[1] == 'Изображение' and el[2] == 'Выбрать несколько правильных ответов':
            self.task = Show_IM.ThisWindow(el[0], i, el[3], el[4], el[5], 'answerfiles/{}'.format(self.filename), el[6], el[7])
            self.task.switch_im.connect(lambda: self.show_score(self.task.score, i))
        elif el[1] == 'Аудио' and el[2] == 'Установить соответствие':
            self.task = Show_AMCH.ThisWindow(el[0], i, el[3], el[4], 'answerfiles/{}'.format(self.filename), el[5], el[6])
            self.task.switch_amch.connect(lambda: self.show_score(self.task.score, i))
        elif el[1] == 'Аудио' and el[2] == 'Выбрать один правильный ответ':
            self.task = Show_AO.ThisWindow(el[0], i, el[3], el[4], el[5], 'answerfiles/{}'.format(self.filename), el[6], el[7])
            self.task.switch_ao.connect(lambda: self.show_score(self.task.score, i))
        elif el[1] == 'Аудио' and el[2] == 'Выбрать несколько правильных ответов':
            self.task = Show_AM.ThisWindow(el[0], i, el[3], el[4], el[5], 'answerfiles/{}'.format(self.filename), el[6], el[7])
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

    def insertToDB(self, testid):
        try:
            cnn = mysql.connector.connect(
                host='stacey789.beget.tech',
                database='stacey789_db',
                user='stacey789_db',
                password='StudyLang_user789',
                port=3306)
        except mysql.connector.Error as e:
            if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with username or password")
            elif e.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database doesn't exist")
            else:
                print(e)
        self.cursor = cnn.cursor()

        self.cursor.execute("SELECT max(id) FROM testing")
        result = self.cursor.fetchall()
        max = result[0][0]
        if max == None:
            n = 1
        else:
            n = int(max) + 1
        self.testid = str(n)

        path = os.getcwd()
        folder = path + '\\answerfiles\\'
        if os.path.exists(folder) is False:
            os.mkdir(folder)
        self.filename = "Test%s.txt" % n
        now = datetime.now()
        date = now.strftime("%d-%m-%Y %H:%M")
        self.cursor.execute("INSERT INTO testing (ID, TEST_ID, DATE, ANSWER_FILE) VALUES "
                            "({}, '{}', '{}', '{}')".format(n, testid, date, self.filename))
        cnn.commit()

        self.cursor.execute("SELECT max(id) FROM work")
        result = self.cursor.fetchall()
        max = result[0][0]
        if max == None:
            id = 1
        else:
            id = int(max) + 1
        self.cursor.execute("INSERT INTO work (ID, PERSON_ID, TRIAL_OR_TEST_ID, MODE) VALUES "
                            "({}, '{}', '{}', '{}')".format(id, int(self.user_id), n, 2))
        cnn.commit()

        cnn.close()
        return self.cursor.rowcount

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


if __name__=="__main__":
    app = QApplication(sys.argv)
    testid = '1'
    test = Showtask(testid, '1')
    sys.exit(app.exec_())
