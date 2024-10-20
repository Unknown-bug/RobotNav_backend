import heapq
import math
from utils.node import Node
from algorithms.base_search import BaseSearch

class GreedyBestFirstSearch(BaseSearch):
    def search(self):
        # Initialize the start node with the heuristic value
        start_node = Node(self.start[0], self.start[1])
        start_node.f_score = self.heuristic(self.start, self.goal)

        # Priority queue to store nodes to be explored
        priority_queue = [(start_node.f_score, start_node)]
        heapq.heapify(priority_queue)
        visited = set()
        total_nodes = 0
        traversed = []

        while priority_queue:
            # Pop the node with the lowest f_score
            _, current = heapq.heappop(priority_queue)
            total_nodes += 1
            traversed.append((current.x, current.y))

            # Check if the goal has been reached
            if (current.x, current.y) == self.goal:
                return self.reconstruct_path(current), total_nodes, traversed

            visited.add((current.x, current.y))

            # Explore neighbors
            for dx, dy in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
                next_x, next_y = current.x + dx, current.y + dy
                if (next_x, next_y) not in visited and self.grid.is_valid(next_x, next_y):
                    next_node = Node(next_x, next_y, current)
                    next_node.f_score = self.heuristic((next_x, next_y), self.goal)
                    heapq.heappush(priority_queue, (next_node.f_score, next_node))
                    visited.add((next_x, next_y))

        return [], total_nodes, traversed

    def heuristic(self, current, goal):
        # Manhattan distance heuristic
        return abs(current[0] - goal[0]) + abs(current[1] - goal[1])

class AStarSearch(BaseSearch):
    def search(self):
        # Initialize the start node with the heuristic value
        start_node = Node(self.start[0], self.start[1])
        start_node.f_score = self.heuristic(self.start, self.goal)

        # Priority queue to store nodes to be explored
        open_set = [(start_node.f_score, start_node)]
        heapq.heapify(open_set)
        closed_set = set()
        g_score = {self.start: 0}

        total_nodes = 0
        traversed = []

        while open_set:
            # Pop the node with the lowest f_score
            _, current_node = heapq.heappop(open_set)
            total_nodes += 1
            traversed.append((current_node.x, current_node.y))

            # Check if the goal has been reached
            if (current_node.x, current_node.y) == self.goal:
                return self.reconstruct_path(current_node), total_nodes, traversed

            closed_set.add((current_node.x, current_node.y))

            # Explore neighbors
            for dx, dy in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
                next_x, next_y = current_node.x + dx, current_node.y + dy
                if not self.grid.is_valid(next_x, next_y) or (next_x, next_y) in closed_set:
                    continue

                neighbor = Node(next_x, next_y, current_node)
                tentative_g_score = g_score[(current_node.x, current_node.y)] + 1

                if (next_x, next_y) not in g_score or tentative_g_score < g_score[(next_x, next_y)]:
                    g_score[(next_x, next_y)] = tentative_g_score
                    f_score = g_score[(next_x, next_y)] + self.heuristic((next_x, next_y), self.goal)
                    neighbor.f_score = f_score
                    heapq.heappush(open_set, (f_score, neighbor))

        return [], total_nodes, traversed

    def heuristic(self, current, goal):
        # Manhattan distance heuristic
        return abs(current[0] - goal[0]) + abs(current[1] - goal[1])

class CustomSearch2(BaseSearch):
    def search(self):
        def update_heuristic(node, goal, traversed_from_goal):
            # Update heuristic based on traversed nodes from the goal
            if not traversed_from_goal:
                return self.manhattan_distance(node, goal)
            return min(self.manhattan_distance(node, t) for t in traversed_from_goal)

        def expand(node, direction, visited, traversed_opposite):
            nonlocal total_nodes
            total_nodes += 1
            x, y = node.x, node.y
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                next_x, next_y = x + dx, y + dy
                if self.grid.is_valid(next_x, next_y) and (next_x, next_y) not in visited:
                    if direction == 'forward':
                        h = update_heuristic((next_x, next_y), self.goal, traversed_opposite)
                    else:
                        h = update_heuristic((next_x, next_y), self.start, traversed_opposite)
                    next_node = Node(next_x, next_y, node, node.path_cost + 1)
                    next_node.f_score = next_node.path_cost + h
                    yield next_node

        # Initialize start and goal nodes
        start_node = Node(self.start[0], self.start[1])
        goal_node = Node(self.goal[0], self.goal[1])
        forward_queue = [(0, start_node)]
        backward_queue = [(0, goal_node)]
        forward_visited = {self.start: start_node}
        backward_visited = {self.goal: goal_node}
        forward_traversed = []
        backward_traversed = []
        total_nodes = 0
        all_traversed = []

        while forward_queue and backward_queue:
            # Expand forward search
            _, current_forward = heapq.heappop(forward_queue)
            forward_traversed.append((current_forward.x, current_forward.y))
            all_traversed.append((current_forward.x, current_forward.y))

            if (current_forward.x, current_forward.y) in backward_visited:
                all_traversed.append((current_forward.x, current_forward.y))
                return self.reconstruct_bidirectional_path(current_forward, backward_visited[(current_forward.x, current_forward.y)]), total_nodes, all_traversed

            for next_node in expand(current_forward, 'forward', forward_visited, backward_traversed):
                if (next_node.x, next_node.y) not in forward_visited or next_node.path_cost < forward_visited[(next_node.x, next_node.y)].path_cost:
                    forward_visited[(next_node.x, next_node.y)] = next_node
                    heapq.heappush(forward_queue, (next_node.f_score, next_node))

            # Expand backward search
            _, current_backward = heapq.heappop(backward_queue)
            backward_traversed.append((current_backward.x, current_backward.y))
            all_traversed.append((current_backward.x, current_backward.y))

            if (current_backward.x, current_backward.y) in forward_visited:
                all_traversed.append((current_backward.x, current_backward.y))
                return self.reconstruct_bidirectional_path(forward_visited[(current_backward.x, current_backward.y)], current_backward), total_nodes, all_traversed

            for next_node in expand(current_backward, 'backward', backward_visited, forward_traversed):
                if (next_node.x, next_node.y) not in backward_visited or next_node.path_cost < backward_visited[(next_node.x, next_node.y)].path_cost:
                    backward_visited[(next_node.x, next_node.y)] = next_node
                    heapq.heappush(backward_queue, (next_node.f_score, next_node))

        return [], total_nodes, all_traversed

    def reconstruct_bidirectional_path(self, forward_node, backward_node):
        # Reconstruct the path from forward and backward nodes
        path = []
        while forward_node:
            path.append(forward_node)
            forward_node = forward_node.parent
        path = path[::-1]
        while backward_node:
            path.append(backward_node)
            backward_node = backward_node.parent
        return path

    def manhattan_distance(self, a, b):
        # Manhattan distance heuristic
        return abs(a[0] - b[0]) + abs(a[1] - b[1])