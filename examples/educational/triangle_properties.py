"""
Educational Example: Triangle Properties
Demonstrates different types of triangles and their properties
"""

import shapix

def main():
    # Create different types of triangles
    geometry = '''
    # Equilateral Triangle (all sides equal, all angles 60°)
    POINT A1 -150 100 "A₁" show_label=true label_position=top_left
    POINT B1 -50 100 "B₁" show_label=true label_position=top_right
    POINT C1 -100 186.6 "C₁" show_label=true label_position=top
    TRIANGLE A1 B1 C1 color=blue show_vertices=true show_angles=true show_angle_measures=true
    
    # Isosceles Triangle (two sides equal)
    POINT A2 0 100 "A₂" show_label=true label_position=top_left
    POINT B2 100 100 "B₂" show_label=true label_position=top_right  
    POINT C2 50 200 "C₂" show_label=true label_position=top
    TRIANGLE A2 B2 C2 color=green show_vertices=true show_angles=true show_angle_measures=true
    
    # Right Triangle (one 90° angle)
    POINT A3 150 100 "A₃" show_label=true label_position=bottom_left
    POINT B3 250 100 "B₃" show_label=true label_position=bottom_right
    POINT C3 150 175 "C₃" show_label=true label_position=top_left
    TRIANGLE A3 B3 C3 color=red show_vertices=true show_angles=true show_angle_measures=true
    
    # Scalene Triangle (all sides different)
    POINT A4 -100 -50 "A₄" show_label=true label_position=bottom_left
    POINT B4 50 -50 "B₄" show_label=true label_position=bottom_right
    POINT C4 -25 50 "C₄" show_label=true label_position=top
    TRIANGLE A4 B4 C4 color=orange show_vertices=true show_angles=true show_angle_measures=true
    '''
    
    # Export to PNG
    shapix.export_geometry_syntax(geometry, "triangle_properties.png", 800, 600)
    
    # Calculate properties of each triangle type
    equilateral = shapix.create_triangle(-150, 100, -50, 100, -100, 186.6)
    isosceles = shapix.create_triangle(0, 100, 100, 100, 50, 200)
    right = shapix.create_triangle(150, 100, 250, 100, 150, 175)
    scalene = shapix.create_triangle(-100, -50, 50, -50, -25, 50)
    
    triangles = [
        ("Equilateral", equilateral),
        ("Isosceles", isosceles), 
        ("Right", right),
        ("Scalene", scalene)
    ]
    
    print("✓ Triangle properties demonstration created")
    for name, triangle in triangles:
        angle_a = triangle.get_angle_measure('a')
        angle_b = triangle.get_angle_measure('b')
        angle_c = triangle.get_angle_measure('c')
        print(f"  {name}: angles = {angle_a:.1f}°, {angle_b:.1f}°, {angle_c:.1f}° (sum = {angle_a+angle_b+angle_c:.1f}°)")
    
    print(f"  Output: examples/educational/triangle_properties.png")

if __name__ == "__main__":
    main()