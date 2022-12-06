import pygame
from constants import Width, Height

class Chicken:
    def __init__(self):
        """Load the spritesheet"""
        path1 = r"C:\Cose Nuove\Code\Mine 2\Freefall\Chicken_Sprite_Sheet.png"
        path2 = r"C:\Cose Nuove\Code\Mine 2\Freefall\Chicken_Sprite_Sheet_Light_Brown.png"
        path3 = r"C:\Cose Nuove\Code\Mine 2\Freefall\Chicken_Sprite_Sheet_Dark_Brown.png"
        path4 = r"C:\Cose Nuove\Code\Mine 2\Freefall\Chicken_Sprite_Sheet_Black.png"

        sheet1 = pygame.image.load(path1).convert_alpha()
        sheet2 = pygame.image.load(path2).convert_alpha()
        sheet3 = pygame.image.load(path3).convert_alpha()
        sheet4 = pygame.image.load(path4).convert_alpha()

        self.chicken1: list[pygame.surface.Surface] = []
        self.chicken2: list[pygame.surface.Surface] = []
        self.chicken3: list[pygame.surface.Surface] = []
        self.chicken4: list[pygame.surface.Surface] = []

        self.sprite_index: float = 0
        self.facing_right: bool = True
        self.position: list[int] = [0, 0]
        self.speed_h: float = 3
        self.speed_v: float = 0.5
        self.left: bool = False
        self.right: bool = False
        self.vel_y: float = 0
        size = 32

        # slice sheet1 and put it in chicken1
        for y in range(0, 4):
            for x in range(0, 4):
                rect = pygame.Rect(x * size, y * size, size, size)
                self.chicken1.append(sheet1.subsurface(rect))

        # slice sheet2 and put it in chicken2
        for y in range(0, 4):
            for x in range(0, 4):
                rect = pygame.Rect(x * size, y * size, size, size)
                self.chicken2.append(sheet2.subsurface(rect))

        # slice sheet3 and put it in chicken3
        for y in range(0, 4):
            for x in range(0, 4):
                rect = pygame.Rect(x * size, y * size, size, size)
                self.chicken3.append(sheet3.subsurface(rect))

        # slice sheet4 and put it in chicken4
        for y in range(0, 4):
            for x in range(0, 4):
                rect = pygame.Rect(x * size, y * size, size, size)
                self.chicken4.append(sheet4.subsurface(rect))

    def update(self, deltaTime: float):
        anim_speed = 5

        self.sprite_index += anim_speed * deltaTime
        self.sprite_index %= 4
        if self.sprite_index >= len(self.chicken1):
            self.sprite_index = 0
        
        
        self.vel_y += self.speed_v
        self.position[1] += self.vel_y # type: ignore WTF is this ERROR?

        if self.position[1] > Height // 2 - 32:
            self.position[1] = Height // 2 - 32
            self.vel_y = 0

        if self.right:
            self.position[0] += self.speed_h
            self.facing_right = False

        if self.left:
            self.position[0] -= self.speed_h
            self.facing_right = True

    def draw(self, screen):
        frame = self.chicken1[int(self.sprite_index)]
        frame = pygame.transform.scale(frame, (64, 64))
        if self.facing_right:
            screen.blit(frame, self.position)
        else:
            screen.blit(pygame.transform.flip(frame, True, False), self.position)

    def move_left(self, yes: bool):
        if yes and self.position[0] > 0:
            self.left = True
        else:
            self.left = False

    def move_right(self, yes: bool):
        if yes and self.position[0] < Width - 64:
            self.right = True
        else:
            self.right = False

    def jump(self):
        self.vel_y = -10
