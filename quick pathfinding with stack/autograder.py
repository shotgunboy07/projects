import os
import subprocess
import glob

EXECUTABLE = "./DFS.exe"
TEST_DIR = "dfs_tests"
TIMEOUT_SECONDS = 2.0

def run_tests():
    test_files = glob.glob(os.path.join(TEST_DIR, "*.in"))
    passed_count = 0
    
    if not test_files:
        print("No test files found. Run generate_dfs_tests.py first.")
        return

    print(f"--- Starting Color-Aware DFS Autograder (Found {len(test_files)} tests) ---")
    
    for in_file in sorted(test_files):
        base_path = os.path.splitext(in_file)[0]
        out_file = base_path + ".out"
        test_name = os.path.basename(base_path)
        
        with open(in_file, 'r') as f: input_data = f.read()
        with open(out_file, 'r') as f: expected_output = f.read().strip()
            
        try:
            result = subprocess.run(
                [EXECUTABLE], input=input_data, text=True, 
                capture_output=True, timeout=TIMEOUT_SECONDS
            )
            
            # C++ might print debug lines above the grid. 
            # We slice the output to only grab the final N rows corresponding to the grid.
            lines = result.stdout.strip().split('\n')
            n_rows = int(input_data.split()[0])
            
            # Extract the last N lines (the actual colored grid)
            actual_grid = "\n".join(lines[-n_rows:]) if len(lines) >= n_rows else result.stdout.strip()
            
            if actual_grid == expected_output:
                print(f"[{test_name}] \033[92mPASS\033[0m")
                passed_count += 1
            else:
                print(f"[{test_name}] \033[91mFAIL\033[0m")
                print("\n=== EXPECTED (Oracle) ===")
                print(expected_output) # This will render with color in your terminal!
                print("\n=== ACTUAL (C++) ===")
                print(actual_grid)     # This will also render with color!
                print("=========================\n")
                
        except subprocess.TimeoutExpired:
            print(f"[{test_name}] \033[91mTIMEOUT\033[0m")

    print(f"\n--- Autograder Finished: {passed_count}/{len(test_files)} Passed ---")

if __name__ == "__main__":
    run_tests()