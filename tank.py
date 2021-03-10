import pygame
import constants
import random
import math
import mob_bullet
import animations

bullets = pygame.sprite.Group()
player_postion = []

class Tank_bullets(pygame.sprite.Sprite):
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

class Tank_body(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('sprites/tank_bottom.png'), (50, 85)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y - 30
        self.speedx = 0
        self.speedy = 1
    def update(self):
        self.rect.centerx += self.speedx
        self.rect.centery += self.speedy
        if self.rect.top > 600:
            self.kill()

class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('sprites/rotation/tank_top_0.png'), (100, 100)).convert_alpha()
        # self.image = pygame.transform.scale(pygame.image.load('sprites/tank_bottom.png'), (125, 83))
        # self.image = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speedx = 0
        self.speedy = 1
        self._layer = 0
        # self.bullets = pygame.sprite.Group()
        self.slope_numbers = [1,1.05,1.1,1.15,1.2,1.25,1.3,1.35,1.4,1.45,1.5,1.55,1.6,1.65,1.7,\
        1.8,1.9,2,2.1,2.2,2.3,2.4,2.5,2.6,2.7,2.8,2.9,3,3.2,3.4,3.6,3.8,4,4.4,4.8,5.4,6,7,8,9,10,12,15,20,30,50]
        self.adjusted_bullet_x = [5,4.87,4.75,4.65,4.53,4.42,4.3,4.22,4.1,4.02,3.92,3.83,3.75,3.65,\
        3.59,3.44,3.3,3.17,3.04,2.93,2.82,2.72,2.63,2.54,2.45,2.38,2.31,2.24,2.11,2,1.89,1.8,1.71,\
        1.57,1.44,1.29,1.16,1,0.88,0.78,0.7,0.59,0.47,0.35,0.24,0.14]
        self.adjusted_bullet_y = [5,5.1135,5.225,5.3475,5.436,5.525,5.59,5.697,5.74,5.829,5.88,5.9365,\
        6,6.0225,6.103,6.192,6.27,6.34,6.384,6.446,6.486,6.528,6.575,6.604,6.615,6.664,6.699,6.72,\
        6.752,6.8,6.804,6.84,6.84,6.908,6.912,6.966,6.96,7,7.04,7.02,7,7.08,7.05,7,7.2,7]
        # self.player_position = []

        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 1200

        self.bullet_speedx = 0
        self.bullet_speedy = 0
        self.count_index = -1

        self.rotation = 0
        self.last_rotate = pygame.time.get_ticks()

        self.delta_x = 0
        self.delta_y = 0
        self.slope = 0
        self.slope_index = 0

        self.shifted_x = 0

    def update(self):
        self.rect.centerx += self.speedx
        self.rect.bottom += self.speedy

        # Rotate the cannons, aim, and FIRE!
        self.rotate(self.rect.centerx, self.rect.centery)
        self.trajectory()
        self.shoot()


        if self.rect.top > 600:
            self.kill()


    def shoot(self):
        now = pygame.time.get_ticks()
        #If slope is neg, player is to the left, pos is to the right
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.bullet_speedx == 0 or self.bullet_speedy == 0:
                self.bullet_speedx = 0
                self.bullet_speedy = 5
            if self.slope > 1 or self.slope < -1:
                projectile = Tank_bullets(self.rect.centerx - 55*math.tan((math.pi/4)*(self.rotation/45)),\
                self.rect.bottom - 15*math.tan((math.pi/4)*(math.sqrt(self.rotation**2)/45)), self.bullet_speedx, self.bullet_speedy, -self.rotation)
                bullets.add(projectile)


    def trajectory(self):
        self.delta_x = self.rect.centerx - player_position[0]
        if self.delta_x == 0:
            self.delta_x = 0.01
        self.delta_y = self.rect.centery - player_position[1]
        self.slope = -1*(self.delta_y / self.delta_x)
        for index in range((len(self.slope_numbers)-2)):
            pos_left_limit = self.slope_numbers[index]
            pos_right_limit = self.slope_numbers[index+1]
            neg_left_limit = -self.slope_numbers[index]
            neg_right_limit = -self.slope_numbers[index+1]
            new_limit = self.rotation
            if pos_left_limit < self.slope < pos_right_limit:
                if self.rotation<0:
                    new_limit = 0
                self.bullet_speedx = -self.adjusted_bullet_x[45-(new_limit+1)]
                self.bullet_speedy = self.adjusted_bullet_y[45-(new_limit+1)]
                self.slope_index = 45 - index
            if neg_left_limit > self.slope > neg_right_limit:
                self.bullet_speedx = self.adjusted_bullet_x[self.rotation]
                self.bullet_speedy = self.adjusted_bullet_y[self.rotation]
                self.slope_index = -45 + index
            if self.slope_numbers[0] > self.slope > -self.slope_numbers[0]:
                 self.bullet_speedx = 0
                 self.bullet_speedy = 5

    def rotate(self, x, y):
        now = pygame.time.get_ticks()
        if now - self.last_rotate > 5:
            # Need to add 45 to self.rotation because the list from animations module is
            # not indexed from -45 to 45. It's from 0 - 90
            self.image = animations.tank_anim[self.rotation + 45]
            if self.slope_index > self.rotation:
                self.rotation += 1
            if self.slope_index < self.rotation:
                self.rotation -= 1
            self.last_rotate = now
            self.rect = self.image.get_rect()
            self.rect.centerx = x
            self.rect.centery = y
            if self.rotation < -45:
                self.rotation == -45
            if self.rotation > 45:
                self.rotation == 45
