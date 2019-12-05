from PyQt5.QtWidgets import (QWidget, QHBoxLayout,
                             QLabel, QApplication, QPushButton)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import sys
from Zid import *

listaZidova = pygame.sprite.Group()  # create static walls group


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
        self.pixmap = QPixmap("pozadina.jpg")
        self.lbl.setPixmap(self.pixmap)
        self.btn.hide()
        self.world = pygame.display.set_mode([800, 600])

        self.backdrop = pygame.image.load('pozadina.jpg')
       # self.rect = self.backdrop.get_rect()
       # backdropbox = world.get_rect()
        for x in range(0, 800, 40):
            z = Zid(x, 0)
            listaZidova.add(z)

        for x in range(0, 800, 40):
            z = Zid(0, x)
            listaZidova.add(z)

        for x in range(0, 800, 40):
            z = Zid(760, x)
            listaZidova.add(z)

        for x in range(0, 800, 40):
            z = Zid(x, 560)
            listaZidova.add(z)

        listaZidova.draw(self.world)
        pygame.display.flip()

        self.world.blit(self.backdrop, (800, 600))
        pygame.display.update()
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())