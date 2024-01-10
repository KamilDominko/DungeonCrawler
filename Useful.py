import pygame as pg
from constants import *


def scale_image(image, scale):
    """Skaluje podany w argumentach obraz przez podaną w argumentach skalę."""
    width = image.get_width()
    height = image.get_height()
    return pg.transform.scale(image, (width * scale, height * scale))


def load_animation_list(charType):
    animation_types = ["idle", "run"]
    animationList = []
    for animation in animation_types:
        tempList = []
        for i in range(4):
            image = pg.image.load(
                f"assets/images/characters/{charType}/{animation}/{i}.png")
            image.convert_alpha()
            image = scale_image(image, SCALE)
            tempList.append(image)
        animationList.append(tempList)
    return animationList
