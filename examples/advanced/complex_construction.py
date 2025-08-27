"""
Advanced Example: Complex Geometric Construction
Recreates the original math problem with advanced features
"""

import shapix

def main():
    # Complex construction similar to the original math problem
    geometry = '''
    # Center and main circle
    POINT O 0 0 "O" show_label=true label_position=bottom_right
    CIRCLE O 400 color=black
    
    # Points on circle and key intersections
    POINT A 0 200 "A" show_label=true label_position=top
    POINT D 0 -200 "D" show_label=true label_position=bottom
    POINT C -153.2 -128.6 "C" show_label=true label_position=bottom_left
    POINT B -174 100 "B" show_label=true label_position=top_left
    POINT E 173.2 -100 "E" show_label=true label_position=bottom_right
    POINT F 0 -57.8 "F" show_label=true label_position=right
    
    # Main construction lines
    LINE A D color=black
    LINE O C color=black
    LINE A B color=black
    LINE B E color=black  
    LINE C D color=black
    LINE A E color=black
    
    # Key angles with measurements
    ANGLE C O D color=red arc=true show_measure=true
    ANGLE D A E color=green arc=true show_measure=true
    ANGLE D F E color=orange arc=true show_measure=true
    
    # Additional construction elements
    TRIANGLE A B F color=blue fill_color=lightblue
    TRIANGLE F E C color=purple fill_color=lightpink
    '''
    
    # Export to PNG
    shapix.export_geometry_syntax(geometry, "complex_construction.png", 1000, 1000)
    
    print("✓ Complex geometric construction created")
    print(f"  This recreates advanced geometric relationships")
    print(f"  Shows intersecting chords and angle relationships")
    print(f"  Output: examples/advanced/complex_construction.png")

if __name__ == "__main__":
    main()