"""
Basic Example: Simple Triangle
Creates a simple triangle with labeled vertices
"""

import shapix

def main():
    # Create a simple triangle using text syntax
    geometry = '''
    # Simple triangle with vertices
    POINT A 0 100 "A" show_label=true label_position=top
    POINT B -87 -50 "B" show_label=true label_position=bottom_left  
    POINT C 87 -50 "C" show_label=true label_position=bottom_right
    
    TRIANGLE A B C color=blue show_vertices=true
    '''
    
    # Export to PNG
    shapix.export_geometry_syntax(geometry, "examples/basic/simple_triangle.png", 600, 600)
    
    # Also demonstrate programmatic creation
    triangle = shapix.create_triangle(0, 100, -87, -50, 87, -50, ("A", "B", "C"))
    triangle.color = "red"
    
    print("✓ Simple triangle example created")
    print(f"  Area: {triangle.get_area():.1f}")
    print(f"  Perimeter: {triangle.get_perimeter():.1f}")
    print(f"  Output: examples/basic/simple_triangle.png")

if __name__ == "__main__":
    main()