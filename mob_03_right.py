import pygame
import constants
import random
import math
import mob_bullet

bullets_group = pygame.sprite.Group()

class Mob_03_right(pygame.sprite.Sprite):
    def __init__(self, x, y, shooting_varaibles):
        (fire_rate, bullet_speed, delay) = shooting_varaibles
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('sprites/mob_0.png'), (47, 66)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.starting_pos = [x, y]
        self.speedx = -3
        self.speedy = -0.5
        self.last_tick = pygame.time.get_ticks()
        self.delay = delay
        self.fire_rate = fire_rate
        self.bullet_speed = bullet_speed
        self.last_shot = pygame.time.get_ticks()
        self.last_burst = pygame.time.get_ticks()
        self.finished_sequence = 0

    def update(self):
        self.rect.centerx += self.speedx
        self.rect.bottom += self.speedy

        if self.rect.centerx < -30:
            self.kill()

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
