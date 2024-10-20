import random
from utils.node import Node

class Particle:
    def __init__(self, x, y, grid):
        self.position = Node(x, y)
        self.grid = grid
        self.best_position = self.position

    def move(self):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
        random.shuffle(directions)
        for dx, dy in directions:
            new_x = self.position.x + dx
            new_y = self.position.y + dy
            if self.grid.is_valid(new_x, new_y):
                self.position = Node(new_x, new_y, self.position)
                self.best_position = self.position
                return
