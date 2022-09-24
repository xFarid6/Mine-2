import pygame
from load_spritesheet import Spritesheet
from enum import Enum


class Anims(Enum):
    BARK = "1"
    WALK = "2"
    RUN = "3"
    TAIL = "4"
    BARK2 = "5"
    TAIL2 = "6"


class OldyKnight:
    def __init__(self) -> None:
        self.knight = Spritesheet("Ye_Oldy_Knight_Guy.png")
        self.anims = self.knight.load_anims(90, 60, ["1", "2", "3", "4", "5", "6"], [3, 6, 5, 4, 3, 4])

        self.anim_frame = 0
        self.curr_anim = self.anims[Anims.RUN.value]
        self.anim_rect = self.curr_anim[0].get_rect()