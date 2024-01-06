import math
import pygame
from constants import *


class Character:
    def __init__(self, x, y, mob_animations, char_type):
        self.char_type = char_type
        self.flip = False
        self.frameIndex = 0
        self.action = 0  # 0-idle    1-run
        self.updateTime = pygame.time.get_ticks()
        self.running = False
        self.animation_list = mob_animations[char_type]
        self.image = self.animation_list[self.action][self.frameIndex]
        self.rect = pygame.Rect(0, 0, 40, 40)
        self.rect.center = (x, y)

    def move(self, dx, dy):
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

    def update(self):
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
            screen.blit(flipped_image, (self.rect.x, self.rect.y - OFFSET*SCALE))
        else:
            screen.blit(flipped_image, self.rect)
        pygame.draw.rect(screen, RED, self.rect, 1)
