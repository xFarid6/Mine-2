from constants import Width, Height, BackgroundColor, FPS, draw_text, color_codes
from dataclasses import dataclass, field
from typing import Any
import pygame

@dataclass(slots=True)
class Game:
    pygame.mixer.pre_init(44100, 32, 2, 4096)
    pygame.init()
    flags: int = pygame.DOUBLEBUF
    screen = pygame.display.set_mode(size=(Width, Height), flags=flags, depth = 16, vsync=1)
    clock = pygame.time.Clock()
    pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])
    game_objects: dict[str, Any] = field(default_factory=dict)
    font: pygame.font.Font = pygame.font.SysFont('Arial', 15)
    pressed_keys: dict[int, bool] = field(default_factory=dict)
    highscore: int = 0

    bg_music = pygame.mixer.music.load('music test.wav')

    def __post_init__(self):
        from player import Player
        self.game_objects['player'] = Player(self)

        from shapes import Shapes
        self.game_objects['shapes'] = Shapes(self)

        pygame.mixer.music.play(-1)

    def run(self):
        while 1:
            dt: float = self.clock.tick(FPS) / 1000.0
            self.events()
            self.update(dt)
            self.draw()

    def events(self):
        keys = pygame.key.get_pressed()
        self.pressed_keys = {key: keys[key] for key in range(len(keys)) if keys[key]}
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            quit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    def update(self, dt: float):
        for game_object in self.game_objects.values():
            game_object.update(dt)

        self.check_collision(self.game_objects['player'], self.game_objects['shapes'])

    def check_collision(self, player, shapes_group):
        for shape_key, shape_value in list(shapes_group.created_shapes.items()):
            if player.player_rect.colliderect(shape_value.shape):
                player.lives -= 1
                """hit_warn = pygame.Surface((Width, Height))
                hit_warn.set_alpha(100)
                hit_warn.fill((240, 220, 220))
                pygame.draw.circle(hit_warn, (255, 0, 0), (0, 0), 50)
                self.screen.blit(hit_warn, (0, 0))
                pygame.display.flip()"""
                # print(shape_key, shape_value)
                hit_warn = pygame.Surface((Width, Height))
                hit_warn.fill((255, 0, 0))
                hit_warn.set_alpha(71)
                pygame.draw.ellipse(hit_warn, (0, 255, 0), (10, 10, Width - 20, Height - 20))
                hit_warn.set_colorkey((0, 255, 0))
                self.screen.blit(hit_warn, (0, 0))
                pygame.display.flip()
                del shapes_group.created_shapes[shape_key]
                continue

        if player.lives <= 0:
            score = len(shapes_group.created_shapes)
            if score > self.highscore:
                self.highscore = score
            self.game_over()

    def game_over(self):
        pygame.mixer.music.stop()
        while 1:
            font = pygame.font.SysFont('Arial', 40)

            draw_text('GAME OVER', font, color_codes.get('white smoke'), self.screen, Width / 2, Height / 2)
            draw_text('Press any key to restart, q to quit', font, color_codes.get('white smoke'), self.screen, Width / 2, Height / 2 + 50)
            draw_text(f"Highscore: {self.highscore}", font, color_codes.get('white smoke'), self.screen, Width / 2, Height / 2 + 100)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()
                    else:
                        self.__post_init__()
                        self.run()

    def draw(self):
        self.screen.fill(BackgroundColor)
        draw_text(f'FPS: {self.clock.get_fps():.3f}', self.font, color_codes.get('white smoke'), self.screen, 50, 50)
        draw_text(f'SHAPES: {len(self.game_objects["shapes"].created_shapes)}', self.font, color_codes.get('white smoke'), self.screen, 50, 70)

        for game_object in self.game_objects.values():
            game_object.draw()

        pygame.display.flip()

if __name__ == '__main__':
    Game().run()