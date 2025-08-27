"""
Basic Example: Circle with Points
Demonstrates circles, points, and basic labeling
"""

import shapix

def main():
    # Create a circle with points on circumference
    geometry = '''
    # Center point
    POINT O 0 0 "O" show_label=true label_position=center
    
    # Points on circumference
    POINT A 50 0 "A" show_label=true label_position=right
    POINT B 0 50 "B" show_label=true label_position=top
    POINT C -50 0 "C" show_label=true label_position=left
    POINT D 0 -50 "D" show_label=true label_position=bottom
    
    # Circle
    CIRCLE O 50 color=navy show_center=true
    
    # Lines from center to points
    LINE O A color=gray
    LINE O B color=gray  
    LINE O C color=gray
    LINE O D color=gray
    '''
    
    # Export to PNG
    shapix.export_geometry_syntax(geometry, "circle_and_points.png", 400, 400)
    
    print("✓ Circle and points example created")
    print(f"  Output: examples/basic/circle_and_points.png")

if __name__ == "__main__":
    main()