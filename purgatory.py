import pygame
import constants
import menu
import text

menu_sprites = pygame.sprite.Group()

screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
background = pygame.image.load('backgrounds/pygame_test_background.jpg').convert()

#Loop that runs the menu screen:
pygame.mixer.music.load('sounds/chiptunes_title_screen.wav')
pygame.mixer.music.set_volume(0.55)
pygame.mixer.music.play(loops = -1)
clock = pygame.time.Clock()

def level_1_summary():
    level_ended = True
    while level_ended == True:


        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # screen.blit(background, (0, 0))
        screen.blit(background, (0, 0))
        compliment_text = text.draw_text(screen, 'Nice Job! Keep Going!', 100, 400, 150, constants.GREEN, "ariel")
        continue_text = text.draw_text(screen, 'Click [SPACE] to go to LEVEL 2', 60, 410, 400, constants.YELLOW, "ariel")
        pygame.display.flip()

        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_SPACE]:
            # current_level.bg_ticks = pygame.time.get_ticks()
            level_ended = False

def level_2_summary():
    level_ended = True
    while level_ended == True:


        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # screen.blit(background, (0, 0))
        screen.blit(background, (0, 0))
        compliment_text = text.draw_text(screen, 'You\'re Almost There!', 100, 400, 150, constants.GREEN, "ariel")
        continue_text = text.draw_text(screen, 'Click [SPACE] to go to LEVEL 3', 60, 410, 400, constants.YELLOW, "ariel")
        pygame.display.flip()

        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_SPACE]:
            # current_level.bg_ticks = pygame.time.get_ticks()
            level_ended = False
