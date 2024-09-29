import heapq
import random

class Node:
    def __init__(self, state, parent=None, g=0, h=0):
        self.state = state
        self.parent = parent
        self.g = g
        self.h = h
        self.f = g + h
    
    def __lt__(self, other):
        return self.f < other.f

def heuristic(node, goal_state):
    h = 0
    for i in range(1, 9):
        current_index = node.state.index(i)
        goal_index = goal_state.index(i)
        current_row, current_col = divmod(current_index, 3)
        goal_row, goal_col = divmod(goal_index, 3)
        h += abs(current_row - goal_row) + abs(current_col - goal_col)
    return h

def get_successors(node):
    successors = []
    index = node.state.index(0)
    quotient = index // 3
    remainder = index % 3
    
    moves = []
    if quotient == 0:
        moves = [3]
    if quotient == 1:
        moves = [-3, 3]
    if quotient == 2:
        moves = [-3]
    if remainder == 0:
        moves += [1]
    if remainder == 1:
        moves += [-1, 1]
    if remainder == 2:
        moves += [-1]

    for move in moves:
        new_index = index + move
        if 0 <= new_index < 9:
            new_state = list(node.state)
            new_state[index], new_state[new_index] = new_state[new_index], new_state[index]
            successor = Node(new_state, node, node.g + 1)
            successors.append(successor)            
    return successors

def search_agent(start_state, goal_state):
    start_node = Node(start_state, g=0, h=heuristic(Node(start_state), goal_state))
    goal_node = Node(goal_state)
    
    frontier = []
    heapq.heappush(frontier, (start_node.f, start_node))
    visited = set()
    
    while frontier:
        _, node = heapq.heappop(frontier)
        
        if tuple(node.state) in visited:
            continue
        visited.add(tuple(node.state))
        
        if node.state == list(goal_node.state):
            path = []
            while node:
                path.append(node.state)
                node = node.parent
            return path[::-1]
        
        for successor in get_successors(node):
            successor.h = heuristic(successor, goal_state)
            successor.f = successor.g + successor.h
            heapq.heappush(frontier, (successor.f, successor))
    
    return None

start_state = [0, 1, 3, 4, 5, 6, 7, 8, 2]
s_node = Node(start_state)

goal_state = [1, 2, 3, 4, 5, 0, 7, 8, 6]

solution = search_agent(start_state, goal_state)
if solution:
    print("Solution found:")
    for step in solution:
        print(step)
else:
    print("No solution found.")