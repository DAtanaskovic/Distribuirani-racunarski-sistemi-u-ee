import  pygame
from Zid import *
from Igrac import*
import IgracApp
import Neprijatelj
from time import sleep
from pygame.locals import *
import  random
import multiprocessing
from multiprocessing import Process, Queue, Value
from PyQt5.QtWidgets import (QWidget, QHBoxLayout,
                             QLabel, QApplication, QPushButton, QLineEdit)
class App(QWidget):
    windowWidth = 800
    windowHeight = 600

    def __init__(self):
        super().__init__()
        self.Nivo = Value('i', 1)
        self.Prikazuj = True
        self.prviIgracIzgubioZivot = False
        self.drugiIgracIzgubioZivot = False
        self.srce = Value('i', 0)
        self.ZivotiPrvogIgraca = 3
        self.ZivotiDrugogIgraca = 3
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
        self.randomEnemy_x1 = Value('i', 0)
        self.randomEnemy_y1 = Value('i', 0)
        self.randomEnemy_x2 = Value('i', 0)
        self.randomEnemy_y2 = Value('i', 0)
        self.randomEnemy_x1_Proslo = 0
        self.randomEnemy_y1_Proslo = 0
        self.randomEnemy_x2_Proslo = 0
        self.randomEnemy_y2_Proslo = 0
        self.enemy1 = None
        self.enemy2 = None
        # ---------------------------------
        print('nestooo')
        self.txtbox1 = QLineEdit(self)
        print('nestoo')
        self.txtbox1.move(100, 100)
        self.txtbox1.resize(93, 23)
        self.txtbox1.setText('Poeni igraca da se prikazu')
        self.txtbox1.setVisible(True)

        self.txtbox2 = QLineEdit(self)
        self.txtbox2.move(344, 315)
        self.txtbox2.resize(93, 23)

        self.bodovi1 = self.txtbox1.text()
        self.bodovi2 = self.txtbox2.text()

        self.p1 = None
        self.p2 = None
        self.p3 = None

        self.neprijatelj_u_zamci1 = False
        self.neprijatelj_u_zamci2 = False
        # --------------------------------------------------------------------------------------------------------------
        # koordinate neocekivane sile
        self.foce_coordinateX1 = 0
        self.force_coordinateY1 = 0
        self.heart = None
        self.force_coordinateX1Proslo = 0
        self.force_coordinateY1Proslo = 0

    # ---------------------------------------------------------------------------------------------------------------

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth, self.windowHeight), pygame.HWSURFACE)
        self._block_surf = pygame.image.load("zid.png").convert()
        self._image_surf = pygame.image.load("lav.png").convert()
        self.tragovi = pygame.image.load("trag.png").convert()
        self.tragovi2 = pygame.image.load("crveniTrag.png").convert()


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
        self.random_setup_force()
        pygame.display.update()
        self.on_execute_Igrac()

    def on_execute_Igrac(self):
            red = Queue()
            red2 = Queue()
            self.p1 = multiprocessing.Process(target=IgracApp.igrac_proces, args=(self.x, self.y, red))
            self.p2 = multiprocessing.Process(target=IgracApp.igrac_proces, args=(self.x2, self.y2, red2))
            self.p1.start()
            self.p2.start()
            clock = pygame.time.Clock()
            self.p3 = multiprocessing.Process(target=Neprijatelj.move_enemy, args=(self.randomEnemy_x1, self.randomEnemy_x2, self.randomEnemy_y1, self.randomEnemy_y2, self.Nivo))
            self.p3.start()

            txtbox1 = QLineEdit(self)

            txtbox1.move(100, 100)
            txtbox1.resize(93, 23)
            txtbox1.setText('Poeni igraca da se prikazu')
            txtbox1.setVisible(True)
            while (True):
                clock.tick(60)
                #self.broj_poena()
                if self.Prikazuj:
                    self.osvezi_sve_zamke()
                    self.osvezi_prikaz()
                #self.move_enemy()
                keys = 0
                #self.prikaz_rezultata()
                for event in pygame.event.get():
                    pygame.event.pump()
                    keys = pygame.key.get_pressed()
                    kraj = self.da_li_je_kraj_nivoa()
                    if kraj:
                        self.p1.terminate()
                        self.p2.terminate()
                        self.p1 = multiprocessing.Process(target=IgracApp.igrac_proces, args=(self.x, self.y, red))
                        self.p2 = multiprocessing.Process(target=IgracApp.igrac_proces, args=(self.x2, self.y2, red2))
                        self.p1.start()
                        self.p2.start()
                    if self.prviIgracIzgubioZivot:
                        self.p1.terminate()
                        self.p1 = multiprocessing.Process(target=IgracApp.igrac_proces, args=(self.x, self.y, red))
                        self.p1.start()
                        self.prviIgracIzgubioZivot = False
                    if self.drugiIgracIzgubioZivot:
                        self.p2.terminate()
                        self.p2 = multiprocessing.Process(target=IgracApp.igrac_proces, args=(self.x2, self.y2, red2))
                        self.p2.start()
                        self.drugiIgracIzgubioZivot = False
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

    # def moveRight(self):
    #     if (self.x + 40 <= 760):
    #         #print(broj)
    #         broj = (self.x + 40) / 40 + self.y / 40 * 20
    #         if (self.matrica[int(broj)] != 1):
    #             self.block = pygame.image.load("lav.png").convert()
    #             self._display_surf.blit(self.block, (self.x + 40, self.y))
    #             if (self.matrica[int(self.x / 40 + self.y / 40 * 20)] != 9):
    #                 self._display_surf.blit(self.tragovi, (self.x, self.y))
    #             self.proveri_da_je_zamka()
    #             self.x = self.x + 40
    #             self.y = self.y
    #             pygame.event.pump()
    #             pygame.display.update()
    #
    # def moveLeft(self):
    #     if (self.x - 40 >= 0):
    #         broj = (self.x - 40) / 40 + self.y / 40 * 20
    #        # print(broj)
    #         if (self.matrica[int(broj)] != 1):
    #             self.block = pygame.image.load("lav.png").convert()
    #             self._display_surf.blit(self.block, (self.x - 40, self.y))
    #             if (self.matrica[int(self.x / 40 + self.y / 40 * 20)] != 9):
    #                 self._display_surf.blit(self.tragovi, (self.x, self.y))
    #             self.proveri_da_je_zamka()
    #             self.x = self.x - 40
    #             self.y = self.y
    #             pygame.event.pump()
    #             pygame.display.update()
    #
    # def moveUp(self):
    #     if (self.y - 40 >= 0):
    #         broj = self.x / 40 + (self.y - 40) / 40 *20
    #        # print(broj)
    #         if (self.matrica[int(broj)] != 1):
    #             self.block = pygame.image.load("lav.png").convert()
    #             self._display_surf.blit(self.block, (self.x, self.y - 40))
    #             if (self.matrica[int(self.x / 40 + self.y / 40 * 20)] != 9):
    #                 self._display_surf.blit(self.tragovi, (self.x, self.y))
    #             self.proveri_da_je_zamka()
    #             self.y = self.y - 40
    #             pygame.event.pump()
    #             pygame.display.update()
    #
    # def moveDown(self):
    #     if (self.y + 40 <= 560):
    #         broj = self.x/40 + (self.y + 40)/40 * 20
    #         #print(broj)
    #         if(self.matrica[int(broj)] != 1 ):
    #             self.block = pygame.image.load("lav.png").convert()
    #             self._display_surf.blit(self.block, (self.x, self.y + 40))
    #             if(self.matrica[int(self.x/40 + self.y /40 * 20)] != 9):
    #                 self._display_surf.blit(self.tragovi, (self.x, self.y))
    #             self.proveri_da_je_zamka()
    #             self.y = self.y + 40
    #             pygame.event.pump()
    #             pygame.display.update()

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
          self.randomEnemy_x1.value = int(random.uniform(1, 19))
          self.randomEnemy_y1.value = int(random.uniform(1, 14))
          self.randomEnemy_x2.value = int(random.uniform(1, 19))
          self.randomEnemy_y2.value = int(random.uniform(1, 14))


          number_of_first_enemy=int(self.randomEnemy_x1.value + self.randomEnemy_y1.value * 20)
          number_of_second_enemy=int(self.randomEnemy_x2.value + self.randomEnemy_y2.value * 20)

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
          self.draw_enemy()
          break

        self.randomEnemy_x1_Proslo = self.randomEnemy_x1.value
        self.randomEnemy_y1_Proslo = self.randomEnemy_y1.value
        self.randomEnemy_x2_Proslo = self.randomEnemy_x2.value
        self.randomEnemy_y2_Proslo = self.randomEnemy_y2.value



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
        enemy1 = pygame.image.load("enemy1.jpg").convert()
        enemy2 = pygame.image.load("enemy2.jpg").convert()
        self._display_surf.blit(enemy1, [self.randomEnemy_x1.value * 40, self.randomEnemy_y1.value * 40])
        self._display_surf.blit(enemy2, [self.randomEnemy_x2.value * 40, self.randomEnemy_y2.value * 40])
        if(self.randomEnemy_x1.value != self.randomEnemy_x1_Proslo or self.randomEnemy_y1.value != self.randomEnemy_y1_Proslo):
            self.da_li_je_neprijatelj_u_zamci()
            if self.neprijatelj_u_zamci1 == False:
                broj = int(self.randomEnemy_x1_Proslo + self.randomEnemy_y1_Proslo * 20)
                if (self.matrica[broj] == 3):
                    self._display_surf.blit(self.tragovi, (self.randomEnemy_x1_Proslo*40, self.randomEnemy_y1_Proslo*40))
                elif (self.matrica[broj] == 4):
                    self._display_surf.blit(self.tragovi2, (self.randomEnemy_x1_Proslo*40, self.randomEnemy_y1_Proslo*40))
                else:
                    zelenaPozadina = pygame.image.load("zelenaPozadina.png").convert()
                    self._display_surf.blit(zelenaPozadina, (self.randomEnemy_x1_Proslo*40, self.randomEnemy_y1_Proslo*40))
                self.randomEnemy_x1_Proslo = self.randomEnemy_x1.value
                self.randomEnemy_y1_Proslo = self.randomEnemy_y1.value
        if (self.randomEnemy_x2.value != self.randomEnemy_x2_Proslo or self.randomEnemy_y2.value != self.randomEnemy_y2_Proslo):
            self.da_li_je_neprijatelj_u_zamci()
            if self.neprijatelj_u_zamci2 == False:
                broj = int(self.randomEnemy_x2_Proslo + self.randomEnemy_y2_Proslo * 20)
                if (self.matrica[broj] == 3):
                    self._display_surf.blit(self.tragovi, (self.randomEnemy_x2_Proslo * 40, self.randomEnemy_y2_Proslo * 40))
                elif (self.matrica[broj] == 4):
                    self._display_surf.blit(self.tragovi2, (self.randomEnemy_x2_Proslo * 40, self.randomEnemy_y2_Proslo * 40))
                else:
                    zelenaPozadina = pygame.image.load("zelenaPozadina.png").convert()
                    self._display_surf.blit(zelenaPozadina, (self.randomEnemy_x2_Proslo * 40, self.randomEnemy_y2_Proslo * 40))
                self.randomEnemy_x2_Proslo = self.randomEnemy_x2.value
                self.randomEnemy_y2_Proslo = self.randomEnemy_y2.value
        if (self.force_coordinateX1.value != self.force_coordinateX1Proslo or self.force_coordinateY1.value != self.force_coordinateY1Proslo):
                    position= int(self.force_coordinateX1Proslo + self.force_coordinateY1Proslo * 20)
                    if (self.matrica[int(position)] == 3):
                        self._display_surf.blit(self.tragovi,
                                                (self.force_coordinateX1Proslo * 40, self.force_coordinateY1Proslo * 40))
                    elif (self.matrica[int(position)] == 4):
                        self._display_surf.blit(self.tragovi2,
                                                (self.force_coordinateX1Proslo * 40, self.force_coordinateY1Proslo * 40))
                    else:
                        green = pygame.image.load("zelenaPozadina.png").convert()
                        self._display_surf.blit(green,
                                                (self.force_coordinateX1Proslo * 40, self.force_coordinateY1Proslo * 40))
                    self.force_coordinateX1Proslo = self.force_coordinateX1.value
                    self.force_coordinateY1Proslo = self.force_coordinateY1.value
        self.da_li_je_neprijatelj()
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
            self.prikaz_rezultata()
            self.Nivo.value = self.Nivo.value + 1
            self.x.value = 40
            self.y.value = 0
            self.x2.value = 80
            self.y2.value = 0
            self._display_surf.fill((34, 177, 76))
            self.maze.draw(self._display_surf, self._block_surf)
            self.maze.vrati_matricu_na_pocetne_vrednosti()
            self.p3.terminate()
            self.p3 = multiprocessing.Process(target=Neprijatelj.move_enemy, args=(self.randomEnemy_x1, self.randomEnemy_x2, self.randomEnemy_y1, self.randomEnemy_y2, self.Nivo))
            self.p3.start()

        return kraj

    def brojPoenaPrvog(self):
        sum1 = 0

        for i in range(0, 20 * 15):
            if (self.matrica[i] == 3):
                sum1 = sum1 + 1

        print('rezultat1', sum1)
        return sum1

    def brojPoenaDrugog(self):

        sum2 = 0
        for i in range(0, 20 * 15):

            if (self.matrica[i] == 4):
                sum2 = sum2 + 1

        print('rezultat2', sum2)
        return sum2

    def smanjiZivotPrvog(self):
        self.ZivotiPrvogIgraca = self.ZivotiPrvogIgraca - 1

        if self.ZivotiPrvogIgraca == 0:
            print('Prvi igrac je izgubio sve zivote')
            self.prikaz_rezultata()
            self.Prikazuj = False
            self.p1.terminate()
            self.p2.terminate()
            self.p3.terminate()
        else:
            self.x.value = 40
            self.y.value = 0
            self.osvezi_prikaz()

    def smanjiZivotDrugog(self):
        self.ZivotiDrugogIgraca = self.ZivotiDrugogIgraca - 1

        if self.ZivotiDrugogIgraca == 0:
            print('Drugi igrac je izgubio sve zivote')
            self.prikaz_rezultata()
            self.Prikazuj = False
            self.p1.terminate()
            self.p2.terminate()
            self.p3.terminate()
            #ovde treba odraditi kraj igrice
        else:
            self.x2.value = 80
            self.y2.value = 0
            self.osvezi_prikaz()

    def da_li_je_neprijatelj(self):
        if(self.x.value == self.randomEnemy_x1.value*40 and self.y.value == self.randomEnemy_y1.value*40):
            self.smanjiZivotPrvog()
            print('neprijatelj')
            self.prviIgracIzgubioZivot = True
            # igrac treba da izgubi zivot i vrati se na pocetnu poziciju

        if (self.x.value == self.randomEnemy_x2.value*40 and self.y.value == self.randomEnemy_y2.value*40):
            self.smanjiZivotPrvog()
            print('neprijatelj')
            self.prviIgracIzgubioZivot = True
            # igrac treba da izgubi zivot i vrati se na pocetnu poziciju

        if (self.x2.value == self.randomEnemy_x1.value*40 and self.y2.value == self.randomEnemy_y1.value*40):
            self.smanjiZivotDrugog()
            print('neprijatelj')
            self.drugiIgracIzgubioZivot = True
            # igrac treba da izgubi zivot i vrati se na pocetnu poziciju

        if (self.x2.value == self.randomEnemy_x2.value*40 and self.y2.value == self.randomEnemy_y2.value*40):
            self.smanjiZivotDrugog()
            print('neprijatelj')
            self.drugiIgracIzgubioZivot = True
            # igrac treba da izgubi zivot i vrati se na pocetnu poziciju

    def draw_enemy(self): #iscrtavanje neprijatelja
        print('crtaj1')
        enemy1 = pygame.image.load("enemy1.jpg").convert()
        enemy2 = pygame.image.load("enemy2.jpg").convert()
        print('crtaj')
        #print(self.randomEnemy_x1 * 40, self.randomEnemy_y1 * 40)
        #print(self.randomEnemy_x2 * 40, self.randomEnemy_y2 * 40)
        self._display_surf.blit(enemy1, [self.randomEnemy_x1.value * 40, self.randomEnemy_y1.value * 40])
        self._display_surf.blit(enemy2, [self.randomEnemy_x2.value * 40, self.randomEnemy_y2.value * 40])
        pygame.display.update()
#--------------------------------------------------------------------------------------------------------------------------------
    #pomeranje neprijatelja
    # def move_enemy(self):#treba dodati da se pre svakog menjanja koordinata, na svakom starom mestu iscrtavaju tragovi/trava
    #     while (True):
    #           random_generator = int(random.uniform(1, 4))
    #           #print("Random", random_generator)
    #           if (random_generator == 1):
    #               temprandomEnemy_x1 = self.randomEnemy_x1 - 2
    #               temprandomEnemy_x2 = self.randomEnemy_x2 - 1
    #               number_of_first_enemy = int(temprandomEnemy_x1 + self.randomEnemy_y1 * 20)
    #               number_of_second_enemy = int(temprandomEnemy_x2 + self.randomEnemy_y2 * 20)
    #               #print(number_of_first_enemy,number_of_second_enemy)
    #               distance = number_of_first_enemy - number_of_second_enemy  # da ne stanu na isto mesto
    #               if (self.matrica[int(number_of_first_enemy)] != 0):  # da je zid
    #                   continue
    #               elif (int(number_of_first_enemy) == 61):  # ako je mesto 2 igraca
    #                   continue
    #               elif (int(number_of_first_enemy) == 41):  # ako je mesto 1 igraca
    #                   continue
    #               elif (self.matrica[int(number_of_first_enemy)] == 5):  # ako je zamka
    #                   continue
    #               if (self.matrica[int(number_of_second_enemy)] != 0):
    #                   continue
    #               elif (int(number_of_second_enemy) == 61):
    #                   continue
    #               elif (int(number_of_second_enemy) == 41):
    #                   continue
    #               elif (self.matrica[int(number_of_second_enemy)] == 5):
    #                   continue
    #               if (distance == 0):
    #                   continue
    #               self.randomEnemy_x1 = temprandomEnemy_x1
    #               self.randomEnemy_x2 = temprandomEnemy_x2
    #               self.draw_enemy()
    #               break
    #
    #           elif (random_generator == 2):
    #               temprandomEnemy_y1 = self.randomEnemy_y1 - 2
    #               temprandomEnemy_y2 = self.randomEnemy_y2 - 1
    #               number_of_first_enemy = int(self.randomEnemy_x1 + temprandomEnemy_y1 * 20)
    #               number_of_second_enemy = int(self.randomEnemy_x2 + temprandomEnemy_y2 * 20)
    #               distance = number_of_first_enemy - number_of_second_enemy  # da ne stanu na isto mesto
    #               if (self.matrica[int(number_of_first_enemy)] != 0):  # da je zid
    #                   continue
    #               elif (int(number_of_first_enemy) == 61):  # ako je mesto 2 igraca
    #                   continue
    #               elif (int(number_of_first_enemy) == 41):  # ako je mesto 1 igraca
    #                   continue
    #               elif (self.matrica[int(number_of_first_enemy)] == 5):  # ako je zamka
    #                   continue
    #               if (self.matrica[int(number_of_second_enemy)] != 0):
    #                   continue
    #               elif (int(number_of_second_enemy) == 61):
    #                   continue
    #               elif (int(number_of_second_enemy) == 41):
    #                   continue
    #               elif (self.matrica[int(number_of_second_enemy)] == 5):
    #                   continue
    #               if (distance == 0):
    #                   continue
    #               self.randomEnemy_y1 = temprandomEnemy_y1
    #               self.randomEnemy_y2 = temprandomEnemy_y2
    #               self.draw_enemy()
    #               break
    #
    #           elif (random_generator == 3):
    #               temprandomEnemy_x1 = self.randomEnemy_x1 + 2
    #               temprandomEnemy_x2 = self.randomEnemy_x2 + 1
    #               number_of_first_enemy = int(temprandomEnemy_x1 + self.randomEnemy_y1 * 20)
    #               number_of_second_enemy = int(temprandomEnemy_x2 + self.randomEnemy_y2 * 20)
    #               distance = number_of_first_enemy - number_of_second_enemy  # da ne stanu na isto mesto
    #               if (self.matrica[int(number_of_first_enemy)] != 0):  # da je zid
    #                   continue
    #               elif (int(number_of_first_enemy) == 61):  # ako je mesto 2 igraca
    #                   continue
    #               elif (int(number_of_first_enemy) == 41):  # ako je mesto 1 igraca
    #                   continue
    #               elif (self.matrica[int(number_of_first_enemy)] == 5):  # ako je zamka
    #                   continue
    #               if (self.matrica[int(number_of_second_enemy)] != 0):
    #                   continue
    #               elif (int(number_of_second_enemy) == 61):
    #                   continue
    #               elif (int(number_of_second_enemy) == 41):
    #                   continue
    #               elif (self.matrica[int(number_of_second_enemy)] == 5):
    #                   continue
    #               if (distance == 0):
    #                   continue
    #               self.randomEnemy_x1 = temprandomEnemy_x1
    #               self.randomEnemy_x2 = temprandomEnemy_x2
    #               self.draw_enemy()
    #               break
    #           elif (random_generator == 4):
    #               temprandomEnemy_y1 = self.randomEnemy_y1 + 2
    #               temprandomEnemy_y2 = self.randomEnemy_y2 + 1
    #               number_of_first_enemy = int(self.randomEnemy_x1 + temprandomEnemy_y1 * 20)
    #               number_of_second_enemy = int(self.randomEnemy_x2 + temprandomEnemy_y2 * 20)
    #               distance = number_of_first_enemy - number_of_second_enemy  # da ne stanu na isto mesto
    #               if (self.matrica[int(number_of_first_enemy)] != 0):  # da je zid
    #                   continue
    #               elif (int(number_of_first_enemy) == 61):  # ako je mesto 2 igraca
    #                   continue
    #               elif (int(number_of_first_enemy) == 41):  # ako je mesto 1 igraca
    #                   continue
    #               elif (self.matrica[int(number_of_first_enemy)] == 5):  # ako je zamka
    #                   continue
    #               if (self.matrica[int(number_of_second_enemy)] != 0):
    #                   continue
    #               elif (int(number_of_second_enemy) == 61):
    #                   continue
    #               elif (int(number_of_second_enemy) == 41):
    #                   continue
    #               elif (self.matrica[int(number_of_second_enemy)] == 5):
    #                   continue
    #               if (distance == 0):
    #                   continue
    #               self.randomEnemy_y1 = temprandomEnemy_y1
    #               self.randomEnemy_y2 = temprandomEnemy_y2
    #               self.draw_enemy()
    #               break
    #           else:
    #               break
#-------------------------------------------------------------------------------------------------------------------------

    def prikaz_rezultata(self):
        rez = pygame.image.load("prikazRezultata.png").convert()
        self._display_surf.blit(rez, (0, 0))
        font_obj = pygame.font.Font('freesansbold.ttf', 50)
        green = (0, 255, 0)
        blue = (0, 0, 180)
        text_surface_obj = font_obj.render(str(self.brojPoenaPrvog() * 100), True, green, blue)
        text_rect_obj = text_surface_obj.get_rect()
        text_rect_obj.center = (330, 330)
        self._display_surf.blit(text_surface_obj, text_rect_obj)
        text_surface_obj2 = font_obj.render(str(self.brojPoenaDrugog() * 100), True, green, blue)
        text_rect_obj2 = text_surface_obj2.get_rect()
        text_rect_obj2.center = (470, 330)
        self._display_surf.blit(text_surface_obj2, text_rect_obj2)
        pygame.display.update()
        sleep(5)

    def da_li_je_neprijatelj_u_zamci(self):
        broj = int(self.randomEnemy_x1.value + self.randomEnemy_y1.value * 20)
        print('broj',broj)
        if(self.matrica[broj] == 9):
            print('Neprijatelj1 je upao u zamku')
            zamka = pygame.image.load("neprzamka1.jpg").convert()
            self._display_surf.blit(zamka, (self.randomEnemy_x1.value * 40, self.randomEnemy_y1.value * 40))
            broj = int(self.randomEnemy_x1_Proslo + self.randomEnemy_y1_Proslo * 20)
            if (self.matrica[broj] == 3):
                self._display_surf.blit(self.tragovi, (self.randomEnemy_x1_Proslo * 40, self.randomEnemy_y1_Proslo * 40))
            elif (self.matrica[broj] == 4):
                self._display_surf.blit(self.tragovi1, (self.randomEnemy_x1_Proslo * 40, self.randomEnemy_y1_Proslo * 40))
            else:
                zelenaPozadina = pygame.image.load("zelenaPozadina.png").convert()
                self._display_surf.blit(zelenaPozadina, (self.randomEnemy_x1_Proslo * 40, self.randomEnemy_y1_Proslo * 40))
            pygame.display.update()
            self.neprijatelj_u_zamci1 = True
            other_proc = multiprocessing.Process(target=neprijatelj_u_zamki, args=(self.neprijatelj_u_zamci1,))
            other_proc.start()

        broj = int(self.randomEnemy_x2.value + self.randomEnemy_y2.value * 20)
        if (self.matrica[broj] == 9):
            print('Neprijatelj2 je upao u zamku')
            zamka = pygame.image.load("neprzamka2.jpg").convert()
            self._display_surf.blit(zamka, (self.randomEnemy_x2.value*40, self.randomEnemy_y2.value*40))
            broj = int(self.randomEnemy_x2_Proslo + self.randomEnemy_y2_Proslo * 20)
            if (self.matrica[broj] == 3):
                self._display_surf.blit(self.tragovi, (self.randomEnemy_x2_Proslo * 40, self.randomEnemy_y2_Proslo * 40))
            elif (self.matrica[broj] == 4):
                self._display_surf.blit(self.tragovi2, (self.randomEnemy_x2_Proslo * 40, self.randomEnemy_y2_Proslo * 40))
            else:
                zelenaPozadina = pygame.image.load("zelenaPozadina.png").convert()
                self._display_surf.blit(zelenaPozadina, (self.randomEnemy_x2_Proslo * 40, self.randomEnemy_y2_Proslo * 40))
            pygame.display.update()
            self.neprijatelj_u_zamci2 = True
            other_proc = multiprocessing.Process(target=neprijatelj_u_zamki, args=(self.neprijatelj_u_zamci2,))
            other_proc.start()

    def rezultat(self):
        poeniPrvogIgraca = 0
        poeniDrugogIgraca = 0
        self._backgroundResult = pygame.image.load("prikazRezultata.png")
        self.screen.blit(self._backgroundResult, [0, 0])
        white=(255,255,255)
        pygame.draw.rect(self._display_surf, white, (300, 200, 40, 50))
        pygame.display.update()
        self.poeniPrvogIgraca = self.brojPoenaPrvog()
        self.poeniDrugogIgraca = self.brojPoenaDrugog()

        wait = True
        while wait:
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    wait = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if 300 < mouse_pos[0] < 340 and 200 < mouse_pos[1] < 250:
                        wait = False

        self.showMaze()

        # ---------------------------------------------------------------------------------------------------------------
        # samo za postavljanje neocekivane sile
    def random_setup_force(self):
            while (True):
                self.force_coordinateX1 = int(random.uniform(1, 19))
                self.force_coordinateY1 = int(random.uniform(1, 14))
                random_time = int(random.uniform(6, 10))

                number_of_heart = int(self.force_coordinateX1 + self.force_coordinateY1 * 20)

                if (self.matrica[int(number_of_heart)] != 0):
                    continue
                elif (self.matrica[int(number_of_heart)] == 61):
                    continue
                elif (self.matrica[int(number_of_heart)] == 41):
                    continue
                elif (self.randomEnemy_x1 == self.force_coordinateX1):
                    continue
                elif (self.randomEnemy_y1 == self.force_coordinateY1):
                    continue
                elif (self.randomEnemy_x2 == self.force_coordinateX1):
                    continue
                elif (self.randomEnemy_y2 == self.force_coordinateY1):
                    continue
                else:
                    sleep(random_time)
                    self.draw_force()
                    self.force_coordinateX1Proslo = self.force_coordinateX1.value
                    self.force_coordinateY1Proslo = self.force_coordinateY1.value
                    sleep(2)
                    continue

    def draw_force(self):  # iscrtaj srce
            self.heart = pygame.image.load("heart.png").convert()
            self._display_surf.blit(self.heart, [self.force_coordinateX1 * 40, self.force_coordinateY1 * 40])
            pygame.display.update()

    def force_act(self):#ukoliko se neko od plejera nadje na sili
            if (self.x.value == self.force_coordinateX1.value * 40 and self.y.value == self.force_coordinateY1.value * 40):
                self.ZivotiPrvogIgraca = self.ZivotiPrvogIgraca + 1
            elif (self.x2.value == self.force_coordinateX1.value * 40 and self.y2.value == self.force_coordinateY1.value * 40):
                self.ZivotiDrugogIgraca = self.ZivotiDrugogIgraca + 1


def otvorena_zamka(broj_zamke):
  sleep(10)
  broj_zamke.value = 0

def neprijatelj_u_zamki(neprijatelj_u_zamci):
    sleep(5)
    neprijatelj_u_zamci.value = False





