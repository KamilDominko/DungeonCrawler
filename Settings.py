from constants import *


class Settings:
    """Przechowuje ustawienia programu."""

    def __init__(self):
        self.screenWidth = SCREEN_WIDTH
        self.screenHeight = SCREEN_HEIGHT
        self.fps = FPS

    def get_res(self):
        """Zwraca szerokość i wysokość okna."""
        return self.screenWidth, self.screenHeight
