class Node:
    def __init__(self, x, y, parent=None, path_cost=0):
        self.x = x
        self.y = y
        self.parent = parent
        self.path_cost = path_cost
        self.depth = 0

    def __lt__(self, other):
        if isinstance(other, Node): 
            return self.x + self.y < other.x + other.y
        return False
    

    def __eq__(self, other):
        if isinstance(other, Node): 
            return self.x == other.x and self.y == other.y
        return False