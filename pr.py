from PyQt5.QtWidgets import (QWidget, QHBoxLayout,
                             QLabel, QApplication, QPushButton)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import sys
from Zid import *
from App import *

class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.hbox = QHBoxLayout(self)
        self.pixmap = QPixmap("pocetna.jpg")

        self.lbl = QLabel(self)
        self.lbl.setPixmap(self.pixmap)

        self.hbox.addWidget(self.lbl)
        self.setLayout(self.hbox)

        self.move(50, 50)
        self.setWindowTitle('Cub Chase')

        self.btn = QPushButton('Start', self)
        self.btn.move(170, 210)
        self.btn.clicked.connect(self.doAction)
        self.btn.clicked.connect(self.hide)
        self.btn.setStyleSheet("background-color: pink; color: blue; font: 15pt")
        self.btn.style

        #self.setFixedSize(400, 400)

        self.show()

    def doAction(self):
        theApp = App()
        theApp.on_execute()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())