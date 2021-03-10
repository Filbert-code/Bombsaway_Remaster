import pygame
import constants
pygame.init()
pygame.display.set_mode()

explosion_anim = {}
explosion_anim['sm'] = []
fighter_anim = []
fighter_reborn = []
bombsaway_anim = []
heli_anim = []
tank_anim = []
jet_exhaust_anim_0 = []
jet_exhaust_anim_1 = []
jet_exhaust_anim_2 = []
jet_exhaust_anim_3 = []
jet_exhaust_anim_4 = []
jet_exhaust_anim_5 = []
jet_exhaust_anim_6 = []
jet_exhaust_anim_up_0 = []
jet_exhaust_anim_up_1 = []
jet_exhaust_anim_up_2 = []
jet_exhaust_anim_up_3 = []
jet_exhaust_anim_up_4 = []
jet_exhaust_anim_up_5 = []
jet_exhaust_anim_up_6 = []
jet_exhaust_anim_down_0 = []
jet_exhaust_anim_down_1 = []
jet_exhaust_anim_down_2 = []
jet_exhaust_anim_down_3 = []
jet_exhaust_anim_down_4 = []
jet_exhaust_anim_down_5 = []
jet_exhaust_anim_down_6 = []
boss_health_images = []
laser_meter_images = []
laser_images = []
boss_3_images = []
portal_anim = []
first_death = 0

civ_image = pygame.transform.scale(pygame.image.load('sprites/civilian_airplane.png'),(90,90))

for i in range(7):
    file = 'sprites/mig/mig_{}.png'.format(i)
    img = pygame.image.load(file).convert()
    img.set_colorkey(constants.BLACK)
    img.set_alpha(150)
    # image = pygame.transform.scale(img, (45, 80))
    fighter_reborn.append(img)

for i in range(7):
    filename = 'sprites/expl{}.png'.format(i)
    img = pygame.image.load(filename).convert_alpha()
    img.set_colorkey(constants.BLACK)
    img_sm = pygame.transform.scale(img, (50, 50))
    explosion_anim['sm'].append(img_sm)

for i in range(7):
    filename = 'sprites/mig/mig_{}.png'.format(i)
    image = pygame.image.load(filename).convert_alpha()
    # image.set_colorkey(constants.WHITE)
    image = pygame.transform.scale(image, (40, 68))
    fighter_anim.append(image)

for i in range(20):
    filename = 'sprites/bombsaway{}00.png'.format(i+1)
    imag = pygame.image.load(filename).convert_alpha()
    imag.set_colorkey(constants.BLACK)
    bombsaway_anim.append(imag)

for i in range(17):
    filename = 'sprites/heli/heli_{}.png'.format(i+1)
    image = pygame.image.load(filename).convert_alpha()
    # image.set_colorkey(constants.WHITE)
    image = pygame.transform.scale(image, (200, 200))
    heli_anim.append(image)

# Tank animation

for i in range(-45, 46):
    filename = 'sprites/rotation/tank_top_{}.png'.format(i)
    image = pygame.image.load(filename).convert_alpha()
    image = pygame.transform.scale(image, (100, 100))
    tank_anim.append(image)

# Jet exhaust idle

for i in range(16):
    filename = 'sprites/mig/mig_0_flames/mig_{}.png'.format(i)
    image = pygame.image.load(filename).convert_alpha()
    # image.set_colorkey(constants.WHITE)
    image = pygame.transform.scale(image, (22, 124))
    jet_exhaust_anim_0.append(image)

for i in range(16):
    filename = 'sprites/mig/mig_1_flames/mig_{}.png'.format(i)
    image = pygame.image.load(filename).convert_alpha()
    # image.set_colorkey(constants.WHITE)
    image = pygame.transform.scale(image, (20, 124))
    jet_exhaust_anim_1.append(image)

for i in range(16):
    filename = 'sprites/mig/mig_2_flames/mig_{}.png'.format(i)
    image = pygame.image.load(filename).convert_alpha()
    # image.set_colorkey(constants.WHITE)
    image = pygame.transform.scale(image, (34, 124))
    jet_exhaust_anim_2.append(image)

for i in range(16):
    filename = 'sprites/mig/mig_3_flames/mig_{}.png'.format(i)
    image = pygame.image.load(filename).convert_alpha()
    # image.set_colorkey(constants.WHITE)
    image = pygame.transform.scale(image, (50, 124))
    jet_exhaust_anim_3.append(image)

for i in range(16):
    filename = 'sprites/mig/mig_4_flames/mig_{}.png'.format(i)
    image = pygame.image.load(filename).convert_alpha()
    # image.set_colorkey(constants.WHITE)
    image = pygame.transform.scale(image, (34, 124))
    jet_exhaust_anim_4.append(image)

for i in range(16):
    filename = 'sprites/mig/mig_5_flames/mig_{}.png'.format(i)
    image = pygame.image.load(filename).convert_alpha()
    # image.set_colorkey(constants.WHITE)
    image = pygame.transform.scale(image, (20, 124))
    jet_exhaust_anim_5.append(image)

for i in range(16):
    filename = 'sprites/mig/mig_6_flames/mig_{}.png'.format(i)
    image = pygame.image.load(filename).convert_alpha()
    # image.set_colorkey(constants.WHITE)
    image = pygame.transform.scale(image, (22, 124))
    jet_exhaust_anim_6.append(image)

# Jet exhaust up

for i in range(15):
    filename = 'sprites/mig/mig_0_flames_up/mig_{}.png'.format(i)
    image = pygame.image.load(filename).convert_alpha()
    # image.set_colorkey(constants.WHITE)
    image = pygame.transform.scale(image, (22, 124))
    jet_exhaust_anim_up_0.append(image)

for i in range(15):
    filename = 'sprites/mig/mig_1_flames_up/mig_{}.png'.format(i)
    image = pygame.image.load(filename).convert_alpha()
    # image.set_colorkey(constants.WHITE)
    image = pygame.transform.scale(image, (20, 124))
    jet_exhaust_anim_up_1.append(image)

for i in range(15):
    filename = 'sprites/mig/mig_2_flames_up/mig_{}.png'.format(i)
    image = pygame.image.load(filename).convert_alpha()
    # image.set_colorkey(constants.WHITE)
    image = pygame.transform.scale(image, (34, 124))
    jet_exhaust_anim_up_2.append(image)

for i in range(15):
    filename = 'sprites/mig/mig_3_flames_up/mig_{}.png'.format(i)
    image = pygame.image.load(filename).convert_alpha()
    # image.set_colorkey(constants.WHITE)
    image = pygame.transform.scale(image, (50, 124))
    jet_exhaust_anim_up_3.append(image)

for i in range(15):
    filename = 'sprites/mig/mig_4_flames_up/mig_{}.png'.format(i)
    image = pygame.image.load(filename).convert_alpha()
    # image.set_colorkey(constants.WHITE)
    image = pygame.transform.scale(image, (34, 124))
    jet_exhaust_anim_up_4.append(image)

for i in range(15):
    filename = 'sprites/mig/mig_5_flames_up/mig_{}.png'.format(i)
    image = pygame.image.load(filename).convert_alpha()
    # image.set_colorkey(constants.WHITE)
    image = pygame.transform.scale(image, (20, 124))
    jet_exhaust_anim_up_5.append(image)

for i in range(15):
    filename = 'sprites/mig/mig_6_flames_up/mig_{}.png'.format(i)
    image = pygame.image.load(filename).convert_alpha()
    # image.set_colorkey(constants.WHITE)
    image = pygame.transform.scale(image, (22, 124))
    jet_exhaust_anim_up_6.append(image)

# Jet exhaust down

for i in range(15):
    filename = 'sprites/mig/mig_0_flames_down/mig_{}.png'.format(i)
    image = pygame.image.load(filename).convert_alpha()
    # image.set_colorkey(constants.WHITE)
    image = pygame.transform.scale(image, (22, 124))
    jet_exhaust_anim_down_0.append(image)

for i in range(15):
    filename = 'sprites/mig/mig_1_flames_down/mig_{}.png'.format(i)
    image = pygame.image.load(filename).convert_alpha()
    # image.set_colorkey(constants.WHITE)
    image = pygame.transform.scale(image, (20, 124))
    jet_exhaust_anim_down_1.append(image)

for i in range(15):
    filename = 'sprites/mig/mig_2_flames_down/mig_{}.png'.format(i)
    image = pygame.image.load(filename).convert_alpha()
    # image.set_colorkey(constants.WHITE)
    image = pygame.transform.scale(image, (34, 124))
    jet_exhaust_anim_down_2.append(image)

for i in range(15):
    filename = 'sprites/mig/mig_3_flames_down/mig_{}.png'.format(i)
    image = pygame.image.load(filename).convert_alpha()
    # image.set_colorkey(constants.WHITE)
    image = pygame.transform.scale(image, (50, 124))
    jet_exhaust_anim_down_3.append(image)

for i in range(15):
    filename = 'sprites/mig/mig_4_flames_down/mig_{}.png'.format(i)
    image = pygame.image.load(filename).convert_alpha()
    # image.set_colorkey(constants.WHITE)
    image = pygame.transform.scale(image, (34, 124))
    jet_exhaust_anim_down_4.append(image)

for i in range(15):
    filename = 'sprites/mig/mig_5_flames_down/mig_{}.png'.format(i)
    image = pygame.image.load(filename).convert_alpha()
    # image.set_colorkey(constants.WHITE)
    image = pygame.transform.scale(image, (20, 124))
    jet_exhaust_anim_down_5.append(image)

for i in range(15):
    filename = 'sprites/mig/mig_6_flames_down/mig_{}.png'.format(i)
    image = pygame.image.load(filename).convert_alpha()
    # image.set_colorkey(constants.WHITE)
    image = pygame.transform.scale(image, (22, 124))
    jet_exhaust_anim_down_6.append(image)

# Boss health bar images
for i in range(11):
    filename = 'sprites/health_bar{}.png'.format((i)*10)
    image = pygame.image.load(filename).convert_alpha()
    boss_health_images.append(image)

# Laser meter images
for i in range(164):
    if i < 10:
        i = "00" + str(i)
    if 9 < int(i) < 100:
        i = "0" + str(i)
    filename = 'sprites/meter/meter_{}.png'.format((i))
    image = pygame.image.load(filename).convert_alpha()
    image = pygame.transform.scale(image, (252, 175))
    laser_meter_images.append(image)

# Laser images
for i in range(80):
    if i < 10:
        i = "00" + str(i)
    if 9 < int(i) < 100:
        i = "0" + str(i)
    filename = 'sprites/laser/laser_{}.png'.format((i))
    image = pygame.image.load(filename).convert_alpha()
    laser_images.append(image)

for i in range(55):
    if i < 10:
        i = "0" + str(i)
    filename = 'sprites/boss_3_anim/anim_{}.png'.format(i)
    image = pygame.image.load(filename).convert_alpha()
    image = pygame.transform.scale(image, (300, 296))
    boss_3_images.append(image)

for i in range(9):
    filename = 'sprites/portals/OrangePortal{}.png'.format(i+1)
    image = pygame.image.load(filename).convert_alpha()
    image = pygame.transform.scale(image, (155, 80))
    portal_anim.append(image)
