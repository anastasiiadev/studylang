import sys
import choosing_test, doing_test
from PyQt5.QtWidgets import QApplication



class Controller:

    def __init__(self, user_id):
        self.user_id = user_id
        self.choosing_test = choosing_test.ThisWindow()
        self.choosing_test.switch_choosetest.connect(lambda: self.do_test())
        self.choosing_test.show()

    def do_test(self):
        self.choosing_test.close()
        self.doing_test = doing_test.Showtask(self.choosing_test.gettestid, self.user_id)


if __name__=="__main__":
    app = QApplication(sys.argv)
    import logging
    logging.basicConfig(filename='logs.log', encoding='utf-8', level=logging.DEBUG)
    controller = Controller('1')
    sys.exit(app.exec_())
