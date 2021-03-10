import pygame
import constants
import animations

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = animations.explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(animations.explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = animations.explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
