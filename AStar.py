from node import *
from utils import *
import heapq
import numpy as np

def minimized_total_weight_heuristic(stones, switches):
    total_cost = 0

    for stone_pos, weight in stones:
        min_distance = float('inf')

        for switch in switches:
            dist = abs(stone_pos[0] - switch[0]) + abs(stone_pos[1] - switch[1])
            weighted_distance = dist * weight

            if weighted_distance < min_distance:
                min_distance = weighted_distance

        total_cost += min_distance

    return total_cost

def AStar(init_state, maze):
    start_node = Node(init_state)
    frontier = []
    heapq.heappush(frontier, (minimized_total_weight_heuristic(start_node.stones, maze.switches), start_node))
    explored_set = set()
    nodes_generated = 1

    while frontier:
        _, current_node = heapq.heappop(frontier)
        nodes_generated += 1

        if is_goal(current_node, maze):
            solution = trace(current_node, maze)
            return solution, current_node.steps, nodes_generated, current_node.weight

        explored_set.add(current_node)

        for action, next_state, cost in get_successors(current_node, maze):
            next_node = Node(state=next_state, parent=current_node, weight=current_node.weight + cost, steps=current_node.steps + action)

            if next_node not in explored_set:
                g_cost = next_node.weight
                h_cost = minimized_total_weight_heuristic(next_node.stones, maze.switches)
                f_cost = g_cost + h_cost

                heapq.heappush(frontier, (f_cost, next_node))

    return None, None, nodes_generated, None