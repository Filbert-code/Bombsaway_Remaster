import pygame
import constants
import math
import random
import animations
import text

bullets = pygame.sprite.Group()
player_postion = []

class Boss_2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('sprites/boss_2.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (179, 289))
        self.rect = self.image.get_rect()
        self.spawn_choice = random.choice((-100, 900))
        self.rect.centerx = self.spawn_choice
        self.rect.centery = 200
        self.speedx = 0
        self.speedy = 0
        self.life = 200
        self.shoot_seq = 1
        self.new_sequence = 0
        self.time_delay = pygame.time.get_ticks()

        self.slope_numbers = [1,1.05,1.1,1.15,1.2,1.25,1.3,1.35,1.4,1.45,1.5,1.55,1.6,1.65,1.7,\
        1.8,1.9,2,2.1,2.2,2.3,2.4,2.5,2.6,2.7,2.8,2.9,3,3.2,3.4,3.6,3.8,4,4.4,4.8,5.4,6,7,8,9,10,12,15,20,30,50]
        self.adjusted_bullet_x = [5,4.87,4.75,4.65,4.53,4.42,4.3,4.22,4.1,4.02,3.92,3.83,3.75,3.65,\
        3.59,3.44,3.3,3.17,3.04,2.93,2.82,2.72,2.63,2.54,2.45,2.38,2.31,2.24,2.11,2,1.89,1.8,1.71,\
        1.57,1.44,1.29,1.16,1,0.88,0.78,0.7,0.59,0.47,0.35,0.24,0.14]
        self.adjusted_bullet_y = [5,5.1135,5.225,5.3475,5.436,5.525,5.59,5.697,5.74,5.829,5.88,5.9365,\
        6,6.0225,6.103,6.192,6.27,6.34,6.384,6.446,6.486,6.528,6.575,6.604,6.615,6.664,6.699,6.72,\
        6.752,6.8,6.804,6.84,6.84,6.908,6.912,6.966,6.96,7,7.04,7.02,7,7.08,7.05,7,7.2,7]
        self.ticks = 0
        self.last_shot = pygame.time.get_ticks()
        self.burst_delay = pygame.time.get_ticks()
        self.last_kill_shot = pygame.time.get_ticks()
        self.shoot_delay = 100
        self.bullet_speedx = 0
        self.bullet_speedy = 0
        self.delta_x = 0
        self.delta_y = 0
        self.slope = 0

    def update(self):
        self.rect.centerx += self.speedx
        self.rect.centery += self.speedy

        if self.rect.top < 0:
            self.speedy *= -1
        if self.rect.bottom > 400:
            self.speedy *= -1

        self.sequence_0()
        self.sequence_1()
        self.sequence_2()
        self.sequence_3()
        self.sequence_4()
        self.sequence_5()

        self.trajectory()
        self.shoot_to_wound(self.rect.centerx - 35, self.rect.centery - 18)
        self.shoot_to_kill()

    def sequence_0(self):
        if self.spawn_choice == -100 and self.new_sequence == 0:
            self.speedx = 1
        if self.spawn_choice == 900 and self.new_sequence == 0:
            self.speedx = -1

        if self.rect.left == 30 and self.new_sequence == 0:
             self.speedx = 2
             self.speedy = 0
             self.new_sequence += 1

        if self.rect.right == 770 and self.new_sequence == 0:
             self.speedx = -2
             self.speedy = 0
             self.new_sequence += 1

    def sequence_1(self):
        if self.new_sequence == 1:
            if 398 < self.rect.centerx < 402:
                now = pygame.time.get_ticks()
                if now - self.time_delay < 11200:
                    print(now - self.time_delay)
                    self.speedx = 0
                else:
                    self.speedx = 2
                    self.speedy = 1
                    self.new_sequence = 2

    def sequence_2(self):
        if self.new_sequence == 2:
            now = pygame.time.get_ticks()
            if now - self.time_delay < 20000:
                print(now - self.time_delay)
                if self.rect.right > 770:
                    self.speedx *= -1
                if self.rect.left < 30:
                    self.speedx *= -1
            if now - self.time_delay > 20000:
                if 398 < self.rect.centerx < 402:
                    print(now - self.time_delay)
                    if now - self.time_delay < 26000:
                        self.speedx = 0
                    else:
                        self.speedx = -2
                        self.speedy = -1
                        self.new_sequence = 3

    def sequence_3(self):
        if self.new_sequence == 3:
            now = pygame.time.get_ticks()
            if now - self.time_delay < 34000:
                print(now - self.time_delay)
                if self.rect.right > 770:
                    self.speedx *= -1
                if self.rect.left < 30:
                    self.speedx *= -1
            if now - self.time_delay > 34000:
                if 398 < self.rect.centerx < 402:
                    print(now - self.time_delay)
                    if now - self.time_delay < 41000:
                        self.speedx = 0
                    else:
                        self.speedx = 2
                        self.speedy = 1
                        self.new_sequence = 4

    def sequence_4(self):
        if self.new_sequence == 4:
            now = pygame.time.get_ticks()
            if now - self.time_delay < 49000:
                print(now - self.time_delay)
                if self.rect.right > 770:
                    self.speedx *= -1
                if self.rect.left < 30:
                    self.speedx *= -1
            if now - self.time_delay > 49000:
                if 398 < self.rect.centerx < 402:
                    print(now - self.time_delay)
                    if now - self.time_delay < 56000:
                        self.speedx = 0
                    else:
                        self.speedx = -2
                        self.speedy = -1
                        self.new_sequence = 5

    def sequence_5(self):
        if self.new_sequence == 5:
            if self.rect.right > 770:
                self.speedx *= -1
            if self.rect.left < 30:
                self.speedx *= -1

    def trajectory(self):
        for index in range((len(self.slope_numbers)-2)):
            pos_left_limit = self.slope_numbers[index]
            pos_right_limit = self.slope_numbers[index+1]
            neg_left_limit = -self.slope_numbers[index]
            neg_right_limit = -self.slope_numbers[index+1]
            if pos_left_limit < self.slope < pos_right_limit:
                self.bullet_speedx = -self.adjusted_bullet_x[(index)]
                self.bullet_speedy = self.adjusted_bullet_y[(index)]
            if neg_left_limit > self.slope > neg_right_limit:
                self.bullet_speedx = self.adjusted_bullet_x[index+1]
                self.bullet_speedy = self.adjusted_bullet_y[index+1]
            if self.slope_numbers[0] > self.slope > -self.slope_numbers[0]:
                 self.bullet_speedx = 0
                 self.bullet_speedy = 5

    def shoot_to_wound(self, x_pos, y_pos):
        if self.rect.centerx > 402 or self.rect.centerx < 398:
            right_now = pygame.time.get_ticks()
            if right_now - self.burst_delay > 2500:
                now = pygame.time.get_ticks()
                self.delta_x = self.rect.centerx - player_position[0]
                if self.delta_x == 0:
                    self.delta_x = 0.01
                self.delta_y = self.rect.centery - player_position[1]
                self.slope = -1*(self.delta_y / self.delta_x)
                #If slope is neg, player is to the left, pos is to the right
                if now - self.last_shot > self.shoot_delay:
                    self.last_shot = now
                    if self.slope > 1 or self.slope < -1:
                        projectile_1 = Boss_2_bullets(self.rect.centerx - 35, self.rect.centery - 18, self.bullet_speedx, self.bullet_speedy, 0)
                        projectile_2 = Boss_2_bullets(self.rect.centerx + 35, self.rect.centery - 18, self.bullet_speedx, self.bullet_speedy, 0)
                        projectile_3 = Boss_2_bullets(self.rect.centerx + 20, self.rect.bottom, self.bullet_speedx, self.bullet_speedy, 0)
                        projectile_4 = Boss_2_bullets(self.rect.centerx - 20, self.rect.bottom, self.bullet_speedx, self.bullet_speedy, 0)
                        bullets.add(projectile_1)
                        bullets.add(projectile_2)
                        bullets.add(projectile_3)
                        bullets.add(projectile_4)
                        self.ticks += 1
                    if self.ticks > 4:
                        self.burst_delay = now
                        self.ticks = 0

    def shoot_to_kill(self):
        if self.speedx == 0:
            now = pygame.time.get_ticks()
            if now - self.last_kill_shot > 1000:
                self.last_kill_shot = now
                for i in range(45):
                    if i % 30 == 0:
                        bullet_speedx = float(4)*math.cos((i/float(360))*float(2)*math.pi)
                        bullet_speedy = float(4)*math.sin((i/float(360))*float(2)*math.pi)
                        projectile = Boss_2_bullets(self.rect.centerx, self.rect.bottom, bullet_speedx, bullet_speedy, 0)
                        bullets.add(projectile)
                for i in range(135, 360):
                    if i % 30 == 0:
                        bullet_speedx = float(4)*math.cos((i/float(360))*float(2)*math.pi)
                        bullet_speedy = float(4)*math.sin((i/float(360))*float(2)*math.pi)
                        projectile = Boss_2_bullets(self.rect.centerx, self.rect.bottom, bullet_speedx, bullet_speedy, 0)
                        bullets.add(projectile)

class Boss_2_bullets(pygame.sprite.Sprite):
    def __init__(self, x, y, speedx, speedy, rotate):
        pygame.sprite.Sprite.__init__(self)
        self.bullet_img = pygame.image.load('sprites/laserRed04.png').convert()
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
