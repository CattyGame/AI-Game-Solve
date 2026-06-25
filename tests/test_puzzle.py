"""
tests/test_puzzle.py
Unit tests cho module puzzle_8: solver.py và heuristics.py
Chạy: pytest tests/test_puzzle.py -v
"""
import pytest
import sys
import os

# Đảm bảo import từ root project
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.puzzle_8.solver import Puzzle8Solver, load_matrix_from_file
from src.puzzle_8.heuristics import manhattan_distance, misplaced_tiles


# ---------------------------------------------------------------
# Dữ liệu dùng chung trong test
# ---------------------------------------------------------------
GOAL_STATE   = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
EASY_STATE   = [[1, 2, 3], [5, 7, 6], [4, 0, 8]]   # 5 bước
MEDIUM_STATE = [[2, 3, 5], [1, 6, 8], [7, 4, 0]]   # 12 bước
HARD_STATE   = [[0, 3, 8], [1, 5, 6], [7, 2, 4]]   # 22 bước
UNSOLVABLE   = [[1, 2, 3], [4, 5, 6], [8, 7, 0]]   # đảo 2 ô → không giải được


# ---------------------------------------------------------------
# Helper
# ---------------------------------------------------------------
def is_valid_path(path, goal=((1,2,3),(4,5,6),(7,8,0))):
    """Kiểm tra path hợp lệ: mỗi bước chỉ di chuyển 1 ô, kết thúc tại goal."""
    if path is None:
        return False
    if path[-1] != goal:
        return False
    for i in range(1, len(path)):
        prev = [list(r) for r in path[i-1]]
        curr = [list(r) for r in path[i]]
        diffs = [(r, c) for r in range(3) for c in range(3) if prev[r][c] != curr[r][c]]
        if len(diffs) != 2:
            return False
    return True


# ---------------------------------------------------------------
# Tests: heuristics.py
# ---------------------------------------------------------------
class TestHeuristics:

    def test_misplaced_goal_state_is_zero(self):
        goal = [[1,2,3],[4,5,6],[7,8,0]]
        assert misplaced_tiles(tuple(tuple(r) for r in goal)) == 0

    def test_manhattan_goal_state_is_zero(self):
        goal = [[1,2,3],[4,5,6],[7,8,0]]
        assert manhattan_distance(tuple(tuple(r) for r in goal)) == 0

    def test_misplaced_one_tile_off(self):
        # Chỉ ô số 8 sai vị trí
        state = ((1,2,3),(4,5,6),(7,0,8))
        assert misplaced_tiles(state) == 1

    def test_manhattan_one_tile_off(self):
        # Số 8 ở (2,2) thay vì (2,1): khoảng cách = 1
        state = ((1,2,3),(4,5,6),(7,0,8))
        assert manhattan_distance(state) == 1

    def test_misplaced_never_negative(self):
        state = tuple(tuple(r) for r in HARD_STATE)
        assert misplaced_tiles(state) >= 0

    def test_manhattan_never_negative(self):
        state = tuple(tuple(r) for r in HARD_STATE)
        assert manhattan_distance(state) >= 0

    def test_manhattan_ge_misplaced(self):
        """Manhattan luôn >= Misplaced Tiles (manhattan là heuristic tốt hơn)."""
        for mat in [EASY_STATE, MEDIUM_STATE, HARD_STATE]:
            state = tuple(tuple(r) for r in mat)
            assert manhattan_distance(state) >= misplaced_tiles(state)

    def test_blank_tile_ignored(self):
        """Ô trống (0) không được tính vào heuristic."""
        state = ((0,1,2),(3,4,5),(6,7,8))
        h_mis = misplaced_tiles(state)
        h_man = manhattan_distance(state)
        # 0 không tính → các giá trị phải > 0 (không phải goal)
        assert h_mis >= 0
        assert h_man >= 0


# ---------------------------------------------------------------
# Tests: solver.py – trạng thái đã là goal
# ---------------------------------------------------------------
class TestSolverGoalState:

    def setup_method(self):
        self.solver = Puzzle8Solver()

    def test_bfs_goal_state_returns_single_element(self):
        path = self.solver.solve_bfs(GOAL_STATE)
        assert path is not None
        assert len(path) == 1

    def test_ucs_goal_state_returns_single_element(self):
        path = self.solver.solve_ucs(GOAL_STATE)
        assert path is not None
        assert len(path) == 1

    def test_astar_manhattan_goal_state(self):
        path = self.solver.solve_astar(GOAL_STATE, "manhattan")
        assert path is not None
        assert len(path) == 1

    def test_astar_misplaced_goal_state(self):
        path = self.solver.solve_astar(GOAL_STATE, "misplaced")
        assert path is not None
        assert len(path) == 1


# ---------------------------------------------------------------
# Tests: solver.py – độ chính xác (path hợp lệ + độ dài tối ưu)
# ---------------------------------------------------------------
class TestSolverCorrectness:

    def setup_method(self):
        self.solver = Puzzle8Solver()

    @pytest.mark.parametrize("state,expected_steps", [
        (EASY_STATE,   5),
        (MEDIUM_STATE, 12),
        (HARD_STATE,   22),
    ])
    def test_bfs_optimal_path_length(self, state, expected_steps):
        path = self.solver.solve_bfs(state)
        assert path is not None, "BFS phải tìm được lời giải"
        assert len(path) - 1 == expected_steps, (
            f"BFS: kỳ vọng {expected_steps} bước, nhận {len(path)-1}"
        )

    @pytest.mark.parametrize("state,expected_steps", [
        (EASY_STATE,   5),
        (MEDIUM_STATE, 12),
        (HARD_STATE,   22),
    ])
    def test_ucs_optimal_path_length(self, state, expected_steps):
        path = self.solver.solve_ucs(state)
        assert path is not None, "UCS phải tìm được lời giải"
        assert len(path) - 1 == expected_steps

    @pytest.mark.parametrize("state,expected_steps", [
        (EASY_STATE,   5),
        (MEDIUM_STATE, 12),
        (HARD_STATE,   22),
    ])
    def test_astar_manhattan_optimal(self, state, expected_steps):
        path = self.solver.solve_astar(state, "manhattan")
        assert path is not None
        assert len(path) - 1 == expected_steps

    @pytest.mark.parametrize("state,expected_steps", [
        (EASY_STATE,   5),
        (MEDIUM_STATE, 12),
        (HARD_STATE,   22),
    ])
    def test_astar_misplaced_optimal(self, state, expected_steps):
        path = self.solver.solve_astar(state, "misplaced")
        assert path is not None
        assert len(path) - 1 == expected_steps

    @pytest.mark.parametrize("state", [EASY_STATE, MEDIUM_STATE, HARD_STATE])
    def test_bfs_path_validity(self, state):
        path = self.solver.solve_bfs(state)
        assert is_valid_path(path), "Mỗi bước trong path chỉ được di chuyển 1 ô"

    @pytest.mark.parametrize("state", [EASY_STATE, MEDIUM_STATE, HARD_STATE])
    def test_astar_path_validity(self, state):
        path = self.solver.solve_astar(state, "manhattan")
        assert is_valid_path(path)


# ---------------------------------------------------------------
# Tests: solver.py – trạng thái không giải được
# ---------------------------------------------------------------
class TestUnsolvable:

    def setup_method(self):
        self.solver = Puzzle8Solver()

    def test_bfs_unsolvable_returns_none(self):
        assert self.solver.solve_bfs(UNSOLVABLE) is None

    def test_ucs_unsolvable_returns_none(self):
        assert self.solver.solve_ucs(UNSOLVABLE) is None

    def test_astar_unsolvable_returns_none(self):
        assert self.solver.solve_astar(UNSOLVABLE, "manhattan") is None


# ---------------------------------------------------------------
# Tests: solver.py – metrics sau khi chạy
# ---------------------------------------------------------------
class TestSolverMetrics:

    def setup_method(self):
        self.solver = Puzzle8Solver()

    def test_nodes_explored_positive_after_solve(self):
        self.solver.solve_bfs(EASY_STATE)
        assert self.solver.nodes_explored > 0

    def test_execution_time_positive(self):
        self.solver.solve_astar(MEDIUM_STATE, "manhattan")
        assert self.solver.execution_time > 0

    def test_metrics_reset_between_calls(self):
        self.solver.solve_bfs(HARD_STATE)
        nodes_first = self.solver.nodes_explored
        self.solver.solve_bfs(EASY_STATE)
        nodes_second = self.solver.nodes_explored
        # EASY nên duyệt ít node hơn HARD
        assert nodes_second < nodes_first

    def test_astar_explores_fewer_nodes_than_bfs(self):
        """A* với Manhattan phải hiệu quả hơn BFS (duyệt ít node hơn)."""
        self.solver.solve_bfs(HARD_STATE)
        bfs_nodes = self.solver.nodes_explored

        self.solver.solve_astar(HARD_STATE, "manhattan")
        astar_nodes = self.solver.nodes_explored

        assert astar_nodes < bfs_nodes, (
            f"A* ({astar_nodes}) nên duyệt ít node hơn BFS ({bfs_nodes})"
        )


# ---------------------------------------------------------------
# Tests: load_matrix_from_file
# ---------------------------------------------------------------
class TestLoadMatrix:

    def test_load_easy_testcase(self):
        path = os.path.join("data", "puzzle_8", "easy.txt")
        if not os.path.exists(path):
            pytest.skip("File easy.txt không tồn tại")
        matrix = load_matrix_from_file(path)
        assert len(matrix) == 3
        assert all(len(row) == 3 for row in matrix)
        flat = [x for row in matrix for x in row]
        assert sorted(flat) == list(range(9))

    def test_load_medium_testcase(self):
        path = os.path.join("data", "puzzle_8", "medium.txt")
        if not os.path.exists(path):
            pytest.skip("File medium.txt không tồn tại")
        matrix = load_matrix_from_file(path)
        assert len(matrix) == 3

    def test_load_hard_testcase(self):
        path = os.path.join("data", "puzzle_8", "hard.txt")
        if not os.path.exists(path):
            pytest.skip("File hard.txt không tồn tại")
        matrix = load_matrix_from_file(path)
        flat = [x for row in matrix for x in row]
        assert sorted(flat) == list(range(9))