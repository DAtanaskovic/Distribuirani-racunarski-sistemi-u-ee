import  pygame
from Zid import *
from Igrac import*
import IgracApp
import NeprijateljOnline
from time import sleep
from pygame.locals import *
import  random
import multiprocessing
import NetworkProgramming
from multiprocessing import Process, Queue, Value
from PyQt5.QtWidgets import (QWidget, QHBoxLayout,
                             QLabel, QApplication, QPushButton, QLineEdit)
class Apponline(QWidget):
    windowWidth = 800
    windowHeight = 600

    def __init__(self):
        #super().__init__()
        self.ukupnoPoenaPrvog = 0
        self.ukupnoPoenaDrugog = 0
        self.noviNivo = False
        self.brojIgraca1 = 1
        self.brojIgraca2 = 2
        self.krajIgrice = False
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
        #self.txtbox1 = QLineEdit(self)
        print('nestoo')
        #self.txtbox1.move(100, 100)
        #self.txtbox1.resize(93, 23)
        #self.txtbox1.setText('Poeni igraca da se prikazu')
        #self.txtbox1.setVisible(True)

        #self.txtbox2 = QLineEdit(self)
        #self.txtbox2.move(344, 315)
        #self.txtbox2.resize(93, 23)

        #self.bodovi1 = self.txtbox1.text()
        #self.bodovi2 = self.txtbox2.text()

        self.p1 = None
        self.p2 = None
        self.p3 = None

        self.neprijatelj_u_zamci1 = Value('i', 0)
        self.neprijatelj_u_zamci2 = Value('i', 0)
        # --------------------------------------------------------------------------------------------------------------
        # koordinate neocekivane sile
        self.force_coordinateX1 = Value('i', 0)
        self.force_coordinateY1 = Value('i', 0)
        self.heart = None
        self.force_coordinateX1Proslo = 0
        self.force_coordinateY1Proslo = 0
        #za network
        self.net = NetworkProgramming.Network()
        self.redZaNeprijatelje = Queue()
        self.posle_crtanja_srca_vrati = False
        self.igraciZajedno = False

    def send_data(self):
        data = str(self.net.pos) + ":" + str(self.x.value) + "," + str(self.y.value)
        reply = self.net.send(data)
        return reply

    def send_data_neprijatelj(self):
        data = str(3) + ":" + str(self.x.value) + "," + str(self.y.value)
        reply = self.net.send(data)
        return reply

    @staticmethod
    def parse_data(data):
        try:
            d = data.split(":")[1].split(",")
            return int(d[0]), int(d[1])
        except:
            return 0, 0

    @staticmethod
    def parse_data_neprijatelj(data):
        try:
            d = data.split(":")[1].split(",")
            if data.split(":")[1] == '3':
                return int(d[0]), int(d[1])
            else:
                return (0, 0)
        except:
            return 0, 0

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth, self.windowHeight), pygame.HWSURFACE)
        self._block_surf = pygame.image.load("zid.png").convert()
        self._image_surf = pygame.image.load("lav.png").convert()
        self.drugi_igrac = pygame.image.load("igrac2.png").convert()
        self.tragovi = pygame.image.load("trag.png").convert()
        self.tragovi2 = pygame.image.load("crveniTrag.png").convert()
        self.aktivnaZamka = pygame.image.load("zamkaakt.jpg").convert()


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
        self._display_surf.blit(self.drugi_igrac, (self.x2.value, self.y2.value))
        self.prikazi_zamke()
        self.setup_enemies_randomly()
        pygame.display.update()
        self.on_execute_Igrac()

    def on_execute_Igrac(self):
        red = Queue()
        red2 = Queue()
        self.p1 = multiprocessing.Process(target=IgracApp.igrac_proces, args=(self.x, self.y, red))
        #self.p2 = multiprocessing.Process(target=IgracApp.igrac_proces, args=(self.x2, self.y2, red2))
        self.p1.start()
        #self.p2.start()
        clock = pygame.time.Clock()
        self.p3 = multiprocessing.Process(target=NeprijateljOnline.move_enemy_online, args=(self.randomEnemy_x1, self.randomEnemy_x2, self.randomEnemy_y1, self.randomEnemy_y2, self.Nivo, self.redZaNeprijatelje))
        self.p3.start()
        self.p4 = multiprocessing.Process(target=random_setup_force, args=(self.force_coordinateX1, self.force_coordinateY1))
        self.p4.start()

        #txtbox1 = QLineEdit(self)

        #txtbox1.move(100, 100)
        #txtbox1.resize(93, 23)
        #txtbox1.setText('Poeni igraca da se prikazu')
        #txtbox1.setVisible(True)
        while (True):
            self.rezultat_na_igrici()
            if self.krajIgrice:
                print('doslo je do kraja')
                #pygame.display.quit()
                #pygame.quit()
                break
            clock.tick(60)
            #self.broj_poena()
            if self.Prikazuj:
                self.osvezi_sve_zamke()
                self.osvezi_prikaz()
            #self.move_enemy()
            keys = 0
            #self.prikaz_rezultata()
            for event in pygame.event.get():
                if self.krajIgrice:
                    print('doslo je do kraja')
                    # pygame.display.quit()
                    # pygame.quit()
                    break
                pygame.event.pump()
                keys = pygame.key.get_pressed()
                kraj = self.da_li_je_kraj_nivoa()
                if kraj:
                    self.p1.terminate()
                    #self.p2.terminate()
                    self.p1 = multiprocessing.Process(target=IgracApp.igrac_proces, args=(self.x, self.y, red))
                    #self.p2 = multiprocessing.Process(target=IgracApp.igrac_proces, args=(self.x2, self.y2, red2))
                    self.p1.start()
                    #self.p2.start()
                if self.prviIgracIzgubioZivot:
                    self.p1.terminate()
                    print('ptvaranjeprocesa')
                    self.p1 = multiprocessing.Process(target=IgracApp.igrac_proces, args=(self.x, self.y, red))
                    self.p1.start()
                    self.prviIgracIzgubioZivot = False
                if self.drugiIgracIzgubioZivot:
                    #self.p2.terminate()
                    #self.p2 = multiprocessing.Process(target=IgracApp.igrac_proces, args=(self.x2, self.y2, red2))
                    #self.p2.start()
                    self.drugiIgracIzgubioZivot = False
                if event.type == pygame.KEYDOWN:
                    self.osvezi_prikaz()
                    if self.ZivotiPrvogIgraca > 0:
                        if (keys[K_RIGHT]):
                            red.put(2)

                        if (keys[K_LEFT]):
                            red.put(1)

                        if (keys[K_UP]):
                            red.put(3)

                        if (keys[K_DOWN]):
                            red.put(4)
                           # self.moveDown()

                    if self.ZivotiDrugogIgraca > 0:
                        if (keys[K_d]):
                            red2.put(2)

                        if (keys[K_a]):
                            red2.put(1)

                        if (keys[K_w]):
                            red2.put(3)

                        if (keys[K_s]):
                            red2.put(4)
                        # self.moveDown()

                        if (keys[K_ESCAPE]):
                            self._running = False

                    pygame.event.pump()





    def prikazi_zamke(self):
            self.block = pygame.image.load("zamka.jpg").convert()  # slika zamke

            rand_x = 5
            rand_y = 4
            broj = int(rand_x + rand_y * 20)
            self.block = pygame.image.load("zamka.jpg").convert() #slika zamke
            self.matrica[int(broj)] = 5
            self.Zamka1X = rand_x * 40
            self.Zamka1Y = rand_y * 40

            rand_x = 12
            rand_y = 13
            broj = int(rand_x + rand_y * 20)
            self.block = pygame.image.load("zamka.jpg").convert()  # slika zamke
            self.matrica[int(broj)] = 5
            self.Zamka2X = rand_x * 40
            self.Zamka2Y = rand_y * 40

            rand_x = 9
            rand_y = 9
            broj = int(rand_x + rand_y * 20)
            self.block = pygame.image.load("zamka.jpg").convert()  # slika zamke
            self.matrica[int(broj)] = 5
            self.Zamka3X = rand_x * 40
            self.Zamka3Y = rand_y * 40

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
          self.randomEnemy_x1.value = 18
          self.randomEnemy_y1.value = 1
          self.randomEnemy_x2.value = 2
          self.randomEnemy_y2.value = 13


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
                if (self.matrica[broj] == 9):
                    self._display_surf.blit(self.aktivnaZamka, (self.xProslo, self.yProslo))
                self.xProslo = self.x.value
                self.yProslo = self.y.value
                self.proveri_da_je_zamka()
        self.x2.value, self.y2.value = self.parse_data(self.send_data())
        #if self.net.pos != 1:
            #x1, y1 = self.parse_data_neprijatelj(self.send_data_neprijatelj())
            #x2, y2 = self.parse_data_neprijatelj(self.send_data_neprijatelj())
            #if x1 != 0:
                #self.randomEnemy_x1.value = x1
                #self.randomEnemy_y1.value = y1
            #if x2 != 0:
            #self.randomEnemy_x2.value = x2
           # self.randomEnemy_y2.value = y2

        if (self.x2.value != self.x2Proslo or self.y2.value != self.y2Proslo):
                self.block = pygame.image.load("igrac2.png").convert()
                self._display_surf.blit(self.block, (self.x2.value, self.y2.value))
                broj = int(self.x2Proslo / 40 + self.y2Proslo / 40 * 20)
                if (self.matrica[broj] == 0):
                    self._display_surf.blit(self.tragovi2, (self.x2Proslo, self.y2Proslo))
                    self.matrica[broj] = 4
                if(self.matrica[broj] == 3):
                    self._display_surf.blit(self.tragovi, (self.x2Proslo, self.y2Proslo))
                if (self.matrica[broj] == 4):
                    self._display_surf.blit(self.tragovi2, (self.x2Proslo, self.y2Proslo))
                if (self.matrica[broj] == 9):
                    self._display_surf.blit(self.aktivnaZamka, (self.x2Proslo, self.y2Proslo))
                print('eveme', self.x2.value, self.y2.value)
                if(self.x2.value == 40 and self.y2.value == 0):
                    self.ZivotiDrugogIgraca = self.ZivotiDrugogIgraca - 1
                    print(self.x2Proslo,self.y2Proslo)
                    if (self.x2Proslo == 40 and self.y2Proslo == 40):
                        self.ZivotiDrugogIgraca = self.ZivotiDrugogIgraca + 1
                    if (self.x2Proslo == 80 and self.y2Proslo == 0):
                        self.ZivotiDrugogIgraca = self.ZivotiDrugogIgraca + 1
                    if (self.x2Proslo == 40 and self.y2Proslo == 0):
                        self.ZivotiDrugogIgraca = self.ZivotiDrugogIgraca + 1
                self.x2Proslo = self.x2.value
                self.y2Proslo = self.y2.value
                self.proveri_da_je_zamka2()

        if(self.x.value == self.x2.value and self.y.value == self.y2.value):
            self.block = pygame.image.load("igracizajedno.png").convert()
            self._display_surf.blit(self.block, (self.x2.value, self.y2.value))
            self.igraciZajedno = True
        if(self.igraciZajedno and (self.x.value != self.x2.value or self.y.value != self.y2.value)):
            self.block = pygame.image.load("lav.png").convert()
            self._display_surf.blit(self.block, (self.x.value, self.y.value))
            self.block = pygame.image.load("igrac2.png").convert()
            self._display_surf.blit(self.block, (self.x2.value, self.y2.value))
            self.igraciZajedno = False
        enemy1 = pygame.image.load("enemy1.jpg").convert()
        enemy2 = pygame.image.load("enemy2.jpg").convert()
        self._display_surf.blit(enemy1, [self.randomEnemy_x1.value * 40, self.randomEnemy_y1.value * 40])
        self._display_surf.blit(enemy2, [self.randomEnemy_x2.value * 40, self.randomEnemy_y2.value * 40])
        if(self.randomEnemy_x1.value != self.randomEnemy_x1_Proslo or self.randomEnemy_y1.value != self.randomEnemy_y1_Proslo):
            self.da_li_je_neprijatelj_u_zamci()
            if self.neprijatelj_u_zamci1.value == 0:
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
            if self.neprijatelj_u_zamci2.value == 0:
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
            if self.posle_crtanja_srca_vrati:
                position = int(self.force_coordinateX1Proslo + self.force_coordinateY1Proslo * 20)
                if (self.matrica[int(position)] == 3):
                    self._display_surf.blit(self.tragovi,
                                            (self.force_coordinateX1Proslo * 40, self.force_coordinateY1Proslo * 40))
                elif (self.matrica[int(position)] == 4):
                    self._display_surf.blit(self.tragovi2,
                                            (self.force_coordinateX1Proslo * 40, self.force_coordinateY1Proslo * 40))
                else:
                    green = pygame.image.load("zelenaPozadina.png").convert()
                    self._display_surf.blit(green, (self.force_coordinateX1Proslo * 40, self.force_coordinateY1Proslo * 40))
                self.posle_crtanja_srca_vrati = False
            if self.force_coordinateX1.value != 0:
                if self.da_li_moze_da_se_iscrta_srce():
                    self.draw_force()
                self.force_coordinateX1Proslo = self.force_coordinateX1.value
                self.force_coordinateY1Proslo = self.force_coordinateY1.value
                self.posle_crtanja_srca_vrati = True
        self.da_li_je_neprijatelj()
        self.da_li_je_stao_na_srce()
        pygame.event.pump()
        pygame.display.update()

    def da_li_je_stao_na_srce(self):
        if(self.x.value == self.force_coordinateX1.value * 40 and self.y.value == self.force_coordinateY1.value * 40):
            self.ZivotiPrvogIgraca = self.ZivotiPrvogIgraca + 1
            self.force_coordinateX1.value = 0
            self.posle_crtanja_srca_vrati = False
            self.block = pygame.image.load("lav.png").convert()
            self._display_surf.blit(self.block, (self.x.value, self.y.value))
            pygame.display.update()
        if (self.x2.value == self.force_coordinateX1.value * 40 and self.y2.value == self.force_coordinateY1.value * 40):
            self.ZivotiDrugogIgraca = self.ZivotiDrugogIgraca + 1
            self.force_coordinateX1.value = 0
            self.posle_crtanja_srca_vrati = False
            self.block = pygame.image.load("igrac2.png").convert()
            self._display_surf.blit(self.block, (self.x2.value, self.y2.value))
            pygame.display.update()

    def da_li_moze_da_se_iscrta_srce(self):
        temp = True
        if(self.force_coordinateX1.value == self.x.value and self.force_coordinateY1.value == self.y.value):
            temp = False
        if(self.force_coordinateX1.value == self.x2.value and self.force_coordinateY1.value == self.y2.value):
            temp = False
        if (self.force_coordinateX1.value == self.randomEnemy_x1.value and self.force_coordinateY1.value == self.randomEnemy_y1.value):
            temp = False
        if (self.force_coordinateX1.value == self.randomEnemy_x2.value and self.force_coordinateY1.value == self.randomEnemy_y2.value):
            temp = False

        return temp

    def da_li_je_kraj_nivoa(self):
        kraj = True
        for i in range(0, 20 * 15):
            if self.matrica[i] == 0:
                kraj = False
                break

        if kraj:
            if self.x.value != 18 * 40 or self.y.value != 14 * 40:
                kraj = False
            if self.x2.value != 18 * 40 or self.y2.value != 14 * 40:
                kraj = False

        if kraj:
            # jos jedan uslov je potreban, da je jedan od igraca na kraju lavirinta
            # ovde treba napraviti novi nivo, sve postaviti na pocetne vrednosti
            self.ukupnoPoenaPrvog = self.ukupnoPoenaPrvog + self.brojPoenaPrvog()
            self.ukupnoPoenaDrugog = self.ukupnoPoenaDrugog + self.brojPoenaDrugog()
            self.prikaz_rezultata()
            self.Nivo.value = self.Nivo.value + 1
            self.x.value = 40
            self.y.value = 0
            self.x2.value = 80
            self.y2.value = 0
            self.ZivotiPrvogIgraca = 3
            self.ZivotiDrugogIgraca = 3
            self._display_surf.fill((34, 177, 76))
            self.maze.draw(self._display_surf, self._block_surf)
            self.maze.vrati_matricu_na_pocetne_vrednosti()
            self.noviNivo = True
            self.p3.terminate()
            self.p3 = multiprocessing.Process(target=NeprijateljOnline.move_enemy_online, args=(self.randomEnemy_x1, self.randomEnemy_x2, self.randomEnemy_y1, self.randomEnemy_y2, self.Nivo, self.redZaNeprijatelje))
            self.p3.start()

        return kraj

    def brojPoenaPrvog(self):
        sum1 = 0

        for i in range(0, 20 * 15):
            if (self.matrica[i] == 3):
                sum1 = sum1 + 1

        #print('rezultat1', sum1)
        return sum1

    def brojPoenaDrugog(self):

        sum2 = 0
        for i in range(0, 20 * 15):

            if (self.matrica[i] == 4):
                sum2 = sum2 + 1

        #print('rezultat2', sum2)
        return sum2

    def smanjiZivotPrvog(self):
        self.ZivotiPrvogIgraca = self.ZivotiPrvogIgraca - 1

        if self.ZivotiPrvogIgraca == 0:
            if self.ZivotiDrugogIgraca == 0:
                print('Prvi igrac je izgubio sve zivote')
                self.prikaz_rezultata()
                self.Prikazuj = False
                self.p1.terminate()
                #self.p2.terminate()
                self.p3.terminate()
                self.p4.terminate()
                self.krajIgrice = True
            else:
                self.x.value = 18 * 40
                self.y.value = 14 * 40
        else:
            self.x.value = 40
            self.y.value = 0
            self.osvezi_prikaz()

    def smanjiZivotDrugog(self):
        #self.ZivotiDrugogIgraca = self.ZivotiDrugogIgraca - 1

        if self.ZivotiDrugogIgraca == 0:
            if self.ZivotiPrvogIgraca == 0:
                print('Drugi igrac je izgubio sve zivote')
                self.prikaz_rezultata()
                self.Prikazuj = False
                self.p1.terminate()
                #self.p2.terminate()
                self.p3.terminate()
                self.p4.terminate()
                self.krajIgrice = True
            else:
                self.x2.value = 18 * 40
                self.y2.value = 14 * 40
            #ovde treba odraditi kraj igrice
        else:
            self.x2.value = 80
            self.y2.value = 0
            self.osvezi_prikaz()

    def da_li_je_neprijatelj(self):
        if(self.x.value == self.randomEnemy_x1.value*40 and self.y.value == self.randomEnemy_y1.value*40):
            if self.neprijatelj_u_zamci1.value == 1:
                return
            self.smanjiZivotPrvog()
            print('neprijatelj')
            self.prviIgracIzgubioZivot = True
            # igrac treba da izgubi zivot i vrati se na pocetnu poziciju

        if (self.x.value == self.randomEnemy_x2.value*40 and self.y.value == self.randomEnemy_y2.value*40):
            if self.neprijatelj_u_zamci2.value == 1:
                return
            self.smanjiZivotPrvog()
            print('neprijatelj')
            self.prviIgracIzgubioZivot = True
            # igrac treba da izgubi zivot i vrati se na pocetnu poziciju

        # if (self.x2.value == self.randomEnemy_x1.value*40 and self.y2.value == self.randomEnemy_y1.value*40):
        #     if self.neprijatelj_u_zamci1.value == 1:
        #         return
        #     self.smanjiZivotDrugog()
        #     print('neprijatelj')
        #     self.drugiIgracIzgubioZivot = True
        #     # igrac treba da izgubi zivot i vrati se na pocetnu poziciju
        #
        # if (self.x2.value == self.randomEnemy_x2.value*40 and self.y2.value == self.randomEnemy_y2.value*40):
        #     if self.neprijatelj_u_zamci2.value == 1:
        #         return
        #     self.smanjiZivotDrugog()
        #     print('neprijatelj')
        #     self.drugiIgracIzgubioZivot = True
        #     # igrac treba da izgubi zivot i vrati se na pocetnu poziciju

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
        #print('broj',broj)
        if(self.matrica[broj] == 9 and self.neprijatelj_u_zamci1.value == 0):
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
            self.neprijatelj_u_zamci1.value = 1
            other_proc = multiprocessing.Process(target=neprijatelj_u_zamki, args=(self.neprijatelj_u_zamci1,))
            other_proc.start()
            self.redZaNeprijatelje.put(3)
            print('stavljen u red')

        broj = int(self.randomEnemy_x2.value + self.randomEnemy_y2.value * 20)
        if (self.matrica[broj] == 9  and self.neprijatelj_u_zamci2.value == 0):
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
            self.neprijatelj_u_zamci2.value = 1
            other_proc = multiprocessing.Process(target=neprijatelj_u_zamki, args=(self.neprijatelj_u_zamci2,))
            other_proc.start()
            self.redZaNeprijatelje.put(4)
            print('stavljen u red')

    def pobednik(self):
        self.poeniPrvogIgraca = self.brojPoenaPrvog()
        self.poeniDrugogIgraca = self.brojPoenaDrugog()
        if self.ukupnoPoenaPrvog > self.ukupnoPoenaPrvog:
            return 1
        else:
            return 2

    def rezultat_na_igrici(self):
        font_obj = pygame.font.Font('freesansbold.ttf', 20)
        green = (0, 255, 0)
        blue = (0, 0, 180)
        text_surface_obj = font_obj.render(
            'igrac' + str(self.brojIgraca1) + ' - ' + str(self.brojPoenaPrvog() * 100) + ' zivota - ' + str(
                self.ZivotiPrvogIgraca), True, green, blue)
        text_rect_obj = text_surface_obj.get_rect()
        text_rect_obj.center = (250, 10)
        self._display_surf.blit(text_surface_obj, text_rect_obj)
        text_surface_obj2 = font_obj.render(
            'igrac' + str(self.brojIgraca2) + ' - ' + str(self.brojPoenaDrugog() * 100) + ' zivota - ' + str(
                self.ZivotiDrugogIgraca), True, green, blue)
        text_rect_obj2 = text_surface_obj2.get_rect()
        text_rect_obj2.center = (550, 10)
        self._display_surf.blit(text_surface_obj2, text_rect_obj2)
        pygame.display.update()

    def draw_force(self):  # iscrtaj srce
            self.heart = pygame.image.load("heart.png").convert()
            self._display_surf.blit(self.heart, [self.force_coordinateX1.value * 40, self.force_coordinateY1.value * 40])
            pygame.display.update()

    def force_act(self):#ukoliko se neko od plejera nadje na sili
            if (self.x.value == self.force_coordinateX1.value * 40 and self.y.value == self.force_coordinateY1.value * 40):
                self.ZivotiPrvogIgraca = self.ZivotiPrvogIgraca + 1
            elif (self.x2.value == self.force_coordinateX1.value * 40 and self.y2.value == self.force_coordinateY1.value * 40):
                self.ZivotiDrugogIgraca = self.ZivotiDrugogIgraca + 1

        # ---------------------------------------------------------------------------------------------------------------
        # samo za postavljanje neocekivane sile
def random_setup_force(force_coordinateX1, force_coordinateY1):
    while (True):
        force_coordinateX1_temp = int(random.uniform(1, 19))
        force_coordinateY1_temp = int(random.uniform(1, 14))
        random_time = int(random.uniform(6, 10))

        number_of_heart = int(force_coordinateX1_temp + force_coordinateY1_temp * 20)

        maze = Maze()
        matrica = maze.maze

        if (matrica[int(number_of_heart)] != 0):
            continue
        elif (matrica[int(number_of_heart)] == 61):
            continue
        elif (matrica[int(number_of_heart)] == 41):
            continue

        else:
            #sleep(random_time)
            force_coordinateX1.value = force_coordinateX1_temp
            force_coordinateY1.value = force_coordinateY1_temp
            sleep(2)
            force_coordinateX1.value = 0
            sleep(random_time)

def otvorena_zamka(broj_zamke):
  sleep(10)
  broj_zamke.value = 0

def neprijatelj_u_zamki(neprijatelj_u_zamci):
    sleep(5)
    neprijatelj_u_zamci.value = 0





