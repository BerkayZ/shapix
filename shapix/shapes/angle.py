"""
Angle shape implementation for shapix
"""

import math
from typing import List, Tuple, Any
from ..core.base import GeometricShape, Point


class Angle(GeometricShape):
    """An angle defined by three points: point1-vertex-point2"""
    
    def __init__(self, point1: Point = None, vertex: Point = None, point2: Point = None, name: str = ""):
        super().__init__(name)
        self.point1 = point1 or Point(-50, 0)
        self.vertex = vertex or Point(0, 0, "O")
        self.point2 = point2 or Point(50, 50)
        self.label = ""
        self.show_arc = True
        self.arc_radius = 30
        self.show_measure = True
    
    def get_points(self) -> List[Point]:
        """Get the three points that define the angle"""
        return [self.point1, self.vertex, self.point2]
    
    def set_points(self, points: List[Point]) -> None:
        """Set the three points that define the angle"""
        if len(points) >= 3:
            self.point1, self.vertex, self.point2 = points[0], points[1], points[2]
    
    def get_measure(self) -> float:
        """Get the angle measure in degrees"""
        # Calculate vectors from vertex to each point
        v1x, v1y = self.point1.x - self.vertex.x, self.point1.y - self.vertex.y
        v2x, v2y = self.point2.x - self.vertex.x, self.point2.y - self.vertex.y
        
        # Calculate dot product and magnitudes
        dot_product = v1x * v2x + v1y * v2y
        mag1 = math.sqrt(v1x * v1x + v1y * v1y)
        mag2 = math.sqrt(v2x * v2x + v2y * v2y)
        
        if mag1 == 0 or mag2 == 0:
            return 0
        
        # Calculate angle using dot product
        cos_angle = dot_product / (mag1 * mag2)
        cos_angle = max(-1, min(1, cos_angle))  # Clamp to valid range
        angle_rad = math.acos(cos_angle)
        
        return math.degrees(angle_rad)
    
    def set_measure(self, degrees: float) -> None:
        """Set the angle measure by rotating point2"""
        if degrees < 0 or degrees >= 360:
            degrees = degrees % 360
        
        # Get current angle from vertex to point1
        current_angle1 = math.degrees(math.atan2(
            self.point1.y - self.vertex.y, 
            self.point1.x - self.vertex.x
        ))
        
        # Calculate new angle for point2
        new_angle2 = current_angle1 + degrees
        
        # Get distance from vertex to point2
        distance = self.vertex.distance_to(self.point2)
        
        # Calculate new position for point2
        angle_rad = math.radians(new_angle2)
        self.point2.x = self.vertex.x + distance * math.cos(angle_rad)
        self.point2.y = self.vertex.y + distance * math.sin(angle_rad)
    
    def is_right_angle(self, tolerance: float = 1e-6) -> bool:
        """Check if this is a right angle (90 degrees)"""
        return abs(self.get_measure() - 90.0) < tolerance
    
    def is_straight_angle(self, tolerance: float = 1e-6) -> bool:
        """Check if this is a straight angle (180 degrees)"""
        return abs(self.get_measure() - 180.0) < tolerance
    
    def is_acute(self) -> bool:
        """Check if this is an acute angle (< 90 degrees)"""
        return self.get_measure() < 90.0
    
    def is_obtuse(self) -> bool:
        """Check if this is an obtuse angle (> 90 degrees)"""
        measure = self.get_measure()
        return 90.0 < measure < 180.0
    
    def get_bisector_point(self, distance: float = 50) -> Point:
        """Get a point on the angle bisector at the specified distance from vertex"""
        # Get unit vectors from vertex to each point
        v1x, v1y = self.point1.x - self.vertex.x, self.point1.y - self.vertex.y
        v2x, v2y = self.point2.x - self.vertex.x, self.point2.y - self.vertex.y
        
        mag1 = math.sqrt(v1x * v1x + v1y * v1y)
        mag2 = math.sqrt(v2x * v2x + v2y * v2y)
        
        if mag1 == 0 or mag2 == 0:
            return Point(self.vertex.x, self.vertex.y)
        
        # Normalize vectors
        u1x, u1y = v1x / mag1, v1y / mag1
        u2x, u2y = v2x / mag2, v2y / mag2
        
        # Bisector direction is the sum of unit vectors
        bisector_x = u1x + u2x
        bisector_y = u1y + u2y
        
        # Normalize bisector
        bisector_mag = math.sqrt(bisector_x * bisector_x + bisector_y * bisector_y)
        if bisector_mag == 0:
            return Point(self.vertex.x, self.vertex.y)
        
        bisector_x /= bisector_mag
        bisector_y /= bisector_mag
        
        # Return point at specified distance along bisector
        return Point(
            self.vertex.x + distance * bisector_x,
            self.vertex.y + distance * bisector_y
        )
    
    def get_bounds(self) -> Tuple[float, float, float, float]:
        """Get bounding box of the angle"""
        all_x = [self.point1.x, self.vertex.x, self.point2.x]
        all_y = [self.point1.y, self.vertex.y, self.point2.y]
        
        # Expand bounds to include arc radius
        padding = self.arc_radius
        return (
            min(all_x) - padding, min(all_y) - padding,
            max(all_x) + padding, max(all_y) + padding
        )
    
    def contains_point(self, point: Point) -> bool:
        """Check if point is near the angle rays or arc"""
        # Check if point is close to either ray
        def point_to_line_distance(p: Point, start: Point, end: Point) -> float:
            A, B = end.x - start.x, end.y - start.y
            C, D = p.x - start.x, p.y - start.y
            dot, len_sq = A * C + B * D, A * A + B * B
            if len_sq == 0:
                return math.sqrt(C * C + D * D)
            param = max(0, dot / len_sq)  # Only consider ray, not full line
            xx, yy = start.x + param * A, start.y + param * B
            return math.sqrt((p.x - xx)**2 + (p.y - yy)**2)
        
        # Check distance to both rays
        dist1 = point_to_line_distance(point, self.vertex, self.point1)
        dist2 = point_to_line_distance(point, self.vertex, self.point2)
        
        return min(dist1, dist2) <= 5  # 5 pixel tolerance
    
    def copy(self) -> 'Angle':
        """Create a deep copy of this angle"""
        new_angle = Angle(
            self.point1.copy(), 
            self.vertex.copy(), 
            self.point2.copy(), 
            f"{self.name}_copy"
        )
        new_angle.label = self.label
        new_angle.show_arc = self.show_arc
        new_angle.arc_radius = self.arc_radius
        new_angle.show_measure = self.show_measure
        new_angle.visible = self.visible
        new_angle.color = self.color
        new_angle.fill_color = self.fill_color
        new_angle.line_width = self.line_width
        new_angle.line_style = self.line_style
        new_angle.layer = self.layer
        new_angle.font_size = self.font_size
        new_angle.text_color = self.text_color
        new_angle._properties = self._properties.copy()
        return new_angle