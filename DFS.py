from collections import deque
from node import *
from utils import *
import time

def DFS(init_state, maze):
    frontier = [Node(init_state)] #Stack
    explored = set()
    nodes_generated = 1
    actions = []
    
    cnt = 0
    while frontier:
        cnt += 1
        node = frontier.pop()
        nodes_generated += 1
        
        if is_goal(node, maze):
            solution = trace(node, maze)
            return (solution, node.steps, nodes_generated, node.weight)
        
        explored.add(node)

        for action, next_state, cost in get_successors(node, maze):
            actions.append(actions)

            if Node(next_state) not in explored and Node(next_state) not in frontier:
                new_steps = node.steps + action
                new_weight = node.weight + cost
                frontier.append(Node(state=next_state, parent=node, weight=new_weight, steps=new_steps))

    return None, None, nodes_generated, None
