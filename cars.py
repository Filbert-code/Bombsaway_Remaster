import pygame
import constants
import random

class Moving_cars_up(object):
    def __init__(self):
        i = random.randint(0,2)
        filename = 'sprites/car_up{}.png'.format(i+1)
        self.image = pygame.image.load(filename).convert()
        self.image.set_colorkey(constants.BLACK)

class Moving_cars_down(object):
    def __init__(self):
        i = random.randint(0,2)
        filename = 'sprites/car_down{}.png'.format(i+1)
        self.image = pygame.image.load(filename).convert()
        self.image.set_colorkey(constants.BLACK)
