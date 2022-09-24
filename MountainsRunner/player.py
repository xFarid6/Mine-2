import pygame
from constants import BackgroundColor, Width, Height, FPS, color_codes
from load_spritesheet import Spritesheet
from enum import Enum


class Anims(Enum):
    BARK = "1"
    WALK = "2"
    RUN = "3"
    TAIL = "4"
    BARK2 = "5"
    TAIL2 = "6"


class Player:
    def __init__(self) -> None:
        self.dog = Spritesheet("Dog.png")
        self.anims = self.dog.load_anims(90, 60, ["1", "2", "3", "4", "5", "6"], [3, 6, 5, 4, 3, 4])

        self.anim_frame = 0
        self.curr_anim = self.anims[Anims.RUN.value]
        self.anim_rect = self.curr_anim[0].get_rect()
        self.anim_rect.x = 100
        self.anim_rect.y = Height - self.anim_rect.height

        self.jumping = 0


    def update_image(self, deltaTime: float):
        if self.jumping == 0:
            self.anim_frame += deltaTime * 10
        else:
            self.anim_frame += deltaTime * 3 # 20
            
        if self.anim_frame >= len(self.curr_anim):
            self.anim_frame = 0

        self.curr_image = self.curr_anim[int(self.anim_frame)]

        if self.jumping:
            self.curr_image = pygame.transform.rotate(self.curr_image, -15)


    def gravity(self, deltaTime: float):
        if self.anim_rect.y < Height - self.anim_rect.height:
            self.anim_rect.y += 4

    def jump(self, deltaTime: float):
        self.anim_rect.y -= 5
        self.jumping -= 1


    def user_input(self, deltaTime: float):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if self.anim_rect.x > 100:
                self.anim_rect.x -= 5
        if keys[pygame.K_RIGHT]:
            if self.anim_rect.x < Width // 2:
                self.anim_rect.x += 5
        if keys[pygame.K_UP]:
            if self.anim_rect.y == Height - self.anim_rect.height:
                self.jumping = 20
        if keys[pygame.K_DOWN]:
            ...


    def update(self, deltaTime: float):
        self.update_image(deltaTime)
        if self.jumping == 0:
            self.gravity(deltaTime)
        else:
            self.jump(deltaTime)
        self.user_input(deltaTime)
            

    def draw(self, screen):
        img = pygame.transform.flip(self.curr_image, True, False)
        screen.blit(img, self.anim_rect)


if __name__ == "__main__":
    from mountain_runners import Game
    game = Game()
    game.run()