import  pygame
from Zid import *
from Igrac import*
from time import sleep
from pygame.locals import *
import  random
import multiprocessing
from multiprocessing import Value

class App:
    windowWidth = 800
    windowHeight = 600

    def __init__(self):
        global matrica
        self._display_surf = None
        self._block_surf = None
        self._image_surf = None
        self.maze = Maze()
        self.matrica = self.maze.maze
        self.x = 1 * 40
        self.y = 0 * 40
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

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth, self.windowHeight), pygame.HWSURFACE)
        self._block_surf = pygame.image.load("zid.png").convert()
        self._image_surf = pygame.image.load("lav.png").convert()
        self.tragovi = pygame.image.load("trag.jpg").convert()

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
        self._display_surf.blit(self.block, (self.x, self.y))
        self.setup_enemies_randomly()
        self.prikazi_zamke()
        pygame.display.update()
        self.on_execute_Igrac()

    def on_execute_Igrac(self):
        #self.on_init()
        #if (self.on_init() == False):
           # self.running = False
            clock = pygame.time.Clock()
            while (True):
                clock.tick(60)
                keys = 0
                self.osvezi_sve_zamke()
                for event in pygame.event.get():
                    pygame.event.pump()
                    keys = pygame.key.get_pressed()
                    if event.type == pygame.KEYDOWN:
                        if (keys[K_RIGHT]):
                            self.moveRight()

                        if (keys[K_LEFT]):
                            self.moveLeft()

                        if (keys[K_UP]):
                            self.moveUp()

                        if (keys[K_DOWN]):
                            self.moveDown()

                        if (keys[K_ESCAPE]):
                            self._running = False


    def moveRight(self):
        if (self.x + 40 <= 760):
            broj = (self.x + 40) / 40 + self.y / 40 * 20
            #print(broj)
            if (self.matrica[int(broj)] != 1):
                self.block = pygame.image.load("lav.png").convert()
                self._display_surf.blit(self.block, (self.x + 40, self.y))
                if (self.matrica[int(self.x / 40 + self.y / 40 * 20)] != 9):
                    self._display_surf.blit(self.tragovi, (self.x, self.y))
                self.x = self.x + 40
                self.y = self.y
                pygame.event.pump()
                pygame.display.update()
                self.proveri_da_je_zamka()

    def moveLeft(self):
        if (self.x - 40 >= 0):
            broj = (self.x - 40) / 40 + self.y / 40 * 20
           # print(broj)
            if (self.matrica[int(broj)] != 1):
                self.block = pygame.image.load("lav.png").convert()
                self._display_surf.blit(self.block, (self.x - 40, self.y))
                if (self.matrica[int(self.x / 40 + self.y / 40 * 20)] != 9):
                    self._display_surf.blit(self.tragovi, (self.x, self.y))
                self.x = self.x - 40
                self.y = self.y
                pygame.event.pump()
                pygame.display.update()
                self.proveri_da_je_zamka()

    def moveUp(self):
        if (self.y - 40 >= 0):
            broj = self.x / 40 + (self.y - 40) / 40 *20
           # print(broj)
            if (self.matrica[int(broj)] != 1):
                self.block = pygame.image.load("lav.png").convert()
                self._display_surf.blit(self.block, (self.x, self.y - 40))
                if (self.matrica[int(self.x / 40 + self.y / 40 * 20)] != 9):
                    self._display_surf.blit(self.tragovi, (self.x, self.y))
                self.y = self.y - 40
                pygame.event.pump()
                pygame.display.update()
                self.proveri_da_je_zamka()

    def moveDown(self):
        if (self.y + 40 <= 560):
            broj = self.x/40 + (self.y + 40)/40 * 20
            #print(broj)
            if(self.matrica[int(broj)] != 1 ):
                self.block = pygame.image.load("lav.png").convert()
                self._display_surf.blit(self.block, (self.x, self.y + 40))
                if(self.matrica[int(self.x/40 + self.y /40 * 20)] != 9):
                    self._display_surf.blit(self.tragovi, (self.x, self.y))
                self.y = self.y + 40
                pygame.event.pump()
                pygame.display.update()
                self.proveri_da_je_zamka()

    def prikazi_zamke(self):
        broj_zamki = 0
        while(True):
            rand_x = int(random.uniform(0, 19))
            rand_y = int(random.uniform(0, 14))
            broj = int(rand_x + rand_y * 20)
            print(broj)
            if(self.matrica[int(broj)] != 0):
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
        broj = self.x / 40 + self.y / 40 * 20
        if(self.matrica[int(broj)]  == 5):
            self.block = pygame.image.load("zamkaakt.jpg").convert()  #slike pokrenute zamke
            self._display_surf.blit(self.block, (self.x, self.y))
            pygame.display.update()
            print(broj)

            self.matrica[int(broj)] = 9
            print(self.matrica[int(broj)])
            if(self.x == self.Zamka1X and self.y == self.Zamka1Y):
                self.Zamka1.value = 1
                other_proc = multiprocessing.Process(target=otvorena_zamka, args=(self.Zamka1, ))
                other_proc.start()
            if (self.x == self.Zamka2X and self.y == self.Zamka2Y):
                self.Zamka2.value = 1
                other_proc = multiprocessing.Process(target=otvorena_zamka, args=(self.Zamka2, ))
                other_proc.start()
            if (self.x == self.Zamka3X and self.y == self.Zamka3Y):
                self.Zamka3.value = 1
                other_proc = multiprocessing.Process(target=otvorena_zamka, args=(self.Zamka3, ))
                other_proc.start()

    def osvezi_sve_zamke(self):
        if(self.Zamka1.value == 0):
            broj = self.Zamka1X / 40 + self.Zamka1Y / 40 * 20
            self.matrica[int(broj)] = 5
            self.block = pygame.image.load("zamka.jpg").convert()  # slika zamke
            self._display_surf.blit(self.block, (self.Zamka1X, self.Zamka1Y))
            print('1.zamka')
        if (self.Zamka2.value == 0):
            broj = self.Zamka2X / 40 + self.Zamka2Y / 40 * 20
            self.matrica[int(broj)] = 5
            self.block = pygame.image.load("zamka.jpg").convert()  # slika zamke
            self._display_surf.blit(self.block, (self.Zamka2X, self.Zamka2Y))
            print('2.zamka')
        if (self.Zamka3.value == 0):
            broj = self.Zamka3X / 40 + self.Zamka3Y / 40 * 20
            self.matrica[int(broj)] = 5
            self.block = pygame.image.load("zamka.jpg").convert()  # slika zamke
            self._display_surf.blit(self.block, (self.Zamka3X, self.Zamka3Y))
            print('3.zamka')


    def otvorena_zamka(broj_zamke):
        sleep(5)
        broj_zamke.value = 0


    def setup_enemies_randomly(self):
        number_of_enemies=0
        while(True):

          self.randomEnemy_x1=int(random.uniform(0, 19))
          self.randomEnemy_y1=int(random.uniform(0, 14))
          self.randomEnemy_x2=int(random.uniform(0, 19))
          self.randomEnemy_y2=int(random.uniform(0, 14))

          number_of_first_enemy=int(self.randomEnemy_x1+self.randomEnemy_y1*20)
          number_of_second_enemy=int(self.randomEnemy_x2+self.randomEnemy_y2*20)

          if(self.matrica[int(number_of_first_enemy)]!=0 or self.matrica[int(number_of_second_enemy)]!=0):#treba dodati da ne moze da dodje na matrica[1][2] mesto
             continue
          self.enemy1 = pygame.image.load("enemy1.jpg").convert()
          self.enemy2 = pygame.image.load("enemy2.jpg").convert()
          self._display_surf.blit(self.enemy1, [self.randomEnemy_x1 * 40, self.randomEnemy_y1 * 40])
          self._display_surf.blit(self.enemy2, [self.randomEnemy_x2* 40, self.randomEnemy_y2 * 40])
          break
