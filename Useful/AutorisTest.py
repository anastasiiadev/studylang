import mysql.connector
from Useful.autorisationInt import *
from PyQt5 import QtWidgets
from mysql.connector import errorcode


try:
    cnn = mysql.connector.connect(
        user='root',
        password='Studydb789',
        host='127.0.0.1',
        port=3306,
        database='studylang')
    print("It works!")
except mysql.connector.Error as e:
    if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with username or password")
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
        login=self.ui.textEdit_2.toPlainText()
        password = self.ui.textEdit.toPlainText()

        query = "SELECT login FROM people"
        cursor.execute(query)
        result = cursor.fetchall()
        print(result)
        logins = []
        for el in result:
            tmp = str(el)
            length = len(tmp)
            newLog = tmp[2:(length-3)]
            logins.append(newLog)
        print(logins)


        query = "SELECT password FROM people WHERE password='orlov123'"
        cursor.execute(query)
        result = cursor.fetchall()
        # Преобразуем пароль
        tmp = str(result)
        length = len(tmp)
        newPas = tmp[3:(length - 4)]

        flag = 0
        for el in logins:
            if(login == el):
                print("Login is correct!")
                flag = 1
                break
        if (flag == 0):
            print("Login fail")

        if(password == newPas):
            print("Password is correct")
        else:
            print("Password fail")


if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())

cnn.close()
