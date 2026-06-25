"""
base_solver.py
Lớp trừu tượng (Abstract Class) chung cho tất cả các bộ giải trong dự án.
Mỗi module (puzzle_8, sudoku, nqueens) kế thừa lớp này.
"""
from abc import ABC, abstractmethod
import time


class BaseSolver(ABC):
    """
    Lớp cơ sở cho tất cả các bộ giải thuật toán.
    Cung cấp:
      - Giao diện thống nhất (phương thức solve bắt buộc override)
      - Bộ đếm metrics chung: nodes_explored, execution_time, memory_used
      - Tiện ích reset và ghi nhận kết quả
    """

    def __init__(self):
        self.nodes_explored: int = 0
        self.execution_time: float = 0.0
        self.memory_used: float = 0.0      # đơn vị MB, do benchmark/metrics.py cập nhật
        self.solution_length: int = 0      # số bước / số lần gán trong lời giải

    # ------------------------------------------------------------------
    # Giao diện bắt buộc – mỗi solver con phải implement
    # ------------------------------------------------------------------

    @abstractmethod
    def solve(self, initial_state):
        """
        Giải bài toán từ trạng thái ban đầu.

        Parameters
        ----------
        initial_state : phụ thuộc module
            - puzzle_8 : list[list[int]] (ma trận 3×3)
            - sudoku   : list[list[int]] (ma trận 9×9, 0 = ô trống)
            - nqueens  : int (kích thước bàn cờ N)

        Returns
        -------
        solution : phụ thuộc module
            - puzzle_8 : list[tuple] – chuỗi trạng thái từ start đến goal
            - sudoku   : list[list[int]] – ma trận đã điền đầy đủ
            - nqueens  : list[int] – vị trí hậu trên mỗi hàng
            Trả về None nếu không tìm được lời giải.
        """
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Tiện ích chung
    # ------------------------------------------------------------------

    def reset_metrics(self):
        """Đặt lại toàn bộ chỉ số đo lường trước mỗi lần chạy."""
        self.nodes_explored = 0
        self.execution_time = 0.0
        self.memory_used = 0.0
        self.solution_length = 0

    def get_metrics(self) -> dict:
        """
        Trả về dict chứa các chỉ số hiệu năng sau khi solve() hoàn tất.
        Dùng để benchmark/metrics.py thu thập kết quả.
        """
        return {
            "nodes_explored": self.nodes_explored,
            "execution_time": self.execution_time,
            "memory_used_mb": self.memory_used,
            "solution_length": self.solution_length,
        }

    def _start_timer(self) -> float:
        """Bắt đầu đếm thời gian, trả về thời điểm bắt đầu."""
        return time.perf_counter()

    def _stop_timer(self, start: float):
        """Dừng đếm thời gian và lưu vào self.execution_time."""
        self.execution_time = time.perf_counter() - start

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"nodes={self.nodes_explored}, "
            f"time={self.execution_time:.6f}s, "
            f"steps={self.solution_length})"
        )