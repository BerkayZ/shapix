"""
Circle shape implementation for shapix
"""

import math
from typing import List, Tuple, Any
from ..core.base import GeometricShape, Point


class Circle(GeometricShape):
    """A circle with center and radius"""
    
    def __init__(self, center: Point = None, radius: float = 50, name: str = ""):
        super().__init__(name)
        self.center = center or Point(0, 0, "O")
        self.radius = max(1, radius)
        self.label = ""
        self.show_center = True
        self.show_radius_line = False
        self.show_diameter = False
    
    def get_area(self) -> float:
        """Calculate the area of the circle"""
        return math.pi * self.radius * self.radius
    
    def get_circumference(self) -> float:
        """Calculate the circumference of the circle"""
        return 2 * math.pi * self.radius
    
    def get_diameter(self) -> float:
        """Get the diameter of the circle"""
        return self.radius * 2
    
    def set_diameter(self, diameter: float) -> None:
        """Set the diameter (updates radius)"""
        self.radius = max(0.5, diameter / 2)
    
    def get_points(self) -> List[Point]:
        """Get the center point of the circle"""
        return [self.center]
    
    def set_points(self, points: List[Point]) -> None:
        """Set the center point of the circle"""
        if points:
            self.center = points[0]
    
    def get_bounds(self) -> Tuple[float, float, float, float]:
        """Get bounding box of the circle"""
        return (
            self.center.x - self.radius, 
            self.center.y - self.radius,
            self.center.x + self.radius, 
            self.center.y + self.radius
        )
    
    def contains_point(self, point: Point) -> bool:
        """Check if point is inside the circle"""
        return self.center.distance_to(point) <= self.radius
    
    def point_on_circumference(self, point: Point, tolerance: float = 5) -> bool:
        """Check if point is on the circle's circumference"""
        distance = self.center.distance_to(point)
        return abs(distance - self.radius) <= tolerance
    
    def get_point_at_angle(self, angle_degrees: float) -> Point:
        """Get a point on the circumference at the given angle"""
        angle_rad = math.radians(angle_degrees)
        x = self.center.x + self.radius * math.cos(angle_rad)
        y = self.center.y + self.radius * math.sin(angle_rad)
        return Point(x, y)
    
    def set_property(self, key: str, value: Any) -> None:
        """Set property with circle-specific handling"""
        if key == 'center_x':
            self.center.x = value
        elif key == 'center_y':
            self.center.y = value
        elif key == 'center_label':
            self.center.label = value
        elif key == 'radius':
            self.radius = max(1, value)
        elif key == 'diameter':
            self.set_diameter(value)
        elif key == 'center':
            self.show_center = bool(value)
        elif key in ['label', 'show_center', 'show_radius_line', 'show_diameter']:
            setattr(self, key, value)
        else:
            super().set_property(key, value)
    
    def get_property(self, key: str, default: Any = None) -> Any:
        """Get property with circle-specific handling"""
        if key == 'center_x':
            return self.center.x
        elif key == 'center_y':
            return self.center.y
        elif key == 'center_label':
            return self.center.label
        elif key == 'radius':
            return self.radius
        elif key == 'diameter':
            return self.get_diameter()
        elif key == 'area':
            return self.get_area()
        elif key == 'circumference':
            return self.get_circumference()
        elif key in ['label', 'show_center', 'show_radius_line', 'show_diameter']:
            return getattr(self, key)
        else:
            return super().get_property(key, default)
    
    def copy(self) -> 'Circle':
        """Create a deep copy of this circle"""
        new_circle = Circle(self.center.copy(), self.radius, f"{self.name}_copy")
        new_circle.label = self.label
        new_circle.show_center = self.show_center
        new_circle.show_radius_line = self.show_radius_line
        new_circle.show_diameter = self.show_diameter
        new_circle.visible = self.visible
        new_circle.color = self.color
        new_circle.fill_color = self.fill_color
        new_circle.line_width = self.line_width
        new_circle.line_style = self.line_style
        new_circle.layer = self.layer
        new_circle.font_size = self.font_size
        new_circle.text_color = self.text_color
        new_circle._properties = self._properties.copy()
        return new_circle