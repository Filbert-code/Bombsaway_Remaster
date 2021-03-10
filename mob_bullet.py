import pygame
import random
import constants
import math

class Mob_bullets(pygame.sprite.Sprite):
    def __init__(self, x, y, speedx, speedy, rotate):
        pygame.sprite.Sprite.__init__(self)
        self.bullet_img = pygame.image.load('sprites/laserRed04.png').convert_alpha()
        self.image = pygame.transform.scale(self.bullet_img, (7, 19))
        self.image = pygame.transform.rotate(self.image, rotate)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = speedy
        self.speedx = speedx
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.bottom > 3840:
            self.kill()

    def circle_shot(self):
        for i in range(360):
            if i % 45 == 0:
                new_bullet = Mob_bullets()
                self.speedx = 4*math.cos((i/360)*2*math.pi)
                self.speedy = 4*math.sin((i/360)*2*math.pi)
