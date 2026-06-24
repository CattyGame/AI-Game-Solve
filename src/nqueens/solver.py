import random
import math
from src.core.base_solver import BaseSolver

class NQueensSolver(BaseSolver):
    def __init__(self):
        pass

    def get_conflicts(self, state):
        n = len(state)
        conflicts = 0
        for i in range(n):
            for j in range(i + 1, n):
                if state[i] == state[j]: # Same row
                    conflicts += 1
                elif abs(state[i] - state[j]) == j - i: # Same diagonal
                    conflicts += 1
        return conflicts

    def solve(self, initial_state, method="Hill Climbing", max_steps=2000, **kwargs):
        """
        Solve N-Queens.
        initial_state: int (representing N) or list of N integers.
        method: "Hill Climbing", "Simulated Annealing", "Genetic Algorithm"
        """
        if isinstance(initial_state, int):
            n = initial_state
            # Create a random initial state
            state = [random.randint(0, n - 1) for _ in range(n)]
        else:
            state = list(initial_state)
            n = len(state)

        if method == "Hill Climbing":
            return self._solve_hill_climbing(state, n, max_steps)
        elif method == "Simulated Annealing":
            return self._solve_simulated_annealing(state, n, max_steps)
        elif method == "Genetic Algorithm":
            pop_size = kwargs.get("pop_size", 100)
            mutation_rate = kwargs.get("mutation_rate", 0.15)
            max_generations = kwargs.get("max_generations", 500)
            return self._solve_genetic_algorithm(n, pop_size, mutation_rate, max_generations)
        else:
            raise ValueError(f"Unknown method: {method}")

    def _solve_hill_climbing(self, start, n, max_steps):
        curr = list(start)
        curr_conflicts = self.get_conflicts(curr)
        nodes_explored = 1
        
        # Max restarts to avoid getting stuck forever
        max_restarts = 50
        restart_count = 0
        
        for step in range(max_steps):
            if curr_conflicts == 0:
                return {"solution": curr, "nodes_explored": nodes_explored, "success": True}
                
            # Find best neighbor
            neighbors = []
            min_conflicts = curr_conflicts
            
            for col in range(n):
                original_row = curr[col]
                for row in range(n):
                    if row != original_row:
                        curr[col] = row
                        nodes_explored += 1
                        conf = self.get_conflicts(curr)
                        if conf < min_conflicts:
                            min_conflicts = conf
                            neighbors = [(col, row)]
                        elif conf == min_conflicts and conf < curr_conflicts:
                            neighbors.append((col, row))
                curr[col] = original_row # Restore
            
            if not neighbors:
                # Local minimum hit
                if restart_count < max_restarts:
                    # Random restart
                    curr = [random.randint(0, n - 1) for _ in range(n)]
                    curr_conflicts = self.get_conflicts(curr)
                    restart_count += 1
                    continue
                else:
                    break
            else:
                # Make the move to a randomly chosen best neighbor
                col, row = random.choice(neighbors)
                curr[col] = row
                curr_conflicts = min_conflicts
                
        return {"solution": curr, "nodes_explored": nodes_explored, "success": curr_conflicts == 0}

    def _solve_simulated_annealing(self, start, n, max_steps):
        curr = list(start)
        curr_conflicts = self.get_conflicts(curr)
        nodes_explored = 1
        
        T = 100.0
        cooling_rate = 0.95
        
        for step in range(max_steps):
            if curr_conflicts == 0:
                return {"solution": curr, "nodes_explored": nodes_explored, "success": True}
                
            T *= cooling_rate
            if T < 0.01:
                if curr_conflicts == 0:
                    break
                else:
                    # Reheat or restart
                    curr = [random.randint(0, n - 1) for _ in range(n)]
                    curr_conflicts = self.get_conflicts(curr)
                    T = 100.0
                    continue
            
            # Select random neighbor (move one random queen to a random row)
            col = random.randint(0, n - 1)
            row = random.randint(0, n - 1)
            while row == curr[col]:
                row = random.randint(0, n - 1)
                
            old_row = curr[col]
            curr[col] = row
            nodes_explored += 1
            new_conflicts = self.get_conflicts(curr)
            
            dE = new_conflicts - curr_conflicts
            
            if dE < 0 or random.random() < math.exp(-dE / T):
                # Accept
                curr_conflicts = new_conflicts
            else:
                # Reject
                curr[col] = old_row
                
        return {"solution": curr, "nodes_explored": nodes_explored, "success": curr_conflicts == 0}

    def _solve_genetic_algorithm(self, n, pop_size, mutation_rate, max_generations):
        # Create initial population
        population = [[random.randint(0, n - 1) for _ in range(n)] for _ in range(pop_size)]
        max_fit = n * (n - 1) // 2
        nodes_explored = pop_size
        
        def fitness(state):
            return max_fit - self.get_conflicts(state)
            
        for gen in range(max_generations):
            # Evaluate fitness
            fit_scores = [fitness(ind) for ind in population]
            
            # Check for solution
            for idx, score in enumerate(fit_scores):
                if score == max_fit:
                    return {"solution": population[idx], "nodes_explored": nodes_explored, "success": True}
            
            # Selection probability
            total_fit = sum(fit_scores)
            if total_fit == 0:
                probs = [1 / pop_size] * pop_size
            else:
                probs = [f / total_fit for f in fit_scores]
                
            # Selection & Reproduce
            new_population = []
            for _ in range(pop_size // 2):
                # Roulette selection
                p1 = random.choices(population, weights=probs, k=1)[0]
                p2 = random.choices(population, weights=probs, k=1)[0]
                
                # Single point crossover
                crossover_pt = random.randint(1, n - 2) if n > 2 else 1
                child1 = p1[:crossover_pt] + p2[crossover_pt:]
                child2 = p2[:crossover_pt] + p1[crossover_pt:]
                
                # Mutation
                if random.random() < mutation_rate:
                    child1[random.randint(0, n - 1)] = random.randint(0, n - 1)
                if random.random() < mutation_rate:
                    child2[random.randint(0, n - 1)] = random.randint(0, n - 1)
                    
                new_population.extend([child1, child2])
                nodes_explored += 2
                
            population = new_population
            
        # Check final population
        fit_scores = [fitness(ind) for ind in population]
        for idx, score in enumerate(fit_scores):
            if score == max_fit:
                return {"solution": population[idx], "nodes_explored": nodes_explored, "success": True}
                
        # Return best so far
        best_idx = fit_scores.index(max(fit_scores))
        return {"solution": population[best_idx], "nodes_explored": nodes_explored, "success": False}
