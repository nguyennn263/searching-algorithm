from utils import *
from node import *
from BFS import *
from DFS import *
from UCS import *
from AStar import *

import tracemalloc
import time
import os
import json
from GUI import GUI

algos = {
    "BFS": BFS,
    "DFS": DFS,
    "UCS": UCS,
    "AStar": AStar,
}

def create_output_compare(len, weight, node_gens, time_ms, mem):
    txt_file = 'compare.csv'
    if len == None:
        with open(txt_file, mode='a') as file:
            file.write("None\n")
        return         
    
     
    with open(txt_file, mode='a') as file:
        row = f"{len},{weight},{node_gens},{time_ms},{mem}\n"
        file.write(row)  


def process(init_state, maze, func_name, output_file):
    tracemalloc.start()
    snapshot_before = tracemalloc.take_snapshot()
    start_time = time.time()
    solution, steps, nodes_generated, weight = algos[func_name](init_state, maze)
    
    end_time = time.time()
    execution_time_ms = (end_time - start_time) * 1000  
    
    snapshot_after = tracemalloc.take_snapshot()
    tracemalloc.stop()
    top_stats = snapshot_after.compare_to(snapshot_before, 'lineno')
    memory_usage_mb = sum(stat.size for stat in top_stats)/(1024*1024)

    if solution is not None: 
        create_output_compare(len(solution) - 1, weight, nodes_generated, execution_time_ms, memory_usage_mb)
        print(f"Steps: {len(solution) - 1}, Weight: {weight}, Node: {nodes_generated}, Time (ms): {execution_time_ms}, Memory (MB): {memory_usage_mb}")
        print(steps)
        with open(output_file, mode='a') as file:
            file.write(f"{func_name}\n")
            file.write(f"Steps: {len(solution) - 1}, Weight: {weight}, Node: {nodes_generated}, Time (ms): {execution_time_ms}, Memory (MB): {memory_usage_mb}\n")
            file.write(f"{steps}\n")
    else:
        print("No solution")
        with open(output_file, mode='a') as file:
            file.write(f"{func_name}\n")
            file.write("No solution\n")
        create_output_compare(None,None,None,None, None)
        solution = [Node(init_state)]
        
    return solution

def create_data_for_gui(solution, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    data = []
    for node in solution:
        data.append({
            "ares_pos": node.ares_pos,
            "stones": node.stones,
            "weight": node.weight
        })

    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4) 

    
def main():

    with open('compare.csv', mode='w') as file:
        file.write('')

    for i in range(1,11):
        print(f"Maze {i}")
        inputs = read_input_file(f"./inputs/input-{i:02}.txt")
        
        init_state = (inputs["ares_pos"], inputs["stones"])
        maze = Maze(inputs["wall"], inputs["switches"])
        
        output_file = f"./outputs/output-{i:02}.txt"
        with open(output_file, mode='w') as file:
            file.write('')
            
            
        for algo in algos:
            print(f"{algo}")
            solution = process(init_state, maze, algo, output_file)
            create_data_for_gui(solution, f"./outputs-for-gui/{algo}/solution-{i:02}.json")
            

if __name__ == "__main__":
    main()