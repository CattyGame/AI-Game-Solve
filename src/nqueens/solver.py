import random
import time
import math

try:
    from core.base_solver import BaseSolver
except ImportError:
    class BaseSolver:
        pass

class NQueensSolver(BaseSolver):
    """
    Bo giai bai toan N-Queens su dung nhom thuat toan Tim kiem cuc bo (Local Search).
    Ke thua tu BaseSolver de dong bo kien truc he thong.
    """
    
    def __init__(self, n=8):
        super().__init__()
        self.n = n

    def get_cost(self, state):
        """
        Ham Heuristic: Dem tong so cap quan hau dang tan cong nhau.
        Muc tieu toi uu la Cost = 0.
        """
        conflicts = 0
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if state[i] == state[j] or abs(state[i] - state[j]) == j - i:
                    conflicts += 1
        return conflicts

    def _format_result(self, algo_name, solution, start_time, nodes, success):
        """
        Chuan hoa du lieu dau ra (Metrics) dong nhat cho he thong Benchmark va UI.
        """
        return {
            "algorithm": algo_name,
            "solution": solution,
            "execution_time": time.time() - start_time,
            "nodes_explored": nodes,
            "success": success
        }

    def solve_hill_climbing(self, max_restarts=100, max_iters=200, max_sideways=10):
        """
        Thuat toan Hill Climbing ket hop Random Restart va Sideways Move de tranh ket Local Optimum.
        """
        start_time = time.time()
        nodes_explored = 0

        for _ in range(max_restarts):
            curr_state = [random.randint(0, self.n - 1) for _ in range(self.n)]
            curr_cost = self.get_cost(curr_state)
            sideways_moves = 0

            for _ in range(max_iters):
                nodes_explored += 1
                if curr_cost == 0:
                    return self._format_result("Hill Climbing", curr_state, start_time, nodes_explored, True)

                neighbors = []
                for col in range(self.n):
                    for row in range(self.n):
                        if row != curr_state[col]:
                            neighbor = list(curr_state)
                            neighbor[col] = row
                            neighbors.append((neighbor, self.get_cost(neighbor)))

                neighbors.sort(key=lambda x: x[1])
                best_neighbor, best_cost = neighbors[0]

                if best_cost < curr_cost:
                    curr_state, curr_cost = best_neighbor, best_cost
                    sideways_moves = 0
                elif best_cost == curr_cost and sideways_moves < max_sideways:
                    curr_state, curr_cost = best_neighbor, best_cost
                    sideways_moves += 1
                else:
                    break

        return self._format_result("Hill Climbing", None, start_time, nodes_explored, False)

    def solve_simulated_annealing(self, max_iters=10000, initial_temp=100.0, alpha=0.98):
        """
        Thuat toan Simulated Annealing su dung xac suat Boltzmann de thinh thoang nhan cac nuoc di xau.
        """
        start_time = time.time()
        nodes_explored = 0
        curr_state = [random.randint(0, self.n - 1) for _ in range(self.n)]
        curr_cost = self.get_cost(curr_state)
        temp = initial_temp

        for _ in range(max_iters):
            nodes_explored += 1
            if curr_cost == 0:
                return self._format_result("Simulated Annealing", curr_state, start_time, nodes_explored, True)
            if temp < 0.001: 
                break

            col = random.randint(0, self.n - 1)
            row = random.randint(0, self.n - 1)
            while row == curr_state[col]: 
                row = random.randint(0, self.n - 1)

            neighbor = list(curr_state)
            neighbor[col] = row
            neighbor_cost = self.get_cost(neighbor)
            delta = neighbor_cost - curr_cost
            
            if delta < 0 or random.random() < math.exp(-delta / temp):
                curr_state, curr_cost = neighbor, neighbor_cost
            temp *= alpha

        success = (curr_cost == 0)
        return self._format_result("Simulated Annealing", curr_state if success else None, start_time, nodes_explored, success)

    def solve_genetic_algorithm(self, pop_size=100, max_generations=1000, mutation_rate=0.15, elitism_count=2):
        """
        Thuat toan Genetic Algorithm tich hop co che Elitism de bao ton cac ca the xuat sac nhat.
        """
        start_time = time.time()
        nodes_explored = 0
        max_conflicts = self.n * (self.n - 1) // 2
        get_fitness = lambda state: max_conflicts - self.get_cost(state)

        population = [[random.randint(0, self.n - 1) for _ in range(self.n)] for _ in range(pop_size)]

        for _ in range(max_generations):
            nodes_explored += pop_size
            population.sort(key=lambda x: get_fitness(x), reverse=True)

            if self.get_cost(population[0]) == 0:
                return self._format_result("Genetic Algorithm", population[0], start_time, nodes_explored, True)

            new_population = population[:elitism_count]
            fitness_scores = [get_fitness(ind) for ind in population]
            total_fitness = sum(fitness_scores)
            
            if total_fitness == 0:
                probs = [1 / pop_size] * pop_size
            else:
                probs = [f / total_fitness for f in fitness_scores]

            while len(new_population) < pop_size:
                p1 = random.choices(population, weights=probs, k=1)[0]
                p2 = random.choices(population, weights=probs, k=1)[0]
                cp = random.randint(1, self.n - 1)
                c1, c2 = p1[:cp] + p2[cp:], p2[:cp] + p1[cp:]
                
                if random.random() < mutation_rate: 
                    c1[random.randint(0, self.n - 1)] = random.randint(0, self.n - 1)
                if random.random() < mutation_rate: 
                    c2[random.randint(0, self.n - 1)] = random.randint(0, self.n - 1)
                new_population.extend([c1, c2])

            population = new_population[:pop_size]

        return self._format_result("Genetic Algorithm", None, start_time, nodes_explored, False)
