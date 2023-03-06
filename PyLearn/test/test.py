import sys

from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget
from ui_widget import Ui_Widget
import resource_rc

class Widget(QWidget, Ui_Widget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("User data")
        self.pushButton.clicked.connect(self.do_something)
        
    def do_something(self):
        print(self.lineEdit.text()," is a ",self.lineEdit_2.text())



app = QtWidgets.QApplication(sys.argv)

window = Widget()
window.show()

app.exec()