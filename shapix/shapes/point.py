"""
Point shape implementation for shapix
"""

from typing import List, Tuple, Any
from ..core.base import GeometricShape, Point


class PointShape(GeometricShape):
    """A drawable point shape with label support"""
    
    def __init__(self, point: Point = None, name: str = ""):
        super().__init__(name)
        self.point = point or Point(0, 0, "P")
        self.point_size = 4
        
    def get_points(self) -> List[Point]:
        """Get the point that defines this shape"""
        return [self.point]
    
    def set_points(self, points: List[Point]) -> None:
        """Set the point that defines this shape"""
        if points:
            self.point = points[0]
    
    def get_bounds(self) -> Tuple[float, float, float, float]:
        """Get bounding box around the point"""
        return (
            self.point.x - self.point_size, 
            self.point.y - self.point_size,
            self.point.x + self.point_size, 
            self.point.y + self.point_size
        )
    
    def contains_point(self, point: Point) -> bool:
        """Check if the given point is within the point's selection area"""
        distance = self.point.distance_to(point)
        return distance <= self.point_size + 5
    
    def set_property(self, key: str, value: Any) -> None:
        """Set property with point-specific handling"""
        if key == 'x': 
            self.point.x = value
        elif key == 'y': 
            self.point.y = value
        elif key == 'label': 
            self.point.label = value
        elif key == 'show_label': 
            self.point.show_label = value
        elif key == 'label_position': 
            self.point.label_position = value
        elif key == 'point_size': 
            self.point_size = value
        else:
            super().set_property(key, value)
    
    def get_property(self, key: str, default: Any = None) -> Any:
        """Get property with point-specific handling"""
        if key == 'x':
            return self.point.x
        elif key == 'y':
            return self.point.y
        elif key == 'label':
            return self.point.label
        elif key == 'show_label':
            return self.point.show_label
        elif key == 'label_position':
            return self.point.label_position
        elif key == 'point_size':
            return self.point_size
        else:
            return super().get_property(key, default)
    
    def copy(self) -> 'PointShape':
        """Create a deep copy of this point shape"""
        new_shape = PointShape(self.point.copy(), f"{self.name}_copy")
        new_shape.point_size = self.point_size
        new_shape.visible = self.visible
        new_shape.color = self.color
        new_shape.fill_color = self.fill_color
        new_shape.line_width = self.line_width
        new_shape.line_style = self.line_style
        new_shape.layer = self.layer
        new_shape.font_size = self.font_size
        new_shape.text_color = self.text_color
        new_shape._properties = self._properties.copy()
        return new_shape