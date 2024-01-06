import pygame

from character import Character
from weapon import Weapon
from constants import *

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dungeon Crawler")

# clock for maintaining frame rate
clock = pygame.time.Clock()

# define player movement variables
moving_left = False
moving_right = False
moving_up = False
moving_down = False


# helped function to scale image
def scale_image(image: pygame.surface.Surface, scale):
    width = image.get_width()
    height = image.get_height()
    return pygame.transform.scale(image, (width * scale, height * scale))


# load weapon images
bow_image = pygame.image.load("assets/images/weapons/bow.png").convert_alpha()
bow_image = scale_image(bow_image, WEAPON_SCALE)
arrow_image = pygame.image.load(
    "assets/images/weapons/arrow.png").convert_alpha()
arrow_image = scale_image(arrow_image, WEAPON_SCALE)

# load character images
mob_animations = []
mob_types = ["elf", "imp", "skeleton", "goblin", "muddy", "tiny_zombie",
             "big_demon"]

animation_types = ["idle", "run"]
for mob in mob_types:
    # load images
    animation_list = []
    for animation in animation_types:
        # reset temporary list of images
        temp_list = []
        for i in range(4):
            path = f"assets/images/characters/{mob}/{animation}/{i}.png"
            image = pygame.image.load(path)
            image.convert_alpha()
            image = scale_image(image, SCALE)
            temp_list.append(image)
        animation_list.append(temp_list)
    mob_animations.append(animation_list)

# create player
player = Character(100, 100, mob_animations, 0)

# create player's weapon
bow = Weapon(bow_image, arrow_image)

# create sprite groups
arrow_group = pygame.sprite.Group()

# main game loop
run = True
while run:

    # control frame rate
    clock.tick(FPS)

    screen.fill(BG)

    # calculate player movement
    dx = 0
    dy = 0
    if moving_right == True:
        dx = SPEED
    if moving_left == True:
        dx = -SPEED
    if moving_up == True:
        dy = -SPEED
    if moving_down == True:
        dy = SPEED

    # move player
    player.move(dx, dy)

    # update player
    player.update()
    arrow = bow.update(player)
    if arrow:
        arrow_group.add(arrow)
    for arrow in arrow_group:
        arrow.update()

    # draw player on screen
    player.draw(screen)
    bow.draw(screen)
    for arrow in arrow_group:
        arrow.draw(screen)

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # take keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w:
                moving_up = True
            if event.key == pygame.K_s:
                moving_down = True
        # keyboard button released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_w:
                moving_up = False
            if event.key == pygame.K_s:
                moving_down = False

    pygame.display.update()
