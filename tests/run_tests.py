#!/usr/bin/env python3
"""
Test runner for DyGETViz package.
"""

import os
import sys
import unittest
import subprocess

def run_all_tests():
    """Run all tests in the tests directory."""
    
    # Add the parent directory to the path so we can import dygetviz
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Discover and run tests
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(os.path.abspath(__file__))
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

def run_specific_test(test_file):
    """Run a specific test file."""
    test_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), test_file)
    
    if not os.path.exists(test_path):
        print(f"Test file {test_file} not found!")
        return False
    
    # Run the specific test file
    result = subprocess.run([sys.executable, test_path], capture_output=True, text=True)
    
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    return result.returncode == 0

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Run specific test
        test_file = sys.argv[1]
        success = run_specific_test(test_file)
    else:
        # Run all tests
        success = run_all_tests()
    
    sys.exit(0 if success else 1) 