import pygame
import math
import constants
import bullet
import random

bullets = pygame.sprite.Group()

class Boss_minion(pygame.sprite.Sprite):
    def __init__(self, x, y, spawn_num):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('sprites/mob_0.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (47, 66))
        self.rect = self.image.get_rect()
        self.rect.centerx = 400
        self.rect.centery = 200
        self.speedx = 0
        self.speedy = 0
        self.sequence = 0
        self.spawn_num = spawn_num
        self.shoot_delay = pygame.time.get_ticks()
        self.random = random.choice([0, 1])
        self.random_2 = random.choice([0,1])

    def update(self):
        self.rect.centerx += self.speedx
        self.rect.centery += self.speedy

        if self.spawn_num == 1:
            self.spawn_1()
        if self.spawn_num == 2:
            self.spawn_2()
        if self.spawn_num == 3:
            self.spawn_3()
        if self.spawn_num == 4:
            self.spawn_4()

        self.shoot()

        if self.rect.right > 800:
            self.speedx *= -1
        if self.rect.left < 0:
            self.speedx *= -1
        if self.rect.top < 0:
            self.speedy *= -1
        if self.rect.bottom > 600:
            self.speedy *= -1

    def spawn_1(self):
        if self.sequence == 0:
            self.speedx = -3
            self.rect.centery = -0.01*((self.rect.centerx - 400)**(2)) + 200
        if self.rect.centerx < 311 and self.sequence == 0:
            self.sequence += 1
            self.speedx = -3
        if self.sequence == 1:
            self.rect.centery = 0.01*((self.rect.centerx - 210)**(2)) + 20
        if self.rect.centerx < 61 and self.sequence == 1:
            self.speedy = 5
            self.sequence += 1
        if self.sequence == 2:
            self.rect.centerx = 0.003*((self.rect.centery - 290)**(2)) + 55
        if self.rect.centery > 589 and self.sequence == 2:
             # self.speedx = 4
             self.sequence += 1
        # if self.sequence == 3:
        #     self.rect.centery = math.sqrt((0.4*(self.rect.centerx - 400)**(2) - 200**2)/-0.7) + 322

    def spawn_2(self):
        if self.sequence == 0:
            self.speedx = 3
            self.rect.centery = -0.01*((self.rect.centerx - 400)**(2)) + 200
        if self.rect.centerx > 492 and self.sequence == 0:
            self.sequence += 1
            self.speedx = 3
        if self.sequence == 1:
            self.rect.centery = 0.01*((self.rect.centerx - 590)**(2)) + 20
        if self.rect.centerx > 738 and self.sequence == 1:
            self.speedy = 5
            self.sequence += 1
        if self.sequence == 2:
            self.rect.centerx = -0.003*((self.rect.centery - 290)**(2)) + 745

    def spawn_3(self):
        if self.sequence == 0:
            if self.random == 0:
                self.speedx = -3
                self.speedy = 1
            if self.random == 1:
                self.speedx = -3
                self.speedy = -1
            self.sequence += 1

    def spawn_4(self):
        if self.sequence == 0:
            if self.random_2 == 0:
                self.speedx = 3
                self.speedy = -1
            if self.random_2 == 1:
                self.speedx = 3
                self.speedy = 1
            self.sequence += 1

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.shoot_delay > 400:
            self.shoot_delay = now
            projectile = bullet.Bullets(self.rect.centerx, self.rect.centery, 0, 8, 0)
            bullets.add(projectile)
