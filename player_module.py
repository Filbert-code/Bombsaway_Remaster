import pygame
import math
import random
import animations
import bullet
import constants
import laser


class Player(pygame.sprite.Sprite):
    def __init__(self):
        print("Player has been initiated")
        pygame.sprite.Sprite.__init__(self)
        self.image = animations.fighter_anim[1]
        self.image.set_colorkey(constants.WHITE)
        self.rect = self.image.get_rect()
        self.radius = 20
        # pygame.draw.circle(self.image, constants.RED, self.rect.center, self.radius)
        self.rect.centerx = constants.WIDTH/2 + 7
        self.rect.bottom = constants.HEIGHT - 60
        self.speedx = 0
        self.speedy = 0
        self.shoot_delay = 300
        self.last_shot = pygame.time.get_ticks()
        self.last_second_shot = pygame.time.get_ticks()
        self.last_missile = pygame.time.get_ticks()
        self.ammo = 20
        self.frame_rate = 100
        self.frame = 3
        self.last_update = pygame.time.get_ticks()
        self.last_anim = pygame.time.get_ticks()
        # self.last_anim_2 = pygame.time.get_ticks()
        # self.last_anim_3 = pygame.time.get_ticks()
        self.bullets = pygame.sprite.Group()
        self.pause = None
        self.last_alive = pygame.time.get_ticks()
        self.animation = 0
        self.animation_up = 0
        self.animation_down = 0
        self.speed_multiplier = 0
        self.speed_mult_time = pygame.time.get_ticks()
        self.speed_timer_start = 0
        self.numbers = 0
        self.upgrade = 0
        self.firing_laser = False
        self.laser_sprite = pygame.sprite.Group()
        self.laser_ready = False
        self.laser_not_ready = False

    def update(self):
        self.speedx = 0
        self.speedy = 0

        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.speedx = -8.5
        if keystate[pygame.K_d]:
            self.speedx = 8.5
        if keystate[pygame.K_w]:
            self.speedy = -6.5
        if keystate[pygame.K_s]:
            self.speedy = 6.5
        if keystate[pygame.K_SPACE]:
            if self.upgrade == 0:
                self.shoot()
            elif self.upgrade == 1:
                self.shoot_more()
            elif self.upgrade == 2:
                self.shoot_even_more()
            elif self.upgrade == 3:
                self.shoot_even_way_more()
        self.laser_logic()


        if self.speed_multiplier == 0:
            self.rect.x += self.speedx
            self.rect.y += self.speedy

        self.speed_multiply()

        if self.rect.right > constants.WIDTH:
            self.rect.right = constants.WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > constants.HEIGHT - 10:
            self.rect.bottom = constants.HEIGHT - 10

        if animations.first_death == 0 or animations.first_death == 2:
            self.player_animation()
        else:
            self.player_death_animation()
            died_once = pygame.time.get_ticks()
            if died_once - self.last_alive > 3000 and animations.first_death == 1:
                animations.first_death += 1
            if animations.first_death == 3:
                died_second = pygame.time.get_ticks()
                if died_second - self.last_alive > 3000:
                    animations.first_death = 0



    def shoot(self):
        shoot_sound = pygame.mixer.Sound('sounds/Laser_Shoot.wav')
        shoot_sound.set_volume(0.4)
        now = pygame.time.get_ticks()

        if now - self.last_shot > self.shoot_delay and self.ammo > 0:
            self.last_shot = now
            projectile = bullet.Bullets(self.rect.centerx + 5, self.rect.top, 0, -10, 0)
            self.bullets.add(projectile)
            shoot_sound.play()
            # self.ammo -= 1
        else:
            pass

    def shoot_more(self):
        shoot_sound = pygame.mixer.Sound('sounds/Laser_Shoot.wav')
        shoot_sound.set_volume(0.4)
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay/1.5 and self.ammo > 0:
            self.last_shot = now
            projectile = bullet.Bullets(self.rect.centerx + 5, self.rect.top,0, -10, 0)
            self.bullets.add(projectile)
            shoot_sound.play()
            # self.ammo -= 1

    def shoot_even_more(self):
        shoot_sound = pygame.mixer.Sound('sounds/Laser_Shoot.wav')
        shoot_sound.set_volume(0.4)
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay/2 and self.ammo > 0:
            self.last_shot = now
            projectile = bullet.Bullets(self.rect.centerx + 5, self.rect.top,0, -10, 0)
            self.bullets.add(projectile)
            shoot_sound.play()
            # self.ammo -= 1

    def shoot_even_way_more(self):
        shoot_sound = pygame.mixer.Sound('sounds/Laser_Shoot.wav')
        shoot_sound.set_volume(0.4)
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay/2 and self.ammo > 0:
            self.last_shot = now
            projectile_1 = bullet.Bullets(self.rect.centerx + 5, self.rect.top,0, -10, 0)
            self.bullets.add(projectile_1)
            shoot_sound.play()
        else:
            pass
        if now - self.last_second_shot > self.shoot_delay and self.ammo > 0:
            self.last_second_shot = now
            projectile_2 = bullet.Bullets(self.rect.centerx + 5, self.rect.top, 1,-8, -7)
            self.bullets.add(projectile_2)
            projectile_3 = bullet.Bullets(self.rect.centerx + 5, self.rect.top, -1, -8, 7)
            self.bullets.add(projectile_3)
        else:
            pass

    def firing_my_laser(self):
        my_laser = laser.Laser()
        self.laser_sprite.add(my_laser)

    def laser_logic(self):
        # Below are the logic statements that control when the laser can and can't be fired
        keystate = pygame.key.get_pressed()
        if len(self.laser_sprite.sprites()) > 0:
            if self.laser_ready == False and self.firing_laser == False:
                while len(self.laser_sprite.sprites()) > 0:
                    self.laser_sprite.sprites()[0].kill()
        if keystate[pygame.K_l] and self.laser_ready == True:
            laser.player_position = [self.rect.centerx, self.rect.centery]
            self.firing_my_laser()
            self.firing_laser = True
        if keystate[pygame.K_l] and self.laser_ready == False:
            self.laser_not_ready = True
        if self.firing_laser == True:
            laser.player_position = [self.rect.centerx, self.rect.centery]


    def speed_multiply(self):
        if self.speed_multiplier == 1:
            now = pygame.time.get_ticks()
            if self.speed_timer_start == 0:
                self.speed_mult_time = now
            if now - self.speed_mult_time < 30000:
                self.rect.x += 1.5*self.speedx
                self.rect.y += 1.5*self.speedy
                self.speed_timer_start = 1
                self.numbers = 30 - int(30*(now - self.speed_mult_time)/30000)
            else:
                self.speed_multiplier = 0
                self.afterburners = "NO FUEL"

    def player_explosion(self):
        frame = 0
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            frame += 1
            if frame == len(animations.explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = animations.explosion_anim[self.size][frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

    def player_animation(self):
        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_d]:
            right_now = pygame.time.get_ticks()
            if right_now - self.last_anim > 50:
                self.last_anim = right_now
                self.frame += 1
                if self.frame > 6:
                    self.frame = 6
                self.animation += 1
                if self.animation > 14:
                    self.animation = 0
                self.animation_up = 0
                self.frames()

        elif keystate[pygame.K_a]:
            right_now = pygame.time.get_ticks()
            if right_now - self.last_anim > 50:
                self.last_anim = right_now
                self.frame -= 1
                if self.frame < 0:
                    self.frame = 0
                self.animation += 1
                if self.animation > 14:
                    self.animation = 0
                self.animation_up = 0
                self.frames()

        elif keystate[pygame.K_w]:
            now = pygame.time.get_ticks()
            if now - self.last_anim > 50:
                self.last_anim = now
                self.animation_up += 1
                if self.animation_up > 14:
                    self.animation_up = 11
                if self.frame > 3:
                    self.frame -= 1
                if self.frame < 3:
                    self.frame += 1
                if self.frame == 3:
                    self.frame = 3
                self.frames_up()

        elif keystate[pygame.K_s]:
            just_now = pygame.time.get_ticks()
            if just_now - self.last_anim > 50:
                self.last_anim = just_now
                self.animation_down += 1
                if self.animation_down > 14:
                    self.animation_down = 11
                if self.frame > 3:
                    self.frame -= 1
                if self.frame < 3:
                    self.frame += 1
                if self.frame == 3:
                    self.frame = 3
                self.frames_down()

        else:
            just_now = pygame.time.get_ticks()
            if just_now - self.last_anim > 50:
                self.last_anim = just_now
                if self.frame > 3:
                    self.frame -= 1
                if self.frame < 3:
                    self.frame += 1
                if self.frame == 3:
                    self.frame = 3
                self.animation += 1
                if self.animation > 14:
                    self.animation = 0
                self.frames()
                # Returns the exhaust animmation from [up] back to [idle]
                if self.animation_down > 0:
                    self.animation_down -= 1
                    self.frames_down()

                if self.animation_up > 0:
                    self.animation_up -= 1
                    self.frames_up()

    def frames(self):
        if self.frame == 0:
            self.image = animations.jet_exhaust_anim_0[self.animation]
        if self.frame == 1:
            self.image = animations.jet_exhaust_anim_1[self.animation]
        if self.frame == 2:
            self.image = animations.jet_exhaust_anim_2[self.animation]
        if self.frame == 3:
            self.image = animations.jet_exhaust_anim_3[self.animation]
        if self.frame == 4:
            self.image = animations.jet_exhaust_anim_4[self.animation]
        if self.frame == 5:
            self.image = animations.jet_exhaust_anim_5[self.animation]
        if self.frame == 6:
            self.image = animations.jet_exhaust_anim_6[self.animation]

    def frames_up(self):
        if self.frame == 0:
            self.image = animations.jet_exhaust_anim_up_0[self.animation_up]
        if self.frame == 1:
            self.image = animations.jet_exhaust_anim_up_1[self.animation_up]
        if self.frame == 2:
            self.image = animations.jet_exhaust_anim_up_2[self.animation_up]
        if self.frame == 3:
            self.image = animations.jet_exhaust_anim_up_3[self.animation_up]
        if self.frame == 4:
            self.image = animations.jet_exhaust_anim_up_4[self.animation_up]
        if self.frame == 5:
            self.image = animations.jet_exhaust_anim_up_5[self.animation_up]
        if self.frame == 6:
            self.image = animations.jet_exhaust_anim_up_6[self.animation_up]

    def frames_down(self):
        if self.frame == 0:
            self.image = animations.jet_exhaust_anim_down_0[self.animation_down]
        if self.frame == 1:
            self.image = animations.jet_exhaust_anim_down_1[self.animation_down]
        if self.frame == 2:
            self.image = animations.jet_exhaust_anim_down_2[self.animation_down]
        if self.frame == 3:
            self.image = animations.jet_exhaust_anim_down_3[self.animation_down]
        if self.frame == 4:
            self.image = animations.jet_exhaust_anim_down_4[self.animation_down]
        if self.frame == 5:
            self.image = animations.jet_exhaust_anim_down_5[self.animation_down]
        if self.frame == 6:
            self.image = animations.jet_exhaust_anim_down_6[self.animation_down]


    def player_death_animation(self):
        now = pygame.time.get_ticks()
        if now - self.last_anim > 75:
            self.last_anim = now
            self.image = animations.fighter_reborn[self.frame]
            self.frame += 1
            if self.frame > 6:
                self.frame = 1
