import  pygame
from Zid import *

class App:
    windowWidth = 800
    windowHeight = 600

    def __init__(self):
        self._display_surf = None
        self._block_surf = None
        self.maze = Maze()

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth, self.windowHeight), pygame.HWSURFACE)
        self._block_surf = pygame.image.load("zid.png").convert()

    def on_render(self):
        self._display_surf.fill((154,205,50))
        self.maze.draw(self._display_surf, self._block_surf)
        pygame.display.flip()
        pygame.display.update()

    def on_execute(self):
        self.on_init()
        self.on_render()