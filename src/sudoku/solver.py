import copy
from src.core.base_solver import BaseSolver

class SudokuSolver(BaseSolver):
    def __init__(self):
        self.nodes_explored = 0

    def solve(self, initial_state, method="Backtracking + MRV + FC"):
        """
        Solve a Sudoku puzzle.
        initial_state: String of length 81 or list of list of 9x9 integers.
        method: "Basic Backtracking", "Backtracking + MRV", "Backtracking + MRV + FC"
        """
        self.nodes_explored = 0
        
        # Parse state to 9x9 board
        if isinstance(initial_state, str):
            board = [[int(initial_state[i*9 + j]) for j in range(9)] for i in range(9)]
        else:
            board = copy.deepcopy(initial_state)

        # Pre-compute domains for Forward Checking
        # domains[r][c] = set of valid values
        domains = [[set(range(1, 10)) if board[r][c] == 0 else {board[r][c]} for c in range(9)] for r in range(9)]
        
        # Initial forward checking constraint propagation
        if "FC" in method:
            for r in range(9):
                for c in range(9):
                    if board[r][c] != 0:
                        if not self._forward_check(board, domains, r, c, board[r][c]):
                            return {"solution": None, "nodes_explored": self.nodes_explored, "success": False}

        success = self._search(board, domains, method)
        
        return {
            "solution": board if success else None,
            "nodes_explored": self.nodes_explored,
            "success": success
        }

    def _search(self, board, domains, method):
        self.nodes_explored += 1
        
        # Find unassigned cell
        cell = self._select_unassigned_variable(board, domains, method)
        if not cell:
            return True # Solved
        
        r, c = cell
        
        # Get values to try
        ordered_values = self._order_domain_values(board, domains, r, c)
        
        for val in ordered_values:
            if self._is_valid(board, r, c, val):
                # Place value
                board[r][c] = val
                
                # Backup domains for FC
                if "FC" in method:
                    domains_backup = [[copy.copy(domains[i][j]) for j in range(9)] for i in range(9)]
                    domains[r][c] = {val}
                    
                    # Forward check
                    if self._forward_check(board, domains, r, c, val):
                        if self._search(board, domains, method):
                            return True
                    
                    # Backtrack domains
                    domains = domains_backup
                else:
                    if self._search(board, domains, method):
                        return True
                
                # Backtrack board
                board[r][c] = 0
                
        return False

    def _is_valid(self, board, r, c, val):
        # Row check
        for j in range(9):
            if board[r][j] == val:
                return False
        # Col check
        for i in range(9):
            if board[i][c] == val:
                return False
        # 3x3 block check
        br, bc = 3 * (r // 3), 3 * (c // 3)
        for i in range(br, br + 3):
            for j in range(bc, bc + 3):
                if board[i][j] == val:
                    return False
        return True

    def _select_unassigned_variable(self, board, domains, method):
        if "MRV" in method:
            # Choose cell with minimum remaining values in domain
            min_remaining = 10
            best_cell = None
            for r in range(9):
                for c in range(9):
                    if board[r][c] == 0:
                        # Count options remaining
                        options = 0
                        for val in range(1, 10):
                            if self._is_valid(board, r, c, val):
                                options += 1
                        if options < min_remaining:
                            min_remaining = options
                            best_cell = (r, c)
            return best_cell
        else:
            # Basic Backtracking: find first unassigned cell (row-by-row)
            for r in range(9):
                for c in range(9):
                    if board[r][c] == 0:
                        return (r, c)
            return None

    def _order_domain_values(self, board, domains, r, c):
        # Return possible values for the cell. 
        # In a more advanced implementation, LCV (Least Constraining Value) Heuristic could be used.
        # Here we return simple values in ascending order that are valid.
        return [val for val in range(1, 10) if self._is_valid(board, r, c, val)]

    def _forward_check(self, board, domains, r, c, val):
        # Update domains of neighbors (same row, same col, same subgrid)
        # Row
        for j in range(9):
            if board[r][j] == 0:
                domains[r][j].discard(val)
                if len(domains[r][j]) == 0:
                    return False
        # Col
        for i in range(9):
            if board[i][c] == 0:
                domains[i][c].discard(val)
                if len(domains[i][c]) == 0:
                    return False
        # Subgrid
        br, bc = 3 * (r // 3), 3 * (c // 3)
        for i in range(br, br + 3):
            for j in range(bc, bc + 3):
                if board[i][j] == 0:
                    domains[i][j].discard(val)
                    if len(domains[i][j]) == 0:
                        return False
        return True
