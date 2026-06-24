# Heuristics for 8-Puzzle

def misplaced_tiles(state, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
    """
    Count the number of misplaced tiles.
    """
    count = 0
    for i in range(len(state)):
        if state[i] != 0 and state[i] != goal[i]:
            count += 1
    return count

def manhattan_distance(state, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
    """
    Sum of Manhattan distances of all tiles from their goal positions.
    """
    dist = 0
    for i in range(9):
        val = state[i]
        if val != 0:
            goal_idx = goal.index(val)
            r_curr, c_curr = i // 3, i % 3
            r_goal, c_goal = goal_idx // 3, goal_idx % 3
            dist += abs(r_curr - r_goal) + abs(c_curr - c_goal)
    return dist

def linear_conflict(state, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
    """
    Manhattan distance + 2 * (number of linear conflicts in rows/columns).
    """
    h_manhattan = manhattan_distance(state, goal)
    conflicts = 0
    
    # Check Row conflicts
    for row in range(3):
        row_tiles = []
        for col in range(3):
            idx = row * 3 + col
            val = state[idx]
            if val != 0:
                goal_idx = goal.index(val)
                goal_row = goal_idx // 3
                if goal_row == row:
                    row_tiles.append((col, goal_idx % 3)) # (current col, goal col)
        
        # Count overlaps
        for i in range(len(row_tiles)):
            for j in range(i + 1, len(row_tiles)):
                if row_tiles[i][0] < row_tiles[j][0] and row_tiles[i][1] > row_tiles[j][1]:
                    conflicts += 1
                elif row_tiles[i][0] > row_tiles[j][0] and row_tiles[i][1] < row_tiles[j][1]:
                    conflicts += 1
                    
    # Check Col conflicts
    for col in range(3):
        col_tiles = []
        for row in range(3):
            idx = row * 3 + col
            val = state[idx]
            if val != 0:
                goal_idx = goal.index(val)
                goal_col = goal_idx % 3
                if goal_col == col:
                    col_tiles.append((row, goal_idx // 3)) # (current row, goal row)
                    
        # Count overlaps
        for i in range(len(col_tiles)):
            for j in range(i + 1, len(col_tiles)):
                if col_tiles[i][0] < col_tiles[j][0] and col_tiles[i][1] > col_tiles[j][1]:
                    conflicts += 1
                elif col_tiles[i][0] > col_tiles[j][0] and col_tiles[i][1] < col_tiles[j][1]:
                    conflicts += 1
                    
    return h_manhattan + 2 * conflicts
