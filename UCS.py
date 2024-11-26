import heapq
from node import *
from utils import *

def UCS(init_state, maze):
    # Hàng đợi ưu tiên cho UCS, sắp xếp theo chi phí (weight)
    frontier = []
    nodes_generated = 1

    # Thêm trạng thái ban đầu vào hàng đợi ưu tiên
    initial_node = Node(init_state)
    heapq.heappush(frontier, (0, initial_node))

    # Theo dõi chi phí thấp nhất đã tìm thấy cho mỗi trạng thái
    cost_so_far = {initial_node: 0}
    
    while frontier:
        current_weight, current_node = heapq.heappop(frontier)

        # Kiểm tra nếu trạng thái hiện tại là mục tiêu
        if is_goal(current_node, maze):
            solution = trace(current_node, maze)
            return (solution, current_node.steps, nodes_generated, current_node.weight)
        
        # Lặp qua các trạng thái kế tiếp
        for action, next_state, cost in get_successors(current_node, maze):
            new_node = Node(next_state, parent=current_node, weight=current_node.weight + cost, steps=current_node.steps + action)
            new_cost = current_node.weight + cost

            # Kiểm tra nếu trạng thái có chi phí thấp hơn để cập nhật
            if new_node not in cost_so_far or new_cost < cost_so_far[new_node]:
                cost_so_far[new_node] = new_cost
                heapq.heappush(frontier, (new_cost, new_node))
                nodes_generated += 1  # Tăng khi thêm một nút mới vào hàng đợi

    # Không tìm được giải pháp
    return None, None, nodes_generated, None
