"""
Sample geometry fixtures for testing
"""

# Basic geometric shapes
SIMPLE_TRIANGLE = '''
POINT A 0 0 "A" show_label=true
POINT B 10 0 "B" show_label=true
POINT C 5 8.66 "C" show_label=true
TRIANGLE A B C color=blue show_vertices=true
'''

CIRCLE_WITH_POINTS = '''
POINT O 0 0 "O" show_label=true label_position=center
CIRCLE O 50 color=navy show_center=true
POINT A 50 0 "A" show_label=true label_position=right
POINT B 0 50 "B" show_label=true label_position=top
POINT C -50 0 "C" show_label=true label_position=left
POINT D 0 -50 "D" show_label=true label_position=bottom
'''

RIGHT_TRIANGLE = '''
POINT A 0 0 "A" show_label=true
POINT B 3 0 "B" show_label=true
POINT C 0 4 "C" show_label=true
TRIANGLE A B C color=red show_vertices=true show_angles=true
'''

# Advanced constructions
INSCRIBED_TRIANGLE = '''
POINT O 0 0 "O" show_label=true label_position=center
CIRCLE O 100 color=blue
POINT A 0 100 "A" show_label=true label_position=top
POINT B -86.6 -50 "B" show_label=true label_position=bottom_left
POINT C 86.6 -50 "C" show_label=true label_position=bottom_right
TRIANGLE A B C color=green fill_color=lightgreen show_vertices=true
LINE O A color=red
LINE O B color=red
LINE O C color=red
'''

COMPLEX_CONSTRUCTION = '''
# Complex geometric construction
POINT O 0 0 "O" show_label=true label_position=bottom_right
CIRCLE O 200 color=black

POINT A 0 200 "A" show_label=true label_position=top
POINT D 0 -200 "D" show_label=true label_position=bottom
POINT C -153.2 -128.6 "C" show_label=true label_position=bottom_left
POINT B -174 100 "B" show_label=true label_position=top_left
POINT E 173.2 -100 "E" show_label=true label_position=bottom_right
POINT F 0 -57.8 "F" show_label=true label_position=right

LINE A D color=black
LINE O C color=black
LINE A B color=black
LINE B E color=black
LINE C D color=black
LINE A E color=black

ANGLE C O D color=red arc=true show_measure=true
ANGLE D A E color=green arc=true show_measure=true
ANGLE D F E color=orange arc=true show_measure=true
'''

# Educational examples
PYTHAGOREAN_DEMO = '''
# Right triangle with squares on sides
POINT A 0 0 "A" show_label=true
POINT B 60 0 "B" show_label=true
POINT C 0 45 "C" show_label=true

TRIANGLE A B C color=red show_vertices=true

# Square on side AB
POINT B1 60 -60 "B₁" show_label=true
POINT B2 0 -60 "B₂" show_label=true
LINE A B2 color=blue
LINE B2 B1 color=blue
LINE B1 B color=blue

# Square on side AC
POINT C1 -45 0 "C₁" show_label=true
POINT C2 -45 45 "C₂" show_label=true
LINE A C1 color=green
LINE C1 C2 color=green
LINE C2 C color=green
'''

ANGLE_TYPES = '''
# Different types of angles
POINT P1 -100 0 "P₁" show_label=true
POINT V1 -50 0 "V₁" show_label=true
POINT P2 -15 35 "P₂" show_label=true
ANGLE P1 V1 P2 color=green arc=true show_measure=true

POINT P3 0 0 "P₃" show_label=true
POINT V2 50 0 "V₂" show_label=true
POINT P4 50 50 "P₄" show_label=true
ANGLE P3 V2 P4 color=blue arc=true show_measure=true

POINT P5 100 0 "P₅" show_label=true
POINT V3 150 0 "V₃" show_label=true
POINT P6 115 35 "P₆" show_label=true
ANGLE P5 V3 P6 color=red arc=true show_measure=true
'''

# Test edge cases
MINIMAL_GEOMETRY = '''
POINT A 0 0 "A"
'''

SINGLE_SHAPE = '''
CIRCLE A 25 color=red
'''

OVERLAPPING_SHAPES = '''
POINT O 0 0 "O" show_label=true
CIRCLE O 50 color=red
CIRCLE O 40 color=blue  
CIRCLE O 30 color=green
POINT A 0 0 "A" show_label=true
'''

# Properties testing
STYLED_SHAPES = '''
POINT A 0 0 "A" show_label=true color=red font_size=16
POINT B 50 50 "B" show_label=true color=blue font_size=12
LINE A B color=purple line_width=3
CIRCLE A 25 color=orange fill_color=yellow
TRIANGLE A B A color=green fill_color=lightgreen
'''

# All sample geometries for easy access
SAMPLE_GEOMETRIES = {
    'simple_triangle': SIMPLE_TRIANGLE,
    'circle_with_points': CIRCLE_WITH_POINTS,
    'right_triangle': RIGHT_TRIANGLE,
    'inscribed_triangle': INSCRIBED_TRIANGLE,
    'complex_construction': COMPLEX_CONSTRUCTION,
    'pythagorean_demo': PYTHAGOREAN_DEMO,
    'angle_types': ANGLE_TYPES,
    'minimal_geometry': MINIMAL_GEOMETRY,
    'single_shape': SINGLE_SHAPE,
    'overlapping_shapes': OVERLAPPING_SHAPES,
    'styled_shapes': STYLED_SHAPES,
}