import  pygame
from Zid import *
from Igrac import*
from time import sleep
from pygame.locals import *
class App:
    windowWidth = 800
    windowHeight = 600

    def __init__(self):
        self._display_surf = None
        self._block_surf = None
        self._image_surf = None
        self.maze = Maze()
        self.matrica = self.maze.maze
        self.x = 1 * 40
        self.y = 0 * 40

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
               # print(self.x, self.y)
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

