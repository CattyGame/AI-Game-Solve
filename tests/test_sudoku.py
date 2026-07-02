"""
test_sudoku.py
Unit test cho Module Sudoku.
Chạy từ thư mục gốc repo: python -m pytest tests/test_sudoku.py -v
"""

import sys
import os
import json
import time
import unittest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from src.sudoku.solver import SudokuSolver

DATA_PATH = os.path.join(PROJECT_ROOT, "data", "sudoku", "puzzles.json")
with open(DATA_PATH, encoding="utf-8") as f:
    PUZZLES = json.load(f)["puzzles"]

PUZZLE_MAP = {p["id"]: p["board"] for p in PUZZLES}


class TestSudokuCorrectness(unittest.TestCase):

    def _solve_and_check(self, puzzle_id):
        board = PUZZLE_MAP[puzzle_id]
        solver = SudokuSolver(use_mrv=True, use_degree=False, use_fc=True)
        sol = solver.solve(board)
        m = solver.get_metrics()
        self.assertIsNotNone(sol, f"[{puzzle_id}] Không tìm được lời giải")
        self.assertTrue(solver.is_valid_solution(sol), f"[{puzzle_id}] Lời giải sai")
        print(f"\n[{puzzle_id}] nodes={m['nodes_explored']:,}  "
              f"time={m['execution_time']:.4f}s  "
              f"mem={m['memory_used_mb']:.3f}MB  steps={m['solution_length']}")
        return sol

    def test_easy(self):
        self._solve_and_check("easy_01")

    def test_medium(self):
        self._solve_and_check("medium_01")

    def test_hard(self):
        self._solve_and_check("hard_01")

    def test_expert(self):
        self._solve_and_check("expert_01")

    def test_input_not_mutated(self):
        board = [row[:] for row in PUZZLE_MAP["easy_01"]]
        original = [row[:] for row in board]
        SudokuSolver().solve(board)
        self.assertEqual(board, original)

    def test_already_filled_board(self):
        solver = SudokuSolver()
        sol = solver.solve(PUZZLE_MAP["easy_01"])
        sol2 = solver.solve(sol)
        self.assertIsNotNone(sol2)
        self.assertTrue(solver.is_valid_solution(sol2))

    def test_invalid_board_returns_none(self):
        bad = [[1,1,0,0,0,0,0,0,0]] + [[0]*9]*8
        self.assertIsNone(SudokuSolver().solve(bad))

    def test_is_valid_rejects_unsolved(self):
        self.assertFalse(SudokuSolver().is_valid_solution(PUZZLE_MAP["easy_01"]))

    def test_reset_metrics(self):
        solver = SudokuSolver()
        solver.solve(PUZZLE_MAP["easy_01"])
        self.assertGreater(solver.nodes_explored, 0)
        solver.reset_metrics()
        self.assertEqual(solver.nodes_explored, 0)
        self.assertEqual(solver.execution_time, 0.0)


class TestHeuristicComparison(unittest.TestCase):

    def test_compare_on_medium(self):
        board = PUZZLE_MAP["medium_01"]
        configs = [
            ("+ Forward Checking", dict(use_mrv=False, use_degree=False, use_fc=True)),
            ("+ MRV",              dict(use_mrv=True,  use_degree=False, use_fc=False)),
            ("+ MRV + FC",         dict(use_mrv=True,  use_degree=False, use_fc=True)),
        ]
        print("\n\n" + "═"*55)
        print("  So sánh hiệu năng – MEDIUM")
        print("═"*55)
        print(f"  {'Cấu hình':<24} {'Nodes':>8} {'Thời gian':>12}")
        print("─"*55)
        results = []
        for label, cfg in configs:
            solver = SudokuSolver(**cfg)
            sol = solver.solve(board)
            m = solver.get_metrics()
            self.assertIsNotNone(sol)
            self.assertTrue(solver.is_valid_solution(sol))
            results.append(m["nodes_explored"])
            print(f"  {label:<24} {m['nodes_explored']:>8,} {m['execution_time']:>11.6f}s")
        print("═"*55)
        # MRV+FC nên duyệt ít node hơn hoặc bằng chỉ FC
        self.assertLessEqual(results[-1], results[0])


if __name__ == "__main__":
    unittest.main(verbosity=2)
