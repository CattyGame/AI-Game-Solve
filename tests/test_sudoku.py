import unittest
from src.sudoku.solver import SudokuSolver

class TestSudoku(unittest.TestCase):
    def test_solve_easy(self):
        solver = SudokuSolver()
        easy_board = "530070000600195000098000060800060003400803001700020006060000280000419005000080079"
        result = solver.solve(easy_board, method="Backtracking + MRV + FC")
        self.assertTrue(result["success"])
        self.assertIsNotNone(result["solution"])
        # Check that top left cell is 5
        self.assertEqual(result["solution"][0][0], 5)

if __name__ == "__main__":
    unittest.main()
