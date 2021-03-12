import pygame, player_module, menu, constants, summary
from os import path
from Level import Level
from Level_01 import Level_01
from Level_02 import Level_02
from Level_03 import Level_03

import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (1200, 1200)  # moves the position of the window


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
pygame.display.set_caption('BombsAway!')

####################################################################
# Below are the loops that run the game.
if __name__ == "__main__":
    # begin the menu display loop
    menu.menu_start()
    # start the clock
    clock = pygame.time.Clock()
    menu_timer = pygame.time.get_ticks()
    # instantiate the first player object
    player = player_module.Player()
    # instantiate the first level
    current_level = Level_01(player, screen, clock)
    current_level_no = 1

    Level.running = True
    # start game music
    pygame.mixer.music.play(loops=-1)
    # game loop
    while Level.running:
        clock.tick(constants.FPS)  # 60 fps
        summary.time = pygame.time.get_ticks() - menu_timer
        # conditions for window to close
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Level.running = False

        # handles switching between levels. The switch happens when the player defeats each boss at
        # the end of the level
        if current_level.spawned_a_boss == 1:
            if len(current_level.boss_sprite) == 0 and current_level_no <= 2:
                # portal sprite that player interacts with to change levels
                current_level.spawn_portal()
                if current_level.portal_activated:
                    # update player statistics
                    current_level.level_summary()
                    current_level.total_score += current_level.score
                    # reset sprite groups
                    current_level.new_level()
                    # new player object
                    player = player_module.Player()
                    # go to level 2
                    if current_level_no == 1:
                        current_level = Level_02(player, screen, clock)
                    # go to level 3
                    elif current_level_no == 2:
                        current_level = Level_03(player, screen, clock)
                    # add new player object to sprite group
                    current_level.all_sprites.add(current_level.player)
                    pygame.mixer.music.play(loops=-1)
                    current_level_no += 1

            # shows player's score if he/she has defeated the final boss and won the game
            elif len(current_level.boss_sprite) == 0 and current_level_no == 3:
                # update the player statistics
                current_level.level_summary()
                current_level.player_won()

        # update the current level
        current_level.update()
        # updates the background position to create the scrolling affect
        current_level.starting_pos += 2
        current_level.total = current_level.starting_pos
        if current_level.total > current_level.starting_pos * -1:
            current_level.total = 0

        # clear the screen
        screen.fill(constants.BLACK)
        # blit background to screen
        screen.blit(current_level.background, (0, current_level.total))
        # draw the level's sprites
        current_level.draw()
        # refresh the display
        pygame.display.flip()

    pygame.quit()
