from collections import deque

def check(prev, new):
    if abs(prev.index(0) - new.index(0)) > 2:
        return False
    elif new.index(0) < 0 or new.index(0) >= len(prev):
        return False
    elif prev[new.index(0)] == -1 and prev.index(0) <= new.index(0):
        return False
    elif prev[new.index(0)] == 1 and prev.index(0) >= new.index(0):
        return False
    else:
        return True

def get_successors(state):
    moves = [-2, -1, 1, 2]
    successors = []
    empty_space_index = state.index(0)
    for m in moves:
        new_index = empty_space_index + m
        if 0 <= new_index < len(state):
            new_state = list(state)
            new_state[empty_space_index], new_state[new_index] = new_state[new_index], new_state[empty_space_index]
            new_state = tuple(new_state)
            if check(state, new_state):
                successors.append(new_state)
    return successors

def bfs(start_state, goal_state):
    dq = deque([(start_state, [])])
    visited = set()
    while dq:
        s = dq.popleft()
        if s[0] in visited:
            continue
        visited.add(s[0])
        successors = get_successors(s[0])
        path = s[1] + [s[0]]
        for succ in successors:
            if succ == goal_state:
                return path + [succ]
            dq.append((succ, path))
    return None

start = (-1, -1, -1, 0, 1, 1, 1)
goal = (1, 1, 1, 0, -1, -1, -1)

ans = bfs(start, goal)

if ans:
    for state in ans:
        print(state)
else:
    print("solution not found")
