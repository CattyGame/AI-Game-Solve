from abc import ABC, abstractmethod

class BaseSolver(ABC):
    @abstractmethod
    def solve(self, initial_state):
        """
        Solve the problem starting from initial_state.
        Should return the solution path/result and any execution metadata/metrics.
        """
        pass
