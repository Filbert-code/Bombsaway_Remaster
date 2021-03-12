import pygame
from os import path
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (1200,300) # moves the position of the window
import player_module
import explosions
import menu, animations
import random, constants
import summary
from Level import Level
from Level_01 import Level_01
from Level_02 import Level_02
from Level_03 import Level_03



# Level 1 Background Art from Kenny.nl game asset store
# Level 2 Background Art from Adam Saltsman --> Check out his work: https://adamatomic.itch.io/
# Level 3 Background Art from Mariusz Szulc --> Follow him on Behance: https://www.behance.net/MariuszSzulc
# Boss art from MillionthVector --> his blog: http://millionthvector.blogspot.de
# Action Chiptunes by Juhani Junkala
# Additional resources: www.bfxr.net | opengameart.org
# Portal art animations by Green Grape --> https://green-grape.itch.io/pixelportal

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
pygame.display.set_caption('BombsAway2!')
clock = pygame.time.Clock()


####################################################################
# Below are the loops that run the game.
if __name__ == "__main__":
    menu.menu_start()
    clock = pygame.time.Clock()
    menu_timer = pygame.time.get_ticks()
    player = player_module.Player()
    current_level = Level_03(player, screen, clock)
    current_level_no = 1

    # game loop
    #Variables used inside gameloop:
    Level.running = True
    #Starts background music, will loop.
    pygame.mixer.music.play(loops = -1)

    while Level.running:
        clock.tick(constants.FPS)  # 60 fps
        summary.time = pygame.time.get_ticks() - menu_timer
        # conditions for window to close
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Level.running = False


        if current_level.spawned_a_boss == 1:
            if len(current_level.boss_sprite) == 0 and current_level_no <= 2:
                current_level.spawn_portal()
                if current_level.portal_activated:
                    current_level.level_summary()
                    current_level.total_score += current_level.score
                    current_level.new_level()
                    player = player_module.Player()
                    if current_level_no == 1:
                        current_level = Level_02(player, screen, clock)
                    elif current_level_no == 2:
                        current_level = Level_03(player, screen, clock)
                    current_level.all_sprites.add(current_level.player)
                    pygame.mixer.music.play(loops = -1)
                    current_level_no += 1

            elif len(current_level.boss_sprite) == 0 and current_level_no == 3:
                current_level.level_summary()
                if current_level.total_score > current_level.highscore_list[9]:
                    current_level.total_score += current_level.score
                    current_level.highscore_list[9] = current_level.total_score
                    current_level.highscore_list.sort(reverse = True)
                    with open(path.join(current_level.dir, "highscore.txt"), 'w') as hs:
                        for i in range(10):
                            hs.write(str(current_level.highscore_list[i]) + "\n")
                menu.total_score += current_level.total_score
                menu.winner_winner()
                Level.running = False


        current_level.update()
        # updates the background position to create the scrolling affect
        current_level.starting_pos += 3
        current_level.total = current_level.starting_pos
        if current_level.total > current_level.starting_pos*-1:
            current_level.total = 0

        # Draw
        screen.fill(constants.BLACK)
        # blit background to screen
        screen.blit(current_level.background, (0, current_level.total))
        # draw the level's sprites
        current_level.draw()
        # refresh display
        pygame.display.flip()

    pygame.quit()
