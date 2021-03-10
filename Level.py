import random
import pygame
from os import path
import animations
import explosions
import menu
import player_module

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