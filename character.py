import math
import pygame
from constants import *


class Character:
    def __init__(self, x, y, health, mob_animations, char_type, boss, size):
        self.char_type = char_type
        self.boss = boss
        self.score = 0
        self.flip = False
        self.animation_list = mob_animations[char_type]
        self.frameIndex = 0
        self.action = 0  # 0-idle    1-run
        self.updateTime = pygame.time.get_ticks()
        self.running = False
        self.health = health
        self.alive = True

        self.image = self.animation_list[self.action][self.frameIndex]
        self.rect = pygame.Rect(0, 0, TILE_SIZE*size, TILE_SIZE*size)
        self.rect.center = (x, y)

    def move(self, dx, dy):
        screen_scroll = [0, 0]
        self.running = False
        if dx != 0 or dy != 0:
            self.running = True
        if dx < 0:
            self.flip = True
        if dx > 0:
            self.flip = False
        # control diagonal speed
        if dx != 0 and dy != 0:
            dx = dx * (math.sqrt(2) / 2)
            dy = dy * (math.sqrt(2) / 2)

        self.rect.x += dx
        self.rect.y += dy

        # logic only applicable to player
        if self.char_type == 0:
            # update scroll based on player position
            # move camera left and right
            if self.rect.right > (SCREEN_WIDTH - SCROLL_THRESH):
                screen_scroll[0] = ((SCREEN_WIDTH - SCROLL_THRESH) -
                                    self.rect.right)
                self.rect.right = SCREEN_WIDTH - SCROLL_THRESH
            if self.rect.left < SCROLL_THRESH:
                screen_scroll[0] = SCROLL_THRESH - self.rect.left
                self.rect.left = SCROLL_THRESH

            # move camera up and down
            if self.rect.bottom > (SCREEN_HEIGHT - SCROLL_THRESH):
                screen_scroll[1] = ((SCREEN_HEIGHT - SCROLL_THRESH) -
                                    self.rect.bottom)
                self.rect.bottom = SCREEN_HEIGHT - SCROLL_THRESH
            if self.rect.top < SCROLL_THRESH:
                screen_scroll[1] = SCROLL_THRESH - self.rect.top
                self.rect.top = SCROLL_THRESH
        return screen_scroll

    def ai(self, screen_scroll):
        # reposition the mobs based on screen scroll
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

    def update(self):
        # check if character has died
        if self.health <= 0:
            self.health = 0
            self.alive = False

        # check what action the player is performing
        if self.running == True:
            self.update_action(1)  # 1-run
        else:
            self.update_action(0)  # 0-idle

        animationCooldown = 70
        # handle animation
        # update image
        self.image = self.animation_list[self.action][self.frameIndex]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.updateTime > animationCooldown:
            self.frameIndex += 1
            self.updateTime = pygame.time.get_ticks()
        # check if the animation has finished
        if self.frameIndex >= len(self.animation_list[self.action]):
            self.frameIndex = 0

    def update_action(self, new_action):
        # check if new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # update animation settings
            self.frameIndex = 0
            self.updateTime = pygame.time.get_ticks()

    def draw(self, screen):
        flipped_image = pygame.transform.flip(self.image, self.flip, False)
        if self.char_type == 0:
            screen.blit(flipped_image,
                        (self.rect.x, self.rect.y - OFFSET * SCALE))
        else:
            screen.blit(flipped_image, self.rect)
        pygame.draw.rect(screen, RED, self.rect, 1)
