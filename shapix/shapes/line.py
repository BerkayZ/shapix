"""
Line and segment implementation for shapix
"""

import math
from typing import List, Tuple, Any
from ..core.base import GeometricShape, Point


class Line(GeometricShape):
    """A line segment between two points"""
    
    def __init__(self, start: Point = None, end: Point = None, name: str = ""):
        super().__init__(name)
        self.start = start or Point(0, 0)
        self.end = end or Point(100, 0)
        self.label = ""
        self.show_length = False
        self.show_endpoints = True
    
    def get_points(self) -> List[Point]:
        """Get the start and end points of the line"""
        return [self.start, self.end]
    
    def set_points(self, points: List[Point]) -> None:
        """Set the start and end points of the line"""
        if len(points) >= 2:
            self.start, self.end = points[0], points[1]
    
    def get_length(self) -> float:
        """Calculate the length of the line segment"""
        return self.start.distance_to(self.end)
    
    def get_angle(self) -> float:
        """Get the angle of the line in degrees"""
        return self.start.angle_to(self.end)
    
    def set_length(self, length: float) -> None:
        """Set the length while maintaining the angle"""
        if length <= 0:
            return
        angle_rad = math.radians(self.get_angle())
        self.end.x = self.start.x + length * math.cos(angle_rad)
        self.end.y = self.start.y + length * math.sin(angle_rad)
    
    def set_angle(self, angle_degrees: float) -> None:
        """Set the angle while maintaining the length"""
        length = self.get_length()
        angle_rad = math.radians(angle_degrees)
        self.end.x = self.start.x + length * math.cos(angle_rad)
        self.end.y = self.start.y + length * math.sin(angle_rad)
    
    def get_midpoint(self) -> Point:
        """Get the midpoint of the line segment"""
        return Point(
            (self.start.x + self.end.x) / 2,
            (self.start.y + self.end.y) / 2
        )
    
    def get_bounds(self) -> Tuple[float, float, float, float]:
        """Get bounding box of the line"""
        return (
            min(self.start.x, self.end.x), 
            min(self.start.y, self.end.y),
            max(self.start.x, self.end.x), 
            max(self.start.y, self.end.y)
        )
    
    def contains_point(self, point: Point) -> bool:
        """Check if point is close to the line segment"""
        def point_to_line_distance(p: Point, line_start: Point, line_end: Point) -> float:
            A = line_end.x - line_start.x
            B = line_end.y - line_start.y
            C = p.x - line_start.x
            D = p.y - line_start.y
            
            dot = A * C + B * D
            len_sq = A * A + B * B
            
            if len_sq == 0:
                return math.sqrt(C * C + D * D)
            
            param = dot / len_sq
            
            if param < 0:
                xx, yy = line_start.x, line_start.y
            elif param > 1:
                xx, yy = line_end.x, line_end.y
            else:
                xx = line_start.x + param * A
                yy = line_start.y + param * B
            
            return math.sqrt((p.x - xx)**2 + (p.y - yy)**2)
        
        return point_to_line_distance(point, self.start, self.end) <= 5
    
    def set_property(self, key: str, value: Any) -> None:
        """Set property with line-specific handling"""
        if key == 'start_x':
            self.start.x = value
        elif key == 'start_y':
            self.start.y = value
        elif key == 'end_x':
            self.end.x = value
        elif key == 'end_y':
            self.end.y = value
        elif key == 'length':
            self.set_length(value)
        elif key == 'angle':
            self.set_angle(value)
        elif key in ['label', 'show_length', 'show_endpoints']:
            setattr(self, key, value)
        else:
            super().set_property(key, value)
    
    def get_property(self, key: str, default: Any = None) -> Any:
        """Get property with line-specific handling"""
        if key == 'start_x':
            return self.start.x
        elif key == 'start_y':
            return self.start.y
        elif key == 'end_x':
            return self.end.x
        elif key == 'end_y':
            return self.end.y
        elif key == 'length':
            return self.get_length()
        elif key == 'angle':
            return self.get_angle()
        elif key in ['label', 'show_length', 'show_endpoints']:
            return getattr(self, key)
        else:
            return super().get_property(key, default)
    
    def copy(self) -> 'Line':
        """Create a deep copy of this line"""
        new_line = Line(self.start.copy(), self.end.copy(), f"{self.name}_copy")
        new_line.label = self.label
        new_line.show_length = self.show_length
        new_line.show_endpoints = self.show_endpoints
        new_line.visible = self.visible
        new_line.color = self.color
        new_line.fill_color = self.fill_color
        new_line.line_width = self.line_width
        new_line.line_style = self.line_style
        new_line.layer = self.layer
        new_line.font_size = self.font_size
        new_line.text_color = self.text_color
        new_line._properties = self._properties.copy()
        return new_line