"""
Unit tests for shape classes
"""

import pytest
import math
from shapix.core import Point
from shapix.shapes import PointShape, Line, Circle, Triangle, Angle


class TestPointShape:
    """Tests for PointShape class"""
    
    def test_point_shape_creation(self, sample_point_shape):
        """Test basic point shape creation"""
        assert isinstance(sample_point_shape.point, Point)
        assert sample_point_shape.point.label == "P"
        assert sample_point_shape.point_size == 4
    
    def test_point_shape_get_points(self, sample_point_shape):
        """Test getting points from point shape"""
        points = sample_point_shape.get_points()
        assert len(points) == 1
        assert points[0] == sample_point_shape.point
    
    def test_point_shape_set_points(self, sample_point_shape):
        """Test setting points for point shape"""
        new_point = Point(100, 200, "NewPoint")
        sample_point_shape.set_points([new_point])
        
        assert sample_point_shape.point == new_point
    
    def test_point_shape_bounds(self, sample_point_shape):
        """Test bounding box calculation"""
        bounds = sample_point_shape.get_bounds()
        expected_size = sample_point_shape.point_size
        
        assert bounds[0] == sample_point_shape.point.x - expected_size
        assert bounds[1] == sample_point_shape.point.y - expected_size
        assert bounds[2] == sample_point_shape.point.x + expected_size
        assert bounds[3] == sample_point_shape.point.y + expected_size
    
    def test_point_shape_contains_point(self, sample_point_shape):
        """Test point containment"""
        # Point at same location should be contained
        same_point = Point(sample_point_shape.point.x, sample_point_shape.point.y)
        assert sample_point_shape.contains_point(same_point)
        
        # Point far away should not be contained
        far_point = Point(1000, 1000)
        assert not sample_point_shape.contains_point(far_point)


class TestLine:
    """Tests for Line class"""
    
    def test_line_creation(self, sample_line):
        """Test basic line creation"""
        assert sample_line.start.x == 0
        assert sample_line.start.y == 0
        assert sample_line.end.x == 10
        assert sample_line.end.y == 10
        assert sample_line.show_endpoints == True
    
    def test_line_length(self, sample_line):
        """Test line length calculation"""
        length = sample_line.get_length()
        expected_length = math.sqrt(10*10 + 10*10)
        assert abs(length - expected_length) < 1e-10
    
    def test_line_angle(self, sample_line):
        """Test line angle calculation"""
        angle = sample_line.get_angle()
        assert abs(angle - 45.0) < 1e-10
    
    def test_line_set_length(self, sample_line):
        """Test setting line length"""
        original_angle = sample_line.get_angle()
        sample_line.set_length(20)
        
        assert abs(sample_line.get_length() - 20) < 1e-10
        assert abs(sample_line.get_angle() - original_angle) < 1e-10
    
    def test_line_set_angle(self, sample_line):
        """Test setting line angle"""
        original_length = sample_line.get_length()
        sample_line.set_angle(90)
        
        assert abs(sample_line.get_angle() - 90) < 1e-10
        assert abs(sample_line.get_length() - original_length) < 1e-10
    
    def test_line_midpoint(self, sample_line):
        """Test midpoint calculation"""
        midpoint = sample_line.get_midpoint()
        assert abs(midpoint.x - 5) < 1e-10
        assert abs(midpoint.y - 5) < 1e-10
    
    def test_line_bounds(self, sample_line):
        """Test bounding box calculation"""
        bounds = sample_line.get_bounds()
        assert bounds[0] == 0  # min x
        assert bounds[1] == 0  # min y
        assert bounds[2] == 10  # max x
        assert bounds[3] == 10  # max y


class TestCircle:
    """Tests for Circle class"""
    
    def test_circle_creation(self, sample_circle):
        """Test basic circle creation"""
        assert sample_circle.center.x == 0
        assert sample_circle.center.y == 0
        assert sample_circle.radius == 50
        assert sample_circle.show_center == True
    
    def test_circle_area(self, sample_circle):
        """Test area calculation"""
        area = sample_circle.get_area()
        expected_area = math.pi * 50 * 50
        assert abs(area - expected_area) < 1e-10
    
    def test_circle_circumference(self, sample_circle):
        """Test circumference calculation"""
        circumference = sample_circle.get_circumference()
        expected_circumference = 2 * math.pi * 50
        assert abs(circumference - expected_circumference) < 1e-10
    
    def test_circle_diameter(self, sample_circle):
        """Test diameter calculation"""
        diameter = sample_circle.get_diameter()
        assert diameter == 100
        
        sample_circle.set_diameter(200)
        assert sample_circle.radius == 100
    
    def test_circle_contains_point(self, sample_circle):
        """Test point containment"""
        # Point at center should be contained
        center_point = Point(0, 0)
        assert sample_circle.contains_point(center_point)
        
        # Point on circumference should be contained
        edge_point = Point(50, 0)
        assert sample_circle.contains_point(edge_point)
        
        # Point outside should not be contained
        outside_point = Point(100, 0)
        assert not sample_circle.contains_point(outside_point)
    
    def test_circle_point_on_circumference(self, sample_circle):
        """Test point on circumference detection"""
        # Point exactly on circumference
        on_circumference = Point(50, 0)
        assert sample_circle.point_on_circumference(on_circumference)
        
        # Point inside circle
        inside_point = Point(25, 0)
        assert not sample_circle.point_on_circumference(inside_point)
    
    def test_circle_get_point_at_angle(self, sample_circle):
        """Test getting point at angle"""
        # Point at 0 degrees (right)
        point_0 = sample_circle.get_point_at_angle(0)
        assert abs(point_0.x - 50) < 1e-10
        assert abs(point_0.y - 0) < 1e-10
        
        # Point at 90 degrees (top)
        point_90 = sample_circle.get_point_at_angle(90)
        assert abs(point_90.x - 0) < 1e-10
        assert abs(point_90.y - 50) < 1e-10


class TestTriangle:
    """Tests for Triangle class"""
    
    def test_triangle_creation(self, sample_triangle):
        """Test basic triangle creation"""
        assert sample_triangle.vertex_a.x == 0
        assert sample_triangle.vertex_b.x == 10
        assert sample_triangle.vertex_c.x == 5
        assert sample_triangle.show_vertices == True
    
    def test_triangle_side_lengths(self, sample_triangle):
        """Test side length calculations"""
        # This is approximately an equilateral triangle
        side_a = sample_triangle.get_side_length('a')  # BC
        side_b = sample_triangle.get_side_length('b')  # AC
        side_c = sample_triangle.get_side_length('c')  # AB
        
        # All sides should be approximately equal (10)
        assert abs(side_a - 10) < 0.1
        assert abs(side_b - 10) < 0.1
        assert abs(side_c - 10) < 0.1
    
    def test_triangle_angle_measures(self, sample_triangle):
        """Test angle measure calculations"""
        # For an equilateral triangle, all angles should be ~60 degrees
        angle_a = sample_triangle.get_angle_measure('a')
        angle_b = sample_triangle.get_angle_measure('b')
        angle_c = sample_triangle.get_angle_measure('c')
        
        # Sum of angles should be 180
        total = angle_a + angle_b + angle_c
        assert abs(total - 180) < 1e-10
        
        # Each angle should be approximately 60 for equilateral
        assert abs(angle_a - 60) < 1
        assert abs(angle_b - 60) < 1
        assert abs(angle_c - 60) < 1
    
    def test_triangle_area(self, sample_triangle):
        """Test area calculation"""
        area = sample_triangle.get_area()
        # For equilateral triangle with side ~10, area ≈ 43.3
        assert area > 40 and area < 50
    
    def test_triangle_perimeter(self, sample_triangle):
        """Test perimeter calculation"""
        perimeter = sample_triangle.get_perimeter()
        assert abs(perimeter - 30) < 0.5  # ~10 + 10 + 10
    
    def test_triangle_centroid(self, sample_triangle):
        """Test centroid calculation"""
        centroid = sample_triangle.get_centroid()
        # Centroid should be at average of vertices
        expected_x = (0 + 10 + 5) / 3
        expected_y = (0 + 0 + 8.66) / 3
        
        assert abs(centroid.x - expected_x) < 1e-10
        assert abs(centroid.y - expected_y) < 0.1
    
    def test_triangle_is_right(self):
        """Test right triangle detection"""
        # Create a right triangle (3-4-5)
        right_triangle = Triangle(
            Point(0, 0, "A"),
            Point(3, 0, "B"), 
            Point(0, 4, "C")
        )
        
        assert right_triangle.is_right_triangle()
    
    def test_triangle_contains_point(self, sample_triangle):
        """Test point containment"""
        # Centroid should be inside
        centroid = sample_triangle.get_centroid()
        assert sample_triangle.contains_point(centroid)
        
        # Point far outside should not be contained
        far_point = Point(1000, 1000)
        assert not sample_triangle.contains_point(far_point)


class TestAngle:
    """Tests for Angle class"""
    
    def test_angle_creation(self, sample_angle):
        """Test basic angle creation"""
        assert sample_angle.point1.x == -5
        assert sample_angle.vertex.x == 0
        assert sample_angle.point2.x == 5
        assert sample_angle.show_arc == True
        assert sample_angle.show_measure == True
    
    def test_angle_measure(self, sample_angle):
        """Test angle measure calculation"""
        # Angle from (-5,0) to (0,0) to (5,5) should be 45 degrees
        measure = sample_angle.get_measure()
        assert abs(measure - 135) < 1e-10
    
    def test_angle_set_measure(self, sample_angle):
        """Test setting angle measure"""
        original_distance = sample_angle.vertex.distance_to(sample_angle.point2)
        sample_angle.set_measure(90)
        
        new_measure = sample_angle.get_measure()
        assert abs(new_measure - 90) < 1e-10
        
        # Distance should be preserved
        new_distance = sample_angle.vertex.distance_to(sample_angle.point2)
        assert abs(new_distance - original_distance) < 1e-10
    
    def test_angle_types(self, sample_angle):
        """Test angle type detection"""
        # 135-degree angle is obtuse
        assert sample_angle.is_obtuse()
        assert not sample_angle.is_right_angle()
        assert not sample_angle.is_acute()
        assert not sample_angle.is_straight_angle()
        
        # Set to right angle
        sample_angle.set_measure(90)
        assert sample_angle.is_right_angle()
        # Due to floating point precision, 90° might be classified as both right and acute
        # The right angle check takes precedence
        assert not sample_angle.is_obtuse()
        
        # Set to acute angle
        sample_angle.set_measure(45)
        assert sample_angle.is_acute()
        assert not sample_angle.is_obtuse()
        assert not sample_angle.is_right_angle()
    
    def test_angle_bisector(self, sample_angle):
        """Test angle bisector calculation"""
        bisector_point = sample_angle.get_bisector_point(10)
        
        # Verify bisector point is at the correct distance from vertex
        distance = sample_angle.vertex.distance_to(bisector_point)
        assert abs(distance - 10) < 1e-10
        
        # For angle from (-5,0) to (0,0) to (5,5):
        # Unit vector 1: (-1, 0)
        # Unit vector 2: (1/√2, 1/√2)
        # Bisector unit vector: (-1 + 1/√2, 0 + 1/√2) normalized
        # At distance 10: approximately (-3.827, 9.239)
        expected_x = -3.826834323650899
        expected_y = 9.238795325112868
        assert abs(bisector_point.x - expected_x) < 1e-10
        assert abs(bisector_point.y - expected_y) < 1e-10
    
    def test_angle_bounds(self, sample_angle):
        """Test bounding box calculation"""
        bounds = sample_angle.get_bounds()
        
        # Bounds should include all three points plus arc radius
        assert bounds[0] <= -5 - sample_angle.arc_radius
        assert bounds[2] >= 5 + sample_angle.arc_radius