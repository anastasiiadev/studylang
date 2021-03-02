import sys
from PyQt5.QtWidgets import QApplication

import choosing_test
import doing_test


class Controller:

    """
    Объект класса вызывает окно выбора теста и далее вызывает контроллер прохождения тестирования.
    """

    def __init__(self, user_id):

        """
        :param user_id: идентификатор пользователя в БД, которому необходимо пройти тестирование
        Отрывается окно выбора теста.
        """

        self.user_id = user_id
        self.choosing_test = choosing_test.ThisWindow()
        self.choosing_test.switch_choosetest.connect(lambda: self.do_test())
        self.choosing_test.show()

    def do_test(self):

        """
        Закрывается окно выбора теста и вызывается контроллер тестирования,
        которому передаются id теста и id пользователя для прохождения тестирования.
        """

        self.choosing_test.close()
        self.doing_test = doing_test.Show_Test_Controller(self.choosing_test.gettestid, self.user_id)


if __name__=="__main__":
    app = QApplication(sys.argv)
    controller = Controller('1')
    sys.exit(app.exec_())
