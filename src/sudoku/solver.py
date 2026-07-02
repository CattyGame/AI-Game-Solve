"""
solver.py  –  MODULE 1: BỘ GIẢI SUDOKU
============================================================

Hiện thực Backtracking kết hợp các kỹ thuật CSP:
  • MRV  (Minimum Remaining Values)
  • Degree Heuristic (tiebreak)
  • Forward Checking

Giao diện công khai 
-------------------------------------------------
  SudokuSolver(use_mrv, use_degree, use_fc)
      .solve(initial_state)  ->  list[list[int]] | None
      .get_metrics()         ->  dict
      .reset_metrics()

Board format: list[list[int]], 9×9, giá trị 0 = ô trống.
"""

import copy
import tracemalloc
from typing import Optional

from src.core.base_solver import BaseSolver

# ──────────────────────────────────────────────────────────
SIZE   = 9
BOX    = 3
DIGITS = set(range(1, 10))


class SudokuSolver(BaseSolver):
    """
    Bộ giải Sudoku: Backtracking + MRV + Degree Heuristic + Forward Checking.

    Parameters
    ----------
    use_mrv    : dùng Minimum Remaining Values khi chọn ô
    use_degree : dùng Degree Heuristic làm tiebreak cho MRV
    use_fc     : dùng Forward Checking để cắt tỉa sớm
    """

    def __init__(
        self,
        use_mrv: bool = True,
        use_degree: bool = True,
        use_fc: bool = True,
    ):
        super().__init__()
        self.use_mrv    = use_mrv
        self.use_degree = use_degree
        self.use_fc     = use_fc

    # ──────────────────────────────────────────────────────
    # Giao diện bắt buộc (override từ BaseSolver)
    # ──────────────────────────────────────────────────────
    def solve(self, initial_state: list[list[int]]) -> Optional[list[list[int]]]:
        """
        Giải Sudoku từ trạng thái ban đầu.

        Parameters
        ----------
        initial_state : 9×9 list[list[int]], ô trống = 0

        Returns
        -------
        Ma trận đã điền đầy đủ hoặc None nếu vô nghiệm.
        """
        self.reset_metrics()

        grid = [row[:] for row in initial_state]

        domains = self._init_domains(grid)
        if domains is None:
            return None

        # Đo thời gian và bộ nhớ theo chuẩn BaseSolver
        tracemalloc.start()
        start = self._start_timer()

        result = self._backtrack(grid, domains)

        self._stop_timer(start)
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        self.memory_used = peak / (1024 * 1024)   # bytes → MB

        if result:
            self.solution_length = sum(
                1 for r in range(SIZE) for c in range(SIZE)
                if initial_state[r][c] == 0
            )
            return copy.deepcopy(result)
        return None

    # ──────────────────────────────────────────────────────
    # Kiểm tra lời giải hợp lệ (tiện ích)
    # ──────────────────────────────────────────────────────
    def is_valid_solution(self, board: list[list[int]]) -> bool:
        """Kiểm tra bảng đã điền đầy đủ và hợp lệ."""
        if not board or len(board) != SIZE:
            return False
        for i in range(SIZE):
            if set(board[i]) != DIGITS:
                return False
            if {board[r][i] for r in range(SIZE)} != DIGITS:
                return False
        for br in range(BOX):
            for bc in range(BOX):
                box_vals = {
                    board[br * BOX + r][bc * BOX + c]
                    for r in range(BOX) for c in range(BOX)
                }
                if box_vals != DIGITS:
                    return False
        return True

    # ──────────────────────────────────────────────────────
    # Khởi tạo domain
    # ──────────────────────────────────────────────────────
    def _init_domains(
        self, grid: list[list[int]]
    ) -> Optional[dict]:
        # Kiểm tra các ô đã điền sẵn có mâu thuẫn với nhau không
        for r in range(SIZE):
            for c in range(SIZE):
                v = grid[r][c]
                if v == 0:
                    continue
                for pr, pc in self._get_peers(r, c):
                    if grid[pr][pc] == v:
                        return None   # 2 ô liền kề cùng giá trị → vô nghiệm

        domains = {}
        for r in range(SIZE):
            for c in range(SIZE):
                if grid[r][c] != 0:
                    domains[(r, c)] = {grid[r][c]}
                else:
                    used = self._get_used_values(grid, r, c)
                    remaining = DIGITS - used
                    if not remaining:
                        return None
                    domains[(r, c)] = remaining
        return domains

    # ──────────────────────────────────────────────────────
    # Backtracking chính
    # ──────────────────────────────────────────────────────
    def _backtrack(
        self,
        grid: list[list[int]],
        domains: dict,
    ) -> Optional[list[list[int]]]:
        cell = self._select_unassigned(grid, domains)
        if cell is None:
            return grid

        r, c = cell
        for value in sorted(domains[(r, c)]):
            self.nodes_explored += 1

            if self._is_consistent(grid, r, c, value):
                grid[r][c] = value

                if self.use_fc:
                    new_domains, ok = self._forward_check(domains, r, c, value)
                    if ok:
                        result = self._backtrack(grid, new_domains)
                        if result:
                            return result
                else:
                    result = self._backtrack(grid, domains)
                    if result:
                        return result

                grid[r][c] = 0

        return None

    # ──────────────────────────────────────────────────────
    # Chọn biến – MRV + Degree Heuristic
    # ──────────────────────────────────────────────────────
    def _select_unassigned(self, grid, domains):
        empty = [
            (r, c)
            for r in range(SIZE) for c in range(SIZE)
            if grid[r][c] == 0
        ]
        if not empty:
            return None
        if not self.use_mrv:
            return empty[0]

        def key(cell):
            r, c = cell
            d = len(domains[(r, c)])
            deg = -self._count_empty_peers(grid, r, c) if self.use_degree else 0
            return (d, deg)

        return min(empty, key=key)

    def _count_empty_peers(self, grid, row, col):
        return sum(1 for r, c in self._get_peers(row, col) if grid[r][c] == 0)

    # ──────────────────────────────────────────────────────
    # Kiểm tra ràng buộc
    # ──────────────────────────────────────────────────────
    def _is_consistent(self, grid, row, col, value):
        return value not in self._get_used_values(grid, row, col)

    def _get_used_values(self, grid, row, col):
        used = set()
        used.update(v for v in grid[row] if v != 0)
        used.update(grid[r][col] for r in range(SIZE) if grid[r][col] != 0)
        br, bc = (row // BOX) * BOX, (col // BOX) * BOX
        used.update(
            grid[br + dr][bc + dc]
            for dr in range(BOX) for dc in range(BOX)
            if grid[br + dr][bc + dc] != 0
        )
        return used

    # ──────────────────────────────────────────────────────
    # Forward Checking
    # ──────────────────────────────────────────────────────
    def _forward_check(self, domains, row, col, value):
        new_domains = {k: set(v) for k, v in domains.items()}
        new_domains[(row, col)] = {value}
        for r, c in self._get_peers(row, col):
            if (r, c) in new_domains:
                new_domains[(r, c)].discard(value)
                if not new_domains[(r, c)]:
                    return new_domains, False
        return new_domains, True

    # ──────────────────────────────────────────────────────
    # Tiện ích
    # ──────────────────────────────────────────────────────
    @staticmethod
    def _get_peers(row, col):
        peers = set()
        peers.update((row, c) for c in range(SIZE) if c != col)
        peers.update((r, col) for r in range(SIZE) if r != row)
        br, bc = (row // BOX) * BOX, (col // BOX) * BOX
        peers.update(
            (br + dr, bc + dc)
            for dr in range(BOX) for dc in range(BOX)
            if (br + dr, bc + dc) != (row, col)
        )
        return list(peers)

    @staticmethod
    def print_board(board: list[list[int]], title: str = "") -> None:
        if title:
            print(f"\n{'─' * 25}  {title}  {'─' * 25}")
        for i, row in enumerate(board):
            if i % BOX == 0 and i != 0:
                print("------+-------+------")
            line = ""
            for j, val in enumerate(row):
                if j % BOX == 0 and j != 0:
                    line += "| "
                line += (str(val) if val != 0 else ".") + " "
            print(line)
        print()
