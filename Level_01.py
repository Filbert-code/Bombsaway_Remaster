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
        self.starting_pos = -7080
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
        self.total_tanks_killed = 0
        self.total_tanks = 0

        self.got_a_tank = 0
        self.new_player = 0
        self.player_input = 0
        self.number_of_tank_hits = 0
        self.tank_life = 10
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
        self.afterburners = "NO FUEL"
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
        self.powerup_ammo()
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
        self.tank_spawn()
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

    def powerup_ammo(self):
        powerup_sound = pygame.mixer.Sound('sounds/ammo_powerup2.wav')
        powerup_sound.set_volume(0.3)
        hits = pygame.sprite.spritecollide(self.player, self.ammo_powerups,\
        True, pygame.sprite.collide_circle)
        for every in hits:
            self.player.ammo += 20
            powerup_sound.play()

    def powerup_bomb(self):
        powerup_sound = pygame.mixer.Sound('sounds/ammo_powerup1.wav')
        powerup_sound.set_volume(0.3)
        hits = pygame.sprite.spritecollide(self.player, self.bomb_powerups,\
        True, pygame.sprite.collide_circle)
        for every in hits:
            self.bombs += 1
            powerup_sound.play()

    def powerup_speed(self):
        powerup_sound = pygame.mixer.Sound('sounds/ammo_powerup1.wav')
        powerup_sound.set_volume(0.3)
        hits = pygame.sprite.spritecollide(self.player, self.speed_powerups,\
        True, pygame.sprite.collide_circle)
        for every in hits:
            self.player.speed_multiplier += 1
            self.afterburners = "ACTIVE  FUEL LEFT:"
            powerup_sound.play()

    def powerup_gun(self):
        powerup_sound = pygame.mixer.Sound('sounds/ammo_powerup1.wav')
        powerup_sound.set_volume(0.3)
        hits = pygame.sprite.spritecollide(self.player, self.gun_powerups, \
        True, pygame.sprite.collide_circle)
        for every in hits:
            self.player.upgrade += 1
            powerup_sound.play()

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

    def mob_spawn_01_left(self):
        now = pygame.time.get_ticks()
        if now - self.mob_01_left_ticks > 750 and self.number_of_spawns[0] < 7:
            self.mob = mob_01_left.Mob_01_left(-30, 400, (300, 4, 2000))
            self.all_sprites.add(self.mob)
            self.mobs.add(self.mob)
            self.mob_01_left_ticks = now
            self.number_of_spawns[0] += 1

    def mob_spawn_01_right(self):
        # right_now = pygame.time.get_ticks()
        # if right_now - self.mob_01_delay > 750:
        now = pygame.time.get_ticks()
        if now - self.mob_01_right_ticks > 750 and self.number_of_spawns[1] < 7:
            self.mob = mob_01_right.Mob_01_right(830, 400, (300, 4, 2000)) #(fire_rate, bullet_speed, delay)
            self.all_sprites.add(self.mob)
            self.mobs.add(self.mob)
            self.mob_01_right_ticks = now
            self.number_of_spawns[1] += 1

    def mob_spawn_02_left(self):
            now = pygame.time.get_ticks()
            if now - self.mob_02_left_ticks > 750 and self.number_of_spawns[2] < 7:
                self.mob = mob_02_left.Mob_02_left(-30, 510, (300, 4, 2000)) #(fire_rate, bullet_speed, delay)
                self.all_sprites.add(self.mob)
                self.mobs.add(self.mob)
                self.mob_02_left_ticks = now
                self.number_of_spawns[2] += 1

    def mob_spawn_02_right(self):
        # right_now = pygame.time.get_ticks()
        # if right_now - self.mob_02_delay > 750:
        now = pygame.time.get_ticks()
        if now - self.mob_02_right_ticks > 750 and self.number_of_spawns[3] < 7:
            self.mob = mob_02_right.Mob_02_right(830, 510, (300, 4, 2000)) #(fire_rate, bullet_speed, delay)
            self.all_sprites.add(self.mob)
            self.mobs.add(self.mob)
            self.mob_02_right_ticks = now
            self.number_of_spawns[3] += 1

    def mob_spawn_03_left(self):
        now = pygame.time.get_ticks()
        if now - self.mob_03_left_ticks > 750 and self.number_of_spawns[4] < 7:
            self.mob = mob_03_left.Mob_03_left(-30, 500, (300, 4, 2000)) #(fire_rate, bullet_speed, delay)
            self.all_sprites.add(self.mob)
            self.mobs.add(self.mob)
            self.mob_03_left_ticks = now
            self.number_of_spawns[4] += 1

    def mob_spawn_03_right(self):
        now = pygame.time.get_ticks()
        if now - self.mob_03_right_ticks > 750 and self.number_of_spawns[5] < 7:
            self.mob = mob_03_right.Mob_03_right(830, 500, (300, 4, 2000)) #(fire_rate, bullet_speed, delay)
            self.all_sprites.add(self.mob)
            self.mobs.add(self.mob)
            self.mob_03_right_ticks = now
            self.number_of_spawns[5] += 1

    def mob_spawn_04_left(self):
        now = pygame.time.get_ticks()
        if now - self.mob_04_left_ticks > 750 and self.number_of_spawns[6] < 4:
            self.mob = mob_04_left.Mob_04_left(-30, 510, (300, 4, 2000)) #(fire_rate, bullet_speed, delay)
            self.all_sprites.add(self.mob)
            self.mobs.add(self.mob)
            self.mob_04_left_ticks = now
            self.number_of_spawns[6] += 1

    def mob_spawn_04_right(self):
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

    def tank_spawn(self):
        # As of right now, only 1 tank can be on the self.screen at a time.
        if self.starting_pos > -4200:
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

        if self.starting_pos > -1800:
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

    def boss_spawn(self):
        if self.total == 0 and len(self.mobs) == 0 and self.spawned_a_boss == 0:
            self.boss = boss.Boss(322, -250, 0, 1)
            self.all_sprites.add(self.boss)
            self.boss_sprite.add(self.boss)
            self.spawned_a_boss = 1

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

    def bomb_animation(self):
        now = pygame.time.get_ticks()
        if now - self.last_bomb_anim > 20:
            self.last_bomb_anim = now
            self.screen.blit(animations.bombsaway_anim[self.bomb_frame], \
            (self.player.rect.centerx-(self.bomb_frame+1)*50, self.player.rect.centery-(self.bomb_frame+1)*float(37.5)))
            self.bomb_frame += 1

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