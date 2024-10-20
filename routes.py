from algorithms import get_search_algorithm
from utils import path_to_directions, append_unique
from utils.grid import Grid
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS configuration (adjust origin as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

class getResult(BaseModel):
    algorithm: str
    initialstate: list[int]
    goalstate: list[list[int]]
    grid: list[list[int]]

@app.post("/getResult")
def get_result(data: getResult):
    algorithm = data.algorithm
    initialstate = (data.initialstate[0], data.initialstate[1])
    goalstate = [(x[0], x[1]) for x in data.goalstate]
    rows = len(data.grid)
    cols = len(data.grid[0])
    grid = Grid(rows, cols)
    grid.set_grid(data.grid)
    
    # Initialize variables
    results = []
    total_nodes = 0
    traversed = []

    # Choose algorithm
    search_algorithm_class = get_search_algorithm(algorithm.upper())
    if not search_algorithm_class:
        return {"error": "Invalid algorithm"}

    for goal in goalstate:
        if(goal[0] > grid.rows or goal[1] > grid.cols):
            continue
        temp_grid = Grid(grid.rows, grid.cols)
        temp_grid.set_grid([row[:] for row in grid.grid])  # Deep copy of grid for each search
        temp_result, temp_total_nodes, temp_traversed = None, 0, []

        search_algorithm = search_algorithm_class(temp_grid, initialstate, goal)
        temp_result, temp_total_nodes, temp_traversed = search_algorithm.search()
        
        results.append({
            "goal": goal,
            "path": path_to_directions(temp_result),
            "total_nodes": temp_total_nodes,
            "traversed": temp_traversed
        })
        total_nodes += temp_total_nodes
        append_unique(traversed, temp_traversed)
        print (results)
    if results:
        return {"path": results, "traversed": traversed, "total_nodes": total_nodes}
    else:
        return {"error": "No path found"}