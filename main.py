import pygame
import csv
from character import Character
from items import Item
from weapon import Weapon
from world import World
from constants import *

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dungeon Crawler")

# clock for maintaining frame rate
clock = pygame.time.Clock()

# define game variables
level = 1
screen_scroll = [0, 0]

# define player movement variables
moving_left = False
moving_right = False
moving_up = False
moving_down = False

# define font
font = pygame.font.Font("assets/fonts/AtariClassic.ttf", 20)


# helped function to scale image
def scale_image(image: pygame.surface.Surface, scale):
    width = image.get_width()
    height = image.get_height()
    return pygame.transform.scale(image, (width * scale, height * scale))


# load hart images
heart_empty = scale_image(
    pygame.image.load("assets/images/items/heart_empty.png").convert_alpha(),
    ITEM_SCALE)
heart_half = scale_image(
    pygame.image.load("assets/images/items/heart_half.png").convert_alpha(),
    ITEM_SCALE)
heart_full = scale_image(
    pygame.image.load("assets/images/items/heart_full.png").convert_alpha(),
    ITEM_SCALE)

# load coin images
coin_images = []
for x in range(4):
    image = scale_image(
        pygame.image.load(f"assets/images/items/coin_f{x}.png").convert_alpha(),
        ITEM_SCALE)
    coin_images.append(image)

# load potion image
red_potion = scale_image(
    pygame.image.load("assets/images/items/potion_red.png").convert_alpha(),
    POTION_SCALE)

item_images = []
item_images.append(coin_images)
item_images.append(red_potion)

# load weapon images
bow_image = pygame.image.load("assets/images/weapons/bow.png").convert_alpha()
bow_image = scale_image(bow_image, WEAPON_SCALE)
arrow_image = pygame.image.load(
    "assets/images/weapons/arrow.png").convert_alpha()
arrow_image = scale_image(arrow_image, WEAPON_SCALE)

# load tile map images
tile_list = []
for x in range(TILE_TYPES):
    tile_image = pygame.image.load(f"assets/images/tiles/"
                                   f"{x}.png").convert_alpha()
    tile_image = pygame.transform.scale(tile_image, (TILE_SIZE, TILE_SIZE))
    tile_list.append(tile_image)

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


# function for displaying game info
def draw_info():
    pygame.draw.rect(screen, PANEL, (0, 0, SCREEN_WIDTH, 50))
    pygame.draw.line(screen, WHITE, (0, 50), (SCREEN_WIDTH, 50))
    # draw lives
    half_hearth_drawn = False
    for i in range(5):
        if player.health >= ((i + 1) * 20):
            screen.blit(heart_full, (10 + i * 50, 0))
        elif (player.health % 20 > 0) and half_hearth_drawn == False:
            screen.blit(heart_half, (10 + i * 50, 0))
            half_hearth_drawn = True
        else:
            screen.blit(heart_empty, (10 + i * 50, 0))
    # level
    draw_text("LEVEL: " + str(level), font, WHITE, SCREEN_WIDTH / 2, 15)
    # show score
    draw_text(f"X{player.score}", font, WHITE, SCREEN_WIDTH - 100, 15)


# create empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)
# load level data and create wotld
with open(f"levels/level{level}_data.csv", newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)

world = World()
world.process_data(world_data, tile_list, item_images, mob_animations)


# function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# damage text class
class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, color):
        super().__init__()
        self.image = font.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        # reposition based on screen scroll
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

        # move damage text up
        self.rect.y -= 1
        # delete the counter after a few seconds
        self.counter += 1
        if self.counter > 30:
            self.kill()


# create player
player = world.player
# create player's weapon
bow = Weapon(bow_image, arrow_image)

# exttract enemies from world data
enemy_list = world.character_list

# create sprite groups
damage_text_group = pygame.sprite.Group()
arrow_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()

score_coin = Item(SCREEN_WIDTH - 115, 23, 0, coin_images, True)
item_group.add(score_coin)
# add the items from the level data
for item in world.item_list:
    item_group.add(item)

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
    screen_scroll = player.move(dx, dy, world.obstacle_tiles)

    # update all objects
    world.update(screen_scroll)
    for enemy in enemy_list:
        enemy.ai(screen_scroll)
        enemy.update()
    player.update()
    arrow = bow.update(player)
    if arrow:
        arrow_group.add(arrow)
    for arrow in arrow_group:
        damage, damage_pos = arrow.update(screen_scroll, enemy_list)
        if damage:
            damage_text = DamageText(damage_pos.centerx, damage_pos.y,
                                     str(damage), RED)
            damage_text_group.add(damage_text)
    damage_text_group.update()
    item_group.update(screen_scroll, player)

    # draw player on screen
    world.draw(screen)
    for enemy in enemy_list:
        enemy.draw(screen)
    player.draw(screen)
    bow.draw(screen)
    for arrow in arrow_group:
        arrow.draw(screen)
    damage_text_group.draw(screen)
    item_group.draw(screen)
    draw_info()
    score_coin.draw(screen)
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
