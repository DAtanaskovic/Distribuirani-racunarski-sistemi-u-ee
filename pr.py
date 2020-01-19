from PyQt5.QtWidgets import (QWidget, QHBoxLayout,
                             QLabel, QApplication, QPushButton, QInputDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import sys
from Zid import *
from App import *
from Igrac import *
from IgracApp import *
import AppOnlineNetwork

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

        #za play online
        self.btn1 = QPushButton('Play online', self)
        self.btn1.move(170, 350)
        self.btn1.clicked.connect(self.doOnline)
        self.btn1.setStyleSheet("background-color: green; color: yellow; font: 15pt ")



        self.text = QLineEdit(self)
        self.text.move(80, 120)
        self.text.hide()

        #self.setFixedSize(400, 400)

        self.show()

    def doAction(self):
        theApp = App()
        theApp.on_execute()
    def doOnline(self):
        online=AppOnlineNetwork.Apponline()
        online.on_execute()
    def Turnir(self):
        t, ok = QInputDialog.getText(
            self, 'Input Dialog', self.text.text())

        if ok:
            self.text.setText(str(t))
            self.pocni_turnir()

    def pocni_turnir(self):
        ukupan_broj_igraca = int(self.text.text())

        lista = []

        for i in range(1, ukupan_broj_igraca+1):
            lista.append(str(i))

        lista_igraca = lista
        lista_za_sledeci_nivo = lista
        igrac1 = lista_igraca[0]
        igrac2 = lista_igraca[1]

        while True:
            lista_igraca = lista_za_sledeci_nivo
            igrac1 = lista_igraca[0]
            igrac2 = lista_igraca[1]
            self.trenutniIgrac1.value = int(igrac1)
            self.trenutniIgrac2.value = int(igrac2)
            print('lsn',lista_za_sledeci_nivo)
            lista_za_sledeci_nivo = []
            print(lista_igraca)
            while len(lista_igraca) >= 2:
                self.p1 = multiprocessing.Process(target=turnir_proces, args=(self.trenutniPobednik, self.trenutniIgrac1, self.trenutniIgrac2))
                self.p1.start()
                self.p1.join()
                lista_igraca.remove(igrac1)
                lista_igraca.remove(igrac2)
                if(self.trenutniPobednik.value == 1):
                    lista_za_sledeci_nivo.append(igrac1)
                else:
                    lista_za_sledeci_nivo.append(igrac2)

            if len(lista_igraca) == 1:
                lista_za_sledeci_nivo.append(lista_igraca[0])

            if(len(lista_za_sledeci_nivo) == 1):
                print('Kraj turnira')
                print('Pobednik turnira je ' + lista_za_sledeci_nivo[0])
                break

def turnir_proces(trenutniPobednik, trenutniIgrac1, trenutniIgrac2):
    theApp = App()
    theApp.brojIgraca1 = trenutniIgrac1.value
    theApp.brojIgraca2 = trenutniIgrac2.value
    theApp.on_execute()
    pobednik = theApp.pobednik()
    trenutniPobednik.value = pobednik
    print('Pobednik je igrac', pobednik)

if __name__ == '__main__':

     app = QApplication(sys.argv)
     ex = Example()
     sys.exit(app.exec_())