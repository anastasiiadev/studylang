#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import mysql.connector
from autorisationInt import *
from PyQt5 import QtCore, QtGui, QtWidgets
from mysql.connector import errorcode


try:
    cnn = mysql.connector.connect(
        user='root',
        password='root',
        host='localhost',
        database='studylang')
    print("It works!")
except mysql.connector.Error as e:
    if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with username ot password")
    elif e.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database doesn't exist")
    else:
        print(e)

cursor = cnn.cursor()



class MyWin(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #кнопка
        self.ui.pushButton.clicked.connect(self.Autorise)

    # Описываем функцию
    def Autorise(self):

        # В переменную stroki получаем текст из левого поля ввода
        file = self.ui.textEdit_2.toPlainText()
        password = self.ui.textEdit.toPlainText()

        query = "SELECT filename FROM tests"
        cursor.execute(query)
        result = cursor.fetchall()
        print(result)
        files = []
        for el in result:
            tmp = str(el)
            length = len(tmp)
            newLog = tmp[2:(length-3)]
            files.append(newLog)
        print(files)


        flag = 0
        for el in files:
            if(file == el):
                print("File is correct!")
                flag = 1
                break
        if (flag == 0):
            pic=file


        hbox = QHBoxLayout(self)
        pixmap = QPixmap(pic)
        lbl = QLabel(self)
        lbl.setPixmap(pixmap)
        hbox.addWidget(lbl)
        self.setLayout(hbox)

        self.move(100, 200)
        self.setWindowTitle('Red Rock')
        self.show()


if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())

cnn.close()



'''
name = "C:\Files\O1btOzifsw.jpg"
f = open('C:\Files\FirstFile.txt', 'w')
f.write(name + '\n')
f.close()


f = open('C:\Files\FirstFile.txt', 'r')
line = f.readline()
while line:
    print(line),
    line = f.readline()
f.close()
'''

