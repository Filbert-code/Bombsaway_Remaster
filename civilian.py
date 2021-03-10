import pygame
import random
import math
import constants
import animations

class Civilian_plane(pygame.sprite.Sprite):
    def __init__(self, x, y, speedx, speedy, rotate):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.transform.scale(pygame.image.load('sprites/civilian_airplane.png'),(124, 124))
        self.image = pygame.transform.rotate(animations.civ_image, rotate)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speedx = speedx
        self.speedy = speedy


    def update(self):
        self.rect.centerx += self.speedx
        self.rect.centery += self.speedy

        if self.rect.centerx >= 1000:
            self.kill()
        if self.rect.centerx <= -200:
            self.kill()
        if self.rect.centery >= 800:
            self.kill()
        if self.rect.centery <= -200:
            self.kill()
