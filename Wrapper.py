import ReadSwitch, EndDo, sys
from PyQt5.QtWidgets import QApplication

class Wrapp():

    def __init__(self, test, score, marks):
        self.score = score
        self.testid = test
        self.marks = marks
        self.obj = ReadSwitch.Showtask('12', '1')
        self.obj.switch_timeout.connect(lambda: self.new())

    def new(self):
        self.wrapp.close()
        o = EndDo.ThisWindow(self.testid, self.score, self.marks)

if __name__=="__main__":
    app = QApplication(sys.argv)
    #myapp = ThisWindow(15, 7.0, ['Оценки', '8', '5', '3', '10'])
    myapp = Wrapp(63, 0, ['Оценки', '3', '0', '0', '3'])
    sys.exit(app.exec_())