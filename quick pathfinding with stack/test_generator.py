import os
import random

def solve_maze_dfs(n, m, maze):
    """The Perfected Stateful DFS Test Oracle."""
    
    # Vector translation
    dir_vec = {"E": (1, 0), "N": (0, -1), "W": (-1, 0), "S": (0, 1)}
    
    # The State Machine Transitions
    rotate_valid = {"E": "N", "N": "W", "W": "S", "S": "E"}
    rotate_invalid = {"E": "S", "N": "E", "W": "N", "S": "W"}
    
    # Stack stores: [x, y, current_path_list, direction_to_try, attempts_made]
    stack = [[0, 0, [(0,0)], "E", 0]] 
    visited = set([(0,0)])
    
    path_found = False
    final_path = set()
    
    while stack:
        curr = stack[-1]
        x, y, current_path, d, attempts = curr
        
        # Pass 1: Destination arrival testing
        if x == m - 1 and y == n - 1:
            path_found = True
            final_path = set(current_path)
            break
            
        # Pass 4 -> Pass 6: If all 4 directions tried, pop the stack and backtrack
        if attempts == 4:
            stack.pop()
            continue
            
        dx, dy = dir_vec[d]
        nx, ny = x + dx, y + dy
        
        # Pass 2 & 3: Invalid/Valid Path Testing
        if 0 <= nx < m and 0 <= ny < n and maze[ny][nx] == 0 and (nx, ny) not in visited:
            # VALID PATH FOUND
            visited.add((nx, ny))
            
            # Update current node so if we backtrack, it tries the NEXT invalid rotation
            curr[3] = rotate_invalid[d]
            curr[4] += 1
            
            # Push new node to stack. Its starting direction uses rotate_valid
            stack.append([nx, ny, current_path + [(nx, ny)], rotate_valid[d], 0])
        else:
            # INVALID PATH
            curr[3] = rotate_invalid[d]
            curr[4] += 1

    # --- THE ANSI STRING BUILDER ---
    GREEN = "\033[1;32m"
    RED = "\033[1;31m"
    RESET = "\033[0m"
    
    output_lines = []
    for i in range(n):
        row_str = ""
        for j in range(m):
            if path_found:
                if (j, i) in final_path:
                    row_str += f"{GREEN}{maze[i][j]}{RESET} "
                else:
                    row_str += f"{maze[i][j]} "
            else:
                if (j, i) in visited:
                    row_str += f"{RED}{maze[i][j]}{RESET} "
                else:
                    row_str += f"{maze[i][j]} "
        
        output_lines.append(row_str)
        
    return "\n".join(output_lines) + "\n"

def maze_to_string(n, m, maze):
    header = f"{n} {m}\n"
    body = "\n".join([" ".join(map(str, row)) for row in maze])
    return header + body + "\n"

def generate_test_cases():
    os.makedirs("dfs_tests", exist_ok=True)
    tests = {}
    
    # Hand-crafted edge cases
    tests["01_vanishing_path"] = [[0,0,0],[1,1,0],[1,1,0]]
    tests["02_phantom_exit"] = [[0,0],[0,1]]
    tests["03_open_field"] = [[0]*4 for _ in range(4)]
    
    # Procedurally generated grids
    random.seed(42)
    for i in range(4, 31):
        n = random.randint(5, 15)
        m = random.randint(5, 15)
        wall_density = random.uniform(0.15, 0.30)
        maze = [[1 if random.random() < wall_density else 0 for _ in range(m)] for _ in range(n)]
        maze[0][0] = 0
        maze[n-1][m-1] = 0
        tests[f"{i:02d}_random_{n}x{m}"] = maze

    for name, maze in tests.items():
        n, m = len(maze), len(maze[0])
        expected_output = solve_maze_dfs(n, m, maze)
        
        with open(os.path.join("dfs_tests", f"{name}.in"), "w") as f:
            f.write(maze_to_string(n, m, maze))
            
        # The .out file will invisibly store the \033 ANSI color bytes
        with open(os.path.join("dfs_tests", f"{name}.out"), "w") as f:
            f.write(expected_output)
            
    print(f"Generated {len(tests)} Color-Aware DFS test cases.")

if __name__ == "__main__":
    generate_test_cases()