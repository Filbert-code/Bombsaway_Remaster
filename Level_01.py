import pygame
import mob, boss, menu, player_module
import powerup, explosions
import animations, cars, purgatory
import text, random, constants
import mob_01_left, mob_01_right, mob_02_left, mob_02_right
import mob_03_left,mob_03_right,mob_04_left, mob_04_right
import tank, helicopter, summary, civilian
from os import path
from Level import Level


# First level
class Level_01(Level):
    def __init__(self, player, screen, clock):
        Level.__init__(self, player)
        self.background = pygame.image.load('backgrounds/rural_city_map16.png').convert()
        self.all_sprites.add(self.player)
        pygame.mixer.music.load('sounds/chiptunes_level_1.wav')
        pygame.mixer.music.set_volume(0.55)

        self.player = player
        self.screen = screen
        self.clock = clock
        ##############
        # Level-child attributes:
        self.total = None


        self.spawn_powerups()


        self.cars_up_images = []
        self.cars_down_images = []
        self.cars_up_y = {}
        self.cars_down_y = {}
        self.cars_up_y[0] = [400, 600, 1000, 1500, 2000, 2500, 2800, 3400]
        self.cars_up_y[1] = [200, 500, 1200, 1400, 2200, 2400, 3000, 3800]
        self.cars_down_y[0] = [100, 400, 800, 1900, 2200, 3000, 3200, 3600]
        self.cars_down_y[1] = [750, 1000, 1350, 2400, 2600, 3200, 3550, 3800]
        self.cars_up_x = [337, 369]
        self.cars_down_x = [415, 447]
        self.car_up_images()
        self.car_down_images()

        self.start_time = pygame.time.get_ticks()
        self.mob_01_delay = pygame.time.get_ticks()
        self.mob_02_delay = pygame.time.get_ticks()
        self.laser_charge_time = pygame.time.get_ticks()

        self.last_bomb_anim = pygame.time.get_ticks()

        # Level Summary tracking information:




        self.new_player = 0
        self.player_input = 0
        self.number_of_tank_hits = 0
        self.tank_life = 10
        self.number_of_heli_hits = 0
        self.heli_life = 20

        self.mob_v2_time = pygame.time.get_ticks()
        self.charge = 0
        self.civ_count = 0
        self.laser_start_pos = self.starting_pos
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
        self.mob_bullets.add(boss.bullets_group)
        self.all_sprites.add(boss.bullets_group)
        self.all_sprites.update()
        self.laser_group.update()
        self.player_lives()
        self.civilian_planes()
        self.explosions()
        self.down_cars_update()
        self.up_cars_update()
        self.powerup_bomb()
        self.powerup_speed()
        self.powerup_gun()
        self.bomb_update()
        self.boss_damage()
        self.player_position()
        self.laser_kill()
        # If self.player presses [p] key, game will pause. Press again for unpause
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_p]:
            self.paused()

    def draw(self):
        for lst in range(len(self.cars_up_y)):
            for i in range(len(self.cars_up_y[lst])):
                self.screen.blit(self.cars_up_images[i], (self.cars_up_x[lst], self.cars_up_y[lst][i]))
        for lst in range(len(self.cars_down_y)):
            for i in range(len(self.cars_down_y[lst])):
                self.screen.blit(self.cars_down_images[i], (self.cars_down_x[lst], self.cars_down_y[lst][i]))
        self.tank_spawn(-4200, -1800)
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
        if self.spawned_a_boss > 0 and self.boss.new_sequence > 0:
            self.health_bar()

    def car_up_images(self):
        for i in range(8):
            self.carname = 'new_car{}'.format(i)
            self.carname = cars.Moving_cars_up()
            self.image = self.carname.image
            self.cars_up_images.append(self.image)

    def car_down_images(self):
        for i in range(8):
            self.carname = 'new_car{}'.format(i)
            self.carname = cars.Moving_cars_down()
            self.image = self.carname.image
            self.cars_down_images.append(self.image)

    def up_cars_update(self):
        for lst in self.cars_up_y:
            for car in range(len(self.cars_up_y[lst])):
                if self.total == 0:
                    self.cars_up_y[lst][car] -= 1
                    if self.cars_up_y[lst][car] < -30:
                        self.cars_up_y[lst][car] += 3840
                else:
                    self.cars_up_y[lst][car] += 1
                    if self.cars_up_y[lst][car] > 3840:
                        self.cars_up_y[lst][car] -= 3870

    def down_cars_update(self):
        for lst in self.cars_down_y:
            for car in range(len(self.cars_down_y[lst])):
                if self.total == 0:
                    self.cars_down_y[lst][car] += 1
                    if self.cars_down_y[lst][car] > 3840:
                        self.cars_down_y[lst][car] -= 3870
                else:
                    self.cars_down_y[lst][car] += 3
                    if self.cars_down_y[lst][car] > 3840:
                        self.cars_down_y[lst][car] -= 3870


    def spawn_powerups(self):
        # for i in range(12):
        #     new_power = powerup.Powerup(i*-1000, 0)
        #     self.all_sprites.add(new_power)
        #     self.ammo_powerups.add(new_power)
        for i in range(1):
            new_power1 = powerup.Powerup(-2500, 1)
            self.all_sprites.add(new_power1)
            self.bomb_powerups.add(new_power1)
        for i in range(1):
            new_power2 = powerup.Powerup(-3500, 2)
            self.all_sprites.add(new_power2)
            self.speed_powerups.add(new_power2)
        for i in range(1):
            new_power3 = powerup.Powerup(-1500, 3)
            self.all_sprites.add(new_power3)
            self.gun_powerups.add(new_power3)


    def mob_draw(self):
        if self.starting_pos > -6000 and self.civ_count < 1:
            self.civilian_spawn(-30, 300, 2, 0, -90)
        if self.starting_pos > -6800:
            self.mob_spawn_02_right()
        if -5700 > self.starting_pos > -6000:
            self.shooting_mobs(0, -30, 100, 4, 1, 3, 1000)
        if self.starting_pos > -5200:
            self.mob_spawn_03_left()
        if self.starting_pos > -4500:
            self.mob_spawn_01_right()
        if -3200 > self.starting_pos > -3600:
            self.shooting_mobs(1, 830, 100, -3, 0, 2, 1000)
        if self.starting_pos > -3200:
            self.mob_spawn_01_left()
        if -2200 > self.starting_pos > -2400:
            self.shooting_mobs(0, -30, 100, 3, 0, 1, 750)
        if self.starting_pos > -1800:
            self.mob_spawn_02_right()


    def boss_spawn(self):
        if self.total == 0 and len(self.mobs) == 0 and self.spawned_a_boss == 0:
            self.boss = boss.Boss(322, -250, 0, 1)
            self.all_sprites.add(self.boss)
            self.boss_sprite.add(self.boss)
            self.spawned_a_boss = 1

    def bomb_animation(self):
        now = pygame.time.get_ticks()
        if now - self.last_bomb_anim > 20:
            self.last_bomb_anim = now
            self.screen.blit(animations.bombsaway_anim[self.bomb_frame], \
            (self.player.rect.centerx-(self.bomb_frame+1)*50, self.player.rect.centery-(self.bomb_frame+1)*float(37.5)))
            self.bomb_frame += 1



    def boss_damage(self):
        if self.spawned_a_boss == 1:
            hits = pygame.sprite.spritecollide(self.boss, self.bullets, True)
            for every in hits:
                self.boss.life -= 1
            if self.boss.life < 1:
                self.boss.kill()

    def spawn_portal(self):
        if self.portal_frame > 7:
            self.portal_frame = 0
        now = pygame.time.get_ticks()
        if now - self.last_portal_anim > 20:
            self.last_portal_anim = now
            self.portal_frame += 1
        if ((self.boss.rect.y+146)-20 <= self.player.rect.bottom - 50 < (self.boss.rect.y+146)+20):
            if ((self.boss.rect.x)-20 <= self.player.rect.centerx - 75 < (self.boss.rect.x)+20):
                self.portal_activated = True

    def health_bar(self):
        for i in range(10):
            if i*10 < self.boss.life <= (i+1)*10:
                image = animations.boss_health_images[(i+1)]
                image.set_colorkey(constants.WHITE)
        if self.boss.life <= 0:
            image = animations.boss_health_images[0]
        text.draw_text(self.screen, 'HEALTH: ', 24, 100, 7, constants.BLACK, "ariel")
        self.screen.blit(image, (135, 5))


    def level_summary(self):
        spawns = 0
        for i in range(8):
            spawns += self.number_of_spawns.get(i)
        self.total_fighters += spawns
        self.total_helicopters += 0
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
        purgatory.level_1_summary()

    def player_position(self):
        tank.player_position = [self.player.rect.centerx, self.player.rect.centery]
        helicopter.player_position = [self.player.rect.centerx, self.player.rect.centery]

