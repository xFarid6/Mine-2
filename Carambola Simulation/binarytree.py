import random
import pygame

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        if self.root is None:
            self.root = Node(value)
        else:
            self._insert(value, self.root)

    def _insert(self, value, node):
        if value < node.value:
            if node.left is None:
                node.left = Node(value)
            else:
                self._insert(value, node.left)
        else:
            if node.right is None:
                node.right = Node(value)
            else:
                self._insert(value, node.right)

    def print_tree(self):
        if self.root is not None:
            self._print_tree(self.root)

    def _print_tree(self, node):
        if node is not None:
            self._print_tree(node.left)
            print(node.value)
            self._print_tree(node.right)

    def height(self):
        if self.root is not None:
            return self._height(self.root, 0)
        else:
            return 0

    def _height(self, node, current_height):
        if node is None:
            return current_height
        left_height = self._height(node.left, current_height + 1)
        right_height = self._height(node.right, current_height + 1)
        return max(left_height, right_height)

    def fill_tree(self, elements, random_fill=False):
        if random_fill:
            for i in range(elements):
                self.insert(random.randint(0, 100))
        else:
            for i in range(elements):
                self.insert(i)

    def search(self, value):
        if self.root is not None:
            return self._search(value, self.root)
        else:
            return False

    def _search(self, value, node):
        if value == node.value:
            return True
        elif value < node.value and node.left is not None:
            return self._search(value, node.left)
        elif value > node.value and node.right is not None:
            return self._search(value, node.right)

    def draw_tree(self, surface: pygame.surface.Surface, width: int, height: int) -> None:
        if self.root is not None:
            self._draw_tree(surface, width, height, self.root, 0, width, 20)

    def _draw_tree(self, surface, width: int, height: int, node: Node, x1: int, x2: int, y: int) -> None:
        if node is not None:
            x = (x1 + x2) // 2
            y2 = y + 50
            # pygame.draw.line(surface, (255, 255, 255), (x, y), (x, y2 + 100), 1)
            pygame.draw.circle(surface, (255, 255, 255), (x, y), 15)
            self._draw_text(surface, str(node.value), x, y)
            if node.left is not None:
                self._draw_tree(surface, width, height, node.left, x1, x, y2)
                # draw the line between the parent and the child
                pygame.draw.line(surface, (255, 255, 255), (x, y), ((x1 + x) // 2, y2), 1)
            if node.right is not None:
                self._draw_tree(surface, width, height, node.right, x, x2, y2)
                # draw the line between the parent and the child
                pygame.draw.line(surface, (255, 255, 255), (x, y), ((x + x2) // 2, y2), 1)

    def _draw_text(self, surface, text, x, y) -> None:
        font = pygame.font.SysFont('arial', 15)
        text_object = font.render(text, True, (0, 0, 0))
        text_rect = text_object.get_rect()
        text_rect.center = (x, y)
        surface.blit(text_object, text_rect)

    def in_order_traversal(self, sep=' '):
        if self.root is not None:
            self._in_order_traversal(self.root, sep)

    def _in_order_traversal(self, node, sep):
        if node is not None:
            self._in_order_traversal(node.left, sep)
            print(node.value, end=sep)
            self._in_order_traversal(node.right, sep)

    def pre_order_traversal(self, sep=' '):
        if self.root is not None:
            self._pre_order_traversal(self.root, sep)

    def _pre_order_traversal(self, node, sep):
        if node is not None:
            print(node.value, end=sep)
            self._pre_order_traversal(node.left, sep)
            self._pre_order_traversal(node.right, sep)

    def post_order_traversal(self, sep=' '):
        if self.root is not None:
            self._post_order_traversal(self.root, sep)

    def _post_order_traversal(self, node, sep):
        if node is not None:
            self._post_order_traversal(node.left, sep)
            self._post_order_traversal(node.right, sep)
            print(node.value, end=sep)

if __name__ == '__main__':
    tree = BinaryTree()
    tree.fill_tree(100, random_fill=True)
    tree.print_tree()
    print("Height: ", tree.height())
    print("Search for 10: ", tree.search(10))
    print("Search for 15: ", tree.search(15))

    