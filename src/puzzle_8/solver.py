import heapq
from collections import deque
from src.core.base_solver import BaseSolver
from src.puzzle_8.heuristics import misplaced_tiles, manhattan_distance, linear_conflict

class Puzzle8Solver(BaseSolver):
    def __init__(self):
        self.goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)

    def get_neighbors(self, state):
        neighbors = []
        zero_idx = state.index(0)
        r, c = zero_idx // 3, zero_idx % 3
        
        # Moves: Up, Down, Left, Right
        moves = []
        if r > 0: moves.append(-3) # Up
        if r < 2: moves.append(3)  # Down
        if c > 0: moves.append(-1) # Left
        if c < 2: moves.append(1)  # Right
        
        for move in moves:
            neighbor = list(state)
            new_idx = zero_idx + move
            # Swap
            neighbor[zero_idx], neighbor[new_idx] = neighbor[new_idx], neighbor[zero_idx]
            neighbors.append(tuple(neighbor))
            
        return neighbors

    def solve(self, initial_state, method="A*", heuristic_name="Manhattan"):
        """
        Solve 8-puzzle.
        initial_state: List or tuple of 9 elements.
        method: "BFS", "UCS", "A*"
        heuristic_name: "Manhattan", "Misplaced Tiles", "Linear Conflict"
        """
        # Convert state to tuple
        start_state = tuple(initial_state)
        
        if method == "BFS":
            return self._solve_bfs(start_state)
        elif method == "UCS":
            return self._solve_ucs(start_state)
        elif method == "A*":
            # Map heuristic name to function
            h_func = manhattan_distance
            if heuristic_name == "Misplaced Tiles":
                h_func = misplaced_tiles
            elif heuristic_name == "Linear Conflict":
                h_func = linear_conflict
            return self._solve_astar(start_state, h_func)
        else:
            raise ValueError(f"Unknown method: {method}")

    def _solve_bfs(self, start):
        if start == self.goal:
            return {"solution": [start], "nodes_explored": 0, "success": True}
            
        queue = deque([(start, [start])])
        visited = {start}
        nodes_explored = 0
        
        while queue:
            curr, path = queue.popleft()
            nodes_explored += 1
            
            # Limit search depth for safety in UI
            if nodes_explored > 50000:
                return {"solution": None, "nodes_explored": nodes_explored, "success": False, "msg": "Limit exceeded"}
                
            for neighbor in self.get_neighbors(curr):
                if neighbor == self.goal:
                    return {"solution": path + [neighbor], "nodes_explored": nodes_explored, "success": True}
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
                    
        return {"solution": None, "nodes_explored": nodes_explored, "success": False}

    def _solve_ucs(self, start):
        # Priority queue stores (cost, state, path)
        # In 8-puzzle, each step cost is 1
        pq = [(0, start, [start])]
        visited = {}
        nodes_explored = 0
        
        while pq:
            cost, curr, path = heapq.heappop(pq)
            nodes_explored += 1
            
            if curr == self.goal:
                return {"solution": path, "nodes_explored": nodes_explored, "success": True}
                
            if curr in visited and visited[curr] <= cost:
                continue
            visited[curr] = cost
            
            if nodes_explored > 50000:
                return {"solution": None, "nodes_explored": nodes_explored, "success": False, "msg": "Limit exceeded"}
                
            for neighbor in self.get_neighbors(curr):
                next_cost = cost + 1
                if neighbor not in visited or next_cost < visited[neighbor]:
                    heapq.heappush(pq, (next_cost, neighbor, path + [neighbor]))
                    
        return {"solution": None, "nodes_explored": nodes_explored, "success": False}

    def _solve_astar(self, start, h_func):
        # Priority queue stores (f_score, g_score, state, path)
        # We also need a tie-breaker count to avoid comparing states directly when scores are equal
        counter = 0
        pq = [(h_func(start), 0, counter, start, [start])]
        visited = {}
        nodes_explored = 0
        
        while pq:
            f, g, _, curr, path = heapq.heappop(pq)
            nodes_explored += 1
            
            if curr == self.goal:
                return {"solution": path, "nodes_explored": nodes_explored, "success": True}
                
            if curr in visited and visited[curr] <= g:
                continue
            visited[curr] = g
            
            if nodes_explored > 50000:
                return {"solution": None, "nodes_explored": nodes_explored, "success": False, "msg": "Limit exceeded"}
                
            for neighbor in self.get_neighbors(curr):
                next_g = g + 1
                if neighbor not in visited or next_g < visited[neighbor]:
                    counter += 1
                    h = h_func(neighbor)
                    heapq.heappush(pq, (next_g + h, next_g, counter, neighbor, path + [neighbor]))
                    
        return {"solution": None, "nodes_explored": nodes_explored, "success": False}
