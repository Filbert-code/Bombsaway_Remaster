import pygame
import constants
import math
import random
import animations
import text
import bullet
import boss_minion
import summary

bullets = pygame.sprite.Group()
minions = pygame.sprite.Group()
player_postion = []

class Boss_3(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = animations.boss_3_images[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = 400
        self.rect.centery = -100
        self.speedx = 0
        self.speedy = 0
        self.life = 300
        self.shoot_seq = 1
        self.new_sequence = 0
        self.sequence_1_speed = (random.choice([-1,1]), random.choice([-1,1]))
        self.anim = 0
        self.anim_time = pygame.time.get_ticks()
        self.radius = 90
        self.shoot_delay = pygame.time.get_ticks()
        self.shoot_angle = 0
        self.bullet_angle = 0
        self.minions_num = 0

    def update(self):
        self.rect.centerx += self.speedx
        self.rect.centery += self.speedy

        if self.rect.bottom > 600:
            self.speedy *= -1
        if self.rect.right > 800:
            self.speedx *= -1
        if self.rect.left < 0:
            self.speedx *= -1

        self.sequence_0()
        self.sequence_1()
        self.sequence_2()
        self.sequence_3()
        self.sequence_4()
        self.sequence_5()
        self.sequence_6()
        self.sequence_7()
        self.sequence_8()

        self.shoot_to_wound()
        self.spawn_minions()
        # if self.rect.top < 0:
        #     self.speedy *= -1

    def sequence_0(self):
        if self.new_sequence == 0:
            self.speedy = 1
        if self.rect.centery > 200 and self.new_sequence == 0:
            self.new_sequence = 1

    def sequence_1(self):
        if self.new_sequence == 0:
            self.timer = pygame.time.get_ticks()
        if self.new_sequence == 1:
            now = pygame.time.get_ticks()
            if now - self.timer < 5000:
                self.speedx = 0
                self.speedy = 0
            if now - self.timer > 5000:
                self.speedy = 2*self.sequence_1_speed[1]
                self.speedx = 2*self.sequence_1_speed[0]
                self.new_sequence = 2

    def sequence_2(self):
        if self.new_sequence == 1:
            self.timer_2 = pygame.time.get_ticks()
        if self.new_sequence == 2:
            now = pygame.time.get_ticks()
            if self.rect.top < 0:
                self.speedy *= -1
            if now - self.timer_2 < 14000:
                self.animation()
            if now - self.timer_2 > 10000 and 398 < self.rect.centerx < 402:
                self.speedx = 0
                if 198 < self.rect.centery < 202:
                    self.speedy = 0
                    self.new_sequence = 3

    def sequence_3(self):
        if self.new_sequence == 2:
            self.timer_3 = pygame.time.get_ticks()
        if self.new_sequence == 3:
            now = pygame.time.get_ticks()
            if now - self.timer_3 < 5000:
                self.speedx = 0
                self.speedy = 0
            if now - self.timer_3 > 5000:
                self.speedy = -2*self.sequence_1_speed[1]
                self.speedx = -2*self.sequence_1_speed[0]
                self.new_sequence = 4

    def sequence_4(self):
        if self.new_sequence == 3:
            self.timer_4 = pygame.time.get_ticks()
        if self.new_sequence == 4:
            now = pygame.time.get_ticks()
            if self.rect.top < 0:
                self.speedy *= -1
            if now - self.timer_4 < 13000:
                self.animation()
            if now - self.timer_4 > 10000 and 398 < self.rect.centerx < 402:
                self.speedx = 0
                if 198 < self.rect.centery < 202:
                    self.speedy = 0
                    self.new_sequence = 5

    def sequence_5(self):
        if self.new_sequence == 4:
            self.timer_5 = pygame.time.get_ticks()
        if self.new_sequence == 5:
            now = pygame.time.get_ticks()
            if now - self.timer_5 < 5000:
                self.speedx = 0
                self.speedy = 0
            if now - self.timer_5 > 5000:
                self.speedy = 2*self.sequence_1_speed[1]
                self.speedx = 2*self.sequence_1_speed[0]
                self.new_sequence = 6

    def sequence_6(self):
        if self.new_sequence == 5:
            self.timer_6 = pygame.time.get_ticks()
        if self.new_sequence == 6:
            now = pygame.time.get_ticks()
            if self.rect.top < 0:
                self.speedy *= -1
            if now - self.timer_6 < 12500:
                self.animation()
            if now - self.timer_6 > 10000 and 398 < self.rect.centerx < 402:
                self.speedx = 0
                if 198 < self.rect.centery < 202:
                    self.speedy = 0
                    self.new_sequence = 7

    def sequence_7(self):
        if self.new_sequence == 6:
            self.timer_7 = pygame.time.get_ticks()
        if self.new_sequence == 7:
            now = pygame.time.get_ticks()
            if now - self.timer_7 < 5000:
                self.speedx = 0
                self.speedy = 0
            if now - self.timer_7 > 5000:
                self.speedy = 2*self.sequence_1_speed[1]
                self.speedx = 2*self.sequence_1_speed[0]
                self.new_sequence = 8

    def sequence_8(self):
        if self.new_sequence == 8:
            self.animation()
            if self.rect.top < 0:
                self.speedy *= -1

    def animation(self):
        self.image = animations.boss_3_images[self.anim]
        now = pygame.time.get_ticks()
        if now - self.anim_time > 25:
            self.anim_time = now
            self.anim += 1
            if self.anim == 55:
                self.anim = 0
            self.shoot_angle += 1
            self.bullet_angle += 1
            if self.shoot_angle > 165:
                self.shoot_angle = 0
            if self.bullet_angle > 165:
                self.bullet_angle = 0

    def shoot_to_wound(self):
        if self.new_sequence == 2 or self.new_sequence == 4 or self.new_sequence == 6 or self.new_sequence == 8:
            now = pygame.time.get_ticks()
            if now - self.shoot_delay > 300:
                self.shoot_delay = now
                x = self.rect.centerx + float(130)*math.cos((self.shoot_angle - float(12))/float(165)*float(2)*math.pi)
                y = self.rect.centery + float(130)*math.sin((self.shoot_angle - float(12))/float(165)*float(2)*math.pi)
                x2 = self.rect.centerx + float(130)*math.cos((self.shoot_angle - float(67))/float(165)*float(2)*math.pi)
                y2 = self.rect.centery + float(130)*math.sin((self.shoot_angle - float(67))/float(165)*float(2)*math.pi)
                x3 = self.rect.centerx + float(130)*math.cos((self.shoot_angle - float(122))/float(165)*float(2)*math.pi)
                y3 = self.rect.centery + float(130)*math.sin((self.shoot_angle - float(122))/float(165)*float(2)*math.pi)
                speedx = float(7)*math.cos((self.shoot_angle/float(165))*float(2)*math.pi)
                speedy = float(7)*math.sin((self.shoot_angle/float(165))*float(2)*math.pi)
                speedx2 = float(7)*math.cos(((self.shoot_angle - float(55))/float(165))*float(2)*math.pi)
                speedy2 = float(7)*math.sin(((self.shoot_angle - float(55))/float(165))*float(2)*math.pi)
                speedx3 = float(7)*math.cos(((self.shoot_angle - float(110))/float(165))*float(2)*math.pi)
                speedy3 = float(7)*math.sin(((self.shoot_angle - float(110))/float(165))*float(2)*math.pi)
                projectile_1 = bullet.Bullets(x, y, speedx, speedy, round(-(self.bullet_angle +108)/float(165)*360))
                bullets.add(projectile_1)
                projectile_2 = bullet.Bullets(x2, y2, speedx2, speedy2, round(-(self.bullet_angle +223)/float(165)*360))
                bullets.add(projectile_2)
                projectile_3 = bullet.Bullets(x3, y3, speedx3, speedy3, round(-(self.bullet_angle +330)/float(165)*360))
                bullets.add(projectile_3)

    def spawn_minions(self):
        if self.new_sequence == 1 or self.new_sequence == 3 or self.new_sequence == 5 or self.new_sequence == 7:
            if self.minions_num == 0:
                self.minions_num += 1
                self.minion = boss_minion.Boss_minion(self.rect.centerx, self.rect.centery, 2)
                minions.add(self.minion)
                self.minion_2 = boss_minion.Boss_minion(self.rect.centerx, self.rect.centery, 1)
                minions.add(self.minion_2)
                self.minion_3 = boss_minion.Boss_minion(self.rect.centerx, self.rect.centery, 3)
                minions.add(self.minion_3)
                self.minion_4 = boss_minion.Boss_minion(self.rect.centerx, self.rect.centery, 4)
                minions.add(self.minion_4)
        if len(minions) == 0:
            self.minions_num = 0
