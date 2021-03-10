import pygame
import constants
import random
import math
import mob_bullet

bullets_group = pygame.sprite.Group()

class Mob_01_right(pygame.sprite.Sprite):
    def __init__(self, x, y, shooting_varaibles):
        (fire_rate, bullet_speed, delay) = shooting_varaibles
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('sprites/mob_0.png'), (47, 66)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.starting_pos = [x, y]
        self.speedx = -2
        self.speedy = 0
        self.last_bottom = 20000
        self.last_centerx = 20000
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
        # print(self.rect.centerx,self.rect.bottom)


        #Equations and graphs can be found at Desmos.com, sign in with gmail.
        if 800 > self.rect.centerx > 592:
            self.speedx = -2.5
            self.rect.bottom = -0.0123*((-self.rect.centerx+800)**(1.66)) + self.starting_pos[1]
        if 592 >= self.rect.centerx >= 249 and self.finished_sequence == 0:
            self.rect.bottom = -150*math.sin(2*math.pi*(self.rect.centerx - 147)/700) + (self.starting_pos[1]-200)
            # print(self.rect.centerx, self.rect.bottom)
            if 249 >= self.rect.centerx:
                self.last_bottom = self.rect.bottom
                self.last_centerx = self.rect.centerx
                # print("last_centerx, last_bottom: " + str(self.last_bottom) + " " + str(self.last_centerx))
                # print("centerx, bottom: "+str(self.rect.bottom)+ " " + str(self.rect.centerx))
        if self.rect.centerx <= self.last_centerx and self.rect.bottom >= self.last_bottom:
            self.speedx = 0
            self.speedy = 3.5
            # IMPORTANT: This value MUST be equal to or more than the last boundary condition for self.rect.centerx: 516
            self.rect.centerx = 0.0015*(self.rect.bottom - 371)**2 + self.starting_pos[1] -277
            # print("me" + str(self.rect.centerx)+ " " + str(self.rect.bottom))
            self.finished_sequence += 1
        if self.rect.bottom > 640:
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
