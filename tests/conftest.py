"""
Pytest configuration and fixtures for shapix tests
"""

import pytest
import tempfile
import os
from shapix.core import Point
from shapix.shapes import PointShape, Line, Circle, Triangle, Angle


@pytest.fixture
def sample_point():
    """Create a sample point for testing"""
    return Point(10, 20, "TestPoint")


@pytest.fixture  
def sample_point_shape():
    """Create a sample point shape for testing"""
    point = Point(5, 15, "P")
    return PointShape(point, "test_point_shape")


@pytest.fixture
def sample_line():
    """Create a sample line for testing"""
    start = Point(0, 0, "A")
    end = Point(10, 10, "B")
    return Line(start, end, "test_line")


@pytest.fixture
def sample_circle():
    """Create a sample circle for testing"""
    center = Point(0, 0, "O")
    return Circle(center, 50, "test_circle")


@pytest.fixture
def sample_triangle():
    """Create a sample triangle for testing"""
    vertex_a = Point(0, 0, "A")
    vertex_b = Point(10, 0, "B")
    vertex_c = Point(5, 8.66, "C")
    return Triangle(vertex_a, vertex_b, vertex_c, "test_triangle")


@pytest.fixture
def sample_angle():
    """Create a sample angle for testing"""
    point1 = Point(-5, 0, "P1")
    vertex = Point(0, 0, "V")
    point2 = Point(5, 5, "P2")
    return Angle(point1, vertex, point2, "test_angle")


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def sample_geometry_syntax():
    """Sample geometry syntax for testing"""
    return '''
    # Test geometry
    POINT A 0 0 "A" show_label=true
    POINT B 10 0 "B" show_label=true  
    POINT C 5 8.66 "C" show_label=true
    
    TRIANGLE A B C color=blue show_vertices=true
    CIRCLE A 15 color=red
    LINE A B color=green
    ANGLE B A C color=orange arc=true show_measure=true
    '''