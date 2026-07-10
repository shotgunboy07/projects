import os
import subprocess
import glob

# Dynamically locate the directory where this script resides
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Configuration (All path declarations are absolute to allow click-to-run)
CPP_SOURCE = os.path.join(SCRIPT_DIR, "maze_BFS.cpp")
EXECUTABLE = os.path.join(SCRIPT_DIR, "B.exe")
TEST_DIR = os.path.join(SCRIPT_DIR, "tests")
TIMEOUT_SECONDS = 2.0

def compile_cpp_source():
    """Compiles the C++ source file into the destination executable."""
    if not os.path.exists(CPP_SOURCE):
        print(f"ERROR: C++ source file not found at '{CPP_SOURCE}'")
        return False

    print(f"--- Compiling {os.path.basename(CPP_SOURCE)} ---")
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
        print("ERROR: 'g++' compiler command not found. Please ensure MinGW/GCC is added to your system PATH.")
        return False

def run_tests():
    # 1. Compile first before running any evaluation
    if not compile_cpp_source():
        return

    # 2. Find all .in files in the test directory
    test_files = glob.glob(os.path.join(TEST_DIR, "*.in"))
    
    if not test_files:
        print(f"No test files found in the '{TEST_DIR}' directory. Run 'test_generation.py' first.")
        return

    print(f"--- Starting Autograder (Found {len(test_files)} tests) ---")
    
    passed_count = 0
    
    for in_file in sorted(test_files):
        # Derive the corresponding .out filename
        base_path = os.path.splitext(in_file)[0]
        out_file = base_path + ".out"
        test_name = os.path.basename(base_path)
        
        if not os.path.exists(out_file):
            print(f"[{test_name}] ERROR: Missing expected output file ({out_file})")
            continue
            
        # Read input and expected output
        with open(in_file, 'r') as f:
            input_data = f.read()
            
        with open(out_file, 'r') as f:
            expected_output = f.read().strip() # Avoid the whitespace trap
            
        try:
            # Run the compiled C++ executable
            result = subprocess.run(
                [EXECUTABLE],
                input=input_data,
                text=True,
                capture_output=True,
                timeout=TIMEOUT_SECONDS # Avoid the infinite loop trap
            )
            
            # The C++ program prints debug logs; filter to check the final output string line
            output_lines = [line for line in result.stdout.strip().split('\n') if line]
            actual_final_line = output_lines[-1] if output_lines else ""
            
            # Compare final outputs
            if actual_final_line == expected_output:
                print(f"[{test_name}] \033[92mPASS\033[0m")
                passed_count += 1
            else:
                print(f"[{test_name}] \033[91mFAIL\033[0m")
                print("  Expected:")
                print(f"    {expected_output}")
                print("  Got:")
                print(f"    {actual_final_line}")
                
        except subprocess.TimeoutExpired:
            print(f"[{test_name}] \033[91mTIMEOUT\033[0m (Exceeded {TIMEOUT_SECONDS}s)")

    print(f"\n--- Autograder Finished: {passed_count}/{len(test_files)} Passed ---")

if __name__ == "__main__":
    run_tests()
    # Keeps console window open if running by clicking directly on Windows
    input("\nPress Enter to exit...")