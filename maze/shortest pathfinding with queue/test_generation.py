import os
import random
from collections import deque

def solve_maze(n, m, maze):
    """The Test Oracle: Generates the ground-truth output string."""
    if maze[0][0] == 1 or maze[n-1][m-1] == 1:
        return "No path found."
    if n == 1 and m == 1:
        return "Shortest Path: (0,0)"

    q = deque([((0,0), [(0,0)])])
    visited = set([(0,0)])
    
    # Must strictly match the C++ direction checking order for equal-length path consistency
    # North (0,-1), East (1,0), South (0,1), West (-1,0)
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)] 

    while q:
        (x, y), path = q.popleft()
        
        if x == m - 1 and y == n - 1:
            path_str = " -> ".join([f"({px},{py})" for px, py in path])
            return f"Shortest Path: {path_str}"

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < m and 0 <= ny < n and maze[ny][nx] == 0 and (nx, ny) not in visited:
                visited.add((nx, ny))
                q.append(((nx, ny), path + [(nx, ny)]))
                
    return "No path found."

def maze_to_string(n, m, maze):
    header = f"{n} {m}\n"
    body = "\n".join([" ".join(map(str, row)) for row in maze])
    return header + body + "\n"

def generate_test_cases():
    os.makedirs("bfs_tests", exist_ok=True)
    tests = {}
    
    # --- HAND-CRAFTED EDGY CASES (1 to 10) ---
    tests["01_vanishing_path"] = [[0,0,0],[1,1,0],[1,1,0]]
    tests["02_phantom_exit"] = [[0,0],[0,1]]
    tests["03_immediate_exit"] = [[0]]
    tests["04_open_field"] = [[0]*4 for _ in range(4)]
    tests["05_decoy_branch"] = [
        [0, 0, 0, 0, 0],
        [1, 1, 0, 1, 0],
        [1, 0, 0, 0, 0],
        [1, 1, 1, 1, 0],
        [1, 1, 1, 1, 0]
    ]
    # Edge: 1D Horizontal Hallway
    tests["06_1d_horizontal"] = [[0]*10] 
    # Edge: 1D Vertical Hallway with a block
    tests["07_1d_vertical_blocked"] = [[0], [0], [0], [1], [0]]
    # Edge: Checkerboard (Unsolvable)
    tests["08_checkerboard"] = [[(i+j)%2 for j in range(5)] for i in range(5)]
    tests["08_checkerboard"][0][0] = 0 # Ensure start is open
    # Edge: The Spiral (Longest possible winding path)
    tests["09_spiral"] = [
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 1, 0, 0, 0],
        [0, 1, 0, 1, 1],
        [0, 0, 0, 1, 0]
    ]
    # Edge: Massive Open Field Stress Test
    tests["10_massive_open"] = [[0]*20 for _ in range(20)]

    # --- PROCEDURALLY GENERATED CASES (11 to 30) ---
    random.seed(42) # Fixed seed for reproducible test cases
    for i in range(11, 31):
        n = random.randint(5, 30)
        m = random.randint(5, 30)
        wall_density = random.uniform(0.15, 0.35)
        
        maze = []
        for r in range(n):
            row = []
            for c in range(m):
                row.append(1 if random.random() < wall_density else 0)
            maze.append(row)
            
        # Guarantee start and end aren't walls so the BFS actually has to work
        maze[0][0] = 0
        maze[n-1][m-1] = 0
        
        tests[f"{i:02d}_random_{n}x{m}"] = maze

    # --- FILE WRITING PIPELINE ---
    for name, maze in tests.items():
        n = len(maze)
        m = len(maze[0])
        
        # 1. Oracle solves the maze
        expected_output = solve_maze(n, m, maze)
        
        # 2. Write Input File
        with open(os.path.join("tests", f"{name}.in"), "w") as f:
            f.write(maze_to_string(n, m, maze))
            
        # 3. Write Output File
        with open(os.path.join("tests", f"{name}.out"), "w") as f:
            f.write(expected_output)
            
    print(f"Generated {len(tests)} battle-ready test cases in the '/tests' directory.")

if __name__ == "__main__":
    generate_test_cases()