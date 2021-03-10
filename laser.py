import pygame
import random
import math
import constants
import animations

player_position = []

class Laser(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = animations.laser_images[0]
        self.rect = self.image.get_rect()
        self.anim_delay = pygame.time.get_ticks()
        self.anim_num = 0

    def update(self):
        self.rect.centerx = player_position[0] + 7
        self.rect.bottom = player_position[1] - 40
        self.image_animation()

    def image_animation(self):
        now = pygame.time.get_ticks()
        if now - self.anim_delay > 50:
            self.anim_delay = now
            self.image = animations.laser_images[self.anim_num]
            self.anim_num += 7
            if self.anim_num > 79:
                self.anim_num = 0
