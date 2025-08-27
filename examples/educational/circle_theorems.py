"""
Educational Example: Circle Theorems
Demonstrates key circle theorems and properties
"""

import shapix

def main():
    # Inscribed angle theorem: inscribed angle = 1/2 central angle
    geometry = '''
    # Main circle
    POINT O 0 0 "O" show_label=true label_position=center
    CIRCLE O 200 color=navy
    
    # Points on circumference
    POINT A 70.7 70.7 "A" show_label=true label_position=top_right
    POINT B -100 0 "B" show_label=true label_position=left
    POINT C 70.7 -70.7 "C" show_label=true label_position=bottom_right
    POINT D 0 100 "D" show_label=true label_position=top
    
    # Central angle BOC
    ANGLE B O C color=red arc=true show_measure=true
    LINE O B color=red
    LINE O C color=red
    
    # Inscribed angle BAC (should be half of central angle)
    ANGLE B A C color=blue arc=true show_measure=true
    LINE A B color=blue
    LINE A C color=blue
    
    # Another inscribed angle BDC (same arc, same measure as BAC)
    ANGLE B D C color=green arc=true show_measure=true
    LINE D B color=green
    LINE D C color=green
    
    # Chord BC
    LINE B C color=purple
    '''
    
    # Export to PNG
    shapix.export_geometry_syntax(geometry, "circle_theorems.png", 600, 600)
    
    print("✓ Circle theorems demonstration created")
    print("  Demonstrates inscribed angle theorem:")
    print("  - Central angle BOC at center O")
    print("  - Inscribed angles BAC and BDC subtending same arc")  
    print("  - Inscribed angles should be half the central angle")
    print("  - All inscribed angles subtending same arc are equal")
    print(f"  Output: examples/educational/circle_theorems.png")

if __name__ == "__main__":
    main()