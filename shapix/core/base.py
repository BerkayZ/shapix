"""
Base classes for geometric shapes in shapix
"""

import math
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Tuple, Any, Optional


@dataclass
class Point:
    """A point in 2D space with label support"""
    x: float
    y: float
    label: str = ""
    show_label: bool = True
    label_position: str = "top_right"
    
    def distance_to(self, other: 'Point') -> float:
        """Calculate Euclidean distance to another point"""
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
    
    def angle_to(self, other: 'Point') -> float:
        """Calculate angle in degrees from this point to another"""
        return math.degrees(math.atan2(other.y - self.y, other.x - self.x))
    
    def move(self, dx: float, dy: float) -> None:
        """Move point by given offset"""
        self.x += dx
        self.y += dy
    
    def copy(self) -> 'Point':
        """Create a deep copy of this point"""
        return Point(self.x, self.y, self.label, self.show_label, self.label_position)
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Point):
            return False
        return (abs(self.x - other.x) < 1e-10 and 
                abs(self.y - other.y) < 1e-10)
    
    def __hash__(self) -> int:
        return hash((round(self.x, 10), round(self.y, 10)))


class GeometricShape(ABC):
    """Abstract base class for all geometric shapes"""
    
    def __init__(self, name: str = ""):
        self.id = str(uuid.uuid4())
        self.name = name or f"{self.__class__.__name__}_{self.id[:8]}"
        self.visible = True
        self.selected = False
        self.color = "black"
        self.fill_color = None
        self.line_width = 2
        self.line_style = "solid"
        self.layer = 0
        self.font_size = 12
        self.text_color = "black"
        
        # Display options
        self.show_labels = True
        self.vertex_labels = True
        self.center_label = True
        self.angle_labels = True
        self.angle_measures = True
        self.side_labels = False
        self.show_label = True
        self.show_endpoints = False
        self.show_length = False
        self.show_measure = True
        self.dimensions = False
        self.radius_lines = False
        
        self._properties = {}
    
    @abstractmethod
    def get_points(self) -> List[Point]:
        """Get all points that define this shape"""
        pass
    
    @abstractmethod
    def set_points(self, points: List[Point]) -> None:
        """Set the points that define this shape"""
        pass
    
    @abstractmethod
    def get_bounds(self) -> Tuple[float, float, float, float]:
        """Get bounding box as (min_x, min_y, max_x, max_y)"""
        pass
    
    @abstractmethod
    def contains_point(self, point: Point) -> bool:
        """Check if the given point is inside this shape"""
        pass
    
    def get_properties(self) -> Dict[str, Any]:
        """Get all properties of this shape"""
        base_props = {
            'id': self.id,
            'name': self.name,
            'visible': self.visible,
            'color': self.color,
            'fill_color': self.fill_color,
            'line_width': self.line_width,
            'line_style': self.line_style,
            'layer': self.layer,
            'font_size': self.font_size,
            'text_color': self.text_color,
            'show_labels': self.show_labels,
            'vertex_labels': self.vertex_labels,
            'center_label': self.center_label,
            'angle_labels': self.angle_labels,
            'angle_measures': self.angle_measures,
            'side_labels': self.side_labels,
            'show_label': self.show_label,
            'show_endpoints': self.show_endpoints,
            'show_length': self.show_length,
            'show_measure': self.show_measure,
            'dimensions': self.dimensions,
            'radius_lines': self.radius_lines
        }
        base_props.update(self._properties)
        return base_props
    
    def set_property(self, key: str, value: Any) -> None:
        """Set a property value"""
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            self._properties[key] = value
    
    def get_property(self, key: str, default: Any = None) -> Any:
        """Get a property value"""
        if hasattr(self, key):
            return getattr(self, key)
        return self._properties.get(key, default)
    
    def move(self, dx: float, dy: float) -> None:
        """Move shape by given offset"""
        points = self.get_points()
        for point in points:
            point.move(dx, dy)
        self.set_points(points)
    
    def copy(self) -> 'GeometricShape':
        """Create a deep copy of this shape"""
        # This is a simplified copy - subclasses should override for proper copying
        new_shape = self.__class__()
        new_shape.name = f"{self.name}_copy"
        new_shape.visible = self.visible
        new_shape.color = self.color
        new_shape.fill_color = self.fill_color
        new_shape.line_width = self.line_width
        new_shape.line_style = self.line_style
        new_shape.layer = self.layer
        new_shape.font_size = self.font_size
        new_shape.text_color = self.text_color
        new_shape.show_labels = self.show_labels
        new_shape._properties = self._properties.copy()
        new_shape.set_points([p.copy() for p in self.get_points()])
        return new_shape
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}', id='{self.id[:8]}...')"
    
    def __repr__(self) -> str:
        return self.__str__()