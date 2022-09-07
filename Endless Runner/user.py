from abc import ABC
from platform import platform
from queue import Queue
from collections import deque
from enum import Enum, auto
from dataclasses import dataclass

@dataclass
class Settings(ABC):
    night_color: tuple[int, int, int] = (27, 3, 52)
    day_color: tuple[int, int, int] = (223, 242, 216)
    accent_color: tuple[int, int, int] = (165, 36, 61)
    platform_color: tuple[int, int, int] = (182, 143, 64)

class UserSettings:
    ...

@dataclass
class Achievements:
    ...