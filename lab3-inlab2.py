import heapq

class MarbleSolitaireAStar:
    def __init__(self, board):
        self.board = board
        self.goal = self.get_goal_state()
        self.exploration_limit = 1000

    def get_goal_state(self):
        goal_state = [[0]*7 for _ in range(7)]
        goal_state[3][3] = 1
        return goal_state

    def is_goal_state(self, state):
        return state == self.goal

    def generate_valid_moves(self, state):
        moves = []
        directions = [
            (-2, 0, -1, 0),
            (2, 0, 1, 0),
            (0, -2, 0, -1),
            (0, 2, 0, 1)
        ]

        for r in range(7):
            for c in range(7):
                if state[r][c] == 1:
                    for dr, dc, dr_over, dc_over in directions:
                        new_r = r + dr
                        new_c = c + dc
                        over_r = r + dr_over
                        over_c = c + dc_over
                        if (0 <= new_r < 7 and 0 <= new_c < 7 and
                                0 <= over_r < 7 and 0 <= over_c < 7 and
                                state[new_r][new_c] == 0 and
                                state[over_r][over_c] == 1):
                            new_state = [row[:] for row in state]
                            new_state[r][c] = 0
                            new_state[over_r][over_c] = 0
                            new_state[new_r][new_c] = 1
                            moves.append(new_state)
        return moves

    def heuristic(self, state):
        return sum(sum(row) for row in state)

    def a_star_search(self):
        priority_queue = []
        explored = set()
        explored_count = 0

        initial_cost = 0 + self.heuristic(self.board)
        heapq.heappush(priority_queue, (initial_cost, self.board))

        while priority_queue:
            f_cost, current_state = heapq.heappop(priority_queue)

            if self.is_goal_state(current_state):
                return current_state

            if tuple(map(tuple, current_state)) not in explored:
                explored.add(tuple(map(tuple, current_state)))
                explored_count += 1

                if explored_count > self.exploration_limit:
                    return None

                valid_moves = self.generate_valid_moves(current_state)

                for move in valid_moves:
                    new_cost = f_cost - self.heuristic(current_state) + 1 + self.heuristic(move)
                    heapq.heappush(priority_queue, (new_cost, move))

        return None

initial_board = [
    [0, 0, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 1, 0, 0],
    [1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1],
    [0, 0, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 1, 0, 0]
]

a_star_solver = MarbleSolitaireAStar(initial_board)
a_star_solution = a_star_solver.a_star_search()
print("A* Search Solution:", a_star_solution)
