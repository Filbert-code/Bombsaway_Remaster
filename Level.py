import random
import pygame
from os import path
import animations
import civilian
import constants
import explosions
import helicopter
import menu
import mob
import player_module
import mob_01_left, mob_01_right, mob_02_left, mob_02_right
import mob_03_left,mob_03_right,mob_04_left, mob_04_right

# Parent level class. Sharing level characteristics are initiated here
import summary
import tank
import text


class Level:
    def __init__(self, player):
        self.player_img = pygame.image.load('sprites/fighterJet1.png').convert()
        self.player = player
        self.score = 0
        self.tanks = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.mob_bullets = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.missile_group = pygame.sprite.Group()
        self.ammo_powerups = pygame.sprite.Group()
        self.bomb_powerups = pygame.sprite.Group()
        self.speed_powerups = pygame.sprite.Group()
        self.gun_powerups = pygame.sprite.Group()
        self.Start_text = pygame.sprite.Group()
        self.boss_sprite = pygame.sprite.Group()
        self.helicopters = pygame.sprite.Group()
        self.laser_group = pygame.sprite.Group()
        self.civ_group = pygame.sprite.Group()
        self.running = True
        self.total_score = 0
        self.highscore = 0
        self.highscore_list = []
        self.load_data()

        # do not have to be reset
        self.total_tanks_killed = 0
        self.total_helicopters_killed = 0
        self.total_fighters_killed = 0
        self.total_fighters = 0
        self.total_helicopters_killed = 0
        self.total_helicopters = 0
        self.total_tanks = 0
        self.bomb_frame = 20

        # need to be reset after each level
        self.start_time = pygame.time.get_ticks()
        self.lives = 50
        self.bombs = 1
        self.number_of_spawns = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}
        self.starting_pos = -7080
        self.got_a_tank = 0
        self.tank_life = 5
        self.heli_num = 0
        self.heli_life = 20
        self.boss = None
        self.spawned_a_boss = 0
        self.charge = 0

        self.laser_time = pygame.time.get_ticks()
        self.blink_delay = pygame.time.get_ticks()
        self.meter_emptying = pygame.time.get_ticks()
        self.laser_charge_time = pygame.time.get_ticks()
        self.last_bomb = pygame.time.get_ticks()



    # load data from the highscore.txt file to get saved data
    def load_data(self):
        # finds current working directory
        with open("highscore.txt", 'r') as hs:
            for i in range(10):
                try:
                    highscore = int(hs.readline())

                except:
                    highscore = 0
                self.highscore_list.append(highscore)
                self.highscore = self.highscore_list[0]
                menu.highscore = self.highscore

    def player_lives(self):
        # This section controls player lives:
        if animations.first_death == 0 or animations.first_death == 2:
            bullet_hits = pygame.sprite.spritecollide(self.player, self.mob_bullets, True,
                                                      pygame.sprite.collide_circle)
            for every in bullet_hits:
                # Makes sure the laser gets deleted when the player dies
                if len(self.laser_group.sprites()) > 0:
                    self.player.laser_ready = False
                    self.player.firing_laser = False
                    self.charge = 0
                self.player.update()
                self.player.kill()
                expl = explosions.Explosion(every.rect.center, 'sm')
                self.all_sprites.add(expl)
                explode = random.randrange(2)
                if explode == 1:
                    self.exp1_sound.play()
                else:
                    self.exp2_sound.play()
                self.player = player_module.Player()
                self.all_sprites.add(self.player)
                animations.first_death += 1
                self.lives -= 1
                if self.lives < 1:
                    # dead()
                    if self.total_score > self.highscore_list[9]:
                        self.total_score += self.score
                        self.highscore_list[9] = self.total_score
                        self.highscore_list.sort(reverse=True)
                        with open(path.join(self.dir, "highscore.txt"), 'w') as hs:
                            for i in range(10):
                                hs.write(str(self.highscore_list[i]) + "\n")
                    if self.total_score == 0:
                        self.total_score += self.score
                    menu.total_score += self.total_score
                    self.level_summary()
                    menu.loser_loser()
                    Level.running = False

            mob_01_hits = pygame.sprite.spritecollide(self.player, self.mobs, True,
                                                      pygame.sprite.collide_circle)
            for every in mob_01_hits:
                # Makes sure the laser gets deleted when the player dies
                if len(self.laser_group.sprites()) > 0:
                    self.player.laser_ready = False
                    self.player.firing_laser = False
                    self.charge = 0
                self.player.update()
                self.player.kill()
                expl = explosions.Explosion(every.rect.center, 'sm')
                self.all_sprites.add(expl)
                explode = random.randrange(2)
                if explode == 1:
                    self.exp1_sound.play()
                else:
                    self.exp2_sound.play()
                self.player = player_module.Player()
                self.all_sprites.add(self.player)
                animations.first_death += 1
                self.lives -= 1
                if self.lives < 1:
                    # dead()
                    if self.total_score > self.highscore_list[9]:
                        self.total_score += self.score
                        self.highscore_list[9] = self.total_score
                        self.highscore_list.sort(reverse=True)
                        with open(path.join(self.dir, "highscore.txt"), 'w') as hs:
                            for i in range(10):
                                hs.write(str(self.highscore_list[i]) + "\n")
                    if self.total_score == 0:
                        self.total_score += self.score
                    menu.total_score += self.total_score
                    self.level_summary()
                    menu.loser_loser()
                    Level.running = False

    def civilian_planes(self):
        civilian_crash = pygame.sprite.spritecollide(self.player, self.civ_group, True,
                                                     pygame.sprite.collide_circle)
        civilian_hits = pygame.sprite.groupcollide(self.civ_group, self.bullets, True,
                                                   pygame.sprite.collide_circle)
        for every in civilian_crash:
            expl = explosions.Explosion(every.rect.center, 'sm')
            self.all_sprites.add(expl)
            explode = random.randrange(2)
            if explode == 1:
                self.exp1_sound.play()
            else:
                self.exp2_sound.play()
            self.total_score -= 100000
            # if total_score < 0:
            #     total_score = 0
        for every in civilian_hits:
            expl = explosions.Explosion(every.rect.center, 'sm')
            self.all_sprites.add(expl)
            explode = random.randrange(2)
            if explode == 1:
                self.exp1_sound.play()
            else:
                self.exp2_sound.play()
            self.total_score -= 100000

    def powerup_bomb(self):
        powerup_sound = pygame.mixer.Sound('sounds/ammo_powerup1.wav')
        powerup_sound.set_volume(0.3)
        hits = pygame.sprite.spritecollide(self.player, self.bomb_powerups,\
        True, pygame.sprite.collide_circle)
        for every in hits:
            self.bombs += 1
            powerup_sound.play()

    def bombsaway(self):
        self.exp1_sound = pygame.mixer.Sound('sounds/Explosion1.wav')
        self.exp1_sound.set_volume(0.3)
        self.exp2_sound = pygame.mixer.Sound('sounds/Explosion2.wav')
        self.exp2_sound.set_volume(0.3)
        mobs = self.mobs.sprites()
        for every in mobs:
            every.kill()
            self.score += 1
            expl = explosions.Explosion(every.rect.center, 'sm')
            self.all_sprites.add(expl)
            explode = random.randrange(2)
            if explode == 1:
                self.exp1_sound.play()
            else:
                self.exp2_sound.play()

    def bomb_update(self):
        # Updates the bombs triggered by the self.player
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
                    self.boss.life -= 20

    def powerup_speed(self):
        powerup_sound = pygame.mixer.Sound('sounds/ammo_powerup1.wav')
        powerup_sound.set_volume(0.3)
        hits = pygame.sprite.spritecollide(self.player, self.speed_powerups,\
        True, pygame.sprite.collide_circle)
        for every in hits:
            self.player.speed_multiplier += 1
            powerup_sound.play()

    def powerup_gun(self):
        powerup_sound = pygame.mixer.Sound('sounds/ammo_powerup1.wav')
        powerup_sound.set_volume(0.3)
        hits = pygame.sprite.spritecollide(self.player, self.gun_powerups, \
        True, pygame.sprite.collide_circle)
        for every in hits:
            self.player.upgrade += 1
            powerup_sound.play()

    def mob_spawn_01_left(self):
        if self.number_of_spawns[0] == 0:
            self.mob_01_left_ticks = self.start_time
        now = pygame.time.get_ticks()
        if now - self.mob_01_left_ticks > 750 and self.number_of_spawns[0] < 7:
            self.mob = mob_01_left.Mob_01_left(-30, 400, (300, 4, 2000))
            self.all_sprites.add(self.mob)
            self.mobs.add(self.mob)
            self.mob_01_left_ticks = now
            self.number_of_spawns[0] += 1

    def mob_spawn_01_right(self):
        if self.number_of_spawns[1] == 0:
            self.mob_01_right_ticks = self.start_time
        now = pygame.time.get_ticks()
        if now - self.mob_01_right_ticks > 750 and self.number_of_spawns[1] < 7:
            self.mob = mob_01_right.Mob_01_right(830, 400, (300, 4, 2000)) #(fire_rate, bullet_speed, delay)
            self.all_sprites.add(self.mob)
            self.mobs.add(self.mob)
            self.mob_01_right_ticks = now
            self.number_of_spawns[1] += 1

    def mob_spawn_02_left(self):
        if self.number_of_spawns[2] == 0:
            self.mob_02_left_ticks = self.start_time
        now = pygame.time.get_ticks()
        # self.mob_02_left_ticks = self.start_time
        if now - self.mob_02_left_ticks > 750 and self.number_of_spawns[2] < 7:
            self.mob = mob_02_left.Mob_02_left(-30, 510, (300, 4, 2000)) #(fire_rate, bullet_speed, delay)
            self.all_sprites.add(self.mob)
            self.mobs.add(self.mob)
            self.mob_02_left_ticks = now
            self.number_of_spawns[2] += 1

    def mob_spawn_02_right(self):
        # right_now = pygame.time.get_ticks()
        # if right_now - self.mob_02_delay > 750:
        if self.number_of_spawns[3] == 0:
            self.mob_02_right_ticks = self.start_time
        now = pygame.time.get_ticks()
        if now - self.mob_02_right_ticks > 750 and self.number_of_spawns[3] < 7:
            self.mob = mob_02_right.Mob_02_right(830, 510, (300, 4, 2000)) #(fire_rate, bullet_speed, delay)
            self.all_sprites.add(self.mob)
            self.mobs.add(self.mob)
            self.mob_02_right_ticks = now
            self.number_of_spawns[3] += 1

    def mob_spawn_03_left(self):
        if self.number_of_spawns[4] == 0:
            self.mob_03_left_ticks = self.start_time
        now = pygame.time.get_ticks()
        if now - self.mob_03_left_ticks > 750 and self.number_of_spawns[4] < 7:
            self.mob = mob_03_left.Mob_03_left(-30, 500, (300, 4, 2000)) #(fire_rate, bullet_speed, delay)
            self.all_sprites.add(self.mob)
            self.mobs.add(self.mob)
            self.mob_03_left_ticks = now
            self.number_of_spawns[4] += 1

    def mob_spawn_03_right(self):
        if self.number_of_spawns[5] == 0:
            self.mob_03_right_ticks = self.start_time
        now = pygame.time.get_ticks()
        if now - self.mob_03_right_ticks > 750 and self.number_of_spawns[5] < 7:
            self.mob = mob_03_right.Mob_03_right(830, 500, (300, 4, 2000)) #(fire_rate, bullet_speed, delay)
            self.all_sprites.add(self.mob)
            self.mobs.add(self.mob)
            self.mob_03_right_ticks = now
            self.number_of_spawns[5] += 1

    def mob_spawn_04_left(self):
        if self.number_of_spawns[6] == 0:
            self.mob_04_left_ticks = self.start_time
        now = pygame.time.get_ticks()
        if now - self.mob_04_left_ticks > 750 and self.number_of_spawns[6] < 4:
            self.mob = mob_04_left.Mob_04_left(-30, 510, (300, 4, 2000)) #(fire_rate, bullet_speed, delay)
            self.all_sprites.add(self.mob)
            self.mobs.add(self.mob)
            self.mob_04_left_ticks = now
            self.number_of_spawns[6] += 1

    def mob_spawn_04_right(self):
        if self.number_of_spawns[7] == 0:
            self.mob_04_right_ticks = self.start_time
        now = pygame.time.get_ticks()
        if now - self.mob_04_right_ticks > 750 and self.number_of_spawns[7] < 4:
            self.mob = mob_04_right.Mob_04_right(830, 510, (300, 4, 2000)) #(fire_rate, bullet_speed, delay)
            self.all_sprites.add(self.mob)
            self.mobs.add(self.mob)
            self.mob_04_right_ticks = now
            self.number_of_spawns[7] += 1

    def civilian_spawn(self, x, y, speedx, speedy, rotate):
        civ_plane = civilian.Civilian_plane(x, y, speedx, speedy, rotate) #(x, y, speedx, speedy, rotate)
        self.all_sprites.add(civ_plane)
        self.civ_group.add(civ_plane)
        self.civ_count += 1
        self.civ_time = pygame.time.get_ticks() + 500

    def civ_alert(self):
        if len(self.civ_group.sprites()) > 0:
            right_now = pygame.time.get_ticks()
            if self.civ_time > right_now:
                text.draw_text(self.screen, '!!Civilians Alert!!', 40, 675, 10, constants.RED, "Haettenschweiler")
            else:
                if right_now - self.civ_time > 500:
                    self.civ_time += 1000

    def shooting_mobs (self, mob_image, x, y, speedx, speedy, speed_mod, spawn_time):
        now = pygame.time.get_ticks()
        if now - self.mob_v2_time > spawn_time:
            # speed mods: 1-slow oscillations 2-fast oscillations 3-linear movement
            moby = mob.Mob(mob_image, x, y, speedx, speedy, speed_mod, (500, 4, 2000)) #(fire_rate, bullet_speed, delay)
            self.all_sprites.add(moby)
            self.mobs.add(moby)
            self.mob_v2_time = now
            summary.total_fighters += 1

    def tank_spawn(self, starting_pos_1, starting_pos_2):
        # As of right now, only 1 tank can be on the self.screen at a time.
        if self.starting_pos > starting_pos_1:
            if self.got_a_tank == 0:
                self.tank_01 = tank.Tank(300, -50)
                self.tank_01_body = tank.Tank_body(300, -50)
                self.all_sprites.add(self.tank_01_body)
                self.tanks.add(self.tank_01_body)
                self.all_sprites.add(self.tank_01)
                self.tanks.add(self.tank_01)
                self.got_a_tank += 1
                self.tank_life = 5
            if self.got_a_tank == 1:
                self.mob_bullets.add(tank.bullets)
                self.all_sprites.add(tank.bullets)
                hits = pygame.sprite.groupcollide(self.tanks, self.bullets, False, True)
                for every in hits:
                    self.tank_life -= 1
                if self.tank_life < 0 and len(self.tanks) > 0:
                    self.charge +=  10
                    self.score += 25000
                    self.total_tanks_killed += 1
                    expl = explosions.Explosion(self.tanks.sprites()[0].rect.center, 'sm')
                    self.all_sprites.add(expl)
                    self.tank_01.kill()
                    self.tank_01_body.kill()
                    self.tank_life -= 1

        if self.starting_pos > starting_pos_2:
            if self.got_a_tank == 1:
                self.tank_02 = tank.Tank(600, -50)
                self.tank_02_body = tank.Tank_body(600, -50)
                self.all_sprites.add(self.tank_02_body)
                self.tanks.add(self.tank_02_body)
                self.all_sprites.add(self.tank_02)
                self.tanks.add(self.tank_02)
                self.got_a_tank += 1
                self.tank_life = 5
            if self.got_a_tank == 2:
                self.mob_bullets.add(tank.bullets)
                self.all_sprites.add(tank.bullets)
                hits = pygame.sprite.groupcollide(self.tanks, self.bullets, False, True)
                for every in hits:
                    self.tank_life -= 1
                if self.tank_life < 0 and len(self.tanks) > 0:
                    self.charge += 10
                    self.score += 25000
                    self.total_tanks_killed += 1
                    expl = explosions.Explosion(self.tanks.sprites()[0].rect.center, 'sm')
                    self.all_sprites.add(expl)
                    self.tank_02.kill()
                    self.tank_02_body.kill()
                    self.tank_life -= 1

    def heli_spawn(self, spawn_pos_list, heli_attributes):
        now = pygame.time.get_ticks()
        if self.heli_num < len(spawn_pos_list) and self.starting_pos > spawn_pos_list[self.heli_num]\
                and len(self.helicopters) == 0:
            heli = helicopter.Helicopter(heli_attributes[self.heli_num][0], heli_attributes[self.heli_num][1],
                                         heli_attributes[self.heli_num][2], heli_attributes[self.heli_num][3])
            self.all_sprites.add(heli)
            self.helicopters.add(heli)
            self.heli_num += 1
            self.heli_life = 20
        if self.heli_num > 0:
            self.mob_bullets.add(helicopter.bullets)
            self.all_sprites.add(helicopter.bullets)
            hits = pygame.sprite.groupcollide(self.helicopters, self.bullets, False, True)
            for every in hits:
                self.heli_life -= 1
            if self.heli_life < 0 and len(self.helicopters) > 0:
                self.charge += 30
                self.score += 100000
                self.total_helicopters_killed += 1
                expl = explosions.Explosion(self.helicopters.sprites()[0].rect.center, 'sm')
                self.all_sprites.add(expl)
                self.helicopters.sprites()[0].kill()

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
        if not self.player.firing_laser:
            self.laser_time = right_now
        if self.player.laser_ready and self.player.firing_laser:
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
        if self.player.firing_laser:
            if self.laser_sound_mix == 0:
                self.laser_sound.play(loops = 0)
                self.laser_sound_mix += 1
            now = pygame.time.get_ticks()
            if now - self.meter_emptying > 50:
                self.charge -= 1.8
                self.meter_emptying = now
        if not self.player.laser_not_ready:
            self.laser_not_ready = right_now + 2000
        if self.player.laser_not_ready:
            if self.laser_not_ready > right_now:
                text.draw_text(self.screen, 'LASER NOT CHARGED', 20, 140, 522, constants.RED, "Haettenschweiler")
            else:
                self.player.laser_not_ready = False

    def paused(self):
        text.draw_text(self.screen, "Paused", 200, 400, 120, constants.BLUE, "ariel")
        text.draw_text(self.screen, "Press [p] key to UNPAUSE", 50, 400, 250, constants.BLUE, "ariel")
        text.draw_text(self.screen, "Press [ESC] key to EXIT GAME", 50, 400, 300, constants.BLUE, "ariel")
        # button_sprites = pygame.sprite.Group()
        # images = ['sprites/enemyBlack1.png', 'sprites/enemyBlue1.png']
        # continue_button = button.Button(images, 300, 600)
        # button_sprites.add(continue_button)
        pause = True
        # The key press code for pause is in the self.player_module
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
            pygame.display.update()
            self.clock.tick(15)

    def draw_hud(self):
        text.draw_text(self.screen, str(self.total_score + self.score), 50, constants.WIDTH/2 + 10 , 10, constants.SCORE_RED, "Haettenschweiler") #(surf, text, size, x, y, color, font name)
        # text.draw_text(self.screen, 'AMMO: ' + str(self.player.ammo), 30, constants.WIDTH - 70, constants.HEIGHT - 120, constants.BLACK, "Haettenschweiler")
        text.draw_text(self.screen, 'BOMBS: ' + str(self.bombs), 20, 140, 497, constants.RED, "Haettenschweiler")
        text.draw_text(self.screen, 'Time: ' + str(round(summary.time/1000)), 20, 140, 470, constants.RED, "Haettenschweiler")
        text.draw_text(self.screen, 'LIVES: ' + str(self.lives), 30, 50, 10, constants.GREEN, "Haettenschweiler")
        text.draw_text(self.screen, '25%', 20, 65, 555, constants.DARK_GREEN, "Haettenschweiler")
        text.draw_text(self.screen, '50%', 20, 115, 555, constants.DARK_GREEN, "Haettenschweiler")
        text.draw_text(self.screen, '75%', 20, 162, 555, constants.DARK_GREEN, "Haettenschweiler")
        text.draw_text(self.screen, '100%', 20, 212, 555, constants.DARK_GREEN, "Haettenschweiler")
