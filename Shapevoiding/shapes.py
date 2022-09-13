from constants import Width, Height, BackgroundColor, FPS, draw_text, color_codes
from dataclasses import dataclass, field
from os import listdir
from main import Game
import numpy as np 
import pygame


@dataclass(slots=True)
class Shapes:
    game: Game

    def update(self):
        pass

    def draw(self):
        pass