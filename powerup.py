import pygame
import constants
import random

class Powerup(pygame.sprite.Sprite):
    def __init__(self, y, index):
        pygame.sprite.Sprite.__init__(self)
        images_list = ['sprites/ammo_powerup1.png', 'sprites/bomb_powerup.png', 'sprites/speed_powerup.png', 'sprites/gun_powerup.png']
        image_scale_list = [(40, 40), (40, 75), (60, 60), (57, 98)]
        self.image = pygame.image.load(images_list[index]).convert_alpha()
        self.image = pygame.transform.scale(self.image, image_scale_list[index])
        self.image.set_colorkey(constants.WHITE)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.speedy = 2.5
        self.radius = 20
        self.rect.x = random.randrange(self.rect.width, constants.WIDTH-self.rect.width)
    def update(self):
        self.rect.y += self.speedy
        if self.rect.y > 3870:
            self.rect.y = 3870
