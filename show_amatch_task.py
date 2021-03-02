import sys
import random
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QApplication, QPushButton, QMessageBox
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QDrag, QPixmap, QPainter
from PyQt5.QtCore import Qt, QMimeData


class DragLabel(QLabel):

    """
    Класс, реализующий надпись, которую можно перетаскивать.
    """

    # def mousePressEvent(self, event):
    #
    #     """
    #     :param event: событие (ожидается нажатие на кнопку)
    #     В атрибут drag_start_position сохраняется координата элемента,
    #         на который нажал пользователь.
    #     """
    #
    #     if event.button() == Qt.LeftButton:
    #         self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):

        """
        :param event: event: событие (ожидается нажатие на кнопку)
        Надпись, на которую нажал пользователь, копируется (прямоугольная область) и перетаскивается следом за курсором.
        """

        if not (event.buttons() & Qt.LeftButton):
            return
        else:
            drag = QDrag(self)

            mimedata = QMimeData()
            mimedata.setText(self.text())

            drag.setMimeData(mimedata)

            # creating the dragging effect
            pixmap = QPixmap(self.size())

            painter = QPainter(pixmap)
            painter.drawPixmap(self.rect(), self.grab())
            painter.end()

            drag.setPixmap(pixmap)
            drag.setHotSpot(event.pos())
            drag.exec_(Qt.CopyAction | Qt.MoveAction)


class DropLabel(QLabel):

    """
    Класс, объектами которого являются надписи, куда перетаскиваются другие надписи.
    """

    def __init__(self, label, parent):

        """
        :param label: надпись (текст)
        :param parent: родительский виджет
        Разрешается собитие отпускания мыши.
        """

        super().__init__(label, parent)
        self.setAcceptDrops(True)


    def dragEnterEvent(self, event):

        """
        Указываем, что пользователь может отпустить переносимый объект в данном виджете.
        :param event: событие (ожидается перетаскивание)
        """

        if event.mimeData().hasText():
            event.acceptProposedAction()


    def dropEvent(self, event):

        """
        :param event: событие (ожидается перетаскивание)
        Текст надписи меняется на перетаскиваемый текст.
        """
        text = event.mimeData().text()
        self.setText(text)
        self.setFont(QtGui.QFont("Century Gothic", 11, QtGui.QFont.Bold))
        event.acceptProposedAction()



class AMatch(QWidget):

    """
    Виджет, реализующий часть окна для ответа типа "Установить соответствие".
    """

    do_task_end = QtCore.pyqtSignal()

    def __init__(self, i, filename, d, maxscore):

        """
        :param i: номер задания
        :param filename: имя файла ответа пользователя
        :param d: словарь с верными соответствиями
        :param maxscore: максимальный балл за данное задание
        """

        super().__init__()
        self.n = i
        self.filename = filename
        self.dict = d
        self.rightanswers = ''
        self.maxscore = int(maxscore)
        self.score = 0
        self.initUI()


    def initUI(self):

        """
        Установка трёх столбцов:
        1 столбец - первые части соответствий;
        2 столбец - места, куда нужно перетащить вторые части соответствий
        3 столбец - вторые част исоответствий, расположенные в рандомном порядке
        """

        # new type
        self.values = []
        for v in self.dict.values():
            self.values.append(v)
        random.shuffle(self.values)
        i = 1
        for el in self.values:
            exec(f'self.lbl_to_drag{i} = DragLabel(el, self)')
            i += 1
        i = 1
        for key in self.dict.keys():
            exec(f'self.lbl{i} = QLabel(key, self)')
            i += 1

        self.matches_number = len(self.dict)
        self.mainbox = QVBoxLayout(self)
        self.abox = QHBoxLayout(self)

        #вертикальная колонка с первой частью соответсвия
        self.firstpart = QVBoxLayout(self)
        for element in range(1, self.matches_number + 1):
            exec(f'self.lbl{element}.setFont(QtGui.QFont("Century Gothic", 11, QtGui.QFont.Bold))')
            exec(f'self.lbl{element}.adjustSize()')
            exec(f'self.firstpart.addWidget(self.lbl{element}, alignment=QtCore.Qt.AlignCenter)')
        self.abox.addLayout(self.firstpart)

        #вертикальная колонка, куда нужно переместить вторую часть соответсвия
        self.placetoput = QVBoxLayout(self)
        self.placetoput.addStretch(1)
        for element in range(1, self.matches_number + 1):
            exec(f'self.lbl_to_drop{element} = DropLabel("Перетащите ответ сюда", self)')
            exec(f'self.lbl_to_drop{element}.setFont(QtGui.QFont("Century Gothic", 11))')
            exec(f'self.lbl_to_drop{element}.adjustSize()')
            exec(f'self.placetoput.addWidget(self.lbl_to_drop{element}, alignment=QtCore.Qt.AlignCenter)')
            exec(f'self.placetoput.addStretch(1)')
        self.abox.addLayout(self.placetoput)

        # вертикальная колонка со второй частью соответсвия
        self.secondpart = QVBoxLayout(self)
        self.secondpart.addStretch(1)
        for element in range(1, self.matches_number + 1):
            exec(f'self.lbl_to_drag{element}.setFont(QtGui.QFont("Century Gothic", 11))')
            exec(f'self.lbl_to_drag{element}.adjustSize()')
            exec(f'self.secondpart.addWidget(self.lbl_to_drag{element}, alignment=QtCore.Qt.AlignCenter)')
            exec(f'self.secondpart.addStretch(1)')
        self.abox.addLayout(self.secondpart)

        self.mainbox.addSpacing(30)
        self.mainbox.addLayout(self.abox)
        self.btn = QPushButton('OK', self)
        self.mainbox.addSpacing(30)
        self.mainbox.addWidget(self.btn, alignment=QtCore.Qt.AlignCenter)
        self.setLayout(self.mainbox)

        #self.btn.clicked.connect(self.WriteToFile)


    def WriteToFile(self):

        """
        Проверка, для всех ли соответствий были указаны вторые части.
        Ответы пользователя и баллы записываются в файл с ответом.
        Атрибут score - набранный балл
        """

        permission = 0
        for el in range(1, self.matches_number + 1):
            exec(f'self.a{el} = self.lbl_to_drop{el}.text()')
            exec(f'globals()["firstpart{el}"] = self.lbl{el}.text()')
            exec(f'globals()["current"] = self.a{el}')
            if current == "Перетащите ответ сюда":
                self.msgnum = QMessageBox(self)
                self.msgnum.critical(self, "Ошибка ", "Пожалуйста, укажите ваш ответ.", QMessageBox.Ok)
                break
            else:
                permission += 1
        if permission == self.matches_number:
            point = self.maxscore / self.matches_number
            with open(self.filename, 'a', encoding='utf-8') as file:
                file.write(f'Вопрос #{self.n}' + '\n')
                file.write('Ответ:\n')
                for el in range(1, self.matches_number + 1):
                    exec(f"file.write('Соответствие{el}:' + globals()['firstpart{el}'] + ' - ' + self.a{el} + '\\n')")
                    exec(f"if globals()['firstpart{el}'] in self.dict and self.a{el} == "
                         f"self.dict[globals()['firstpart{el}']]: self.score += point")

                self.score = round(self.score, 1)
                ost = self.score % 1
                if ost == 0:
                    self.score = round(self.score)
                file.write('Баллы: ' + str(self.score) + '\n')
                file.write('\n')
            self.do_task_end.emit()


if __name__=="__main__":
    app = QApplication(sys.argv)
    myapp = AMatch(3, 'answerfiles/Test2.txt', {'Бейонсе': 'Джей Зи', 'Ким Кардашьян': 'Кенью Уэст'}, 2)
    myapp.show()
    sys.exit(app.exec_())
