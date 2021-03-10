import pygame
import constants
import random
import math
import mob_bullet

bullets_group = pygame.sprite.Group()
#(-30, 510)
class Mob_02_left(pygame.sprite.Sprite):
    def __init__(self, x, y, shooting_varaibles):
        (fire_rate, bullet_speed, delay) = shooting_varaibles
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('sprites/mob_1.png'), (47, 66)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.starting_pos = [x, y]
        self.speedx = 0
        self.speedy = 0
        self.last_tick = pygame.time.get_ticks()
        self.delay = delay
        self.fire_rate = fire_rate
        self.bullet_speed = bullet_speed
        self.last_shot = pygame.time.get_ticks()
        self.last_burst = pygame.time.get_ticks()
        self.finished_sequence = 0
        self._layer = 1

    def update(self):
        self.rect.centerx += self.speedx
        self.rect.bottom += self.speedy

        #Equations and graphs can be found at Desmos.com, sign in with gmail.
        if 514 >= self.rect.centerx and self.finished_sequence == 0:
            self.speedx = 4
            self.rect.bottom = 0.002*((self.rect.centerx-400)**2) + 140
            if 514 <= self.rect.centerx:
                self.finished_sequence = 1
        if self.finished_sequence == 1:
            self.speedy = 2.5
            self.speedx = 0
            self.rect.centerx = -0.007*((self.rect.bottom-300)**2) + 640
            # print(self.rect.centerx, self.rect.bottom)
            if 433 <= self.rect.bottom:
                self.finished_sequence = 2
        if self.finished_sequence == 2:
            self.speedx = -4
            self.speedy = 0
            self.rect.bottom = -0.002*((self.rect.centerx-400)**2) + 460
        if self.rect.bottom < -50:
            self.kill()
            # print("Yay! He died!")
        # self.shoot(self.fire_rate, self.bullet_speed, self.delay)

    def shoot(self, fire_rate, bullet_speed, delay):
        self.right_now = pygame.time.get_ticks()
        if self.delay < self.right_now - self.last_burst < self.delay*2:
            self.shoot_now = pygame.time.get_ticks()
            if self.shoot_now - self.last_shot > self.fire_rate:
                self.last_shot = self.shoot_now
                bullet = mob_bullet.Mob_bullets(self.rect.centerx, self.rect.centery, 0, self.bullet_speed, 0)
                bullets_group.add(bullet)
        elif self.right_now - self.last_burst < self.delay:
            pass
        else:
            self.last_burst = self.right_now
