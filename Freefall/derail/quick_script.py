class Node:
    def __init__(self, position, parent):
        self.position = position
        self.parent = parent


class Tree:
    def __init__(self) -> None:
        self.root: Node = Node((0, 0), None)
        self.nodes = []

    def add_node(self, node):
        self.nodes.append(node)

    def shortest_path(self, start:Node, end:Node) -> list[tuple[int, int]]:
        path = []
        current = end
        while current != start:
            path.append(current.position)
            current = current.parent
        path.append(start.position)
        path.reverse()
        return path


def knight_path(start, end):
    # happy coding! :)
    right_up = (1, 2)
    right_down = (1, -2)
    left_up = (-1, 2)
    left_down = (-1, -2)
    
    if start == end: return list(start)

    tree = Tree()
    tree.root = Node(start, None)
    tree.add_node(tree.root)

    while not Node(end, Node) in tree.nodes:
        for node in tree.nodes:
            if node.position == end:
                return node
            tree.add_node(Node((node.position[0] + right_up[0], node.position[1] + right_up[1]), node))
            tree.add_node(Node((node.position[0] + right_down[0], node.position[1] + right_down[1]), node))
            tree.add_node(Node((node.position[0] + left_up[0], node.position[1] + left_up[1]), node))
            tree.add_node(Node((node.position[0] + left_down[0], node.position[1] + left_down[1]), node))

    return tree.shortest_path(tree.root, Node(end, None))


if __name__ == '__main__':
    print(knight_path((0, 0), (1, 2)))  # [(0, 0), (1, 2)]
    print(knight_path((0, 0), (3, 3)))  # [(0, 0), (1, 2), (3, 3)]
    print(knight_path((3, 3), (0, 0)))  # [(3, 3), (1, 2), (0, 0)]
    print(knight_path((0, 0), (2, 1)))  # [(0, 0), (1, 2), (2, 4), (4, 3), (2, 1)]
    print(knight_path((0, 0), (7, 7)))  # [(0, 0), (1, 2), (3, 3), (5, 4), (7, 5), (5, 6), (7, 7)]
    print(knight_path((0, 0), (6, 6)))  # [(0, 0), (1, 2), (3, 3), (5, 4), (7, 5), (6, 7), (8, 6), (6, 6)]
    print(knight_path((0, 0), (7, 6)))  # [(0, 0), (1, 2), (3, 3), (5, 4), (7, 5), (6, 7), (8, 6), (7, 8), (9, 7), (7, 6)]
    print(knight_path((0, 0), (6, 7)))  # [(0, 0), (1, 2), (3, 3), (5, 4), (7, 5), (6, 7)]
    print(knight_path((0, 0), (7, 8)))  # [(0, 0), (1, 2), (3, 3), (5, 4), (7, 5), (6, 7), (8, 6), (7, 8)]
    print(knight_path((0, 0), (8, 6)))  # [(0, 0), (1, 2), (3, 3), (5, 4), (7, 5), (6, 7), (8, 6)]