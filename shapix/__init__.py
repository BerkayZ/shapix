"""
Shapix - A geometry engine for Python

Shapix provides a simple, text-based syntax for creating geometric shapes
and exporting them to PNG images. It includes a comprehensive set of 
geometric shapes and mathematical operations.
"""

from .core import Point, GeometricShape
from .shapes import PointShape, Line, Circle, Triangle, Angle
from .syntax import GeometrySyntaxParser, export_geometry_syntax
from .rendering import ShapeRenderer

__version__ = "0.1.0"
__author__ = "BerkayZ"
__email__ = "zelyurtberkay@gmail.com"

__all__ = [
    # Core classes
    'Point',
    'GeometricShape',
    
    # Shape classes
    'PointShape',
    'Line',
    'Circle', 
    'Triangle',
    'Angle',
    
    # Syntax and export
    'GeometrySyntaxParser',
    'export_geometry_syntax',
    
    # Rendering
    'ShapeRenderer',
    
    # Package info
    '__version__',
    '__author__',
    '__email__',
]

def create_point(x: float, y: float, label: str = "") -> Point:
    """Convenience function to create a point"""
    return Point(x, y, label)

def create_circle(center_x: float = 0, center_y: float = 0, radius: float = 50, label: str = "O") -> Circle:
    """Convenience function to create a circle"""
    center = Point(center_x, center_y, label)
    return Circle(center, radius)

def create_triangle(x1: float, y1: float, x2: float, y2: float, x3: float, y3: float, 
                   labels: tuple = ("A", "B", "C")) -> Triangle:
    """Convenience function to create a triangle"""
    vertex_a = Point(x1, y1, labels[0])
    vertex_b = Point(x2, y2, labels[1])  
    vertex_c = Point(x3, y3, labels[2])
    return Triangle(vertex_a, vertex_b, vertex_c)

def quick_export(syntax: str, filename: str = "output.png", width: int = 800, height: int = 600) -> None:
    """Quick export function for geometry syntax"""
    export_geometry_syntax(syntax, filename, width, height)