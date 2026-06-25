from abc import ABC, abstractmethod

class BaseSolver(ABC):
    @abstractmethod
    def solve(self, initial_state, **kwargs):
        """
        Abstract method to solve a problem instance.
        """
        pass
