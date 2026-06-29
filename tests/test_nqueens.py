from solver import NQueensSolver

def main():
    print("="*60)
    print("--- KET QUA TEST 3 THUAT TOAN N-QUEENS (LOCAL SEARCH) ---")
    print("="*60)
    
    # Khoi tao ban co N = 8
    solver = NQueensSolver(n=8)
    
    # 1. Test Hill Climbing
    hc = solver.solve_hill_climbing()
    print(f"\n[{hc['algorithm'].upper()}]")
    print(f" - Trang thai: {'[SUCCESS] Thanh cong' if hc['success'] else '[FAILED] That bai'}")
    print(f" - Ban co:     {hc['solution']}")
    print(f" - Thoi gian:  {hc['execution_time']:.4f}s")
    print(f" - So node:    {hc['nodes_explored']}")
    
    # 2. Test Simulated Annealing
    sa = solver.solve_simulated_annealing()
    print(f"\n[{sa['algorithm'].upper()}]")
    print(f" - Trang thai: {'[SUCCESS] Thanh cong' if sa['success'] else '[FAILED] That bai'}")
    print(f" - Ban co:     {sa['solution']}")
    print(f" - Thoi gian:  {sa['execution_time']:.4f}s")
    print(f" - So node:    {sa['nodes_explored']}")
    
    # 3. Test Genetic Algorithm
    ga = solver.solve_genetic_algorithm()
    print(f"\n[{ga['algorithm'].upper()}]")
    print(f" - Trang thai: {'[SUCCESS] Thanh cong' if ga['success'] else '[FAILED] That bai'}")
    print(f" - Ban co:     {ga['solution']}")
    print(f" - Thoi gian:  {ga['execution_time']:.4f}s")
    print(f" - So node:    {ga['nodes_explored']}")

if __name__ == "__main__":
    main()
