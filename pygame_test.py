import pygame
import random
import constants
import math
import player_module
import boss_3
import boss_minion
import animations

pygame.init()
screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
background = pygame.image.load('backgrounds/pygame_test_background.jpg').convert()
pygame.display.set_caption('Pygame Experiments')
clock = pygame.time.Clock()


sprites = pygame.sprite.Group()
player = player_module.Player()
sprites.add(player)
portal_frame = 0
last_portal_anim = pygame.time.get_ticks()

running = True
while running:
    print(portal_frame)
    clock.tick(constants.FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Level.running = False

    # Update the objects
    # update()
    sprites.update()
    # Draw
    screen.blit(background, (0, 0))
    if portal_frame > 7:
        portal_frame = 0
    now = pygame.time.get_ticks()
    if now - last_portal_anim > 50:
        last_portal_anim = now
        portal_frame += 1
    screen.blit(animations.portal_anim[portal_frame], (300, 200))
    sprites.draw(screen)

    # screen.blit(current_level.background, (0, 0))
    # draw()

    pygame.display.flip()

pygame.quit()
