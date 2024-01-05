import math
import pygame
from constants import *


class Character:
    def __init__(self, x, y, animationList):
        self.flip = False
        self.frameIndex = 0
        self.updateTime = pygame.time.get_ticks()
        self.animationList = animationList
        self.image = animationList[self.frameIndex]
        self.rect = pygame.Rect(0, 0, 40, 40)
        self.rect.center = (x, y)

    def move(self, dx, dy):
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
        animationCooldown = 70
        # handle animation
        # update image
        self.image = self.animationList[self.frameIndex]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.updateTime > animationCooldown:
            self.frameIndex += 1
            self.updateTime = pygame.time.get_ticks()
        # check if the animation has finished
        if self.frameIndex >= len(self.animationList):
            self.frameIndex = 0

    def draw(self, screen):
        flipped_image = pygame.transform.flip(self.image, self.flip, False)
        screen.blit(flipped_image, self.rect)
        pygame.draw.rect(screen, RED, self.rect, 1)
