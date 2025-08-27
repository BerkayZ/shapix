"""
Comprehensive test runner for shapix package
Runs all tests and examples to verify everything works
"""

import sys
import os
import subprocess
import importlib.util
from pathlib import Path

def run_command(cmd, description, cwd=None):
    """Run a command and report results"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print('='*60)
    
    try:
        result = subprocess.run(
            cmd, 
            cwd=cwd, 
            capture_output=True, 
            text=True, 
            timeout=300  # 5 minute timeout
        )
        
        if result.stdout:
            print("STDOUT:")
            print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        if result.returncode == 0:
            print(f"✅ {description} - SUCCESS")
            return True
        else:
            print(f"❌ {description} - FAILED (exit code: {result.returncode})")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ {description} - TIMEOUT")
        return False
    except Exception as e:
        print(f"💥 {description} - ERROR: {e}")
        return False

def run_python_file(file_path, description):
    """Run a Python file and report results"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"File: {file_path}")
    print('='*60)
    
    try:
        # Load and execute the module
        spec = importlib.util.spec_from_file_location("test_module", file_path)
        module = importlib.util.module_from_spec(spec)
        
        # Capture stdout
        import io
        from contextlib import redirect_stdout, redirect_stderr
        
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        
        with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
            spec.loader.exec_module(module)
            if hasattr(module, 'main'):
                module.main()
        
        stdout_content = stdout_capture.getvalue()
        stderr_content = stderr_capture.getvalue()
        
        if stdout_content:
            print("OUTPUT:")
            print(stdout_content)
        
        if stderr_content:
            print("ERRORS:")
            print(stderr_content)
        
        print(f"✅ {description} - SUCCESS")
        return True
        
    except Exception as e:
        print(f"❌ {description} - FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run comprehensive tests"""
    print("🚀 Starting Shapix Comprehensive Test Suite")
    print("This will run unit tests, integration tests, and examples")
    
    # Get project root directory
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    results = []
    
    # 1. Run unit tests
    success = run_command(
        ["python", "-m", "pytest", "tests/unit/", "-v", "--tb=short", "-x"],
        "Unit Tests",
        project_root
    )
    results.append(("Unit Tests", success))
    
    # 2. Run integration tests (skip GUI tests)
    success = run_command(
        ["python", "-m", "pytest", "tests/integration/", "-v", "--tb=short", "-m", "not gui", "-x"],
        "Integration Tests",
        project_root
    )
    results.append(("Integration Tests", success))
    
    # 3. Test package installation
    success = run_command(
        ["python", "-c", "import shapix; print(f'Shapix version: {shapix.__version__}')"],
        "Package Import Test",
        project_root
    )
    results.append(("Package Import", success))
    
    # 4. Run basic examples
    examples_to_test = [
        ("examples/basic/simple_triangle.py", "Simple Triangle Example"),
        ("examples/basic/circle_and_points.py", "Circle and Points Example"),
        ("examples/educational/pythagorean_theorem.py", "Pythagorean Theorem Example"),
    ]
    
    for example_path, description in examples_to_test:
        if os.path.exists(example_path):
            success = run_python_file(example_path, description)
            results.append((description, success))
    
    # 5. Test CLI functionality (if available)
    test_geo_content = '''
    POINT A 0 0 "A" show_label=true
    POINT B 10 10 "B" show_label=true
    LINE A B color=red
    '''
    
    with open("test_cli.geo", "w") as f:
        f.write(test_geo_content)
    
    success = run_command(
        ["python", "-m", "shapix.cli", "test_cli.geo", "test_cli_output.png", "--width", "400", "--height", "300"],
        "CLI Test",
        project_root
    )
    results.append(("CLI Test", success))
    
    # Clean up test files
    for test_file in ["test_cli.geo", "test_cli_output.png"]:
        if os.path.exists(test_file):
            os.remove(test_file)
    
    # 6. Test mathematical operations
    success = run_command([
        "python", "-c", """
import shapix
triangle = shapix.create_triangle(0, 0, 3, 0, 0, 4)
print(f'Triangle area: {triangle.get_area()}')
print(f'Is right triangle: {triangle.is_right_triangle()}')
circle = shapix.create_circle(0, 0, 10)
print(f'Circle area: {circle.get_area():.2f}')
print('Mathematical operations test passed!')
        """],
        "Mathematical Operations Test",
        project_root
    )
    results.append(("Mathematical Operations", success))
    
    # 7. Test syntax parsing
    success = run_command([
        "python", "-c", """
import shapix
syntax = '''
POINT A 0 0 "A" show_label=true
CIRCLE A 50 color=blue
TRIANGLE A A A color=red
'''
parser = shapix.GeometrySyntaxParser()
shapes = parser.parse(syntax)
print(f'Parsed {len(shapes)} shapes')
print('Syntax parsing test passed!')
        """],
        "Syntax Parsing Test",
        project_root
    )
    results.append(("Syntax Parsing", success))
    
    # Print summary
    print(f"\n{'='*80}")
    print("📊 TEST SUMMARY")
    print(f"{'='*80}")
    
    passed = 0
    failed = 0
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name:<30} {status}")
        if success:
            passed += 1
        else:
            failed += 1
    
    print(f"\n📈 Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! Shapix is working correctly.")
        return 0
    else:
        print(f"💥 {failed} test(s) failed. Please check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())