"""
Basic Example: Line Segments
Demonstrates different line styles and measurements
"""

import shapix

def main():
    # Create various line segments
    geometry = '''
    # Horizontal line
    POINT A1 -100 50 "A" show_label=true label_position=left
    POINT A2 100 50 "B" show_label=true label_position=right
    LINE A1 A2 color=red show_endpoints=true show_length=true
    
    # Vertical line
    POINT B1 -50 -100 "C" show_label=true label_position=bottom
    POINT B2 -50 100 "D" show_label=true label_position=top
    LINE B1 B2 color=blue show_endpoints=true
    
    # Diagonal line
    POINT C1 0 -50 "E" show_label=true label_position=bottom_right
    POINT C2 75 75 "F" show_label=true label_position=top_left
    LINE C1 C2 color=green show_endpoints=true show_length=true
    '''
    
    # Export to PNG
    shapix.export_geometry_syntax(geometry, "line_segments.png", 600, 600)
    
    # Demonstrate programmatic line creation
    line = shapix.Line(shapix.Point(0, 0), shapix.Point(100, 100))
    print("✓ Line segments example created")
    print(f"  Line length: {line.get_length():.1f}")
    print(f"  Line angle: {line.get_angle():.1f}°")
    print(f"  Output: examples/basic/line_segments.png")

if __name__ == "__main__":
    main()