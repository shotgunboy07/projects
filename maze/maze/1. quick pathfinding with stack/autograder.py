import os
import subprocess
import glob

# Dynamically locate the directory where this script resides
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Configuration Area ---
# Make sure this matches your actual C++ source filename (e.g., maze_DFS.cpp)
CPP_SOURCE_NAME = "maze_DFS.cpp" 
EXE_OUTPUT_NAME = "A.exe"
# --------------------------

# Set up absolute paths so the script works perfectly from any directory or via double-click
CPP_SOURCE = os.path.join(SCRIPT_DIR, CPP_SOURCE_NAME)
EXECUTABLE = os.path.join(SCRIPT_DIR, EXE_OUTPUT_NAME)
TEST_DIR = os.path.join(SCRIPT_DIR, "dfs_tests")
TIMEOUT_SECONDS = 2.0

def compile_cpp_source():
    """Compiles the C++ source file into the target executable."""
    if not os.path.exists(CPP_SOURCE):
        print(f"ERROR: C++ source file not found at '{CPP_SOURCE}'")
        return False

    print(f"--- Compiling {CPP_SOURCE_NAME} ---")
    try:
        # Run g++ compilation command
        result = subprocess.run(
            ["g++", "-std=c++17", CPP_SOURCE, "-o", EXECUTABLE],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("Compilation successful! Executable generated.\n")
            return True
        else:
            print("\033[91mCOMPILATION FAILED:\033[0m")
            print(result.stderr)
            return False
            
    except FileNotFoundError:
        print("ERROR: 'g++' command not found. Please ensure MinGW/GCC is added to your system PATH.")
        return False

def run_tests():
    # 1. Compile the C++ program first
    if not compile_cpp_source():
        return

    # 2. Find all .in files in the test directory
    test_files = glob.glob(os.path.join(TEST_DIR, "*.in"))
    
    if not test_files:
        print(f"ERROR: No test files found in '{TEST_DIR}'. Run 'test_generation.py' first.")
        return

    print(f"--- Starting Color-Aware DFS Autograder (Found {len(test_files)} tests) ---")
    
    passed_count = 0
    
    for in_file in sorted(test_files):
        base_path = os.path.splitext(in_file)[0]
        out_file = base_path + ".out"
        test_name = os.path.basename(base_path)
        
        if not os.path.exists(out_file):
            print(f"[{test_name}] ERROR: Missing expected output file (*.out)")
            continue
            
        with open(in_file, 'r') as f:
            input_data = f.read()
            
        with open(out_file, 'r') as f:
            expected_output = f.read().strip()
            
        try:
            # Run the executable using its absolute path
            result = subprocess.run(
                [EXECUTABLE],
                input=input_data,
                text=True,
                capture_output=True,
                timeout=TIMEOUT_SECONDS
            )
            
            # Split expected output into individual lines to determine its grid height
            expected_lines = expected_output.split('\n')
            num_expected_lines = len(expected_lines)
            
            # Clean and split the actual program output lines
            output_lines = [line for line in result.stdout.strip().split('\n') if line]
            
            # Dynamically pull the last N lines to catch the full multi-line grid
            actual_final_output = "\n".join(output_lines[-num_expected_lines:]) if output_lines else ""
            
            if actual_final_output == expected_output:
                print(f"[{test_name}] \033[92mPASS\033[0m")
                passed_count += 1
            else:
                print(f"[{test_name}] \033[91mFAIL\033[0m")
                print("  Expected:")
                for line in expected_lines:
                    print(f"    {line}")
                print("  Got:")
                for line in actual_final_output.split('\n'):
                    print(f"    {line}")
                
        except subprocess.TimeoutExpired:
            print(f"[{test_name}] \033[91mTIMEOUT\033[0m (Exceeded {TIMEOUT_SECONDS}s)")

    print(f"\n--- Autograder Finished: {passed_count}/{len(test_files)} Passed ---")

if __name__ == "__main__":
    run_tests()
    # Keeps the console window open when running by double-clicking the script
    input("\nPress Enter to exit...")