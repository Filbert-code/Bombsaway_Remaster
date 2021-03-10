import pygame
import random
import constants
import text
import summary
from os import path
# import HS_FILE

class Start_text(pygame.sprite.Sprite):
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('backgrounds/menu_start.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.bottom = 600
        self.rect.centerx = x
        self.speedx = -2

    def update(self):
        self.rect.centerx += self.speedx

        if self.rect.right < 260:
            self.rect.right += 1100

highscore_list = []
def load_data():
    with open("highscore.txt", 'r') as hs:
        for i in range(10):
            try:
                highscore = int(hs.readline())

            except:
                highscore = 0
            highscore_list.append(highscore)

menu_sprites = pygame.sprite.Group()
total_score = 0
highscore = 0
text1 = Start_text(0)
text2 = Start_text(370)
text3 = Start_text(740)
menu_sprites.add(text1)
menu_sprites.add(text2)
menu_sprites.add(text3)

screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
background = pygame.image.load('backgrounds/menu_background.png').convert_alpha()

#Loop that runs the menu screen:
pygame.mixer.music.load('sounds/chiptunes_title_screen.wav')
pygame.mixer.music.set_volume(0.55)
pygame.mixer.music.play(loops = -1)
clock = pygame.time.Clock()

def menu_start():
    menu_ = True
    highscore_page = False
    load_data()
    while menu_ == True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        menu_sprites.update()
        screen.fill(constants.MENU_FILL)
        screen.blit(background, (0, 0))
        menu_sprites.draw(screen)

        if highscore_page == True:
            screen.fill(constants.BLUE)
            text.draw_text(screen, "HIGHSCORES", 100, constants.WIDTH/2 , 20, constants.BLACK, "Haettenschweiler")
            text.draw_text(screen, "Press [ESCAPE] to return to MENU", 25, constants.WIDTH/2 - 150 , constants.HEIGHT - 40, constants.BLACK, "Haettenschweiler")
            text.draw_text(screen, "Press [SPACE] to START", 25, constants.WIDTH/2 + 150, constants.HEIGHT - 40, constants.BLACK, "Haettenschweiler")
            for i in range(10):
                text.draw_text(screen, str(i+1) + ". " + str(highscore_list[i]), 30, constants.WIDTH/2 , 150+40*i, constants.BLACK, "Haettenschweiler")

        pygame.display.flip()

        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_SPACE]:
            # current_level.bg_ticks = pygame.time.get_ticks()
            menu_ = False

        if keystate[pygame.K_h]:
            highscore_page = True
        if highscore_page == True:
            if keystate[pygame.K_ESCAPE]:
                highscore_page = False

def winner_winner():
    # You won! Good job gamer
    pygame.mixer.music.load('sounds/chiptunes_ending.wav')
    pygame.mixer.music.set_volume(0.55)
    pygame.mixer.music.play(loops = -1)
    s = pygame.Surface((constants.WIDTH, constants.HEIGHT))
    highscore_page = False
    pause = True
    fade_bg = []
    background = pygame.image.load('backgrounds/pygame_test_background.jpg').convert()
    arrow_image = pygame.transform.scale(pygame.image.load('sprites/arrow_image.png').convert_alpha(), (25, 25))
    fade_num = 0
    arrow = 0
    while pause:
        clock.tick(15)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        fade_num += 1
        if fade_num < 30:
            background.set_alpha(fade_num*8)
            screen.blit(background, (0, 0))
        elif highscore_page == True:
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_ESCAPE]:
                highscore_page = False
            screen.fill(constants.BLUE)
            text.draw_text(screen, "HIGHSCORES", 100, constants.WIDTH/2 , 20, constants.BLACK, "Haettenschweiler")
            text.draw_text(screen, "Press [ESCAPE] to return to GAME SUMMARY", 25, constants.WIDTH/2 , constants.HEIGHT - 40, constants.BLACK, "Haettenschweiler")
            for i in range(10):
                text.draw_text(screen, str(i+1) + ". " + str(highscore_list[i]), 30, constants.WIDTH/2 , 150+40*i, constants.BLACK, "Haettenschweiler")
        else:
            background.set_alpha(255)
            screen.blit(background, (0, 0))

            keystate = pygame.key.get_pressed()
            if fade_num > 20 and total_score > highscore:
                text.draw_text(screen, 'Congratulations, you just beat your all time HIGHSCORE!', 40, 400, 50, constants.GREEN, "Haettenschweiler")
            if fade_num > 20 and total_score < highscore:
                text.draw_text(screen, 'Amazing run! Good job beating those bosses', 50, 400, 50, constants.GREEN, "Haettenschweiler")
            if fade_num > 60:
                text.draw_text(screen, 'Your SCORE: ' + str(total_score), 40, 400, 130, constants.YELLOW, "Haettenschweiler")
            if fade_num > 80:
                text.draw_text(screen, 'Current HIGHSCORE: ' + str(highscore), 40, 400, 200, constants.RED, "Haettenschweiler")
            if fade_num > 100:
                text.draw_text(screen, 'Fighters Destroyed: ' + str(summary.total_fighters_killed) + "/" + str(summary.total_fighters), 30, 400, 270, constants.WHITE, "Haettenschweiler")
            if fade_num > 110:
                text.draw_text(screen, 'Tanks Destroyed: ' + str(summary.total_tanks_killed) + "/" + str(summary.total_tanks), 30, 400, 320, constants.WHITE, "Haettenschweiler")
            if fade_num > 120:
                text.draw_text(screen, 'Helicopters Destroyed: ' + str(summary.total_helicopters_killed) + "/" + str(summary.total_helicopters), 30, 400, 370, constants.WHITE, "Haettenschweiler")
            if fade_num > 130:
                text.draw_text(screen, 'Time Elapsed: ' + str(round((summary.time/1000),2)), 30, 400, 420, constants.WHITE, "Haettenschweiler")
            if fade_num > 162:
                text.draw_text(screen, 'EXIT GAME', 40, 240, 540, constants.WHITE, "Haettenschweiler")
                text.draw_text(screen, 'HIGHSCORES', 40, 645, 540, constants.WHITE, "Haettenschweiler")
                # Here, I need to create return to menu and exit buttons.
                if arrow == 0:
                    screen.blit(arrow_image, (150, 550))
                if arrow == 1:
                    screen.blit(arrow_image, (550, 550))
                if keystate[pygame.K_SPACE] and arrow == 0:
                    pause = False
                if keystate[pygame.K_SPACE] and arrow == 1:
                    highscore_page = True
                if keystate[pygame.K_LEFT]:
                    arrow = 0
                if keystate[pygame.K_RIGHT]:
                    arrow = 1

        pygame.display.update()

fade_num = 0
def loser_loser():
    pygame.mixer.music.load('sounds/chiptunes_ending.wav')
    pygame.mixer.music.set_volume(0.55)
    pygame.mixer.music.play(loops = -1)
    # You lost! Better luck next time
    s = pygame.Surface((constants.WIDTH, constants.HEIGHT))
    random_sequence = [0,1,2,3]
    choice = random.choice(random_sequence)
    highscore_page = False
    pause = True
    fade_bg = []
    background = pygame.image.load('backgrounds/pygame_test_background.jpg').convert()
    arrow_image = pygame.transform.scale(pygame.image.load('sprites/arrow_image.png').convert_alpha(), (25, 25))
    fade_num = 0
    arrow = 0
    while pause:
        clock.tick(15)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        fade_num += 1
        if fade_num < 30:
            background.set_alpha(fade_num*8)
            screen.blit(background, (0, 0))
        elif highscore_page == True:
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_ESCAPE]:
                highscore_page = False
            screen.fill(constants.BLUE)
            text.draw_text(screen, "HIGHSCORES", 100, constants.WIDTH/2 , 20, constants.BLACK, "Haettenschweiler")
            text.draw_text(screen, "Press [ESCAPE] to return to GAME SUMMARY", 25, constants.WIDTH/2 , constants.HEIGHT - 40, constants.BLACK, "Haettenschweiler")
            for i in range(10):
                text.draw_text(screen, str(i+1) + ". " + str(highscore_list[i]), 30, constants.WIDTH/2 , 150+40*i, constants.BLACK, "Haettenschweiler")
        else:
            background.set_alpha(255)
            screen.blit(background, (0, 0))
            keystate = pygame.key.get_pressed()
            if fade_num > 20 and total_score > highscore:
                text.draw_text(screen, 'Congratulations, you just beat your all time HIGHSCORE!', 80, 400, 50, constants.GREEN, "Haettenschweiler")
            if fade_num > 20 and total_score < highscore:
                if choice == 0:
                    text.draw_text(screen, 'Better luck next time', 80, 400, 50, constants.GREEN, "Haettenschweiler")
                elif choice == 1:
                    text.draw_text(screen, 'Hah! Is that all you got?', 60, 400, 50, constants.GREEN, "Haettenschweiler")
                elif choice == 2:
                    text.draw_text(screen, 'Get your ass back training camp noobie', 60, 400, 50, constants.GREEN, "Haettenschweiler")
                elif choice == 3:
                    text.draw_text(screen, "We don't accept losers here, beat it" , 60, 400, 50, constants.GREEN, "Haettenschweiler")
            if fade_num > 60:
                text.draw_text(screen, 'Your SCORE: ' + str(total_score), 40, 400, 130, constants.YELLOW, "Haettenschweiler")
            if fade_num > 80:
                text.draw_text(screen, 'Current HIGHSCORE: ' + str(highscore), 40, 400, 200, constants.RED, "Haettenschweiler")
            if fade_num > 100:
                text.draw_text(screen, 'Fighters Destroyed: ' + str(summary.total_fighters_killed) + "/" + str(summary.total_fighters), 30, 400, 270, constants.WHITE, "Haettenschweiler")
            if fade_num > 110:
                text.draw_text(screen, 'Tanks Destroyed: ' + str(summary.total_tanks_killed) + "/" + str(summary.total_tanks), 30, 400, 320, constants.WHITE, "Haettenschweiler")
            if fade_num > 120:
                text.draw_text(screen, 'Helicopters Destroyed: ' + str(summary.total_helicopters_killed) + "/" + str(summary.total_helicopters), 30, 400, 370, constants.WHITE, "Haettenschweiler")
            if fade_num > 130:
                text.draw_text(screen, 'Time Elapsed: ' + str(round((summary.time/1000),2)), 30, 400, 420, constants.WHITE, "Haettenschweiler")
            if fade_num > 162:
                text.draw_text(screen, 'EXIT GAME', 40, 240, 540, constants.WHITE, "Haettenschweiler")
                text.draw_text(screen, 'HIGHSCORES', 40, 645, 540, constants.WHITE, "Haettenschweiler")
                if arrow == 0:
                    screen.blit(arrow_image, (150, 550))
                if arrow == 1:
                    screen.blit(arrow_image, (550, 550))

                if keystate[pygame.K_SPACE] and arrow == 0:
                    pause = False
                if keystate[pygame.K_SPACE] and arrow == 1:
                    highscore_page = True
                if keystate[pygame.K_LEFT]:
                    arrow = 0
                if keystate[pygame.K_RIGHT]:
                    arrow = 1

        pygame.display.update()

#star_image = pygame.image.load('sprites/star.png').convert_alpha()
#def draw_star():
#    stars_num = 0
#    if 0.20 > total_score/1180000 > 0:
#        stars_num = 1
#    if 0.40 > total_score/1180000 > 0.20:
#        stars_num = 2
#    if 0.60 > total_score/1180000 > 0.40:
#        stars_num = 3
#    if 0.80 > total_score/1180000 > 0.60:
#        stars_num = 4
#    if 1.00 > total_score/1180000 > 0.80:
#        stars_num = 5
#    for i in range(stars_num):
#        screen.blit(star_image, (150 + i*100, 400))
#    fade_num = 152
