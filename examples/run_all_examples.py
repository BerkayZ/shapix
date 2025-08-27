"""
Run All Examples
Executes all example scripts and generates their outputs
"""

import os
import sys
import importlib.util

def run_example(example_path, example_name):
    """Run a single example script"""
    try:
        # Load and execute the module
        spec = importlib.util.spec_from_file_location(example_name, example_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        if hasattr(module, 'main'):
            module.main()
        
        return True
    except Exception as e:
        print(f"❌ Error running {example_name}: {e}")
        return False

def main():
    """Run all examples"""
    print("=== Running All Shapix Examples ===\n")
    
    examples_dir = os.path.dirname(__file__)
    
    # Define examples to run
    examples = [
        # Basic examples
        ("basic/simple_triangle.py", "Simple Triangle"),
        ("basic/circle_and_points.py", "Circle and Points"),
        ("basic/angles_demo.py", "Angles Demo"),
        ("basic/line_segments.py", "Line Segments"),
        
        # Advanced examples
        ("advanced/inscribed_triangle.py", "Inscribed Triangle"),
        ("advanced/complex_construction.py", "Complex Construction"),
        
        # Educational examples
        ("educational/pythagorean_theorem.py", "Pythagorean Theorem"),
        ("educational/triangle_properties.py", "Triangle Properties"),
        ("educational/circle_theorems.py", "Circle Theorems"),
    ]
    
    successful = 0
    total = len(examples)
    
    for example_file, example_name in examples:
        example_path = os.path.join(examples_dir, example_file)
        
        if os.path.exists(example_path):
            print(f"Running {example_name}...")
            if run_example(example_path, example_name.replace(" ", "_").lower()):
                successful += 1
            print()  # Empty line for readability
        else:
            print(f"❌ Example not found: {example_path}")
    
    print(f"=== Results ===")
    print(f"Successfully ran {successful}/{total} examples")
    
    if successful == total:
        print("🎉 All examples completed successfully!")
        print("\nGenerated files:")
        
        # List generated PNG files
        for root, dirs, files in os.walk(examples_dir):
            for file in files:
                if file.endswith('.png'):
                    rel_path = os.path.relpath(os.path.join(root, file), examples_dir)
                    print(f"  - {rel_path}")
    else:
        print(f"⚠️  {total - successful} examples failed")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())