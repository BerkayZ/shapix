"""
Integration tests for end-to-end workflows
"""

import pytest
import os
import tempfile
from shapix import (
    export_geometry_syntax, 
    create_point, 
    create_circle, 
    create_triangle,
    GeometrySyntaxParser,
    Point
)


class TestEndToEndWorkflows:
    """End-to-end integration tests"""
    
    def test_complete_geometry_creation_and_export(self, temp_dir):
        """Test complete workflow from syntax to PNG export"""
        # Define a complete geometry problem
        geometry = '''
        # Complete geometric construction
        POINT O 0 0 "O" show_label=true label_position=center
        POINT A 80 0 "A" show_label=true label_position=right
        POINT B 0 80 "B" show_label=true label_position=top
        POINT C -80 0 "C" show_label=true label_position=left
        POINT D 0 -80 "D" show_label=true label_position=bottom
        
        # Main circle
        CIRCLE O 80 color=navy show_center=true
        
        # Inscribed square
        LINE A B color=red
        LINE B C color=red
        LINE C D color=red
        LINE D A color=red
        
        # Diagonals
        LINE A C color=blue
        LINE B D color=blue
        
        # Angles
        ANGLE A O B color=green arc=true show_measure=true
        ANGLE B O C color=green arc=true show_measure=true
        '''
        
        output_file = os.path.join(temp_dir, "complete_geometry.png")
        
        try:
            # Parse and export
            export_geometry_syntax(geometry, output_file, 600, 600)
            
            # Verify parser worked correctly
            parser = GeometrySyntaxParser()
            shapes = parser.parse(geometry)
            
            # Should have created all expected shapes
            assert len(shapes) > 10  # Points + circle + lines + angles
            
            # Verify specific shape types
            shape_types = [type(s).__name__ for s in shapes]
            assert 'PointShape' in shape_types
            assert 'Circle' in shape_types
            assert 'Line' in shape_types
            assert 'Angle' in shape_types
            
        except Exception as e:
            if "DISPLAY" in str(e) or "tkinter" in str(e):
                pytest.skip("Skipping end-to-end test - no display available")
            else:
                raise
    
    def test_programmatic_api_workflow(self):
        """Test complete workflow using programmatic API"""
        # Create geometry programmatically
        center = create_point(0, 0, "Center")
        circle = create_circle(0, 0, 50, "O")
        triangle = create_triangle(-40, -30, 40, -30, 0, 40, ("A", "B", "C"))
        
        # Set properties
        circle.color = "blue"
        circle.show_center = True
        
        triangle.color = "red"
        triangle.show_vertices = True
        triangle.show_angles = True
        
        # Test calculations
        area = triangle.get_area()
        perimeter = triangle.get_perimeter()
        
        assert area > 0
        assert perimeter > 0
        
        # Test circle properties
        circle_area = circle.get_area()
        circumference = circle.get_circumference()
        
        assert circle_area > 0
        assert circumference > 0
    
    def test_mathematical_relationships(self):
        """Test mathematical relationships between shapes"""
        # Create right triangle
        right_triangle = create_triangle(0, 0, 3, 0, 0, 4, ("A", "B", "C"))
        
        # Verify it's a right triangle
        assert right_triangle.is_right_triangle()
        
        # Verify Pythagorean theorem: a² + b² = c²
        side_a = right_triangle.get_side_length('a')  # BC = 5
        side_b = right_triangle.get_side_length('b')  # AC = 4  
        side_c = right_triangle.get_side_length('c')  # AB = 3
        
        # Find hypotenuse (longest side)
        sides = [side_a, side_b, side_c]
        sides.sort()
        
        # Verify Pythagorean theorem
        assert abs(sides[0]**2 + sides[1]**2 - sides[2]**2) < 1e-10
        
        # Test inscribed circle relationships
        circle = create_circle(0, 0, 100)
        
        # Points on circumference
        point_0 = circle.get_point_at_angle(0)    # (100, 0)
        point_90 = circle.get_point_at_angle(90)  # (0, 100)
        point_180 = circle.get_point_at_angle(180)  # (-100, 0)
        
        # All should be on circumference
        assert circle.point_on_circumference(point_0)
        assert circle.point_on_circumference(point_90)
        assert circle.point_on_circumference(point_180)
        
        # Distance from center should equal radius
        assert abs(circle.center.distance_to(point_0) - 100) < 1e-10
        assert abs(circle.center.distance_to(point_90) - 100) < 1e-10
    
    def test_complex_construction_workflow(self):
        """Test complex geometric construction"""
        # Recreate the original math problem structure
        construction_syntax = '''
        # Complex geometric construction
        POINT O 0 0 "O" show_label=true
        POINT A 0 100 "A" show_label=true label_position=top
        POINT D 0 -100 "D" show_label=true label_position=bottom
        POINT C -76.6 -64.3 "C" show_label=true label_position=bottom_left
        POINT B -87 50 "B" show_label=true label_position=top_left
        POINT E 86.6 -50 "E" show_label=true label_position=bottom_right
        POINT F 0 -28.9 "F" show_label=true label_position=right
        
        CIRCLE O 100 color=black
        
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
        
        # Parse the construction
        parser = GeometrySyntaxParser()
        shapes = parser.parse(construction_syntax)
        
        # Verify all components are present
        points = [s for s in shapes if s.__class__.__name__ == 'PointShape']
        circles = [s for s in shapes if s.__class__.__name__ == 'Circle']
        lines = [s for s in shapes if s.__class__.__name__ == 'Line']
        angles = [s for s in shapes if s.__class__.__name__ == 'Angle']
        
        assert len(points) == 7  # O, A, D, C, B, E, F
        assert len(circles) == 1  # Main circle
        assert len(lines) == 6   # Various construction lines
        assert len(angles) == 3  # Three marked angles
        
        # Test mathematical properties
        main_circle = circles[0]
        assert main_circle.radius == 100
        assert main_circle.get_area() > 30000  # π * 100²
    
    def test_error_recovery(self):
        """Test error handling and recovery"""
        # Test with partially malformed syntax
        problematic_syntax = '''
        POINT A 0 0 "A"
        POINT B 10 10 "B"
        LINE A B color=red
        
        # This line has invalid syntax
        INVALID_SHAPE X Y Z
        
        # But this should still work
        CIRCLE A 25 color=blue
        '''
        
        parser = GeometrySyntaxParser()
        shapes = parser.parse(problematic_syntax)
        
        # Should have parsed the valid parts
        assert len(shapes) >= 3  # At least the valid shapes
        
        # Should have points, line, and circle
        shape_types = [type(s).__name__ for s in shapes]
        assert 'PointShape' in shape_types
        assert 'Line' in shape_types
        assert 'Circle' in shape_types
    
    def test_property_inheritance_and_overrides(self):
        """Test property inheritance and override behavior"""
        syntax = '''
        POINT A 0 0 "A" show_label=true color=red font_size=16
        POINT B 10 10 "B" show_label=true color=blue
        LINE A B color=green line_width=3
        TRIANGLE A B A color=purple fill_color=pink
        '''
        
        parser = GeometrySyntaxParser()
        shapes = parser.parse(syntax)
        
        # Find specific shapes and verify properties
        points = [s for s in shapes if s.__class__.__name__ == 'PointShape']
        lines = [s for s in shapes if s.__class__.__name__ == 'Line']
        triangles = [s for s in shapes if s.__class__.__name__ == 'Triangle']
        
        # Verify point properties
        point_a = next(s for s in points if s.point.label == 'A')
        point_b = next(s for s in points if s.point.label == 'B')
        
        assert point_a.color == "red"
        assert point_a.font_size == 16
        assert point_b.color == "blue"
        
        # Verify line properties
        if lines:
            line = lines[0]
            assert line.color == "green"
            assert line.line_width == 3
        
        # Verify triangle properties
        if triangles:
            triangle = triangles[0]
            assert triangle.color == "purple"
            assert triangle.fill_color == "pink"


class TestPerformanceAndScaling:
    """Performance and scaling integration tests"""
    
    def test_large_geometry_parsing(self):
        """Test parsing large geometry files"""
        # Generate a large geometry with many shapes
        large_syntax = "# Large geometry test\n"
        
        # Create a grid of points
        for i in range(20):
            for j in range(20):
                large_syntax += f'POINT P{i}_{j} {i*10} {j*10} "P{i}{j}" show_label=false\n'
        
        # Add some shapes connecting points
        for i in range(19):
            large_syntax += f'LINE P{i}_0 P{i+1}_0 color=blue\n'
            large_syntax += f'LINE P0_{i} P0_{i+1} color=red\n'
        
        # Parse the large geometry
        parser = GeometrySyntaxParser()
        shapes = parser.parse(large_syntax)
        
        # Should have created all shapes
        expected_points = 20 * 20  # 400 points
        expected_lines = 19 + 19   # 38 lines
        expected_total = expected_points + expected_lines
        
        assert len(shapes) == expected_total
    
    def test_memory_usage(self):
        """Test memory usage with multiple operations"""
        # Create and delete many shapes to test memory management
        for _ in range(100):
            # Create shapes
            triangle = create_triangle(0, 0, 10, 0, 5, 8)
            circle = create_circle(0, 0, 50)
            
            # Perform calculations
            triangle.get_area()
            triangle.get_perimeter()
            circle.get_area()
            circle.get_circumference()
            
            # Python garbage collection should handle cleanup
            del triangle
            del circle
        
        # If we reach here without memory issues, test passes
        assert True