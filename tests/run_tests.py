"""
Test runner script for shapix
"""

import sys
import os
import subprocess
import argparse

def main():
    """Run tests with various options"""
    parser = argparse.ArgumentParser(description="Run shapix tests")
    
    parser.add_argument(
        "--unit", 
        action="store_true", 
        help="Run only unit tests"
    )
    parser.add_argument(
        "--integration", 
        action="store_true", 
        help="Run only integration tests"
    )
    parser.add_argument(
        "--coverage", 
        action="store_true", 
        help="Run tests with coverage report"
    )
    parser.add_argument(
        "--verbose", "-v", 
        action="store_true", 
        help="Verbose output"
    )
    parser.add_argument(
        "--no-gui", 
        action="store_true", 
        help="Skip tests requiring GUI/display"
    )
    parser.add_argument(
        "--fast", 
        action="store_true", 
        help="Skip slow tests"
    )
    parser.add_argument(
        "path", 
        nargs="?", 
        default="tests/", 
        help="Path to test file or directory"
    )
    
    args = parser.parse_args()
    
    # Build pytest command
    cmd = ["python", "-m", "pytest"]
    
    # Add path
    cmd.append(args.path)
    
    # Add options based on arguments
    if args.verbose:
        cmd.extend(["-v", "--tb=long"])
    
    if args.unit:
        cmd.extend(["-m", "unit"])
    elif args.integration:
        cmd.extend(["-m", "integration"])
    
    if args.no_gui:
        cmd.extend(["-m", "not gui"])
    
    if args.fast:
        cmd.extend(["-m", "not slow"])
    
    if args.coverage:
        cmd.extend([
            "--cov=shapix", 
            "--cov-report=html",
            "--cov-report=term-missing"
        ])
    
    # Add default options
    cmd.extend(["--color=yes", "--tb=short"])
    
    print(f"Running command: {' '.join(cmd)}")
    print("=" * 60)
    
    # Run tests
    try:
        result = subprocess.run(cmd, cwd=os.path.dirname(os.path.dirname(__file__)))
        return result.returncode
    except FileNotFoundError:
        print("Error: pytest not found. Install with: pip install pytest")
        return 1
    except KeyboardInterrupt:
        print("\nTests interrupted by user")
        return 130

def run_quick_tests():
    """Run a quick subset of tests for development"""
    print("Running quick development tests...")
    
    cmd = [
        "python", "-m", "pytest", 
        "tests/unit/test_core.py",
        "tests/unit/test_shapes.py::TestPointShape",
        "-v", "--tb=short", "--no-header"
    ]
    
    try:
        result = subprocess.run(cmd, cwd=os.path.dirname(os.path.dirname(__file__)))
        return result.returncode
    except Exception as e:
        print(f"Error running quick tests: {e}")
        return 1

def run_all_tests():
    """Run complete test suite"""
    print("Running complete test suite...")
    
    cmd = [
        "python", "-m", "pytest", 
        "tests/",
        "-v", 
        "--tb=short",
        "--color=yes",
        "-m", "not gui"  # Skip GUI tests by default
    ]
    
    try:
        result = subprocess.run(cmd, cwd=os.path.dirname(os.path.dirname(__file__)))
        return result.returncode
    except Exception as e:
        print(f"Error running tests: {e}")
        return 1

if __name__ == "__main__":
    if len(sys.argv) == 1:
        # No arguments, run all tests
        sys.exit(run_all_tests())
    elif len(sys.argv) == 2 and sys.argv[1] == "--quick":
        # Quick development tests
        sys.exit(run_quick_tests())
    else:
        # Parse arguments and run accordingly
        sys.exit(main())