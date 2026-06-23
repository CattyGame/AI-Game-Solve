# [AI_Project] Bộ Giải Tự Động & Đánh Giá Hiệu Năng Thuật Toán Cho Game Logic

Dự án nghiên cứu, hiện thực và so sánh hiệu năng của các nhóm thuật toán Trí tuệ nhân tạo (Tìm kiếm mù, Tìm kiếm Heuristic, Local Search) trong việc giải quyết 3 bài toán game logic kinh điển: **Sudoku**, **8-Puzzle**, và **N-Queens**.

---

## 📌 1. Giới Thiệu Đề Tài

Dự án tập trung vào việc xây dựng một ứng dụng thử nghiệm và phân tích giải thuật (Algorithm Benchmarking Suite) cho 3 trò chơi trí tuệ. Mục tiêu cốt lõi là không chỉ tìm ra lời giải mà còn đo đạc, phân tích định lượng để làm rõ ưu/nhược điểm của từng tiếp cận thuật toán khác nhau đối với từng không gian trạng thái (State Space).

### Phân hệ bài toán & Các thuật toán hiện thực:
1. **Sudoku Solver:** * Thuật toán: *Backtracking (Duyệt lui)* cơ bản kết hợp cải tiến Heuristic chọn biến (*MRV - Minimum Remaining Values*, *Degree Heuristic*) và kỹ thuật kiểm tra trước (*Forward Checking*).
2. **8-Puzzle Solver:**
   * Thuật toán: *BFS (Breadth-First Search)*, *UCS (Uniform Cost Search)*, và thuật toán tìm kiếm tối ưu *$A^*$* sử dụng các hàm Heuristic khác nhau (*Misplaced Tiles*, *Manhattan Distance*, *Linear Conflict*) để so sánh độ hiệu quả của hàm Heuristic.
3. **N-Queens Solver:**
   * Thuật toán: Tiếp cận Tìm kiếm cục bộ (*Local Search*) bao gồm *Hill Climbing (Leo đồi)*, *Simulated Annealing (Luyện kim giả lập)*, và *Genetic Algorithm (Giải thuật di truyền)* để giải quyết bài toán với kích thước bàn cờ lớn ($N \ge 8$).

---

## 👥 2. Phân Chia Công Việc (Nhóm 4 Thành Viên)

Để đảm bảo tiến độ và khối lượng công việc được phân rã rõ ràng trên Git, các thành viên sẽ chịu trách nhiệm theo từng module thuật toán và phần lõi thống kê:

* **Thành viên 1 (Trưởng nhóm):** Thiết kế kiến trúc tổng thể, quản lý dữ liệu đầu vào và hiện thực **Module 8-Puzzle** (BFS, UCS, $A^*$ và các hàm Heuristic).
* **Thành viên 2:** Hiện thực **Module Sudoku** (Backtracking, các kỹ thuật tối ưu hóa CSP như MRV, Forward Checking để tăng tốc độ giải ma trận khó).
* **Thành viên 3:** Hiện thực **Module N-Queens** (Các thuật toán Local Search: Hill Climbing, Simulated Annealing, Genetic Algorithm).
* **Thành viên 4:** Xây dựng **Module Benchmark** (Bộ đếm thời gian, bộ nhớ, số node đã duyệt) và phát triển **Giao diện người dùng (UI/Dashboard)** để trực quan hóa các bước giải và biểu đồ so sánh.

---

## 📂 3. Cấu Trúc Thư Mục Dự Án

Cấu trúc thư mục được thiết kế theo dạng module hóa (Modular Design), giúp tách biệt phần xử lý thuật toán, dữ liệu mẫu và giao diện hiển thị:

```text
ai-game-solver/
│
├── data/                           # Dữ liệu kiểm thử mẫu (Testcases)
│   ├── sudoku/                     # Các ma trận Sudoku từ dễ đến cực khó (.txt / .json)
│   ├── puzzle_8/                   # Các trạng thái khởi đầu của 8-puzzle (đảm bảo giải được)
│   └── nqueens/                    # Cấu hình kích thước bàn cờ N mẫu
│
├── src/                            # Mã nguồn chính của dự án
│   ├── __init__.py
│   │
│   ├── core/                       # Lõi xử lý dữ liệu và cấu trúc chung
│   │   ├── __init__.py
│   │   └── base_solver.py          # Lớp trừu tượng (Abstract Class) cho các bộ giải
│   │
│   ├── sudoku/                     # MODULE 1: BỘ GIẢI SUDOKU
│   │   ├── __init__.py
│   │   └── solver.py               # Backtracking + MRV + Forward Checking
│   │
│   ├── puzzle_8/                   # MODULE 2: BỘ GIẢI 8-PUZZLE
│   │   ├── __init__.py
│   │   ├── heuristics.py           # Định nghĩa Manhattan, Misplaced Tiles...
│   │   └── solver.py               # Hiện thực BFS, UCS, A*
│   │
│   ├── nqueens/                    # MODULE 3: BỘ GIẢI N-QUEENS
│   │   ├── __init__.py
│   │   └── solver.py               # Hiện thực Hill Climbing, Annealing, Genetic
│   │
│   ├── benchmark/                  # MODULE 4: ĐO ĐẠC & PHÂN TÍCH HIỆU NĂNG
│   │   ├── __init__.py
│   │   └── metrics.py              # Công cụ thu thập: Execution Time, Memory, Nodes Explored
│   │
│   └── ui/                         # MODULE 5: GIAO DIỆN TRỰC QUAN HÓA
│       ├── __init__.py
│       ├── assets/                 # Hình ảnh, style CSS (nếu có)
│       ├── components/             # Giao diện bàn cờ, lưới Sudoku, bảng thống kê
│       └── app.py                  # File chạy ứng dụng chính (Streamlit / PyQt / Tkinter)
│
├── tests/                          # Thư mục unit test đảm bảo thuật toán chạy đúng
│   ├── test_sudoku.py
│   ├── test_puzzle.py
│   └── test_nqueens.py
│
├── docs/                           # Tài liệu báo cáo, Slide thuyết trình
├── .gitignore                      # Cấu hình bỏ qua file thừa khi push lên Git
├── README.md                       # File hướng dẫn hiện tại
└── requirements.txt                # Danh sách thư viện (NumPy, Matplotlib, Streamlit...)
