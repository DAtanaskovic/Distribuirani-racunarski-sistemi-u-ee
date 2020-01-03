import  pygame
from Zid import *
from Igrac import*
import IgracApp
from time import sleep
from pygame.locals import *
import  random
import multiprocessing
from multiprocessing import Process, Queue, Value
from PyQt5.QtWidgets import (QWidget, QHBoxLayout,
                             QLabel, QApplication, QPushButton)
class App:
    windowWidth = 800
    windowHeight = 600

    def __init__(self):
        self.Rezultat1 = 0
        self.Rezultat2 = 0
        self._display_surf = None
        self._block_surf = None
        self._image_surf = None
        self.maze = Maze()
        self.matrica = self.maze.maze
        self.x = Value('i', 40)
        self.y = Value('i', 0)
        self.xProslo = 40
        self.yProslo = 0
        # --- igrac2 ----
        self.x2 = Value('i', 80)
        self.y2 = Value('i', 0)
        self.x2Proslo = 80
        self.y2Proslo = 0
        # --- ---- ----
        self.Zamka1 = Value('i', 0)  # neaktivna, ako je aktivna stavljace se 1
        self.Zamka1X = 0
        self.Zamka1Y = 0
        self.Zamka2 = Value('i', 0)  # neaktivna, ako je aktivna stavljace se 1
        self.Zamka2X = 0
        self.Zamka2Y = 0
        self.Zamka3 = Value('i', 0)  # neaktivna, ako je aktivna stavljace se 1
        self.Zamka3X = 0
        self.Zamka3Y = 0
        # --------------------------------------------------------------------------
        # neprijatelji
        self.randomEnemy_x1 = 0
        self.randomEnemy_y1 = 0
        self.randomEnemy_x2 = 0
        self.randomEnemy_y2 = 0
        self.enemy1 = None
        self.enemy2 = None
        # ---------------------------------


    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth, self.windowHeight), pygame.HWSURFACE)
        self._block_surf = pygame.image.load("zid.png").convert()
        self._image_surf = pygame.image.load("lav.png").convert()
        self.tragovi = pygame.image.load("trag.jpg").convert()
        self.tragovi2 = pygame.image.load("trag2.jpg").convert()

    def on_render(self):
        self._display_surf.fill((34, 177, 76))
       # self._display_surf.blit(self._image_surf,(100, 100))
        self.maze.draw(self._display_surf, self._block_surf)
        pygame.display.flip()
        pygame.display.update()

    def on_execute(self):
        self.on_init()
        self.on_render()
        self.block = pygame.image.load("lav.png").convert()
        self._display_surf.blit(self.block, (self.x.value, self.y.value))
        self._display_surf.blit(self.block, (self.x2.value, self.y2.value))
        self.prikazi_zamke()
        self.setup_enemies_randomly()
        pygame.display.update()
        self.on_execute_Igrac()

    def on_execute_Igrac(self):
        #self.on_init()
        #if (self.on_init() == False):
           # self.running = False
            red = Queue()
            red2 = Queue()
            p1 = multiprocessing.Process(target=IgracApp.igrac_proces, args=(self.x, self.y, red))
            p2 = multiprocessing.Process(target=IgracApp.igrac_proces, args=(self.x2, self.y2, red2))
            p1.start()
            p2.start()
            clock = pygame.time.Clock()
            while (True):
                clock.tick(60)
                keys = 0
                self.osvezi_sve_zamke()
                #self.prikazi_rezultat()
                for event in pygame.event.get():
                    pygame.event.pump()
                    keys = pygame.key.get_pressed()
                    self.osvezi_prikaz()
                    kraj = self.da_li_je_kraj_nivoa()
                    if kraj:
                        p1.terminate()
                        p2.terminate()
                        p1 = multiprocessing.Process(target=IgracApp.igrac_proces, args=(self.x, self.y, red))
                        p2 = multiprocessing.Process(target=IgracApp.igrac_proces, args=(self.x2, self.y2, red2))
                        p1.start()
                        p2.start()
                    if event.type == pygame.KEYDOWN:
                        if (keys[K_RIGHT]):
                            #self.moveRight()
                            red.put(2)

                        if (keys[K_LEFT]):
                            #self.moveLeft()
                            red.put(1)

                        if (keys[K_UP]):
                            #self.moveUp()
                            red.put(3)

                        if (keys[K_DOWN]):
                            red.put(4)
                           # self.moveDown()

                        if (keys[K_d]):
                            # self.moveRight()
                            red2.put(2)

                        if (keys[K_a]):
                            # self.moveLeft()
                            red2.put(1)

                        if (keys[K_w]):
                            # self.moveUp()
                            red2.put(3)

                        if (keys[K_s]):
                            red2.put(4)
                        # self.moveDown()

                        if (keys[K_ESCAPE]):
                            self._running = False

    def moveRight(self):
        if (self.x + 40 <= 760):
            #print(broj)
            broj = (self.x + 40) / 40 + self.y / 40 * 20
            if (self.matrica[int(broj)] != 1):
                self.block = pygame.image.load("lav.png").convert()
                self._display_surf.blit(self.block, (self.x + 40, self.y))
                if (self.matrica[int(self.x / 40 + self.y / 40 * 20)] != 9):
                    self._display_surf.blit(self.tragovi, (self.x, self.y))
                self.proveri_da_je_zamka()
                self.x = self.x + 40
                self.y = self.y
                pygame.event.pump()
                pygame.display.update()

    def moveLeft(self):
        if (self.x - 40 >= 0):
            broj = (self.x - 40) / 40 + self.y / 40 * 20
           # print(broj)
            if (self.matrica[int(broj)] != 1):
                self.block = pygame.image.load("lav.png").convert()
                self._display_surf.blit(self.block, (self.x - 40, self.y))
                if (self.matrica[int(self.x / 40 + self.y / 40 * 20)] != 9):
                    self._display_surf.blit(self.tragovi, (self.x, self.y))
                self.proveri_da_je_zamka()
                self.x = self.x - 40
                self.y = self.y
                pygame.event.pump()
                pygame.display.update()

    def moveUp(self):
        if (self.y - 40 >= 0):
            broj = self.x / 40 + (self.y - 40) / 40 *20
           # print(broj)
            if (self.matrica[int(broj)] != 1):
                self.block = pygame.image.load("lav.png").convert()
                self._display_surf.blit(self.block, (self.x, self.y - 40))
                if (self.matrica[int(self.x / 40 + self.y / 40 * 20)] != 9):
                    self._display_surf.blit(self.tragovi, (self.x, self.y))
                self.proveri_da_je_zamka()
                self.y = self.y - 40
                pygame.event.pump()
                pygame.display.update()

    def moveDown(self):
        if (self.y + 40 <= 560):
            broj = self.x/40 + (self.y + 40)/40 * 20
            #print(broj)
            if(self.matrica[int(broj)] != 1 ):
                self.block = pygame.image.load("lav.png").convert()
                self._display_surf.blit(self.block, (self.x, self.y + 40))
                if(self.matrica[int(self.x/40 + self.y /40 * 20)] != 9):
                    self._display_surf.blit(self.tragovi, (self.x, self.y))
                self.proveri_da_je_zamka()
                self.y = self.y + 40
                pygame.event.pump()
                pygame.display.update()

    def prikazi_zamke(self):
        broj_zamki = 0
        while(True):
            rand_x = int(random.uniform(1, 19))
            rand_y = int(random.uniform(1, 14))
            broj = int(rand_x + rand_y * 20)
           # print(broj)
            if(self.matrica[int(broj)] != 0):
                continue
            elif(int(broj)!=41 and int(broj)==61):
                continue
            self.block = pygame.image.load("zamka.jpg").convert() #slika zamke
            self._display_surf.blit(self.block, (rand_x * 40, rand_y * 40))
            broj_zamki = broj_zamki + 1

            if(broj_zamki == 1):
                self.Zamka1X = rand_x * 40
                self.Zamka1Y = rand_y * 40
            if (broj_zamki == 2):
                self.Zamka2X = rand_x * 40
                self.Zamka2Y = rand_y * 40
            if (broj_zamki == 3):
                self.Zamka3X = rand_x * 40
                self.Zamka3Y = rand_y * 40

            self.matrica[int(broj)] = 5
            if(broj_zamki == 3):
                break

    def proveri_da_je_zamka(self):
        broj = self.x.value / 40 + self.y.value / 40 * 20
        if(self.matrica[int(broj)]  == 5):
            self.block = pygame.image.load("zamkaakt.jpg").convert()  #slike pokrenute zamke
            self._display_surf.blit(self.block, (self.x.value, self.y.value))
            pygame.display.update()

            self.matrica[int(broj)] = 9
            print(self.matrica[int(broj)])
            if(self.x.value == self.Zamka1X and self.y.value == self.Zamka1Y):
                self.Zamka1.value = 1
                other_proc = multiprocessing.Process(target=otvorena_zamka, args=(self.Zamka1, ))
                other_proc.start()
            if (self.x.value == self.Zamka2X and self.y.value == self.Zamka2Y):
                self.Zamka2.value = 1
                other_proc = multiprocessing.Process(target=otvorena_zamka, args=(self.Zamka2, ))
                other_proc.start()
            if (self.x.value == self.Zamka3X and self.y.value == self.Zamka3Y):
                self.Zamka3.value = 1
                other_proc = multiprocessing.Process(target=otvorena_zamka, args=(self.Zamka3, ))
                other_proc.start()

    def proveri_da_je_zamka2(self):
        broj = self.x2.value / 40 + self.y2.value / 40 * 20
        if(self.matrica[int(broj)]  == 5):
            self.block = pygame.image.load("zamkaakt.jpg").convert()  #slike pokrenute zamke
            self._display_surf.blit(self.block, (self.x2.value, self.y2.value))
            pygame.display.update()

            self.matrica[int(broj)] = 9
            print(self.matrica[int(broj)])
            if(self.x2.value == self.Zamka1X and self.y2.value == self.Zamka1Y):
                self.Zamka1.value = 1
                other_proc = multiprocessing.Process(target=otvorena_zamka, args=(self.Zamka1, ))
                other_proc.start()
            if (self.x2.value == self.Zamka2X and self.y2.value == self.Zamka2Y):
                self.Zamka2.value = 1
                other_proc = multiprocessing.Process(target=otvorena_zamka, args=(self.Zamka2, ))
                other_proc.start()
            if (self.x2.value == self.Zamka3X and self.y2.value == self.Zamka3Y):
                self.Zamka3.value = 1
                other_proc = multiprocessing.Process(target=otvorena_zamka, args=(self.Zamka3, ))
                other_proc.start()

    def osvezi_sve_zamke(self):
        if(self.Zamka1.value == 0):
            broj = self.Zamka1X / 40 + self.Zamka1Y / 40 * 20
            self.matrica[int(broj)] = 5
            self.block = pygame.image.load("zamka.jpg").convert()  # slika zamke
            self._display_surf.blit(self.block, (self.Zamka1X, self.Zamka1Y))
            #print('1.zamka')
        if (self.Zamka2.value == 0):
            broj = self.Zamka2X / 40 + self.Zamka2Y / 40 * 20
            self.matrica[int(broj)] = 5
            self.block = pygame.image.load("zamka.jpg").convert()  # slika zamke
            self._display_surf.blit(self.block, (self.Zamka2X, self.Zamka2Y))
            #print('2.zamka')
        if (self.Zamka3.value == 0):
            broj = self.Zamka3X / 40 + self.Zamka3Y / 40 * 20
            self.matrica[int(broj)] = 5
            self.block = pygame.image.load("zamka.jpg").convert()  # slika zamke
            self._display_surf.blit(self.block, (self.Zamka3X, self.Zamka3Y))
            #print('3.zamka')


    def setup_enemies_randomly(self):
        distance=0
        while(True):
          self.randomEnemy_x1=int(random.uniform(1, 19))
          self.randomEnemy_y1=int(random.uniform(1, 14))
          self.randomEnemy_x2=int(random.uniform(1, 19))
          self.randomEnemy_y2=int(random.uniform(1, 14))


          number_of_first_enemy=int(self.randomEnemy_x1+self.randomEnemy_y1*20)
          number_of_second_enemy=int(self.randomEnemy_x2+self.randomEnemy_y2*20)

          print("nep1",number_of_first_enemy)
          print("nep2",number_of_second_enemy)

          #-------------------------------------------------------------------------------
          #provera kolizija za prvog neprijatelja
          distance=number_of_first_enemy-number_of_second_enemy#da ne stanu na isto mesto
          if(self.matrica[int(number_of_first_enemy)]!=0):#da je zid
              continue
          elif(int(number_of_first_enemy)==61):#ako je mesto 2 igraca
              continue
          elif(int(number_of_first_enemy)==41):#ako je mesto 1 igraca
              continue
          elif(self.matrica[int(number_of_first_enemy)]==5):#ako je zamka
              continue


          #--------------------------------------------------
          #provera kolizija za drugog neprijatelja
          if(self.matrica[int(number_of_second_enemy)] != 0):
              continue
          elif(int(number_of_second_enemy) == 61):
              continue
          elif(int(number_of_second_enemy) == 41):
              continue
          elif (self.matrica[int(number_of_second_enemy)] == 5):
              continue
          if(distance==0):
              continue

          self.enemy1 = pygame.image.load("enemy1.jpg").convert()
          self.enemy2 = pygame.image.load("enemy2.jpg").convert()
          self._display_surf.blit(self.enemy1, [self.randomEnemy_x1 * 40, self.randomEnemy_y1 * 40])
          self._display_surf.blit(self.enemy2, [self.randomEnemy_x2 * 40, self.randomEnemy_y2 * 40])
          break

    def osvezi_prikaz(self):
        if(self.x.value != self.xProslo or self.y.value != self.yProslo):
            self.block = pygame.image.load("lav.png").convert()
            self._display_surf.blit(self.block, (self.x.value, self.y.value))
            broj = int(self.xProslo / 40 + self.yProslo / 40 * 20)
            if(self.matrica[broj] == 0):
                self._display_surf.blit(self.tragovi, (self.xProslo, self.yProslo))
                self.matrica[broj] = 3
            if (self.matrica[broj] == 4):
                self._display_surf.blit(self.tragovi2, (self.xProslo, self.yProslo))
            if (self.matrica[broj] == 3):
                self._display_surf.blit(self.tragovi, (self.xProslo, self.yProslo))
            self.xProslo = self.x.value
            self.yProslo = self.y.value
            self.proveri_da_je_zamka()
        if (self.x2.value != self.x2Proslo or self.y2.value != self.y2Proslo):
            self.block = pygame.image.load("lav.png").convert()
            self._display_surf.blit(self.block, (self.x2.value, self.y2.value))
            broj = int(self.x2Proslo / 40 + self.y2Proslo / 40 * 20)
            if (self.matrica[broj] == 0):
                self._display_surf.blit(self.tragovi2, (self.x2Proslo, self.y2Proslo))
                self.matrica[broj] = 4
            if(self.matrica[broj] == 3):
                self._display_surf.blit(self.tragovi, (self.x2Proslo, self.y2Proslo))
            if (self.matrica[broj] == 4):
                self._display_surf.blit(self.tragovi2, (self.x2Proslo, self.y2Proslo))
            self.x2Proslo = self.x2.value
            self.y2Proslo = self.y2.value
            self.proveri_da_je_zamka2()
        pygame.event.pump()
        pygame.display.update()


    def da_li_je_kraj_nivoa(self):
        kraj = True
        for i in range(0, 20 * 15):
            if self.matrica[i] == 0:
                kraj = False
                break

        if kraj:
            # jos jedan uslov je potreban, da je jedan od igraca na kraju lavirinta
            # ovde treba napraviti novi nivo, sve postaviti na pocetne vrednosti
            self.x.value = 40
            self.y.value = 0
            self.x2.value = 80
            self.y2.value = 0
            self._display_surf.fill((34, 177, 76))
            self.maze.draw(self._display_surf, self._block_surf)
            self.maze.vrati_matricu_na_pocetne_vrednosti()

        return kraj


def otvorena_zamka(broj_zamke):
  sleep(5)
  broj_zamke.value = 0
