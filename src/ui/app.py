import sys
import os
# Add project root to python path to avoid ModuleNotFoundError when running via Streamlit
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import streamlit as st
import json
import pandas as pd
import time

# Solvers and benchmark utilities
from src.sudoku.solver import SudokuSolver
from src.puzzle_8.solver import Puzzle8Solver
from src.nqueens.solver import NQueensSolver
from src.benchmark.metrics import benchmark_solver
from src.ui.components.board_draw import draw_sudoku_board, draw_puzzle8_board, draw_nqueens_board

st.set_page_config(
    page_title="AI Game Solver Dashboard",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load sample data helper
def load_samples(filepath, fallback):
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return fallback

# Fallback presets if JSON files are missing
SUDOKU_FALLBACK = {
    "easy": {
        "board": "530070000600195000098000060800060003400803001700020006060000280000419005000080079",
        "description": "Easy board with many clues."
    },
    "medium": {
        "board": "000600400700003600000091080000000000050180003000306045040200060903000000020000100",
        "description": "Medium board requiring basic search."
    },
    "hard": {
        "board": "800000000003600000070090200050007000000045700000100030001000068008500010090000400",
        "description": "Hard board requiring deep backtracking search."
    }
}

PUZZLE8_FALLBACK = {
    "easy": {
        "board": [1, 2, 3, 4, 0, 5, 7, 8, 6],
        "description": "Easy puzzle needing only 1 move to solve."
    },
    "medium": {
        "board": [1, 3, 5, 4, 2, 6, 7, 8, 0],
        "description": "Medium difficulty puzzle."
    },
    "hard": {
        "board": [8, 6, 7, 2, 5, 4, 3, 0, 1],
        "description": "Hard puzzle requiring many moves."
    }
}

NQUEENS_FALLBACK = {
    "easy": {"n": 4, "description": "4-Queens problem on a 4x4 board."},
    "medium": {"n": 8, "description": "8-Queens problem on a standard 8x8 board."},
    "hard": {"n": 12, "description": "12-Queens problem on a 12x12 board."}
}

# Load actual presets
sudoku_samples = load_samples("data/sudoku/samples.json", SUDOKU_FALLBACK)
puzzle8_samples = load_samples("data/puzzle_8/samples.json", PUZZLE8_FALLBACK)
nqueens_samples = load_samples("data/nqueens/samples.json", NQUEENS_FALLBACK)

# Header Section
st.markdown("""
<div style="background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%); padding: 25px 35px; border-radius: 15px; margin-bottom: 25px; border: 1px solid #334155;">
    <h1 style="color: #38BDF8; font-family: 'Outfit', sans-serif; margin: 0; font-weight: 800; font-size: 2.3rem;">👑 AI Game Solver & Benchmark Suite</h1>
    <p style="color: #94A3B8; font-family: 'Inter', sans-serif; margin-top: 8px; font-size: 1.05rem; margin-bottom: 0;">
        Giải quyết và đo đạc hiệu năng định lượng các thuật toán (Duyệt lui Heuristic, Tìm kiếm mù, Tìm kiếm cục bộ) trên các bài toán game logic.
    </p>
</div>
""", unsafe_allow_html=True)

# Main Navigation Tabs
tab_sudoku, tab_puzzle, tab_nqueens, tab_benchmark = st.tabs([
    "🧩 Sudoku Solver",
    "🔢 8-Puzzle Solver",
    "👑 N-Queens Solver",
    "📈 Comparative Benchmarks"
])

# ----------------- SUDOKU TAB -----------------
with tab_sudoku:
    st.header("Sudoku Solver")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Settings")
        preset = st.selectbox("Select Preset Puzzle", list(sudoku_samples.keys()), key="sudoku_preset")
        st.info(sudoku_samples[preset]["description"])
        
        algorithm = st.selectbox("Algorithm", [
            "Backtracking + MRV + FC",
            "Backtracking + MRV",
            "Basic Backtracking"
        ], key="sudoku_algo")
        
        board_str = sudoku_samples[preset]["board"]
        
        # Display starting board
        st.subheader("Original Board")
        starting_board = [[int(board_str[i*9 + j]) for j in range(9)] for i in range(9)]
        st.markdown(draw_sudoku_board(starting_board, starting_board), unsafe_allow_html=True)

    with col2:
        st.subheader("Solver Output")
        if st.button("Solve Sudoku", type="primary"):
            solver = SudokuSolver()
            
            with st.spinner("Solving..."):
                res = benchmark_solver(solver, board_str, method=algorithm)
                
            if res.success:
                st.success("Sudoku Solved Successfully!")
                
                # Metrics Row
                m1, m2, m3 = st.columns(3)
                m1.metric("Execution Time", f"{res.time_taken:.6f} s")
                m2.metric("Peak Memory", f"{res.peak_memory_kb:.2f} KB")
                m3.metric("Nodes Explored", f"{res.nodes_explored}")
                
                st.markdown(draw_sudoku_board(res.solution, starting_board), unsafe_allow_html=True)
            else:
                st.error(f"Failed to solve Sudoku: {res.error if res.error else 'Unsolvable configuration'}")


# ----------------- 8-PUZZLE TAB -----------------
with tab_puzzle:
    st.header("8-Puzzle Solver")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Settings")
        preset = st.selectbox("Select Preset Puzzle", list(puzzle8_samples.keys()), key="puzzle_preset")
        st.info(puzzle8_samples[preset]["description"])
        
        algorithm = st.selectbox("Algorithm", ["A*", "BFS", "UCS"], key="puzzle_algo")
        
        heuristic = "Manhattan"
        if algorithm == "A*":
            heuristic = st.selectbox("Heuristic Function", [
                "Manhattan", 
                "Misplaced Tiles", 
                "Linear Conflict"
            ], key="puzzle_heuristic")
            
        initial_board = puzzle8_samples[preset]["board"]
        
        st.subheader("Initial Board")
        st.markdown(draw_puzzle8_board(initial_board), unsafe_allow_html=True)

    with col2:
        st.subheader("Solver Output")
        if st.button("Solve 8-Puzzle", type="primary"):
            solver = Puzzle8Solver()
            
            with st.spinner("Solving..."):
                res = benchmark_solver(solver, initial_board, method=algorithm, heuristic_name=heuristic)
                
            if res.success:
                st.success(f"Puzzle Solved! Steps: {len(res.solution) - 1}")
                
                # Metrics Row
                m1, m2, m3 = st.columns(3)
                m1.metric("Execution Time", f"{res.time_taken:.6f} s")
                m2.metric("Peak Memory", f"{res.peak_memory_kb:.2f} KB")
                m3.metric("Nodes Explored", f"{res.nodes_explored}")
                
                # Save solution path in session state to play it back
                st.session_state["puzzle_solution"] = res.solution
                st.session_state["puzzle_step"] = 0
            else:
                st.error(f"Failed to solve puzzle: {res.error if res.error else 'Unsolvable or search limits exceeded'}")
                
        # Interactive Step Playback
        if "puzzle_solution" in st.session_state and st.session_state["puzzle_solution"]:
            solution = st.session_state["puzzle_solution"]
            st.write("---")
            st.subheader("Step-by-step Solution Playback")
            
            step = st.slider("Select Step", 0, len(solution) - 1, key="step_slider")
            
            st.markdown(draw_puzzle8_board(solution[step]), unsafe_allow_html=True)
            st.write(f"Step {step} of {len(solution) - 1}")


# ----------------- N-QUEENS TAB -----------------
with tab_nqueens:
    st.header("N-Queens Solver")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Settings")
        n_size = st.slider("Board Size (N)", 4, 16, 8, key="n_queens_slider")
        
        algorithm = st.selectbox("Algorithm", [
            "Hill Climbing", 
            "Simulated Annealing", 
            "Genetic Algorithm"
        ], key="nqueens_algo")
        
        st.markdown(f"Solving for **{n_size} Queens** on a **{n_size}x{n_size}** Board.")

    with col2:
        st.subheader("Solver Output")
        if st.button("Solve N-Queens", type="primary"):
            solver = NQueensSolver()
            
            with st.spinner("Searching for solution..."):
                res = benchmark_solver(solver, n_size, method=algorithm)
                
            if res.success:
                st.success("Solution Found (0 conflicts)!")
                
                # Metrics Row
                m1, m2, m3 = st.columns(3)
                m1.metric("Execution Time", f"{res.time_taken:.6f} s")
                m2.metric("Peak Memory", f"{res.peak_memory_kb:.2f} KB")
                m3.metric("Nodes Explored", f"{res.nodes_explored}")
                
                st.markdown(draw_nqueens_board(res.solution), unsafe_allow_html=True)
            else:
                st.warning("Failed to find a perfect conflict-free solution within limits.")
                if res.solution:
                    st.write(f"Best solution found (Conflicts: {solver.get_conflicts(res.solution)}):")
                    st.markdown(draw_nqueens_board(res.solution), unsafe_allow_html=True)


# ----------------- COMPARATIVE BENCHMARKS TAB -----------------
with tab_benchmark:
    st.header("Algorithm Performance Comparison Suite")
    st.write("Run and compare all algorithm implementations side-by-side to study space and time complexities.")
    
    game_type = st.selectbox("Select Game to Compare", ["Sudoku", "8-Puzzle", "N-Queens"])
    
    if game_type == "Sudoku":
        selected_case = st.selectbox("Select Case", list(sudoku_samples.keys()), key="bench_sudoku")
        input_data = sudoku_samples[selected_case]["board"]
        algos = {
            "Basic Backtracking": {"method": "Basic Backtracking"},
            "Backtracking + MRV": {"method": "Backtracking + MRV"},
            "Backtracking + MRV + FC": {"method": "Backtracking + MRV + FC"}
        }
        solver_instance = SudokuSolver()
        
    elif game_type == "8-Puzzle":
        selected_case = st.selectbox("Select Case", list(puzzle8_samples.keys()), key="bench_puzzle")
        input_data = puzzle8_samples[selected_case]["board"]
        algos = {
            "BFS": {"method": "BFS"},
            "UCS": {"method": "UCS"},
            "A* (Misplaced)": {"method": "A*", "heuristic_name": "Misplaced Tiles"},
            "A* (Manhattan)": {"method": "A*", "heuristic_name": "Manhattan"},
            "A* (Linear Conflict)": {"method": "A*", "heuristic_name": "Linear Conflict"}
        }
        solver_instance = Puzzle8Solver()
        
    else: # N-Queens
        selected_case = st.slider("Select Board Size (N)", 4, 12, 8, key="bench_nqueens")
        input_data = selected_case
        algos = {
            "Hill Climbing": {"method": "Hill Climbing"},
            "Simulated Annealing": {"method": "Simulated Annealing"},
            "Genetic Algorithm": {"method": "Genetic Algorithm"}
        }
        solver_instance = NQueensSolver()
        
    if st.button("Run Comprehensive Benchmark Comparison", type="primary"):
        results = []
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, (name, params) in enumerate(algos.items()):
            status_text.text(f"Running {name}...")
            
            res = benchmark_solver(solver_instance, input_data, **params)
            
            results.append({
                "Algorithm": name,
                "Time (s)": res.time_taken,
                "Memory (KB)": res.peak_memory_kb,
                "Nodes Explored": res.nodes_explored,
                "Success": "Yes" if res.success else "No"
            })
            
            progress_bar.progress((i + 1) / len(algos))
            
        status_text.text("Benchmark complete!")
        
        df = pd.DataFrame(results)
        
        # Display Results Table
        st.subheader("Performance Metrics Table")
        st.dataframe(df, use_container_width=True)
        
        # Plots
        st.subheader("Performance Comparison Charts")
        
        c1, c2, c3 = st.columns(3)
        
        with c1:
            st.markdown("**Execution Time (Seconds)**")
            time_df = df.set_index("Algorithm")[["Time (s)"]]
            st.bar_chart(time_df)
            
        with c2:
            st.markdown("**Peak Memory Allocation (KB)**")
            mem_df = df.set_index("Algorithm")[["Memory (KB)"]]
            st.bar_chart(mem_df)
            
        with c3:
            st.markdown("**Nodes Explored (State Evaluations)**")
            nodes_df = df.set_index("Algorithm")[["Nodes Explored"]]
            st.bar_chart(nodes_df)
