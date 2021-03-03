import sys
import logging
from PyQt5.QtWidgets import QApplication, QMessageBox

import files
import dbinteraction as db
import create_task
import test_window
import type_task_window
import creating_end
import folder


class TaskController:

    """
    Контроллер создания задания.
    """

    def __init__(self, test, n, i, filename, score):

        """
        :param test: объект контроллера создания теста
        :param n: количество вопросов в тесте
        :param i: номер текущего задания
        :param filename: имя файла с тестом
        :param score: текущее максимальное количество баллов за весь тест
        Контроллер вызывает окно выбора типа задания,
            если номер текущего задания меньше количества вопросов теста,
            или вызывает окно завершения теста в противном случае.
        """

        self.testscore = score
        self.test = test
        self.n = int(n)
        self.i = int(i)
        self.filename = filename
        if self.i > self.n:
            self.end_window = creating_end.ThisWindow(self.testscore, filename)
            self.end_window.switch_end.connect(lambda: self.test.sendtest())
            self.end_window.show()
        else:
            if self.i == 1:
                self.test.test_directory = folder.Making_Folder('\\testfiles\\')
            self.type_task = type_task_window.ThisWindow(self.i, self.filename)
            self.type_task.switch_type_task.connect(self.general)
            print('show type task window')
            self.type_task.show()


    def general(self, q, a):

        """
        Аргументы передаются из сигнала.
        :param q: тип вопроса
        :param a: тип ответа
        Закрывается окно выбора типа задания и открывается окно создания задания.
        """

        self.task = create_task.ThisWindow(self.i, self.filename, q, a)
        print('show task window')
        self.task.switch_create_task_end.connect(lambda: self.new())
        self.type_task.close()
        self.task.show()

    def new(self):

        """
        Закрывается окно создания задания.
        Общее количество баллов за тест увеличивается на количество баллов за текущее задание.
        Вызов нового контроллера задания.
        """

        print('step to NEW')
        print('score before rising:', self.testscore)
        self.task.close()
        self.testscore += int(self.task.acomponents.maxscore)
        print('in new, score: ', self.testscore)
        TestController.create_new_task(self.test, self.n, self.i + 1, self.filename, self.testscore)


class TestController:

    """
    Контроллер создания теста.
    """

    def __init__(self, user_id):

        """
        :param user_id: идентификатор пользователя в БД, создающего тест
        Отрывается окно создания теста, в котором преподавателю необходимо
            ввести название теста и количество вопросов.
        """

        self.user_id = user_id
        self.test_window = test_window.ThisWindow(self.user_id)
        self.test_window.switch_newtest.connect(lambda: self.tasks_controller())
        self.test_window.show()

    def tasks_controller(self):

        """
        Закрывается окно создания теста.
        Вызывается функция, создающая контроллер создания задания.
        """

        self.test_window.close()
        self.create_new_task(self.test_window.questions, 1, f'testfiles/{self.test_window.filename}', 0)

    def create_new_task(self, n, i, filename, score):

        """
        :param n: количество вопросов в тесте
        :param i: номер текущего задания
        :param filename: имя файла с тестом
        :param score: текущее максимальное количество баллов за весь тест
        Вызов контроллера создания задания.
        """

        self.taskcontroller = TaskController(self, n, i, filename, score)

    def sendtest(self):

        """
        Отправка файла с тестом на google-диск.
        Запись fileid (идентификатора текстового файла с тестом на google-диске) в БД в таблицу table.
        Удаление файла с тестом.
        Вызов функции, открывающей окно завершения создания теста,
            в котором необходимо указать максимальное время, отведенное на тест, и баллы для получения оценок 3, 4, 5.
        """

        try:
            f = files.File()
            fileid = f.post(self.test_window.filename, f'testfiles/{self.test_window.filename}', 'tests')
            conn = db.create_connection()
            query = f"UPDATE tests SET fileid='{fileid}' WHERE id={self.test_window.new_test_id}"
            db.execute_query(conn, query, 'insert')
        except Exception as e:
            self.msgnofile = QMessageBox(None)
            self.msgnofile.critical(None, "Ошибка ", "Не удалось загрузить ваш файл.", QMessageBox.Ok)
            logging.error(e)
        self.test_directory.remove(self.test_window.filename)
        self.taskcontroller.end_window.close()


if __name__=="__main__":
    app = QApplication(sys.argv)
    logging.basicConfig(filename='logs.log', encoding='utf-8', level=logging.DEBUG)
    controller = TestController(1)
    sys.exit(app.exec_())
