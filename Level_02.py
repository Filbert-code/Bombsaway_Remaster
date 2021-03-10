import pygame
import mob, boss, boss_2
import powerup, explosions
import animations, purgatory
import text, random, constants
import mob_01_left, mob_01_right, mob_02_left, mob_02_right
import mob_03_left,mob_03_right,mob_04_left, mob_04_right
import tank, helicopter, summary, civilian
from Level import Level

# Second level
class Level_02(Level):
    def __init__(self, player, screen, clock):
        Level.__init__(self, player)
        self.all_sprites.add(player)
        # background tileset creations from https://twitter.com/gallet_city
        self.background = pygame.image.load('backgrounds/gallet_background.png').convert()
        self.background = pygame.transform.scale(self.background, (1200, 11520))
        pygame.mixer.music.load('sounds/chiptunes_level_2.wav')
        pygame.mixer.music.set_volume(0.55)
        self.player = player
        self.screen = screen
        self.clock = clock
        ##############
        # Level-child attributes:
        self.bombs = 1
        self.total = None
        self.bomb_frame = 20
        self.spawned_a_boss = 0
        self.spawn_powerups()


        self.last_bomb = pygame.time.get_ticks()
        self.last_bomb_anim = pygame.time.get_ticks()
        self.mob_01_left_ticks = pygame.time.get_ticks()
        self.mob_01_right_ticks = pygame.time.get_ticks()
        self.mob_02_left_ticks = pygame.time.get_ticks()
        self.mob_02_right_ticks = pygame.time.get_ticks()
        self.mob_03_left_ticks = pygame.time.get_ticks()
        self.mob_03_right_ticks = pygame.time.get_ticks()
        self.mob_04_left_ticks = pygame.time.get_ticks()
        self.mob_04_right_ticks = pygame.time.get_ticks()
        self.mob_01_delay = pygame.time.get_ticks()
        self.mob_02_delay = pygame.time.get_ticks()
        self.laser_charge_time = pygame.time.get_ticks()
        # Level Summary tracking information:
        self.number_of_spawns = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0}
        self.total_fighters_killed = 0
        self.total_fighters = 0
        self.total_helicopters_killed = 0
        self.total_helicopters = 0
        self.total_tanks = 0

        self.number_of_tank_hits = 0
        self.tank_life = 5
        self.got_a_heli = 0
        self.number_of_heli_hits = 0
        self.heli_life = 20
        self.mob_v2_time = pygame.time.get_ticks()
        self.charge = 0
        self.civ_count = 0
        self.laser_start_pos = self.starting_pos
        self.laser_time = pygame.time.get_ticks()
        self.blink_delay = pygame.time.get_ticks()
        self.meter_emptying = pygame.time.get_ticks()
        self.laser_sound_mix = 0
        self.last_portal_anim = pygame.time.get_ticks()
        self.portal_frame = 0
        self.portal_activated = False

    def update(self):
        self.bullets.add(self.player.bullets)
        self.all_sprites.add(self.player.bullets)
        self.mob_bullets.add(mob.bullets_group)
        self.all_sprites.add(mob.bullets_group)
        self.laser_group.add(self.player.laser_sprite)
        self.mob_bullets.add(mob_01_left.bullets_group)
        self.all_sprites.add(mob_01_left.bullets_group)
        self.mob_bullets.add(mob_01_right.bullets_group)
        self.all_sprites.add(mob_01_right.bullets_group)
        self.mob_bullets.add(boss_2.bullets)
        self.all_sprites.add(boss_2.bullets)
        self.all_sprites.update()
        self.laser_group.update()
        self.player_lives()
        self.civilian_planes()
        self.explosions()
        self.powerup_bomb()
        self.powerup_speed()
        self.powerup_gun()
        self.bomb_update()
        self.boss_damage()
        self.player_position()
        self.laser_kill()
        # If player presses [p] key, game will pause. Press again for unpause
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_p]:
            self.paused()
        if self.player.upgrade == 0:
            self.player.upgrade += 1

    def draw(self):
        self.tank_spawn(-3200, -1800)
        self.heli_spawn([-4500], [[-50, 100, 1, 0]])
        self.mob_draw()
        self.civ_alert()
        self.laser_meter()
        self.draw_hud()
        # Draws the portal animation after defeating the boss
        if self.portal_activated == False and self.spawned_a_boss == 1:
            if len(self.boss_sprite) == 0:
                self.screen.blit(animations.portal_anim[self.portal_frame], (self.boss.rect.x, self.boss.rect.y + 146))
        self.all_sprites.draw(self.screen)
        self.laser_group.draw(self.screen)
        player_speed = self.player.speed_multiplier
        if player_speed == 1:
            text.draw_text(self.screen, 'You are FAST! ' + str(self.player.numbers), 60, constants.WIDTH/2, constants.HEIGHT - 100, constants.RED, "ariel")
        self.boss_spawn()
        if self.bomb_frame < 20:
            self.bomb_animation()
        if self.spawned_a_boss > 0:
            self.health_bar()

    def explosions(self):
        self.exp1_sound = pygame.mixer.Sound('sounds/Explosion1.wav')
        self.exp1_sound.set_volume(0.3)
        self.exp2_sound = pygame.mixer.Sound('sounds/Explosion2.wav')
        self.exp2_sound.set_volume(0.3)
        mob_hits = pygame.sprite.groupcollide(self.mobs, self.bullets, \
        True, True, pygame.sprite.collide_circle)
        for every in mob_hits:
            self.total_fighters_killed += 1
            self.charge += 3
            if self.charge > 162:
                self.charge = 163
            self.score += 5000
            expl = explosions.Explosion(every.rect.center, 'sm')
            self.all_sprites.add(expl)
            explode = random.randrange(2)
            if explode == 1:
                self.exp1_sound.play()
            else:
                self.exp2_sound.play()

    def spawn_powerups(self):
        for i in range(1):
            new_power1 = powerup.Powerup(-1500, 1)
            self.all_sprites.add(new_power1)
            self.bomb_powerups.add(new_power1)
        for i in range(1):
            new_power2 = powerup.Powerup(-2500, 2)
            self.all_sprites.add(new_power2)
            self.speed_powerups.add(new_power2)
        for i in range(1):
            new_power3 = powerup.Powerup(-2000, 3)
            self.all_sprites.add(new_power3)
            self.gun_powerups.add(new_power3)


    def mob_draw(self):
        if self.starting_pos > -7000:
            self.mob_spawn_03_right()
        if -5700 > self.starting_pos > -6000:
            self.shooting_mobs(0, -30, 100, 4, 1, 3, 1000)
        if self.starting_pos > -5700 and self.civ_count < 1:
            self.civilian_spawn(700, -100, 0, 6, -180)
        if self.starting_pos > -5500:
            self.mob_spawn_01_right()
        if -3200 > self.starting_pos > -4000:
            self.shooting_mobs(1, 830, 100, -3, 0, 2, 1000)
        if self.starting_pos > 4400:
            self.mob_spawn_01_left()
        if self.starting_pos > -3200:
            self.mob_spawn_03_left()
        if -2200 > self.starting_pos > -2400:
            self.shooting_mobs(0, -30, 100, 2, 0, 1, 1000)
        if self.starting_pos > -2500:
            self.mob_spawn_02_right()
        if self.starting_pos > -2000 and self.civ_count < 2:
            self.civilian_spawn(830, 300, -2, 0, 90)
        if self.starting_pos > -1800:
            self.mob_spawn_03_right()
        if self.starting_pos > -1000:
            self.mob_spawn_04_left()
        if -1200 > self.starting_pos > -800:
            self.shooting_mobs(0, -30, 100, 2, 0, 1, 1000)




    def boss_spawn(self):
        if self.total == 0 and len(self.mobs) == 0 and self.spawned_a_boss == 0:
            self.boss = boss_2.Boss_2()
            self.all_sprites.add(self.boss)
            self.boss_sprite.add(self.boss)
            self.spawned_a_boss = 1

    def laser_kill(self):
        if len(self.laser_group.sprites()) > 0:
            mob_hits = pygame.sprite.groupcollide(self.mobs, self.laser_group, True, False)
            for every in mob_hits:
                self.total_fighters_killed += 1
                self.score += 5000
                expl = explosions.Explosion(every.rect.center, 'sm')
                self.all_sprites.add(expl)
                explode = random.randrange(2)
                if explode == 1:
                    self.exp1_sound.play()
                else:
                    self.exp2_sound.play()
            tank_hits = pygame.sprite.groupcollide(self.tanks, self.laser_group, False, False)
            for every in tank_hits:
                self.tank_life -= 0.05
                # expl = explosions.Explosion((every.rect.centerx, every.rect.bottom), 'sm')
                # self.all_sprites.add(expl)

            heli_hits = pygame.sprite.groupcollide(self.helicopters, self.laser_group, False, False)
            for every in heli_hits:
                # self.total_fighters_killed += 1
                # self.score += 5000
                self.heli_life -= 0.05
                # expl = explosions.Explosion(every.rect.center, 'sm')
                # self.all_sprites.add(expl)
                # explode = random.randrange(2)
                # if explode == 1:
                #     self.exp1_sound.play()
                # else:
                #     self.exp2_sound.play()
            mob_bullet_hits = pygame.sprite.groupcollide(self.mob_bullets, self.laser_group, True, False)

            if self.spawned_a_boss == 1:
                boss_hits = pygame.sprite.groupcollide(self.boss_sprite, self.laser_group, False, False)
                for every in boss_hits:
                    self.boss.life -= 0.25

    def laser_meter(self):
        self.laser_sound = pygame.mixer.Sound('sounds/laser_beam_1.wav')
        self.laser_sound.set_volume(1)
        right_now = pygame.time.get_ticks()
        if self.player.firing_laser == False:
            self.laser_time = right_now
        if self.player.laser_ready == True and self.player.firing_laser == True:
            if right_now - self.laser_time > 5000:
                self.player.laser_ready = False
                self.player.firing_laser = False
                self.charge = 0

        now = pygame.time.get_ticks()
        if now - self.laser_charge_time > 1000:
            self.charge += 2
            self.laser_charge_time = now
        if self.charge > 162:
            self.player.laser_ready = True
            self.charge = 163
        self.screen.blit(animations.laser_meter_images[round(self.charge)], (10, 455))
        # Laser-ready blinking code
        if self.charge < 163:
            self.blink_delay = pygame.time.get_ticks() + 1000
        if self.charge == 163:
            just_now = pygame.time.get_ticks()
            if self.blink_delay > just_now:
                text.draw_text(self.screen, 'LASER CHARGED', 20, 140, 522, constants.GREEN, "Haettenschweiler")
            else:
                if just_now - self.blink_delay > 1000:
                    self.blink_delay += 2000
        # Laser firing causes meter to empty
        if self.player.firing_laser == True:
            if self.laser_sound_mix == 0:
                self.laser_sound.play(loops = 0)
                self.laser_sound_mix += 1
            now = pygame.time.get_ticks()
            if now - self.meter_emptying > 50:
                self.charge -= 1.8
                self.meter_emptying = now
        if self.player.laser_not_ready == False:
            self.laser_not_ready = right_now + 2000
        if self.player.laser_not_ready == True:
            if self.laser_not_ready > right_now:
                text.draw_text(self.screen, 'LASER NOT CHARGED', 20, 140, 522, constants.RED, "Haettenschweiler")
            else:
                self.player.laser_not_ready = False

    def bomb_animation(self):
        now = pygame.time.get_ticks()
        if now - self.last_bomb_anim > 20:
            self.last_bomb_anim = now
            self.screen.blit(animations.bombsaway_anim[self.bomb_frame], \
            (self.player.rect.centerx-(self.bomb_frame+1)*50, self.player.rect.centery-(self.bomb_frame+1)*float(37.5)))
            self.bomb_frame += 1

    def bomb_update(self):
        # Updates the bombs triggered by the player
        keystate = pygame.key.get_pressed()
        now = pygame.time.get_ticks()
        if now - self.last_bomb > 200:
            if keystate[pygame.K_b] and self.bombs > 0:
                self.bombsaway()
                self.last_bomb = now
                self.bomb_frame = 0
                self.bombs -= 1
                # Change this so that the boss will lose health when bomb is triggered
                if self.spawned_a_boss == 1:
                     self.boss.life -= 40

    def boss_damage(self):
        if self.spawned_a_boss == 1:
            hits = pygame.sprite.spritecollide(self.boss, self.bullets, True)
            for every in hits:
                self.boss.life -= 1
            if self.boss.life < 1:
                self.boss.kill()

    def spawn_portal(self):
        print("portal frames" + str(self.portal_frame))
        if self.portal_frame > 7:
            self.portal_frame = 0
        now = pygame.time.get_ticks()
        if now - self.last_portal_anim > 20:
            print("going through anims")
            self.last_portal_anim = now
            self.portal_frame += 1
        print(0,self.boss.rect.x+86, self.boss.rect.y+146)
        print(1,self.player.rect.centerx - 75, self.player.rect.bottom-50)
        if ((self.boss.rect.y+146)-20 <= self.player.rect.bottom - 50 < (self.boss.rect.y+146)+20):
            if ((self.boss.rect.x)-20 <= self.player.rect.centerx - 75 < (self.boss.rect.x)+20):
                print("in position for warp")
                self.portal_activated = True

    def health_bar(self):
        for i in range(10):
            if i*20 < self.boss.life <= (i+1)*20:
                image = animations.boss_health_images[(i+1)]
                image.set_colorkey(constants.WHITE)
        if self.boss.life <= 0:
            image = animations.boss_health_images[0]
        text.draw_text(self.screen, 'HEALTH: ', 24, 100, 7, constants.BLACK, "ariel")
        self.screen.blit(image, (135, 5))

    def paused(self):
        text.draw_text(self.screen, "Paused", 200, 400, 120, constants.BLUE, "ariel")
        text.draw_text(self.screen, "Press [p] key to UNPAUSE", 50, 400, 250, constants.BLUE, "ariel")
        text.draw_text(self.screen, "Press [ESC] key to EXIT GAME", 50, 400, 300, constants.BLUE, "ariel")
        # button_sprites = pygame.sprite.Group()
        # images = ['sprites/enemyBlack1.png', 'sprites/enemyBlue1.png']
        # continue_button = button.Button(images, 300, 600)
        # button_sprites.add(continue_button)
        pause = True
        # The key press code for pause is in the player_module
        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        pause = False
                        self.player.pause = False
                    if event.key == pygame.K_ESCAPE:
                        Level.running = False
                        pause = False
                        self.player.pause = False
            # button_sprites.update()
            # button_sprites.draw(self.screen)
            # if continue_button.function == 1:
            #     self.draw_one()
            pygame.display.update()
            self.clock.tick(15)

    def level_summary(self):
        spawns = 0
        for i in range(8):
            spawns += self.number_of_spawns.get(i)
        self.total_fighters += spawns
        self.total_helicopters += 1
        self.total_tanks += 2
        summary.total_fighters += self.total_fighters
        summary.total_fighters_killed += self.total_fighters_killed
        summary.total_tanks += self.total_tanks
        summary.total_tanks_killed += self.total_tanks_killed
        summary.total_helicopters += self.total_helicopters
        summary.total_helicopters_killed += self.total_helicopters_killed

    def new_level(self):
        self.player.kill()
        self.all_sprites.empty()
        self.mob_bullets.empty()
        self.bullets.empty()
        mob_01_left.bullets_group.empty()
        mob_01_right.bullets_group.empty()
        mob_02_left.bullets_group.empty()
        mob_02_right.bullets_group.empty()
        mob_03_left.bullets_group.empty()
        mob_03_right.bullets_group.empty()
        boss.bullets_group.empty()
        purgatory.level_2_summary()

    def player_position(self):
        tank.player_position = [self.player.rect.centerx, self.player.rect.centery]
        helicopter.player_position = [self.player.rect.centerx, self.player.rect.centery]
        boss_2.player_position = [self.player.rect.centerx, self.player.rect.centery]

    def draw_hud(self):
        text.draw_text(self.screen, str(self.total_score + self.score), 50, constants.WIDTH/2 + 10 , 10, constants.SCORE_RED, "Haettenschweiler") #(surf, text, size, x, y, color, font name)
        # text.draw_text(self.screen, 'AMMO: ' + str(player.ammo), 30, constants.WIDTH - 70, constants.HEIGHT - 120, constants.BLACK, "Haettenschweiler")
        text.draw_text(self.screen, 'BOMBS: ' + str(self.bombs), 20, 140, 497, constants.RED, "Haettenschweiler")
        text.draw_text(self.screen, 'Time: ' + str(round(summary.time/1000)), 20, 140, 470, constants.RED, "Haettenschweiler")
        text.draw_text(self.screen, 'LIVES: ' + str(self.lives), 30, 50, 10, constants.GREEN, "Haettenschweiler")
        text.draw_text(self.screen, '25%', 20, 65, 555, constants.DARK_GREEN, "Haettenschweiler")
        text.draw_text(self.screen, '50%', 20, 115, 555, constants.DARK_GREEN, "Haettenschweiler")
        text.draw_text(self.screen, '75%', 20, 162, 555, constants.DARK_GREEN, "Haettenschweiler")
        text.draw_text(self.screen, '100%', 20, 212, 555, constants.DARK_GREEN, "Haettenschweiler")