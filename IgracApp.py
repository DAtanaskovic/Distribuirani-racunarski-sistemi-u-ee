from Igrac import *
import pygame
from pygame.locals import *
from App import  *

class IgracApp:
    def __init(self):
        self.running = True

    def on_event(self, event):
        if event.type == QUIT:
            self_running = False

    def on_execute(self):
        #self.on_init()
        #if (self.on_init() == False):
           # self.running = False
            while (True):
                pygame.event.pump()
                keys = pygame.key.get_pressed()

                if (keys[K_RIGHT]):
                    self.moveRight()

                if (keys[K_LEFT]):
                    self.igrac.moveLeft()

                if (keys[K_UP]):
                    self.igrac.moveUp()

                if (keys[K_DOWN]):
                    self.igrac.moveDown()

                if (keys[K_ESCAPE]):
                    self._running = False


    def moveRight(self):
       # self.x = self.x + self.speed
        self.block = pygame.image.load("lav.png").convert()
        self._display_surf.blit(self.block, (10 * 40, 10 * 40))
        pygame.display.update()

