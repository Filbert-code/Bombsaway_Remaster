import pygame
import math
import random
import animations
import mob_bullet
import constants

bullets_group = pygame.sprite.Group()

class Mob(pygame.sprite.Sprite):
    def __init__(self, enemy_image_no, x, y, speedx, speedy, speed_mod, xxx_todo_changeme):
        (fire_rate, bullet_speed, delay) = xxx_todo_changeme
        pygame.sprite.Sprite.__init__(self)
        self.enemy_list = []
        self.enemy_list.append('sprites/flying_mob_0.png')
        self.enemy_list.append('sprites/flying_mob_1.png')
        self.enemy_list.append('sprites/flying_mob_2.png')
        self.image = pygame.transform.scale(pygame.image.load(self.enemy_list[enemy_image_no]), (47, 66)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speedx = speedx
        self.speedy = speedy
        self.delay = delay
        self.fire_rate = fire_rate
        self.bullet_speed = bullet_speed
        self.last_shot = pygame.time.get_ticks()
        self.last_burst = pygame.time.get_ticks()
        self.bullets = pygame.sprite.Group()
        self.speed_mod = speed_mod

    def update(self):
        if self.speed_mod == 1:
            self.speedy = 3*math.sin(math.pi*2*(self.rect.x/400))
            self.rect.x += self.speedx
            self.rect.y += self.speedy

        if self.speed_mod == 2:
            self.speedy = 4*math.sin(math.pi*2*(self.rect.x/200))
            self.rect.x += self.speedx
            self.rect.y += self.speedy

        if self.speed_mod == 3:
            if self.rect.x > constants.WIDTH-self.rect.width:
                self.speedx *= -1
            if self.rect.x < 0 and self.speedx < 0:
                self.speedx *= -1
            if self.rect.y > 300:
                self.speedy *= -1
            if self.rect.y < 0:
                self.speedy *= -1
            self.rect.x += self.speedx
            self.rect.y += self.speedy

        self.shoot(self.fire_rate, self.bullet_speed, self.delay)

        if self.rect.top > 600:
            self.kill()
        if self.rect.right < -100:
            self.kill()
        if self.rect.left > 1000:
            self.kill()
        if self.rect.bottom < 0:
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
