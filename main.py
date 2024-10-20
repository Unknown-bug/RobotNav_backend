import sys
from data.input_parser import InputParser
from algorithms import get_search_algorithm
from gui import GUI
from utils import get_direction, append_unique
from utils.grid import Grid

def main():
    filename = sys.argv[1]
    method = sys.argv[2]

    input_parser = InputParser(filename)
    grid, start, goals = input_parser.parse()

    search_algorithm_class = get_search_algorithm(method)
    if not search_algorithm_class:
        print("Invalid search method. Please choose among: DFS, BFS, CUS1 (uninformed) and GBFS, AS, CUS2 (informed)")
        sys.exit(1)

    results = []
    all_total_nodes = 0
    all_traversed = []  # Changed to list to maintain order
    all_paths = []
    index=0
    if goals == []:
        print(f"{filename} {method}")
        print(f"No goal is reachable; {0}")
        sys.exit(0)

    for goal in goals:
        index += 1
        temp_grid = Grid(grid.rows, grid.cols)
        temp_grid.set_grid([row[:] for row in grid.grid])  # Deep copy of grid for each search
        temp_result, temp_total_nodes, temp_traversed = None, 0, []
        
        search_algorithm = search_algorithm_class(temp_grid, start, goal)
        temp_result, temp_total_nodes, temp_traversed = search_algorithm.search()

        if index == 1:
            if temp_result:
                print(f"{filename} {method}")
                print(f"< Node ({goal[0]}, {goal[1]})> {temp_total_nodes}") # add {len(path)} component for printing path's length
                print([get_direction(temp_result[i], temp_result[i+1]) for i in range(len(temp_result)-1)]) # get direction for path i to i+1 that not include the coordination of starting point.
            else:
                print(f"{filename} {method}")
                print(f"No goal is reachable; {temp_total_nodes}") # return total_nodes explored although no path found

        results.append((goal, temp_result, temp_total_nodes))
        all_total_nodes += temp_total_nodes
        append_unique(all_traversed, temp_traversed)
        all_paths.append(temp_result)

    if all_paths:
        grid_instance = Grid(grid.rows, grid.cols)
        gui_paths = [[(node.x, node.y) for node in path] for path in all_paths]
        combined_path = [coord for path in gui_paths for coord in path]

        app = GUI(grid_instance, grid, start, goals, combined_path, all_traversed)
        app.mainloop()

if __name__ == "__main__":
    main()