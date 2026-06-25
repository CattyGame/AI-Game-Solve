def get_goal_positions():
    goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    return {goal[r][c]: (r, c) for r in range(3) for c in range(3)}

GOAL_POSITIONS = get_goal_positions()

def misplaced_tiles(state):
    count = 0
    for r in range(3):
        for c in range(3):
            val = state[r][c]
            if val != 0 and (r, c) != GOAL_POSITIONS[val]:
                count += 1
    return count

def manhattan_distance(state):
    distance = 0
    for r in range(3):
        for c in range(3):
            val = state[r][c]
            if val != 0:
                goal_r, goal_c = GOAL_POSITIONS[val]
                distance += abs(r - goal_r) + abs(c - goal_c)
    return distance