import re
from utils.grid import Grid

class InputParser:
    def __init__(self, filename):
        self.filename = filename

    def parse(self):
        with open(self.filename, 'r') as file:
            lines = [line.strip() for line in file.readlines()]

        dimension_match = re.match(r'\[(\d+),\s*(\d+)\]', lines[0])
        cols, rows = map(int, (dimension_match.group(1), dimension_match.group(2)))

        start_match = re.match(r'\((\d+),\s*(\d+)\)', lines[1])
        start = (int(start_match.group(1)), int(start_match.group(2)))

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

        grid = Grid(rows, cols)
        for wall in lines[3:]:
            wall_coords = re.findall(r'\d+', wall)
            if len(wall_coords) == 4:
                grid.add_wall(*map(int, wall_coords))

        return grid, start, goals