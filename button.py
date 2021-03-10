import pygame
import constants
import text

class Button(pygame.sprite.Sprite):
    # This button will look like its being pressed when cursor is hovering over it.
    # Therefore it needs a list of 2 images.
    def __init__(self, two_images, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.two_images = two_images
        self.image = pygame.image.load(self.two_images[0]).convert()
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
        self.width, self.height = self.image.get_size()
        self.screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
        self.function = 0

    def update(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.rect.left < mouse_x < self.rect.left + self.width and self.rect.top < mouse_y < self.rect.top + self.height:
            self.image = pygame.image.load(self.two_images[1]).convert()
            mouse_press = pygame.mouse.get_pressed()
            if mouse_press[0] == 1:
                self.function = 1
        else:
            self.image = pygame.image.load(self.two_images[0]).convert()
