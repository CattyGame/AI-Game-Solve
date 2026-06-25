# main.py
import os
from src.puzzle_8.solver import Puzzle8Solver, load_matrix_from_file

# ---------------------------------------------------------------
# Thư mục chứa testcase mặc định
# ---------------------------------------------------------------
DATA_DIR = os.path.join("data", "puzzle_8")

TESTCASES = {
    "easy":    os.path.join(DATA_DIR, "easy.txt"),
    "medium":  os.path.join(DATA_DIR, "medium.txt"),
    "hard":    os.path.join(DATA_DIR, "hard.txt"),
    "default": os.path.join(DATA_DIR, "default.txt"),
}


def print_solution(path, algorithm_name, nodes, exec_time):
    print(f"=== KẾT QUẢ: {algorithm_name} ===")
    if path:
        print(f"  - Số bước di chuyển (Path length)    : {len(path) - 1}")
        print(f"  - Số trạng thái đã duyệt (Nodes)     : {nodes}")
        print(f"  - Thời gian thực thi                  : {exec_time:.6f} giây")
        print("  - Trạng thái đích đạt được ✓")
    else:
        print("  -> Không tìm thấy lời giải.")
    print("-" * 45)


def run_all_algorithms(solver: Puzzle8Solver, initial_matrix, label: str = ""):
    if label:
        print(f"\n{'='*45}")
        print(f"  TESTCASE: {label.upper()}")
        print(f"{'='*45}")
        for row in initial_matrix:
            print("  ", row)
        print()

    path_bfs = solver.solve_bfs(initial_matrix)
    print_solution(path_bfs, "BFS", solver.nodes_explored, solver.execution_time)

    path_ucs = solver.solve_ucs(initial_matrix)
    print_solution(path_ucs, "UCS", solver.nodes_explored, solver.execution_time)

    path_astar_mis = solver.solve_astar(initial_matrix, heuristic_type="misplaced")
    print_solution(path_astar_mis, "A* (Misplaced Tiles)", solver.nodes_explored, solver.execution_time)

    path_astar_man = solver.solve_astar(initial_matrix, heuristic_type="manhattan")
    print_solution(path_astar_man, "A* (Manhattan Distance)", solver.nodes_explored, solver.execution_time)


def main():
    solver = Puzzle8Solver()

    # Chạy lần lượt tất cả testcase
    for label, file_path in TESTCASES.items():
        if not os.path.exists(file_path):
            print(f"[WARN] Không tìm thấy file: {file_path} — bỏ qua.")
            continue
        matrix = load_matrix_from_file(file_path)
        run_all_algorithms(solver, matrix, label)


if __name__ == "__main__":
    main()