class Maze:
    def __init__(self, wall, switches):
        self.wall = wall
        self.switches = switches
    def is_valid_move(self, x, y):
        return 0 <= x < len(self.wall) and 0 <= y < len(self.wall[0]) and self.wall[x][y] in [' ', '.']

class Node:
    def __init__(self, state, parent=None, weight=0, steps=''):
        self.parent = parent
        self.ares_pos = state[0]
        self.stones = state[1]
        self.weight = weight
        self.steps = steps
        
    def __lt__(self, other):
        return self.weight < other.weight

    def __hash__(self):
        ares_pos, stones = self.ares_pos, self.stones
        return hash((ares_pos, frozenset(stones)))

    def __eq__(self, other):
        return self.ares_pos == other.ares_pos and self.stones == other.stones

