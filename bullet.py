
import pygame
import constants
import random
import math

class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y, speedx ,speedy, rotate):
        pygame.sprite.Sprite.__init__(self)
        self.bullet_img = pygame.image.load('sprites/laserRed04.png').convert_alpha()
        self.image = pygame.transform.scale(self.bullet_img, (7, 19))
        self.image = pygame.transform.rotate(self.image, rotate)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedx = speedx
        self.speedy = speedy

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()
