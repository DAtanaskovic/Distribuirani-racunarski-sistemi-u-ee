import pygame

class Zid(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('zid.png')
        self.rect = self.image.get_rect(topleft=(100, 100))
        self.rect.x = x
        self.rect.y = y
