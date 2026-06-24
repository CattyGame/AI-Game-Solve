import unittest
import time
from src.core.base_solver import BaseSolver
from src.benchmark.metrics import benchmark_solver

class MockSolver(BaseSolver):
    def __init__(self, sleep_duration=0.1, memory_allocation_size=100000, nodes=42):
        self.sleep_duration = sleep_duration
        self.memory_allocation_size = memory_allocation_size
        self.nodes = nodes

    def solve(self, initial_state, **kwargs):
        # Simulate time delay
        time.sleep(self.sleep_duration)
        # Simulate memory allocation
        self.dummy_data = [0] * self.memory_allocation_size
        return {
            "solution": "mock_solution",
            "nodes_explored": self.nodes,
            "success": True
        }

class TestBenchmark(unittest.TestCase):
    def test_benchmark_metrics(self):
        solver = MockSolver(sleep_duration=0.05, memory_allocation_size=50000, nodes=100)
        result = benchmark_solver(solver, None)
        
        self.assertTrue(result.success)
        self.assertEqual(result.nodes_explored, 100)
        self.assertEqual(result.solution, "mock_solution")
        self.assertGreater(result.time_taken, 0.04) # Should be at least ~0.05 seconds
        self.assertGreater(result.peak_memory_kb, 10) # Should be some KB allocated

if __name__ == "__main__":
    unittest.main()
