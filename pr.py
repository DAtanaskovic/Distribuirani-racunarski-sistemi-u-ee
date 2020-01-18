from PyQt5.QtWidgets import (QWidget, QHBoxLayout,
                             QLabel, QApplication, QPushButton, QInputDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import sys
from Zid import *
from App import *
from Igrac import *
from IgracApp import *

class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.trenutniPobednik = Value('i', 0)
        self.trenutniIgrac1 = Value('i', 0)
        self.trenutniIgrac2 = Value('i', 0)

        self.hbox = QHBoxLayout(self)
        self.pixmap = QPixmap("pocetna.png")

        self.lbl = QLabel(self)
        self.lbl.setPixmap(self.pixmap)

        self.hbox.addWidget(self.lbl)
        self.setLayout(self.hbox)

        self.move(50, 50)
        self.setWindowTitle('Cub Chase')

        self.btn = QPushButton('Start', self)
        self.btn.move(170, 250)
        self.btn.clicked.connect(self.doAction)
        self.btn.clicked.connect(self.hide)
        self.btn.setStyleSheet("background-color: green; color: yellow; font: 15pt ")

        self.btn1 = QPushButton('Turnir', self)
        self.btn1.move(170, 300)
        self.btn1.clicked.connect(self.Turnir)
        #self.btn.clicked.connect(self.hide)
        self.btn1.setStyleSheet("background-color: green; color: yellow; font: 15pt ")
        #self.btn.style

        self.text = QLineEdit(self)
        self.text.move(80, 120)
        self.text.hide()

        #self.setFixedSize(400, 400)

        self.show()

    def doAction(self):
        theApp = App()
        theApp.on_execute()

    def Turnir(self):
        t, ok = QInputDialog.getText(
            self, 'Input Dialog', self.text.text())

        if ok:
            self.text.setText(str(t))
            self.pocni_turnir()

if __name__ == '__main__':

     app = QApplication(sys.argv)
     ex = Example()
     sys.exit(app.exec_())