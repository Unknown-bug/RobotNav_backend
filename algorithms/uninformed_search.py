from collections import deque
from utils.node import Node
from utils.particle import Particle
from algorithms.base_search import BaseSearch
import heapq

# Depth First Search Implementation
class DepthFirstSearch(BaseSearch):
    def search(self):
        stack = [(Node(self.start[0], self.start[1]), [])]
        visited = set()
        total_nodes = 0
        traversed = []

        while stack:
            current, path = stack.pop()
            total_nodes += 1
            traversed.append((current.x, current.y))
            if (current.x, current.y) == self.goal:
                return path + [current], total_nodes, traversed
            visited.add((current.x, current.y))
            unvisited_neighbors = []
            for dx, dy in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
                next_x, next_y = current.x + dx, current.y + dy
                if self.grid.is_valid(next_x, next_y) and (next_x, next_y) not in visited:
                    child_node = Node(next_x, next_y, current, current.path_cost + 1)
                    unvisited_neighbors.append((child_node, path + [current]))
            stack.extend(unvisited_neighbors[::-1])
        return [], total_nodes, traversed

# Breadth First Search Implementation
class BreadthFirstSearch(BaseSearch):
    def search(self):
        queue = deque([[Node(self.start[0], self.start[1])]])
        visited = set()
        total_nodes = 0
        traversed = []

        while queue:
            path = queue.popleft()
            total_nodes += 1
            current = path[-1]
            traversed.append((current.x, current.y))
            visited.add((current.x, current.y))
            if (current.x, current.y) == self.goal:
                return path, total_nodes, traversed
            for dx, dy in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
                next_x, next_y = current.x + dx, current.y + dy
                if (next_x, next_y) not in visited and self.grid.is_valid(next_x, next_y):
                    child_node = Node(next_x, next_y)
                    queue.append(path + [child_node])
                    visited.add((next_x, next_y))
                    traversed.append((next_x, next_y))
        return [], total_nodes, traversed

# Custom Bidirectional Search Implementation
class CustomSearch1(BaseSearch):
    def search(self):
        if self.start == self.goal:
            return [Node(self.start[0], self.start[1])], 0, [(self.start[0], self.start[1])]

        # Initialize forward and backward search
        forward_queue = deque([Node(self.start[0], self.start[1])])
        backward_queue = deque([Node(self.goal[0], self.goal[1])])

        forward_visited = {(self.start[0], self.start[1]): None}
        backward_visited = {(self.goal[0], self.goal[1]): None}

        total_nodes = 0
        traversed = []

        meeting_node = None

        while forward_queue and backward_queue:
            # Expand forward search
            current_forward = forward_queue.popleft()
            total_nodes += 1
            traversed.append((current_forward.x, current_forward.y))

            for dx, dy in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
                next_x, next_y = current_forward.x + dx, current_forward.y + dy
                if self.grid.is_valid(next_x, next_y) and (next_x, next_y) not in forward_visited:
                    forward_visited[(next_x, next_y)] = current_forward
                    forward_queue.append(Node(next_x, next_y, current_forward))
                    if (next_x, next_y) in backward_visited:
                        meeting_node = (next_x, next_y)
                        break
            if meeting_node:
                traversed.append(meeting_node)
                break

            # Expand backward search
            current_backward = backward_queue.popleft()
            total_nodes += 1
            traversed.append((current_backward.x, current_backward.y))

            for dx, dy in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
                next_x, next_y = current_backward.x + dx, current_backward.y + dy
                if self.grid.is_valid(next_x, next_y) and (next_x, next_y) not in backward_visited:
                    backward_visited[(next_x, next_y)] = current_backward
                    backward_queue.append(Node(next_x, next_y, current_backward))
                    if (next_x, next_y) in forward_visited:
                        meeting_node = (next_x, next_y)
                        break
            if meeting_node:
                traversed.append(meeting_node)
                break

        if meeting_node:
            # Reconstruct path from start to meeting_node
            path_forward = []
            node = forward_visited[meeting_node]
            while node:
                path_forward.append(node)
                node = node.parent
            
            path_forward = path_forward[::-1]
            path_forward.append(Node(meeting_node[0], meeting_node[1]))
            traversed.append(meeting_node)

            # Reconstruct path from meeting_node to goal
            path_backward = []
            path_backward.append(Node(meeting_node[0], meeting_node[1]))
            node = backward_visited[meeting_node]
            while node:
                path_backward.append(node)
                node = node.parent

            full_path = path_forward + path_backward
            return full_path, total_nodes, traversed
        else:
            return [], total_nodes, traversed

# Custom Particle Swarm Optimization Search Implementation
class CustomSearch3(BaseSearch):
    def __init__(self, grid, start, goal, num_particles=20, max_iterations=1000):
        super().__init__(grid, start, goal)
        self.num_particles = num_particles
        self.max_iterations = max_iterations

    def search(self):
        # Initialize particles
        particles = [Particle(self.start[0], self.start[1], self.grid) for _ in range(self.num_particles)]
        total_nodes = 0
        traversed = set()
        global_best = None

        for _ in range(self.max_iterations):
            for particle in particles:
                total_nodes += 1
                traversed.add((particle.position.x, particle.position.y))

                if (particle.position.x, particle.position.y) == self.goal:
                    return self.reconstruct_path(particle.position), total_nodes, list(traversed)

                particle.move()

                # Update global best position (closest to goal)
                if global_best is None or self.manhattan_distance(particle.position, self.goal) < self.manhattan_distance(global_best, self.goal):
                    global_best = particle.position

        # If no path found, return the best approximate path
        return self.reconstruct_path(global_best) if global_best else [], total_nodes, list(traversed)

    def manhattan_distance(self, node, goal):
        return abs(node.x - goal[0]) + abs(node.y - goal[1])