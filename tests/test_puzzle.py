import unittest
from src.puzzle_8.solver import Puzzle8Solver

class TestPuzzle(unittest.TestCase):
    def test_solve_easy(self):
        solver = Puzzle8Solver()
        easy_board = [1, 2, 3, 4, 0, 5, 7, 8, 6]
        result = solver.solve(easy_board, method="A*", heuristic_name="Manhattan")
        self.assertTrue(result["success"])
        self.assertEqual(result["solution"][-1], (1, 2, 3, 4, 5, 6, 7, 8, 0))

if __name__ == "__main__":
    unittest.main()
