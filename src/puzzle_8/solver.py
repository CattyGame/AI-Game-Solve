import collections
import heapq
import time
from src.puzzle_8.heuristics import manhattan_distance, misplaced_tiles

def load_matrix_from_file(file_path):
    matrix = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                matrix.append([int(x) for x in line.split()])
    return matrix

class Puzzle8Solver:
    def __init__(self):
        self.nodes_explored = 0
        self.execution_time = 0.0
        self.goal_state = ((1, 2, 3), (4, 5, 6), (7, 8, 0))

    def reset_metrics(self):
        self.nodes_explored = 0
        self.execution_time = 0.0

    def _get_neighbors(self, state):
        neighbors = []
        r_zero, c_zero = -1, -1
        for r in range(3):
            for c in range(3):
                if state[r][c] == 0:
                    r_zero, c_zero = r, c
                    break
        
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r_zero + dr, c_zero + dc
            if 0 <= nr < 3 and 0 <= nc < 3:
                new_state = [list(row) for row in state]
                new_state[r_zero][c_zero], new_state[nr][nc] = new_state[nr][nc], new_state[r_zero][c_zero]
                neighbors.append(tuple(tuple(row) for row in new_state))
        return neighbors

    def solve_bfs(self, initial_state):
        self.reset_metrics()
        start_time = time.perf_counter()
        start_node = tuple(tuple(row) for row in initial_state)
        if start_node == self.goal_state:
            self.execution_time = time.perf_counter() - start_time
            return [start_node]
        queue = collections.deque([(start_node, [start_node])])
        visited = {start_node}
        while queue:
            current, path = queue.popleft()
            self.nodes_explored += 1
            for neighbor in self._get_neighbors(current):
                if neighbor not in visited:
                    if neighbor == self.goal_state:
                        self.execution_time = time.perf_counter() - start_time
                        self.nodes_explored += 1
                        return path + [neighbor]
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        self.execution_time = time.perf_counter() - start_time
        return None

    def solve_ucs(self, initial_state):
        self.reset_metrics()
        start_time = time.perf_counter()
        start_node = tuple(tuple(row) for row in initial_state)
        count = 0
        pq = [(0, count, start_node, [start_node])]
        visited = {}
        while pq:
            cost, _, current, path = heapq.heappop(pq)
            self.nodes_explored += 1
            if current == self.goal_state:
                self.execution_time = time.perf_counter() - start_time
                return path
            if current in visited and visited[current] <= cost:
                continue
            visited[current] = cost
            for neighbor in self._get_neighbors(current):
                next_cost = cost + 1
                if neighbor not in visited or next_cost < visited[neighbor]:
                    count += 1
                    heapq.heappush(pq, (next_cost, count, neighbor, path + [neighbor]))
        self.execution_time = time.perf_counter() - start_time
        return None

    def solve_astar(self, initial_state, heuristic_type="manhattan"):
        self.reset_metrics()
        start_time = time.perf_counter()
        h_func = manhattan_distance if heuristic_type == 'manhattan' else misplaced_tiles
        start_node = tuple(tuple(row) for row in initial_state)
        count = 0
        g_start = 0
        f_start = g_start + h_func(start_node)
        pq = [(f_start, count, g_start, start_node, [start_node])]
        visited = {}
        while pq:
            f, _, g, current, path = heapq.heappop(pq)
            self.nodes_explored += 1
            if current == self.goal_state:
                self.execution_time = time.perf_counter() - start_time
                return path
            if current in visited and visited[current] <= g:
                continue
            visited[current] = g
            for neighbor in self._get_neighbors(current):
                g_next = g + 1
                if neighbor not in visited or g_next < visited[neighbor]:
                    count += 1
                    f_next = g_next + h_func(neighbor)
                    heapq.heappush(pq, (f_next, count, g_next, neighbor, path + [neighbor]))
        self.execution_time = time.perf_counter() - start_time
        return None

    def solve(self, initial_state):
        return self.solve_astar(initial_state, heuristic_type='manhattan')