import sys
import ChooseTest, ReadSwitch
from PyQt5.QtWidgets import QApplication



class Controller:

    def __init__(self, user_id):
        self.user_id = user_id
        self.show_task()

    def show_task(self):
        self.choose = ChooseTest.ThisWindow()
        self.choose.switch_choosetest.connect(lambda: self.dotest())
        self.choose.show()

    def dotest(self):
        self.choose.close()
        self.window = ReadSwitch.Showtask(self.choose.gettestid, self.user_id)



if __name__=="__main__":
    app = QApplication(sys.argv)
    controller = Controller('1')
    sys.exit(app.exec_())
