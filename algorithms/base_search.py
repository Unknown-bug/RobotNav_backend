from abc import ABC, abstractmethod

class BaseSearch(ABC):
    def __init__(self, grid, start, goal):
        self.grid = grid
        self.start = start
        self.goal = goal

    @abstractmethod
    def search(self):
        pass

    def reconstruct_path(self, node):
        path = []
        while node:
            path.append(node)
            node = node.parent
        return path[::-1]
