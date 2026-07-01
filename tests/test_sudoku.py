"""
test_sudoku.py
Unit test cho Module Sudoku – kiểm tra tất cả chế độ heuristic.
Chạy: python -m pytest tests/test_sudoku.py -v
   hoặc: python tests/test_sudoku.py
"""

import sys
import os
import json
import time
import unittest

# Thêm đường dẫn gốc dự án vào sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "src"))

from sudoku.solver import SudokuSolver

# ──────────────────────────────────────────────────────────
# Tải dữ liệu kiểm thử
# ──────────────────────────────────────────────────────────
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "sudoku", "puzzles.json")
with open(DATA_PATH, encoding="utf-8") as f:
    PUZZLES = json.load(f)["puzzles"]

PUZZLE_MAP = {p["id"]: p["board"] for p in PUZZLES}


# ──────────────────────────────────────────────────────────
# Test Cases
# ──────────────────────────────────────────────────────────
class TestSudokuSolverCorrectness(unittest.TestCase):
    """Kiểm tra tính đúng đắn của lời giải."""

    def _run_and_assert(self, board, label=""):
        solver = SudokuSolver(use_mrv=True, use_degree=True, use_fc=True)
        solution = solver.solve(board)
        self.assertIsNotNone(solution, f"[{label}] Không tìm được lời giải")
        self.assertTrue(
            solver.is_valid_solution(solution),
            f"[{label}] Lời giải không hợp lệ"
        )
        return solution, solver.get_stats()

    def test_easy(self):
        sol, stats = self._run_and_assert(PUZZLE_MAP["easy_01"], "easy_01")
        print(f"\n[easy_01] nodes={stats['nodes_explored']}, time={stats['time_seconds']}s")

    def test_medium(self):
        sol, stats = self._run_and_assert(PUZZLE_MAP["medium_01"], "medium_01")
        print(f"\n[medium_01] nodes={stats['nodes_explored']}, time={stats['time_seconds']}s")

    def test_hard(self):
        sol, stats = self._run_and_assert(PUZZLE_MAP["hard_01"], "hard_01")
        print(f"\n[hard_01] nodes={stats['nodes_explored']}, time={stats['time_seconds']}s")

    def test_expert(self):
        sol, stats = self._run_and_assert(PUZZLE_MAP["expert_01"], "expert_01")
        print(f"\n[expert_01] nodes={stats['nodes_explored']}, time={stats['time_seconds']}s")

    def test_no_mutation_of_input(self):
        """Input board không bị thay đổi sau khi giải."""
        board = [row[:] for row in PUZZLE_MAP["easy_01"]]
        original = [row[:] for row in board]
        solver = SudokuSolver()
        solver.solve(board)
        self.assertEqual(board, original, "Board đầu vào bị biến đổi!")

    def test_already_solved(self):
        """Board đã giải sẵn → is_valid_solution phải True."""
        solver = SudokuSolver()
        sol = solver.solve(PUZZLE_MAP["easy_01"])
        self.assertTrue(solver.is_valid_solution(sol))
        # Giải lại bảng đã giải xong
        sol2 = solver.solve(sol)
        self.assertIsNotNone(sol2)
        self.assertTrue(solver.is_valid_solution(sol2))


class TestSudokuHeuristicComparison(unittest.TestCase):
    """So sánh hiệu năng giữa các chế độ heuristic (dùng bảng hard)."""

    CONFIGS = [
        ("Backtracking thuần",    dict(use_mrv=False, use_degree=False, use_fc=False)),
        ("+ Forward Checking",    dict(use_mrv=False, use_degree=False, use_fc=True)),
        ("+ MRV",                 dict(use_mrv=True,  use_degree=False, use_fc=False)),
        ("+ MRV + FC",            dict(use_mrv=True,  use_degree=False, use_fc=True)),
        ("+ MRV + Degree + FC",   dict(use_mrv=True,  use_degree=True,  use_fc=True)),
    ]

    def test_compare_configs(self):
        board = PUZZLE_MAP["medium_01"]
        print("\n\n" + "═" * 60)
        print("  So sánh hiệu năng trên bảng MEDIUM")
        print("═" * 60)
        print(f"  {'Cấu hình':<28} {'Nodes':>10} {'Thời gian':>14}")
        print("─" * 60)

        results = []
        for label, cfg in self.CONFIGS:
            solver = SudokuSolver(**cfg)
            t0 = time.perf_counter()
            sol = solver.solve(board)
            elapsed = time.perf_counter() - t0
            self.assertIsNotNone(sol, f"[{label}] không giải được")
            self.assertTrue(solver.is_valid_solution(sol))
            stats = solver.get_stats()
            results.append((label, stats["nodes_explored"], elapsed))
            print(f"  {label:<28} {stats['nodes_explored']:>10,} {elapsed:>13.6f}s")

        print("═" * 60)

        # MRV+FC nên duyệt ít node hơn thuần backtracking
        nodes_bt  = results[0][1]
        nodes_all = results[-1][1]
        self.assertLessEqual(
            nodes_all, nodes_bt,
            "MRV+Degree+FC nên duyệt ≤ Backtracking thuần"
        )


class TestSudokuEdgeCases(unittest.TestCase):
    """Các trường hợp biên."""

    def test_invalid_board_returns_none(self):
        """Board mâu thuẫn ngay từ đầu → trả về None."""
        bad_board = [
            [1, 1, 0, 0, 0, 0, 0, 0, 0],  # 2 số 1 cùng hàng
            [0]*9, [0]*9, [0]*9, [0]*9,
            [0]*9, [0]*9, [0]*9, [0]*9,
        ]
        solver = SudokuSolver()
        result = solver.solve(bad_board)
        self.assertIsNone(result)

    def test_is_valid_solution_rejects_wrong(self):
        """Bảng chưa điền đủ → is_valid_solution False."""
        board = PUZZLE_MAP["easy_01"]
        solver = SudokuSolver()
        self.assertFalse(solver.is_valid_solution(board))

    def test_reset_clears_stats(self):
        board = PUZZLE_MAP["easy_01"]
        solver = SudokuSolver()
        solver.solve(board)
        self.assertGreater(solver.nodes_explored, 0)
        solver.reset()
        self.assertEqual(solver.nodes_explored, 0)
        self.assertFalse(solver.solved)


# ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    unittest.main(verbosity=2)
