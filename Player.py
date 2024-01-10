import math

import pygame as pg
from constants import *
from Useful import *


class Player:
    def __init__(self, x, y):
        self.flip = False
        self.rect = pg.Rect(0, 0, 40, 40)
        self.rect.center = (x, y)
        self.frameIndex = 0
        self.running = False
        self.action = 0  # 0-idle, 1-run
        self.updateTime = pg.time.get_ticks()
        self.animationList = load_animation_list("elf")
        self.image = self.animationList[self.action][self.frameIndex]

        self.speed = 5

        self._movingUp = False
        self._movingDown = False
        self._movingLeft = False
        self._movingRight = False

    def _animation(self):
        if self.running:
            self._update_action(1)
        else:
            self._update_action(0)
        animation_cooldown = 150
        self.image = self.animationList[self.action][self.frameIndex]
        if pg.time.get_ticks() - self.updateTime > animation_cooldown:
            self.frameIndex += 1
            self.updateTime = pg.time.get_ticks()
        if self.frameIndex >= len(self.animationList[self.action]):
            self.frameIndex = 0

    def _update_action(self, newAction):
        if newAction != self.action:
            self.action = newAction
            self.frameIndex = 0
            self.updateTime = pg.time.get_ticks()

    def _move(self):
        """Odpowiada za poruszanie się gracza."""
        dx, dy = 0, 0
        self.running = False
        if self._movingUp:
            dy = -self.speed
        if self._movingDown:
            dy = self.speed
        if self._movingLeft:
            dx = -self.speed
        if self._movingRight:
            dx = self.speed

        if dx != 0 or dy != 0:
            self.running = True

        # sprawdź, w którą stronę skierowany jest gracz
        if dx < 0:
            self.flip = True
        if dx > 0:
            self.flip = False
        # ruch po przekątnej
        if dx != 0 and dy != 0:
            dx = dx * (math.sqrt(2) / 2)
            dy = dy * (math.sqrt(2) / 2)
        # przesuń gracza
        self.rect.x += dx
        self.rect.y += dy

    def update(self):
        self._move()
        self._animation()

    def draw(self, screen):
        flippedImage = pg.transform.flip(self.image, self.flip, False)
        screen.blit(flippedImage, self.rect)
        pg.draw.rect(screen, RED, self.rect, 1)

    def input(self, event):
        """Funkcja sprawdza input z klawiatury i myszy dla gracza."""
        if event.type == pg.KEYDOWN:  # Wciśnięcie klawiszy
            if event.key == pg.K_w:
                self._movingUp = True
            if event.key == pg.K_s:
                self._movingDown = True
            if event.key == pg.K_a:
                self._movingLeft = True
            if event.key == pg.K_d:
                self._movingRight = True
        if event.type == pg.KEYUP:  # Zwolnienie klawiszy
            if event.key == pg.K_w:
                self._movingUp = False
            if event.key == pg.K_s:
                self._movingDown = False
            if event.key == pg.K_a:
                self._movingLeft = False
            if event.key == pg.K_d:
                self._movingRight = False
