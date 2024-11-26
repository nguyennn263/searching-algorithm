from collections import deque
from node import *
from utils import *
import time

def BFS(init_state, maze):
    frontier = deque([Node(init_state)])
    explored = set()
    nodes_generated = 1
    actions = []
    
    while frontier:
        node = frontier.popleft()
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
                # print(action, next_state[1])
                if is_goal(Node(next_state), maze):
                    new_node = Node(state=next_state, parent=node, weight=new_weight, steps=new_steps)
                    solution = trace(new_node, maze)

                    return (solution, node.steps, nodes_generated, new_weight)                
                frontier.append(Node(state=next_state, parent=node, weight=new_weight, steps=new_steps))

    return None, None, nodes_generated, None

