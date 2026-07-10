import os
import subprocess
import glob

# Configuration
EXECUTABLE = "./B.exe"
TEST_DIR = "tests"
TIMEOUT_SECONDS = 2.0

def run_tests():
    # Find all .in files in the test directory
    test_files = glob.glob(os.path.join(TEST_DIR, "*.in"))
    
    if not test_files:
        print(f"No test files found in the '{TEST_DIR}' directory.")
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
            # Run the C++ executable
            result = subprocess.run(
                [EXECUTABLE],
                input=input_data,
                text=True,
                capture_output=True,
                timeout=TIMEOUT_SECONDS # Avoid the infinite loop trap
            )
            
            # The C++ program prints a lot of debug logs.
            # We only want to compare the very last line containing the final result.
            output_lines = [line for line in result.stdout.strip().split('\n') if line]
            actual_final_line = output_lines[-1] if output_lines else ""
            
            # Compare
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
        except FileNotFoundError:
            print(f"ERROR: Executable '{EXECUTABLE}' not found. Did you compile it?")
            return

    print(f"\n--- Autograder Finished: {passed_count}/{len(test_files)} Passed ---")

if __name__ == "__main__":
    run_tests()