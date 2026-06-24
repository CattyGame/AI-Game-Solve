import unittest
from src.nqueens.solver import NQueensSolver

class TestNQueens(unittest.TestCase):
    def test_solve_hill_climbing(self):
        solver = NQueensSolver()
        # Solve 4-Queens
        result = solver.solve(4, method="Hill Climbing")
        self.assertTrue(result["success"])
        self.assertEqual(solver.get_conflicts(result["solution"]), 0)

if __name__ == "__main__":
    unittest.main()
