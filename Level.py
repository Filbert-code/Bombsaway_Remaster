import random
import pygame
from os import path
import animations
import explosions
import menu
import player_module
import mob_01_left, mob_01_right, mob_02_left, mob_02_right
import mob_03_left,mob_03_right,mob_04_left, mob_04_right

# Parent level class. Sharing level characteristics are initiated here


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

        self.lives = 50
        self.number_of_spawns = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}

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