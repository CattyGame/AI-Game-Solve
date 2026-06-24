from abc import ABC, abstractmethod

class BaseSolver(ABC):
    @abstractmethod
    def solve(self, initial_state, **kwargs):
        """
        Solve the problem starting from initial_state.
        
        Parameters:
        - initial_state: The initial board or configuration.
        - kwargs: Additional search parameters (e.g. heuristics, max steps).
        
        Returns:
        A dictionary containing:
        - "solution": The final state, path of states, or board layout.
        - "nodes_explored": Integer, number of states/nodes expanded during search.
        - "success": Boolean, whether a solution was found.
        """
        pass
