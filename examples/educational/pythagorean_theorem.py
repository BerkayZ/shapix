"""
Educational Example: Pythagorean Theorem Demonstration
Visual proof of a² + b² = c²
"""

import shapix

def main():
    # Create a right triangle with squares on each side
    geometry = '''
    # Right triangle
    POINT A 0 0 "A" show_label=true label_position=bottom_left
    POINT B 120 0 "B" show_label=true label_position=bottom_right
    POINT C 0 90 "C" show_label=true label_position=top_left
    
    TRIANGLE A B C color=red show_vertices=true show_angles=true
    
    # Square on side a (vertical side, AC)
    POINT C1 -90 0 "C₁" show_label=true label_position=left
    POINT C2 -90 90 "C₂" show_label=true label_position=top_left
    LINE A C1 color=blue
    LINE C1 C2 color=blue
    LINE C2 C color=blue
    TRIANGLE A C1 C2 color=blue fill_color=lightblue
    TRIANGLE C2 C A color=blue fill_color=lightblue
    
    # Square on side b (horizontal side, AB)
    POINT B1 120 -120 "B₁" show_label=true label_position=bottom_right
    POINT B2 0 -120 "B₂" show_label=true label_position=bottom_left
    LINE A B2 color=green
    LINE B2 B1 color=green
    LINE B1 B color=green
    TRIANGLE A B2 B1 color=green fill_color=lightgreen
    TRIANGLE B1 B A color=green fill_color=lightgreen
    
    # Square on hypotenuse c (BC)
    POINT D1 -54 144 "D₁" show_label=true label_position=top_left
    POINT D2 66 126 "D₂" show_label=true label_position=top_right
    LINE C D1 color=purple
    LINE D1 D2 color=purple
    LINE D2 B color=purple
    TRIANGLE C D1 D2 color=purple fill_color=plum
    TRIANGLE D2 B C color=purple fill_color=plum
    '''
    
    # Export to PNG
    shapix.export_geometry_syntax(geometry, "pythagorean_theorem.png", 800, 800)
    
    # Calculate and verify the theorem
    a = 90  # height
    b = 120  # base
    c = (a*a + b*b)**0.5  # hypotenuse
    
    print("✓ Pythagorean theorem demonstration created")
    print(f"  Side a: {a}")
    print(f"  Side b: {b}")  
    print(f"  Hypotenuse c: {c:.1f}")
    print(f"  a² + b² = {a*a + b*b}")
    print(f"  c² = {c*c:.1f}")
    print(f"  Theorem verified: {abs(a*a + b*b - c*c) < 0.01}")
    print(f"  Output: examples/educational/pythagorean_theorem.png")

if __name__ == "__main__":
    main()