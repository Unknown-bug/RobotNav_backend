import csv
import os
import time
from data.input_parser import InputParser
from algorithms import get_search_algorithm
from utils.grid import Grid
from utils import get_direction

def run_test(filename, method):
    input_parser = InputParser(filename)
    grid, start, goals = input_parser.parse()

    search_algorithm_class = get_search_algorithm(method)
    if not search_algorithm_class:
        return None

    results = []
    total_nodes = 0
    total_time = 0

    for goal in goals:
        temp_grid = Grid(grid.rows, grid.cols)
        temp_grid.set_grid([row[:] for row in grid.grid])

        search_algorithm = search_algorithm_class(temp_grid, start, goal)
        
        path, nodes_explored, _ = search_algorithm.search()

        total_nodes += nodes_explored

        # Generate directions if path exists
        if path:
            directions = [get_direction(path[i], path[i + 1]) for i in range(len(path) - 1)]
            directions_str = '-'.join([direction[0].upper() for direction in directions])
        else:
            directions_str = "N/A"  # No path found

        results.append({
            'goal': goal,
            'path_length': len(path) if path else 0,
            'nodes_explored': nodes_explored,
            'directions': directions_str  # Add the directions here
        })

    return {
        'filename': filename,
        'method': method,
        'total_nodes': total_nodes,
        'total_time': total_time,
        'results': results
    }

def main():
    algorithms = ['DFS', 'BFS', 'CUS1', 'GBFS', 'AS', 'CUS2']
    input_files = [f for f in os.listdir('test_files') if f.endswith('.txt')]

    with open('algorithm_performance.csv', 'w', newline='') as csvfile:
        fieldnames = ['Filename', 'Algorithm', 'Goal', 'Path Length', 'Nodes Explored', 'Execution Time (s)', 'Total Nodes', 'Total Time (s)', 'Directions']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for filename in input_files:
            for algorithm in algorithms:
                result = run_test(os.path.join('test_files', filename), algorithm)
                if result:
                    for goal_result in result['results']:
                        writer.writerow({
                            'Filename': result['filename'],
                            'Algorithm': result['method'],
                            'Goal': f"({goal_result['goal'][0]}, {goal_result['goal'][1]})",
                            'Path Length': goal_result['path_length'],
                            'Nodes Explored': goal_result['nodes_explored'],
                            'Total Nodes': result['total_nodes'],
                            'Directions': goal_result['directions']  # Export the directions
                        })

    print("Testing completed. Results saved in 'algorithm_performance.csv'")

if __name__ == "__main__":
    main()
