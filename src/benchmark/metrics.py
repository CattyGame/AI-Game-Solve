import time
import tracemalloc
import sys
from typing import Dict, Any, Type
from src.core.base_solver import BaseSolver

class BenchmarkResult:
    def __init__(self, time_taken: float, peak_memory_kb: float, nodes_explored: int, success: bool, solution: Any, error: str = ""):
        self.time_taken = time_taken
        self.peak_memory_kb = peak_memory_kb
        self.nodes_explored = nodes_explored
        self.success = success
        self.solution = solution
        self.error = error

    def to_dict(self) -> Dict[str, Any]:
        return {
            "time_taken": self.time_taken,
            "peak_memory_kb": self.peak_memory_kb,
            "nodes_explored": self.nodes_explored,
            "success": self.success,
            "solution": self.solution,
            "error": self.error
        }

def benchmark_solver(solver: BaseSolver, initial_state: Any, **kwargs) -> BenchmarkResult:
    """
    Run a solver on an initial state and track execution time, peak memory usage,
    and nodes explored.
    """
    # Start tracing memory
    tracemalloc.start()
    tracemalloc.reset_peak()
    
    start_time = time.perf_counter()
    
    success = False
    solution = None
    nodes_explored = 0
    error_msg = ""
    
    try:
        # Run solver
        result = solver.solve(initial_state, **kwargs)
        
        # Parse return value
        if isinstance(result, dict):
            solution = result.get("solution")
            nodes_explored = result.get("nodes_explored", 0)
            success = result.get("success", False)
        else:
            solution = result
            success = result is not None
    except Exception as e:
        error_msg = str(e)
        success = False
    
    end_time = time.perf_counter()
    
    # Get peak memory
    _, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    time_taken = end_time - start_time
    # Convert memory bytes to Kilobytes
    peak_memory_kb = peak_memory / 1024.0
    
    return BenchmarkResult(
        time_taken=time_taken,
        peak_memory_kb=peak_memory_kb,
        nodes_explored=nodes_explored,
        success=success,
        solution=solution,
        error=error_msg
    )
