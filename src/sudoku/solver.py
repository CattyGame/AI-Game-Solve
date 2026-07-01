"""
solver.py  –  MODULE 1: BỘ GIẢI SUDOKU
============================================================
Hiện thực Backtracking (Duyệt lui) kết hợp các kỹ thuật CSP tối ưu:
  • MRV  (Minimum Remaining Values)  – chọn ô có ít giá trị hợp lệ nhất
  • Degree Heuristic                 – tiebreak: ô ràng buộc nhiều ô trống nhất
  • Forward Checking                 – sau mỗi gán giá trị, cập nhật domain
                                       của các ô liên quan và phát hiện sớm
                                       dead-end (domain rỗng).

Giao diện công khai
-------------------
  SudokuSolver(use_mrv, use_degree, use_fc)
      .solve(board)  ->  list[list[int]] | None
      .is_valid_solution(board)  ->  bool
      .get_stats()   ->  dict

Board format: list[list[int]], 9×9, giá trị 0 = ô trống.
"""

import copy
import time
from typing import Optional

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from core.base_solver import BaseSolver

# ──────────────────────────────────────────────────────────
# Hằng số
# ──────────────────────────────────────────────────────────
SIZE   = 9          # kích thước bảng
BOX    = 3          # kích thước ô vuông con
DIGITS = set(range(1, 10))


# ══════════════════════════════════════════════════════════
# Lớp chính
# ══════════════════════════════════════════════════════════
class SudokuSolver(BaseSolver):
    """
    Bộ giải Sudoku với Backtracking + CSP Heuristics.

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
        self.time_taken: float = 0.0

    # ──────────────────────────────────────────────────────
    # Giao diện công khai
    # ──────────────────────────────────────────────────────
    def solve(self, board: list[list[int]]) -> Optional[list[list[int]]]:
        """
        Giải Sudoku.

        Parameters
        ----------
        board : 9×9 list[list[int]], ô trống = 0

        Returns
        -------
        Bảng đã giải (9×9 list[list[int]]) hoặc None nếu vô nghiệm.
        """
        self.reset()

        # Sao chép để không làm thay đổi input gốc
        grid = [row[:] for row in board]

        # Khởi tạo domain cho từng ô
        domains = self._init_domains(grid)
        if domains is None:
            return None          # board đầu vào mâu thuẫn ngay

        start = time.perf_counter()
        result = self._backtrack(grid, domains)
        self.time_taken = time.perf_counter() - start

        if result:
            self.solved   = True
            self.solution = result
            return copy.deepcopy(result)
        return None

    def is_valid_solution(self, board: list[list[int]]) -> bool:
        """Kiểm tra bảng đã điền đầy đủ và hợp lệ."""
        if not board or len(board) != SIZE:
            return False
        for i in range(SIZE):
            if len(board[i]) != SIZE:
                return False
            # Kiểm tra hàng
            if set(board[i]) != DIGITS:
                return False
            # Kiểm tra cột
            col = {board[r][i] for r in range(SIZE)}
            if col != DIGITS:
                return False
        # Kiểm tra 9 ô vuông con 3×3
        for br in range(BOX):
            for bc in range(BOX):
                box_vals = {
                    board[br * BOX + r][bc * BOX + c]
                    for r in range(BOX) for c in range(BOX)
                }
                if box_vals != DIGITS:
                    return False
        return True

    def get_stats(self) -> dict:
        base = super().get_stats()
        base.update({
            "time_seconds": round(self.time_taken, 6),
            "use_mrv":      self.use_mrv,
            "use_degree":   self.use_degree,
            "use_fc":       self.use_fc,
        })
        return base

    # ──────────────────────────────────────────────────────
    # Khởi tạo domain
    # ──────────────────────────────────────────────────────
    def _init_domains(
        self, grid: list[list[int]]
    ) -> Optional[dict[tuple, set[int]]]:
        """
        Xây dựng domains[ô] = tập giá trị hợp lệ cho ô đó.
        Ô đã điền sẵn có domain = {giá trị}.
        Trả về None nếu phát hiện mâu thuẫn ngay từ đầu.
        """
        domains: dict[tuple, set[int]] = {}
        for r in range(SIZE):
            for c in range(SIZE):
                if grid[r][c] != 0:
                    domains[(r, c)] = {grid[r][c]}
                else:
                    used = self._get_used_values(grid, r, c)
                    remaining = DIGITS - used
                    if not remaining:
                        return None   # mâu thuẫn
                    domains[(r, c)] = remaining
        return domains

    # ──────────────────────────────────────────────────────
    # Backtracking chính
    # ──────────────────────────────────────────────────────
    def _backtrack(
        self,
        grid: list[list[int]],
        domains: dict[tuple, set[int]],
    ) -> Optional[list[list[int]]]:
        """Đệ quy Backtracking. Trả về bảng giải hoặc None."""

        # Tìm ô trống tiếp theo cần điền
        cell = self._select_unassigned(grid, domains)
        if cell is None:
            # Không còn ô trống → đã giải xong
            return grid

        r, c = cell
        for value in sorted(domains[(r, c)]):   # thứ tự tăng dần để tái hiện được
            self.nodes_explored += 1

            if self._is_consistent(grid, r, c, value):
                # Gán thử
                grid[r][c] = value

                if self.use_fc:
                    # Forward Checking: cập nhật domains & phát hiện dead-end
                    new_domains, ok = self._forward_check(domains, r, c, value)
                    if ok:
                        result = self._backtrack(grid, new_domains)
                        if result:
                            return result
                else:
                    result = self._backtrack(grid, domains)
                    if result:
                        return result

                # Backtrack
                grid[r][c] = 0

        return None   # không tìm được giá trị nào phù hợp

    # ──────────────────────────────────────────────────────
    # Chọn biến (Variable Selection)
    # ──────────────────────────────────────────────────────
    def _select_unassigned(
        self,
        grid: list[list[int]],
        domains: dict[tuple, set[int]],
    ) -> Optional[tuple[int, int]]:
        """
        Chọn ô trống tiếp theo:
          • Nếu use_mrv=False  : lấy ô trống đầu tiên (left-to-right, top-to-bottom)
          • Nếu use_mrv=True   : MRV – ô có ít giá trị khả thi nhất
          • Nếu use_degree=True: tiebreak bằng Degree Heuristic
        """
        empty_cells = [
            (r, c)
            for r in range(SIZE) for c in range(SIZE)
            if grid[r][c] == 0
        ]
        if not empty_cells:
            return None

        if not self.use_mrv:
            return empty_cells[0]

        # MRV
        def mrv_key(cell):
            r, c = cell
            domain_size  = len(domains[(r, c)])
            degree_break = 0
            if self.use_degree:
                # Degree: số ô trống mà ô này ràng buộc (càng nhiều càng ưu tiên)
                # → dùng âm để sort tăng dần vẫn chọn đúng
                degree_break = -self._count_empty_peers(grid, r, c)
            return (domain_size, degree_break)

        return min(empty_cells, key=mrv_key)

    def _count_empty_peers(
        self, grid: list[list[int]], row: int, col: int
    ) -> int:
        """Đếm số ô trống trong cùng hàng, cột, và box với (row, col)."""
        count = 0
        peers = self._get_peers(row, col)
        for r, c in peers:
            if grid[r][c] == 0:
                count += 1
        return count

    # ──────────────────────────────────────────────────────
    # Kiểm tra ràng buộc (Constraint Check)
    # ──────────────────────────────────────────────────────
    def _is_consistent(
        self, grid: list[list[int]], row: int, col: int, value: int
    ) -> bool:
        """Trả về True nếu gán value vào (row, col) không vi phạm ràng buộc."""
        return value not in self._get_used_values(grid, row, col)

    def _get_used_values(
        self, grid: list[list[int]], row: int, col: int
    ) -> set[int]:
        """Tập giá trị đã xuất hiện trong cùng hàng, cột, box với (row, col)."""
        used: set[int] = set()
        # Hàng
        used.update(v for v in grid[row] if v != 0)
        # Cột
        used.update(grid[r][col] for r in range(SIZE) if grid[r][col] != 0)
        # Box 3×3
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
    def _forward_check(
        self,
        domains: dict[tuple, set[int]],
        row: int,
        col: int,
        value: int,
    ) -> tuple[dict[tuple, set[int]], bool]:
        """
        Sau khi gán value vào (row, col):
          1. Tạo bản sao domains mới (tránh ảnh hưởng khi backtrack).
          2. Loại value khỏi domain của các ô liên quan (peers).
          3. Nếu domain nào đó rỗng → trả về (_, False) (dead-end).

        Returns
        -------
        (new_domains, ok)
        """
        # Shallow copy dict, deep copy mỗi set
        new_domains = {k: set(v) for k, v in domains.items()}
        # Ô đã gán thì domain = {value}
        new_domains[(row, col)] = {value}

        for r, c in self._get_peers(row, col):
            if (r, c) in new_domains:
                new_domains[(r, c)].discard(value)
                if not new_domains[(r, c)]:
                    return new_domains, False   # dead-end

        return new_domains, True

    # ──────────────────────────────────────────────────────
    # Tiện ích
    # ──────────────────────────────────────────────────────
    @staticmethod
    def _get_peers(row: int, col: int) -> list[tuple[int, int]]:
        """Trả về tất cả ô cùng hàng, cột, box với (row, col), loại bản thân."""
        peers: set[tuple[int, int]] = set()
        # Hàng
        peers.update((row, c) for c in range(SIZE) if c != col)
        # Cột
        peers.update((r, col) for r in range(SIZE) if r != row)
        # Box
        br, bc = (row // BOX) * BOX, (col // BOX) * BOX
        peers.update(
            (br + dr, bc + dc)
            for dr in range(BOX) for dc in range(BOX)
            if (br + dr, bc + dc) != (row, col)
        )
        return list(peers)

    # ──────────────────────────────────────────────────────
    # In bảng (debug / demo)
    # ──────────────────────────────────────────────────────
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
