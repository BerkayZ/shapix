"""
Unit tests for syntax parsing and export
"""

import pytest
import os
from shapix.syntax import GeometrySyntaxParser, GeometryPNGExporter, export_geometry_syntax
from shapix.shapes import PointShape, Line, Circle, Triangle, Angle


class TestGeometrySyntaxParser:
    """Tests for GeometrySyntaxParser class"""
    
    def test_parser_creation(self):
        """Test parser creation"""
        parser = GeometrySyntaxParser()
        assert len(parser.shapes) == 0
        assert len(parser.points) == 0
        assert len(parser.named_shapes) == 0
    
    def test_parse_point(self):
        """Test parsing point definitions"""
        parser = GeometrySyntaxParser()
        syntax = 'POINT A 10 20 "TestPoint" show_label=true label_position=top'
        
        shapes = parser.parse(syntax)
        
        assert len(shapes) == 1
        assert isinstance(shapes[0], PointShape)
        assert shapes[0].point.x == 10
        assert shapes[0].point.y == 20
        assert shapes[0].point.label == "TestPoint"
        assert shapes[0].point.show_label == True
        assert shapes[0].point.label_position == "top"
    
    def test_parse_line(self):
        """Test parsing line definitions"""
        parser = GeometrySyntaxParser()
        syntax = '''
        POINT A 0 0 "A"
        POINT B 10 10 "B"
        LINE A B color=red show_endpoints=true
        '''
        
        shapes = parser.parse(syntax)
        
        # Should have 2 points + 1 line = 3 shapes
        assert len(shapes) == 3
        line_shapes = [s for s in shapes if isinstance(s, Line)]
        assert len(line_shapes) == 1
        
        line = line_shapes[0]
        assert line.color == "red"
        assert line.show_endpoints == True
    
    def test_parse_circle(self):
        """Test parsing circle definitions"""
        parser = GeometrySyntaxParser()
        syntax = '''
        POINT O 0 0 "Origin"
        CIRCLE O 50 color=blue show_center=true
        '''
        
        shapes = parser.parse(syntax)
        
        circle_shapes = [s for s in shapes if isinstance(s, Circle)]
        assert len(circle_shapes) == 1
        
        circle = circle_shapes[0]
        assert circle.radius == 50
        assert circle.color == "blue"
        assert circle.show_center == True
    
    def test_parse_triangle(self):
        """Test parsing triangle definitions"""
        parser = GeometrySyntaxParser()
        syntax = '''
        POINT A 0 0 "A"
        POINT B 10 0 "B"
        POINT C 5 8 "C"
        TRIANGLE A B C color=green show_vertices=true
        '''
        
        shapes = parser.parse(syntax)
        
        triangle_shapes = [s for s in shapes if isinstance(s, Triangle)]
        assert len(triangle_shapes) == 1
        
        triangle = triangle_shapes[0]
        assert triangle.color == "green"
        assert triangle.show_vertices == True
    
    def test_parse_angle(self):
        """Test parsing angle definitions"""
        parser = GeometrySyntaxParser()
        syntax = '''
        POINT P1 -5 0 "P1"
        POINT V 0 0 "V"
        POINT P2 5 5 "P2"
        ANGLE P1 V P2 color=orange arc=true show_measure=true
        '''
        
        shapes = parser.parse(syntax)
        
        angle_shapes = [s for s in shapes if isinstance(s, Angle)]
        assert len(angle_shapes) == 1
        
        angle = angle_shapes[0]
        assert angle.color == "orange"
        assert angle.show_arc == True
        assert angle.show_measure == True
    
    def test_parse_comments_and_empty_lines(self):
        """Test handling comments and empty lines"""
        parser = GeometrySyntaxParser()
        syntax = '''
        # This is a comment
        POINT A 0 0 "A"
        
        # Another comment
        POINT B 10 10 "B"
        
        LINE A B color=red
        '''
        
        shapes = parser.parse(syntax)
        
        # Should ignore comments and empty lines
        assert len(shapes) == 3  # 2 points + 1 line
    
    def test_parse_properties(self):
        """Test parsing various properties"""
        parser = GeometrySyntaxParser()
        
        # Test different property types
        test_cases = [
            ('color=red', {'color': 'red'}),
            ('show_label=true', {'show_label': 'true'}),
            ('show_label=false', {'show_label': 'false'}),
            ('line_width=3', {'line_width': '3'}),
            ('font_size=14', {'font_size': '14'}),
            ('label_position=top_right', {'label_position': 'top_right'}),
        ]
        
        for prop_str, expected in test_cases:
            props = parser._parse_properties(f'POINT A 0 0 {prop_str}')
            for key, value in expected.items():
                assert props[key] == value
    
    def test_parse_bool_values(self):
        """Test parsing boolean values"""
        parser = GeometrySyntaxParser()
        
        true_values = ['true', 'True', '1', 'yes', 'on']
        false_values = ['false', 'False', '0', 'no', 'off']
        
        for value in true_values:
            assert parser._parse_bool(value) == True
        
        for value in false_values:
            assert parser._parse_bool(value) == False
    
    def test_complex_syntax_parsing(self, sample_geometry_syntax):
        """Test parsing complex geometry syntax"""
        parser = GeometrySyntaxParser()
        shapes = parser.parse(sample_geometry_syntax)
        
        # Should parse multiple types of shapes
        shape_types = [type(s).__name__ for s in shapes]
        
        assert 'PointShape' in shape_types
        assert 'Triangle' in shape_types
        assert 'Circle' in shape_types
        assert 'Line' in shape_types
        assert 'Angle' in shape_types
    
    def test_get_point_by_name(self):
        """Test retrieving points by name"""
        parser = GeometrySyntaxParser()
        syntax = 'POINT A 10 20 "TestPoint"'
        
        parser.parse(syntax)
        
        point = parser.get_point('A')
        assert point is not None
        assert point.x == 10
        assert point.y == 20
        
        # Non-existent point should return None
        assert parser.get_point('Z') is None


class TestGeometryPNGExporter:
    """Tests for GeometryPNGExporter class"""
    
    def test_exporter_creation(self):
        """Test exporter creation"""
        exporter = GeometryPNGExporter(800, 600)
        assert exporter.width == 800
        assert exporter.height == 600
        assert exporter.origin_x == 400
        assert exporter.origin_y == 300
        assert exporter.scale == 1.0
    
    def test_world_to_canvas_conversion(self):
        """Test coordinate conversion"""
        exporter = GeometryPNGExporter(800, 600)
        
        # Test center point
        canvas_x, canvas_y = exporter.world_to_canvas(0, 0)
        assert canvas_x == 400  # width // 2
        assert canvas_y == 300  # height // 2
        
        # Test other points
        canvas_x, canvas_y = exporter.world_to_canvas(100, 100)
        assert canvas_x == 500  # 400 + 100
        assert canvas_y == 200  # 300 - 100 (Y is flipped)
    
    def test_export_to_png(self, temp_dir, sample_geometry_syntax):
        """Test PNG export functionality"""
        output_file = os.path.join(temp_dir, "test_output.png")
        
        # This test mainly verifies the function doesn't crash
        # Actual PNG generation requires GUI components
        try:
            export_geometry_syntax(sample_geometry_syntax, output_file, 400, 300)
            # If we get here without exception, consider it a success
            assert True
        except Exception as e:
            # On systems without proper display, this might fail
            # We'll accept certain known exceptions
            if "DISPLAY" in str(e) or "Xlib" in str(e) or "tkinter" in str(e):
                pytest.skip("Skipping PNG export test - no display available")
            else:
                raise
    
    def test_auto_scaling(self):
        """Test auto-scaling functionality"""
        exporter = GeometryPNGExporter(800, 600)
        
        # Create shapes with known bounds
        from shapix.shapes import PointShape
        from shapix.core import Point
        
        shapes = [
            PointShape(Point(-100, -100), "p1"),
            PointShape(Point(100, 100), "p2"),
        ]
        
        exporter._auto_scale_shapes(shapes)
        
        # Scale should be calculated to fit content with padding
        assert exporter.scale > 0
        assert exporter.scale <= 2.0  # Max scale constraint


class TestSyntaxIntegration:
    """Integration tests for syntax parsing and export"""
    
    def test_parse_and_export_cycle(self, temp_dir):
        """Test complete parse -> export cycle"""
        syntax = '''
        POINT A 0 0 "A" show_label=true
        POINT B 50 0 "B" show_label=true
        LINE A B color=red
        '''
        
        # Parse syntax
        parser = GeometrySyntaxParser()
        shapes = parser.parse(syntax)
        
        assert len(shapes) == 3  # 2 points + 1 line
        
        # Export should work without errors
        output_file = os.path.join(temp_dir, "integration_test.png")
        try:
            export_geometry_syntax(syntax, output_file, 400, 300)
            assert True
        except Exception as e:
            if "DISPLAY" in str(e) or "tkinter" in str(e):
                pytest.skip("Skipping integration test - no display available")
            else:
                raise
    
    def test_syntax_error_handling(self):
        """Test handling of malformed syntax"""
        parser = GeometrySyntaxParser()
        
        # Test incomplete point definition
        malformed_syntax = "POINT A"  # Missing coordinates
        
        # Should not crash, but may not create shapes
        shapes = parser.parse(malformed_syntax)
        # We don't assert specific behavior for malformed input
        # as long as it doesn't crash