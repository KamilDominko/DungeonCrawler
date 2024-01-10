import pygame as pg
from Settings import Settings
from Player import Player
from constants import *


class Program:
    def __init__(self):
        self.settings = Settings()
        self.run = True
        self.screen = pg.display.set_mode(self.settings.get_res())
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()

        self.player = Player(40, 40)

    def _update_screen(self):
        self.screen.fill(BG)
        self.player.draw(self.screen)
        pg.display.update()

    def _update_entities(self):
        self.player.update()

    def _check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.run = False
            self.player.input(event)

    def start(self):
        while self.run:
            self._check_events()
            self._update_entities()
            self._update_screen()
            self.clock.tick(self.settings.fps)


game = Program()
game.start()
