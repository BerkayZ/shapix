"""
Basic Example: Angles Demonstration
Shows different types of angles with measurements
"""

import shapix

def main():
    # Create various angles
    geometry = '''
    # Acute angle (45 degrees)
    POINT P1 -100 0 "P1" show_label=true label_position=left
    POINT V1 -50 0 "V1" show_label=true label_position=bottom
    POINT P2 -15 35 "P2" show_label=true label_position=top_right
    ANGLE P1 V1 P2 color=green arc=true show_measure=true
    
    # Right angle (90 degrees)  
    POINT P3 0 0 "P3" show_label=true label_position=left
    POINT V2 50 0 "V2" show_label=true label_position=bottom
    POINT P4 50 50 "P4" show_label=true label_position=top
    ANGLE P3 V2 P4 color=blue arc=true show_measure=true
    
    # Obtuse angle (135 degrees)
    POINT P5 100 0 "P5" show_label=true label_position=right
    POINT V3 150 0 "V3" show_label=true label_position=bottom  
    POINT P6 115 35 "P6" show_label=true label_position=top_left
    ANGLE P5 V3 P6 color=red arc=true show_measure=true
    '''
    
    # Export to PNG
    shapix.export_geometry_syntax(geometry, "angles_demo.png", 800, 400)
    
    print("✓ Angles demonstration example created")
    print(f"  Output: examples/basic/angles_demo.png")

if __name__ == "__main__":
    main()