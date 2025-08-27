"""
Advanced Example: Inscribed Triangle in Circle
Demonstrates complex geometric relationships
"""

import shapix
import math

def main():
    # Create an inscribed equilateral triangle
    geometry = '''
    # Circle
    POINT O 0 0 "O" show_label=true label_position=center
    CIRCLE O 100 color=navy show_center=true
    
    # Equilateral triangle inscribed in circle
    # Vertices at 120-degree intervals
    POINT A 0 100 "A" show_label=true label_position=top
    POINT B -86.6 -50 "B" show_label=true label_position=bottom_left
    POINT C 86.6 -50 "C" show_label=true label_position=bottom_right
    
    TRIANGLE A B C color=darkgreen fill_color=lightgreen show_vertices=false 
    
    # Show radii to vertices
    LINE O A color=red
    LINE O B color=red  
    LINE O C color=red
    
    # Show angles at center (each should be 120°)
    ANGLE A O B color=orange arc=true show_measure=true
    ANGLE B O C color=orange arc=true show_measure=true
    ANGLE C O A color=orange arc=true show_measure=true
    '''
    
    # Export to PNG
    shapix.export_geometry_syntax(geometry, "inscribed_triangle.png", 600, 600)
    
    # Calculate properties programmatically
    triangle = shapix.create_triangle(0, 100, -86.6, -50, 86.6, -50)
    circle = shapix.create_circle(0, 0, 100)
    
    print("✓ Inscribed triangle example created")
    print(f"  Triangle area: {triangle.get_area():.1f}")
    print(f"  Circle area: {circle.get_area():.1f}")
    print(f"  Ratio (triangle/circle): {triangle.get_area()/circle.get_area():.3f}")
    print(f"  Output: examples/advanced/inscribed_triangle.png")

if __name__ == "__main__":
    main()