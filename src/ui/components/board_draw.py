def draw_sudoku_board(board, original_board=None):
    """
    Renders a 9x9 Sudoku board in Streamlit using HTML/CSS.
    If original_board is provided, it highlights the solved values vs starting values.
    """
    html = """
    <style>
    .sudoku-container {
        display: flex;
        justify-content: center;
        margin: 20px 0;
    }
    .sudoku-table {
        border-collapse: collapse;
        border: 3px solid #1E293B; /* Slate 800 */
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3), 0 4px 6px -4px rgba(0, 0, 0, 0.3);
        border-radius: 8px;
        overflow: hidden;
        background-color: #0F172A; /* Slate 900 */
    }
    .sudoku-cell {
        width: 45px;
        height: 45px;
        text-align: center;
        font-size: 20px;
        font-family: 'Outfit', sans-serif;
        font-weight: 600;
        border: 1px solid #334155; /* Slate 700 */
        color: #F8FAFC; /* Slate 50 */
    }
    /* Thick borders for 3x3 subgrids */
    .sudoku-table tr:nth-child(3n) td {
        border-bottom: 3px solid #1E293B;
    }
    .sudoku-table td:nth-child(3n) {
        border-right: 3px solid #1E293B;
    }
    .sudoku-cell.original {
        color: #94A3B8; /* Slate 400 for original clues */
        background-color: #1E293B; /* Slightly darker */
    }
    .sudoku-cell.solved {
        color: #38BDF8; /* Sky 400 for solved numbers */
        font-weight: bold;
        background-color: #0F172A;
        animation: pulse-solved 1.5s ease-out;
    }
    @keyframes pulse-solved {
        0% { background-color: rgba(56, 189, 248, 0.2); }
        100% { background-color: #0F172A; }
    }
    </style>
    <div class="sudoku-container">
        <table class="sudoku-table">
    """
    for r in range(9):
        html += "<tr>"
        for c in range(9):
            val = board[r][c]
            val_str = str(val) if val != 0 else ""
            
            # Determine if cell was original
            is_original = False
            if original_board:
                if isinstance(original_board, str):
                    orig_val = int(original_board[r*9 + c])
                    is_original = orig_val != 0
                else:
                    is_original = original_board[r][c] != 0
            
            cell_class = "sudoku-cell"
            if val != 0:
                if is_original:
                    cell_class += " original"
                else:
                    cell_class += " solved"
            
            html += f'<td class="{cell_class}">{val_str}</td>'
        html += "</tr>"
    html += "</table></div>"
    return html


def draw_puzzle8_board(state):
    """
    Renders an 8-Puzzle board using HTML/CSS.
    state: Tuple/list of 9 numbers (0 represents empty).
    """
    html = """
    <style>
    .puzzle-container {
        display: flex;
        justify-content: center;
        margin: 20px 0;
    }
    .puzzle-grid {
        display: grid;
        grid-template-columns: repeat(3, 80px);
        grid-template-rows: repeat(3, 80px);
        gap: 8px;
        padding: 10px;
        background-color: #1E293B; /* Slate 800 */
        border-radius: 12px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
    }
    .puzzle-tile {
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        border-radius: 8px;
        background: linear-gradient(135deg, #38BDF8 0%, #0284C7 100%); /* Sky gradient */
        color: #FFFFFF;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .puzzle-tile:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px -2px rgba(56, 189, 248, 0.4);
    }
    .puzzle-tile.empty {
        background: #0F172A; /* Slate 900 */
        box-shadow: inset 0 2px 4px 0 rgba(0, 0, 0, 0.6);
        border: 1px dashed #334155;
    }
    </style>
    <div class="puzzle-container">
        <div class="puzzle-grid">
    """
    for val in state:
        if val == 0:
            html += '<div class="puzzle-tile empty"></div>'
        else:
            html += f'<div class="puzzle-tile">{val}</div>'
    html += "</div></div>"
    return html


def draw_nqueens_board(state):
    """
    Renders an N-Queens chessboard.
    state: List of N row positions for queens in each column.
    """
    n = len(state)
    # Calculate cell size based on board size to keep it readable
    cell_size = max(30, min(60, 480 // n))
    
    html = f"""
    <style>
    .chess-container {{
        display: flex;
        justify-content: center;
        margin: 20px 0;
    }}
    .chess-table {{
        border-collapse: collapse;
        border: 4px solid #1E293B;
        box-shadow: 0 12px 25px -5px rgba(0, 0, 0, 0.4);
        border-radius: 8px;
        overflow: hidden;
    }}
    .chess-cell {{
        width: {cell_size}px;
        height: {cell_size}px;
        text-align: center;
        font-size: {int(cell_size * 0.6)}px;
        line-height: {cell_size}px;
        cursor: default;
    }}
    .chess-cell.light {{
        background-color: #E2E8F0; /* Slate 200 */
    }}
    .chess-cell.dark {{
        background-color: #475569; /* Slate 600 */
    }}
    .queen-icon {{
        color: #F59E0B; /* Amber 500 for royal crown */
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        animation: scale-up 0.3s ease-out;
    }}
    @keyframes scale-up {{
        0% {{ transform: scale(0); }}
        100% {{ transform: scale(1); }}
    }}
    </style>
    <div class="chess-container">
        <table class="chess-table">
    """
    for r in range(n):
        html += "<tr>"
        for c in range(n):
            # Alternating colors
            cell_type = "light" if (r + c) % 2 == 0 else "dark"
            
            # Check if there is a queen in this row and column
            has_queen = state[c] == r
            queen_content = '<span class="queen-icon">👑</span>' if has_queen else ""
            
            html += f'<td class="chess-cell {cell_type}">{queen_content}</td>'
        html += "</tr>"
    html += "</table></div>"
    return html
