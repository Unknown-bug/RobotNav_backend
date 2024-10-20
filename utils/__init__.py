def get_direction(current, next):
    if current.y < next.y:
        return 'down'
    elif current.y > next.y:
        return 'up'
    elif current.x < next.x:
        return 'right'
    elif current.x > next.x:
        return 'left'
    else:
        return 'stay' 

def append_unique(lst, items):
    for item in items:
        if item not in lst:
            lst.append(item)
            
def get_path(directions, start):
    path = []
    position = start
    path.append(position)
    for direction in directions:
        if direction == 'up':
            position = (position[0], position[1] - 1)
        elif direction == 'left':
            position = (position[0] - 1, position[1])
        elif direction == 'down':
            position = (position[0], position[1] + 1)
        elif direction == 'right':
            position = (position[0] + 1, position[1])
        path.append(position)
    return path

def path_to_directions(path):
    directions = []
    for i in range(len(path) - 1):
        current = path[i]
        next_node = path[i + 1]
        direction = get_direction(current, next_node)
        directions.append(direction)
    return directions