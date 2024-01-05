import pygame
from constants import *
from character import Character

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
def scale_image(image, scale):
    width = image.get_width()
    height = image.get_height()
    return pygame.transform.scale(image, (width * scale, height * scale))

animation_list = []
for i in range(4):
    image = pygame.image.load(f"assets/images/characters/elf/idle/{i}.png")
    image.convert_alpha()
    image = scale_image(image, SCALE)
    animation_list.append(image)

# create player
player = Character(100, 100, animation_list)

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

    # draw player on screen
    player.draw(screen)

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
