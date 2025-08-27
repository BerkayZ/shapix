"""
Unit tests for core classes (Point, GeometricShape)
"""

import pytest
import math
from shapix.core import Point, GeometricShape
from shapix.shapes import PointShape


class TestPoint:
    """Tests for Point class"""
    
    def test_point_creation(self):
        """Test basic point creation"""
        point = Point(10, 20, "TestPoint")
        assert point.x == 10
        assert point.y == 20
        assert point.label == "TestPoint"
        assert point.show_label == True
        assert point.label_position == "top_right"
    
    def test_point_defaults(self):
        """Test point creation with defaults"""
        point = Point(5, 15)
        assert point.x == 5
        assert point.y == 15
        assert point.label == ""
        assert point.show_label == True
        assert point.label_position == "top_right"
    
    def test_distance_to(self):
        """Test distance calculation"""
        point1 = Point(0, 0)
        point2 = Point(3, 4)
        distance = point1.distance_to(point2)
        assert abs(distance - 5.0) < 1e-10
    
    def test_angle_to(self):
        """Test angle calculation"""
        origin = Point(0, 0)
        point_right = Point(10, 0)
        point_up = Point(0, 10)
        point_diagonal = Point(10, 10)
        
        assert abs(origin.angle_to(point_right) - 0) < 1e-10
        assert abs(origin.angle_to(point_up) - 90) < 1e-10
        assert abs(origin.angle_to(point_diagonal) - 45) < 1e-10
    
    def test_point_move(self, sample_point):
        """Test point movement"""
        original_x, original_y = sample_point.x, sample_point.y
        sample_point.move(5, -3)
        
        assert sample_point.x == original_x + 5
        assert sample_point.y == original_y - 3
    
    def test_point_copy(self, sample_point):
        """Test point copying"""
        copy_point = sample_point.copy()
        
        assert copy_point.x == sample_point.x
        assert copy_point.y == sample_point.y
        assert copy_point.label == sample_point.label
        assert copy_point.show_label == sample_point.show_label
        assert copy_point.label_position == sample_point.label_position
        
        # Ensure it's a deep copy
        copy_point.x = 999
        assert sample_point.x != 999
    
    def test_point_equality(self):
        """Test point equality"""
        point1 = Point(10, 20)
        point2 = Point(10, 20)
        point3 = Point(10, 21)
        
        assert point1 == point2
        assert point1 != point3
        assert point1 != "not_a_point"
    
    def test_point_hash(self):
        """Test point hashing"""
        point1 = Point(10, 20)
        point2 = Point(10, 20)
        point3 = Point(10, 21)
        
        assert hash(point1) == hash(point2)
        assert hash(point1) != hash(point3)
        
        # Test in set
        point_set = {point1, point2, point3}
        assert len(point_set) == 2  # point1 and point2 should be same


class TestGeometricShape:
    """Tests for GeometricShape base class"""
    
    def test_shape_creation(self, sample_point_shape):
        """Test basic shape creation"""
        assert sample_point_shape.name == "test_point_shape"
        assert sample_point_shape.visible == True
        assert sample_point_shape.selected == False
        assert sample_point_shape.color == "black"
        assert sample_point_shape.layer == 0
    
    def test_shape_properties(self, sample_point_shape):
        """Test shape property management"""
        # Test setting existing properties
        sample_point_shape.set_property("color", "red")
        assert sample_point_shape.color == "red"
        
        # Test setting custom properties
        sample_point_shape.set_property("custom_prop", "custom_value")
        assert sample_point_shape.get_property("custom_prop") == "custom_value"
        
        # Test getting with default
        assert sample_point_shape.get_property("nonexistent", "default") == "default"
    
    def test_shape_get_properties(self, sample_point_shape):
        """Test getting all properties"""
        props = sample_point_shape.get_properties()
        
        assert "id" in props
        assert "name" in props
        assert "visible" in props
        assert "color" in props
        assert props["name"] == "test_point_shape"
        assert props["visible"] == True
    
    def test_shape_move(self, sample_point_shape):
        """Test shape movement"""
        original_point = sample_point_shape.point.copy()
        sample_point_shape.move(10, -5)
        
        assert sample_point_shape.point.x == original_point.x + 10
        assert sample_point_shape.point.y == original_point.y - 5
    
    def test_shape_copy(self, sample_point_shape):
        """Test shape copying"""
        copy_shape = sample_point_shape.copy()
        
        assert copy_shape.name == f"{sample_point_shape.name}_copy"
        assert copy_shape.color == sample_point_shape.color
        assert copy_shape.visible == sample_point_shape.visible
        
        # Ensure deep copy
        copy_shape.color = "blue"
        assert sample_point_shape.color != "blue"
    
    def test_shape_str_repr(self, sample_point_shape):
        """Test string representation"""
        str_repr = str(sample_point_shape)
        assert "PointShape" in str_repr
        assert "test_point_shape" in str_repr
        
        # repr should be same as str
        assert repr(sample_point_shape) == str(sample_point_shape)