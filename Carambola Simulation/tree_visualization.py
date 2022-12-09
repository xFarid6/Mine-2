import pygame
from binarytree import BinaryTree

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.pre_init(44100, -16, 2, 512)
        self.width = 1700
        self.height = 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Freefall")
        self.clock = pygame.time.Clock()

        self.tree = BinaryTree()
        num_of_values = 500
        lower_bound = 0
        upper_bound = 1000
        self.tree.fill_tree(num_of_values, True, lower_bound, upper_bound)

        self.tree.in_order_traversal(sep=" ")
        print()
        self.tree.pre_order_traversal(sep=" ")
        print()
        self.tree.post_order_traversal(sep=" ")

    def run(self):
        while 1:
            self.clock.tick(60)
            deltaTime: float = self.clock.get_time() / 1000
            self.events()
            self.update(deltaTime)
            self.draw()

    def update(self, deltaTime: float):
        pass

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    def draw(self):
        self.screen.fill((30, 30, 30))

        self.draw_text("FPS: " + str(int(self.clock.get_fps())), 18, (255, 255, 255), 10, 10)

        self.tree.draw_tree(self.screen, self.width, self.height)

        pygame.display.flip()

    def draw_text(self, text, size, color, x, y, align="nw"):
        font = pygame.font.SysFont("comicsans", size, bold=True)
        label = font.render(text, True, color)

        if align == "nw":
            self.screen.blit(label, (x, y))
        if align == "ne":
            self.screen.blit(label, (x - label.get_width(), y))
        if align == "sw":
            self.screen.blit(label, (x, y - label.get_height()))
        if align == "se":
            self.screen.blit(label, (x - label.get_width(), y - label.get_height()))
        if align == "n":
            self.screen.blit(label, (x - label.get_width() / 2, y))
        if align == "s":
            self.screen.blit(label, (x - label.get_width() / 2, y - label.get_height()))
        if align == "e":
            self.screen.blit(label, (x - label.get_width(), y - label.get_height() / 2))
        if align == "w":
            self.screen.blit(label, (x, y - label.get_height() / 2))
        if align == "center":
            self.screen.blit(label, (x - label.get_width() / 2, y - label.get_height() / 2))

if __name__ == "__main__":
    Game().run()