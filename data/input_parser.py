import re
from utils.grid import Grid

class InputParser:
    def __init__(self, filename):
        self.filename = filename

    def parse(self):
        with open(self.filename, 'r') as file:
            lines = [line.strip() for line in file.readlines()]

        # Parse grid dimensions
        dimension_match = re.match(r'\[(\d+),\s*(\d+)\]', lines[0])
        cols, rows = map(int, (dimension_match.group(1), dimension_match.group(2)))

        # Parse starting position
        start_match = re.match(r'\((\d+),\s*(\d+)\)', lines[1])
        start = (int(start_match.group(1)), int(start_match.group(2)))

        # Parse goals
        goal_coords = re.findall(r'\((\d+),\s*(\d+)\)', lines[2])
        goals = []
        for x_str, y_str in goal_coords:
            try:
                x, y = map(int, (x_str, y_str))
                goals.append((x, y))
            except ValueError:
                print(f"Invalid coordinate format: ({x_str}, {y_str}).")

        if not goals:
            print("No valid goal node found.")
            return None, None, None

        # Create grid and parse walls
        grid = Grid(rows, cols)
        walls = []
        for wall in lines[3:]:
            wall_coords = re.findall(r'\d+', wall)
            if len(wall_coords) == 4:
                wall_x1, wall_y1, wall_x2, wall_y2 = map(int, wall_coords)
                grid.add_wall(wall_x1, wall_y1, wall_x2, wall_y2)
                # Store wall positions for checking overlaps
                walls.append(((wall_x1, wall_y1), (wall_x2, wall_y2)))

        # Remove goals that overlap with walls
        goals = [goal for goal in goals if not self._goal_overlaps_wall(goal, walls)]

        return grid, start, goals

    def _goal_overlaps_wall(self, goal, walls):
        """Helper function to check if a goal overlaps any wall."""
        goal_x, goal_y = goal
        for (wall_x1, wall_y1), (wall_x2, wall_y2) in walls:
            if (goal_x == wall_x1 and goal_y == wall_y1) or (goal_x == wall_x2 and goal_y == wall_y2):
                # print(f"Goal at ({goal_x}, {goal_y}) overlaps with a wall. Removing goal.")
                return True
        return False
