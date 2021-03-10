import pygame
import animations
import constants
import math
import text
import mob_bullet

bullets_group = pygame.sprite.Group()

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, speedx, speedy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('sprites/boss.png').convert_alpha()
        self.image.set_colorkey(constants.BLACK)
        self.rect = self.image.get_rect()
        self.speedx = speedx
        self.speedy = speedy
        self.rect.x = x
        self.rect.y = y
        self.life = 100
        self.last_shot = pygame.time.get_ticks()
        self.shoot_seq = 1
        self.rotate = 0
        self.bullets = pygame.sprite.Group()
        self.new_sequence = 0

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.right > 800:
            self.speedx *= -1
        if self.rect.left < 0:
            self.speedx *= -1
        if self.rect.bottom > 400:
            self.speedy *= -1

        if self.rect.top == 30 and self.new_sequence == 0:
             self.speedx = -2
             self.speedy = 0
             self.new_sequence += 1

        if self.rect.right > 800 and self.new_sequence == 1:
            self.speedx = -2
            self.speedy = 2
            self.new_sequence += 1

        if self.new_sequence == 2:
            if self.rect.top < 0:
                self.speedy *= -1
        self.shoot()

    def shoot(self):
        if self.shoot_seq == 1:
            now = pygame.time.get_ticks()
            if now - self.last_shot > 200:
                self.last_shot = now
                bullets = mob_bullet.Mob_bullets(self.rect.centerx, self.rect.bottom, 0, 4, 0)
                bullets_group.add(bullets)
        if self.rect.left < 0:
            self.shoot_seq = 2
        if self.shoot_seq == 2:
            now = pygame.time.get_ticks()
            if now - self.last_shot > 400:
                self.last_shot = now
                self.rotate += float(45)
                speedx = float(4)*math.cos((self.rotate/float(360))*float(2)*math.pi)
                speedy = float(4)*math.sin((self.rotate/float(360))*float(2)*math.pi)
                bullets = mob_bullet.Mob_bullets(self.rect.centerx, self.rect.bottom, speedx, speedy, 0)
                bullets_group.add(bullets)
                right_now = pygame.time.get_ticks()
                if right_now > 40000:
                    self.shoot_seq = 3
        if self.shoot_seq == 3:
            ok_now = pygame.time.get_ticks()
            if ok_now - self.last_shot > 1000:
                self.last_shot = ok_now
                for i in range(360):
                    if i % 45 == 0:
                        speedx = float(4)*math.cos((i/float(360))*float(2)*math.pi)
                        speedy = float(4)*math.sin((i/float(360))*float(2)*math.pi)
                        bullets = mob_bullet.Mob_bullets(self.rect.centerx, self.rect.bottom, speedx, speedy, 90 - i)
                        bullets_group.add(bullets)
