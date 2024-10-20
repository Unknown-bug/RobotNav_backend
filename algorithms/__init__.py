from .uninformed_search import DepthFirstSearch, BreadthFirstSearch, CustomSearch1
from .informed_search import GreedyBestFirstSearch, AStarSearch, CustomSearch2

def get_search_algorithm(method):
    algorithms = {
        "DFS": DepthFirstSearch,
        "BFS": BreadthFirstSearch,
        "CUS1": CustomSearch1,
        "GBFS": GreedyBestFirstSearch,
        "AS": AStarSearch,
        "CUS2": CustomSearch2,
    }
    return algorithms.get(method)