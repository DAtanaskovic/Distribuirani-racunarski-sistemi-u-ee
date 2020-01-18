from Igrac import *
import pygame
from pygame.locals import *
from App import  *
from multiprocessing import Process, Queue, Value
from Zid import *


def igrac_proces(x, y, queue):
    #print('igracproces')
    trenutnoX = x.value
    trenutnoY = y.value
    matrica = Maze().maze
    while True:
        if not queue.empty():
            broj = queue.get()
            if(broj == 1):  # levo
                if (trenutnoX - 40 >= 0):
                    broj = (trenutnoX - 40) / 40 + trenutnoY / 40 * 20
                    # print(broj)
                    if (matrica[int(broj)] != 1):  # ovde je sad potrebno proveriti matricu
                        # postavljanje slike lava na novu poziciju
                        #if (self.matrica[int(self.x / 40 + self.y / 40 * 20)] != 9):  postavljanje tragova
                        #  self._display_surf.blit(self.tragovi, (self.x, self.y))
                        # provera da li je zamka
                        trenutnoX = trenutnoX - 40
                        trenutnoY = trenutnoY
                        #update prikaza
            if(broj == 2):  # desno
                if (trenutnoX + 40 <= 760):
                    broj = (trenutnoX + 40) / 40 + trenutnoY / 40 * 20
                    if (matrica[int(broj)] != 1):
                        trenutnoX = trenutnoX + 40
                        trenutnoY = trenutnoY
            if(broj == 3):  # gore
                if (trenutnoY - 40 >= 0):
                    broj = trenutnoX / 40 + (trenutnoY - 40) / 40 * 20
                    if (matrica[int(broj)] != 1):
                        trenutnoY = trenutnoY - 40
            if(broj == 4):  # dole
                #print('dole')
                if (trenutnoY + 40 <= 560):
                    broj = trenutnoX / 40 + (trenutnoY + 40) / 40 * 20
                    if (matrica[int(broj)] != 1):
                        trenutnoY = trenutnoY + 40
            x.value = trenutnoX
            y.value = trenutnoY
           # print('iz procesa', x.value, y.value)

