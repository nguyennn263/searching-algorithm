from node import Node, Maze
import json

def draw(node, maze):
    tmp = maze.wall
    # print(node.ares_pos)
    for i, row in enumerate(maze.wall):
        for j, cell in enumerate(row):
            tmp[i][j] = ' '  # Default: white
            if cell == '#':
                tmp[i][j] = '#'  # Wall: black
            elif cell == '.':
                tmp[i][j] = '.'  # Switch: green
            if node.ares_pos == (i, j):
                tmp[i][j] = '@'
                if tmp[i][j] == '.':
                    tmp[i][j] = '+'
            for (stone_pos, weight) in node.stones:
                if stone_pos == (i, j):
                    tmp[i][j] = f'{weight}'  # Display weight with the stone
    for row in tmp:
        print(row)
    print()

directions = {
    'u': (-1, 0),  # Up
    'd': (1, 0),   # Down
    'l': (0, -1),  # Left
    'r': (0, 1)    # Right
}


def read_input_file(filename):
    with open(filename, 'r') as f:
        weights = list(map(int, f.readline().strip().split()))
        wall = []
        stones = []
        switches = set()
        ares_pos = None
        index_stone = 0
        for i, line in enumerate(f):
            row = list(line.strip())
            wall.append(row)

            for j, char in enumerate(row):
                if char == '@':
                    wall[i][j] = ' '
                    ares_pos = (i, j)
                elif char == '$':
                    wall[i][j] = ' '
                    stones.append(((i, j), weights[index_stone]))  
                    index_stone += 1
                elif char == '.':
                    switches.add((i, j))
                elif char == '+':
                    switches.add((i, j))
                    ares_pos = (i, j)

    return {
        'wall': wall,
        'ares_pos': ares_pos,
        'stones': stones,
        'switches': switches
    }

def is_goal(node, maze):
    return set((stone[0] for stone in node.stones)) == set(maze.switches)

def get_successors(node, maze, with_cost=False):
    x, y = node.ares_pos
    stones = {pos: weight for pos, weight in node.stones}  # Use a dictionary for quick lookups

    successors = []

    for action, (dx, dy) in directions.items():
        new_x, new_y = x + dx, y + dy

        # Ares moves to an empty space
        if maze.is_valid_move(new_x, new_y) and (new_x, new_y) not in stones:
            successors.append((action, ((new_x, new_y), node.stones), 0))

        # Ares pushes a stone
        elif (new_x, new_y) in stones:
            push_x, push_y = new_x + dx, new_y + dy

            if maze.is_valid_move(push_x, push_y) and (push_x, push_y) not in stones:
                # Update the pushed stone's position while keeping others the same
                new_stones = [
                    ((push_x, push_y), stones[(new_x, new_y)]) if (pos == (new_x, new_y)) 
                    else (pos, weight) for pos, weight in node.stones
                ]
                cost = stones[(new_x, new_y)] # Cost = base + weight of the stone
                successors.append((action.upper(), ((new_x, new_y), new_stones), cost))

    return successors

def trace(node, maze):
    solution = [node]
    while node.parent is not None:
        solution.append(node.parent)
        node = node.parent

    solution = list(reversed(solution))
    return solution

def read_solution(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    nodes = []
    for item in data:
        ares_pos = tuple(item['ares_pos'])
        stones = [((pos[0], pos[1]) , weight) for pos, weight in item['stones']]
        weight = item['weight']
        node = Node(state=(ares_pos, stones), weight=weight)
        nodes.append(node)
    
    return nodes