"""
Triangle shape implementation for shapix
"""

import math
from typing import List, Tuple, Any
from ..core.base import GeometricShape, Point


class Triangle(GeometricShape):
    """A triangle defined by three vertices"""
    
    def __init__(self, vertex_a: Point = None, vertex_b: Point = None, vertex_c: Point = None, name: str = ""):
        super().__init__(name)
        self.vertex_a = vertex_a or Point(-50, 50, "A")
        self.vertex_b = vertex_b or Point(50, 50, "B")
        self.vertex_c = vertex_c or Point(0, -50, "C")
        
        # Display properties
        self.show_vertices = True
        self.show_side_labels = False
        self.show_angles = False
        self.show_angle_measures = False
        
        # Labels
        self.side_a_label = ""  # BC
        self.side_b_label = ""  # AC
        self.side_c_label = ""  # AB
        self.angle_a_label = ""  # at A
        self.angle_b_label = ""  # at B
        self.angle_c_label = ""  # at C
    
    def get_points(self) -> List[Point]:
        """Get the three vertices of the triangle"""
        return [self.vertex_a, self.vertex_b, self.vertex_c]
    
    def set_points(self, points: List[Point]) -> None:
        """Set the three vertices of the triangle"""
        if len(points) >= 3:
            self.vertex_a, self.vertex_b, self.vertex_c = points[0], points[1], points[2]
    
    def get_side_length(self, side: str) -> float:
        """Get the length of a side ('a', 'b', or 'c')"""
        if side.lower() == 'a':
            return self.vertex_b.distance_to(self.vertex_c)
        elif side.lower() == 'b':
            return self.vertex_a.distance_to(self.vertex_c)
        elif side.lower() == 'c':
            return self.vertex_a.distance_to(self.vertex_b)
        return 0
    
    def get_angle_measure(self, vertex: str) -> float:
        """Get angle measure at vertex ('a', 'b', or 'c') in degrees"""
        if vertex.lower() == 'a':
            return self._calculate_angle(self.vertex_b, self.vertex_a, self.vertex_c)
        elif vertex.lower() == 'b':
            return self._calculate_angle(self.vertex_a, self.vertex_b, self.vertex_c)
        elif vertex.lower() == 'c':
            return self._calculate_angle(self.vertex_a, self.vertex_c, self.vertex_b)
        return 0
    
    def _calculate_angle(self, p1: Point, vertex: Point, p2: Point) -> float:
        """Calculate angle at vertex between two points"""
        v1x, v1y = p1.x - vertex.x, p1.y - vertex.y
        v2x, v2y = p2.x - vertex.x, p2.y - vertex.y
        
        dot_product = v1x * v2x + v1y * v2y
        mag1 = math.sqrt(v1x * v1x + v1y * v1y)
        mag2 = math.sqrt(v2x * v2x + v2y * v2y)
        
        if mag1 == 0 or mag2 == 0:
            return 0
        
        cos_angle = dot_product / (mag1 * mag2)
        cos_angle = max(-1, min(1, cos_angle))
        return math.degrees(math.acos(cos_angle))
    
    def get_area(self) -> float:
        """Calculate the area of the triangle using the cross product"""
        ax, ay = self.vertex_a.x, self.vertex_a.y
        bx, by = self.vertex_b.x, self.vertex_b.y
        cx, cy = self.vertex_c.x, self.vertex_c.y
        return abs((ax * (by - cy) + bx * (cy - ay) + cx * (ay - by)) / 2.0)
    
    def get_perimeter(self) -> float:
        """Calculate the perimeter of the triangle"""
        return (self.get_side_length('a') + 
                self.get_side_length('b') + 
                self.get_side_length('c'))
    
    def get_centroid(self) -> Point:
        """Get the centroid of the triangle"""
        x = (self.vertex_a.x + self.vertex_b.x + self.vertex_c.x) / 3
        y = (self.vertex_a.y + self.vertex_b.y + self.vertex_c.y) / 3
        return Point(x, y, "centroid")
    
    def is_right_triangle(self, tolerance: float = 1e-6) -> bool:
        """Check if the triangle is a right triangle"""
        sides = [self.get_side_length('a'), self.get_side_length('b'), self.get_side_length('c')]
        sides.sort()
        return abs(sides[0]**2 + sides[1]**2 - sides[2]**2) < tolerance
    
    def get_bounds(self) -> Tuple[float, float, float, float]:
        """Get bounding box of the triangle"""
        all_x = [self.vertex_a.x, self.vertex_b.x, self.vertex_c.x]
        all_y = [self.vertex_a.y, self.vertex_b.y, self.vertex_c.y]
        return (min(all_x), min(all_y), max(all_x), max(all_y))
    
    def contains_point(self, point: Point) -> bool:
        """Check if point is inside the triangle using barycentric coordinates"""
        def sign(p1: Point, p2: Point, p3: Point) -> float:
            return (p1.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p3.y)
        
        d1 = sign(point, self.vertex_a, self.vertex_b)
        d2 = sign(point, self.vertex_b, self.vertex_c)
        d3 = sign(point, self.vertex_c, self.vertex_a)
        
        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
        
        return not (has_neg and has_pos)
    
    def copy(self) -> 'Triangle':
        """Create a deep copy of this triangle"""
        new_triangle = Triangle(
            self.vertex_a.copy(), 
            self.vertex_b.copy(), 
            self.vertex_c.copy(), 
            f"{self.name}_copy"
        )
        new_triangle.show_vertices = self.show_vertices
        new_triangle.show_side_labels = self.show_side_labels
        new_triangle.show_angles = self.show_angles
        new_triangle.show_angle_measures = self.show_angle_measures
        new_triangle.side_a_label = self.side_a_label
        new_triangle.side_b_label = self.side_b_label
        new_triangle.side_c_label = self.side_c_label
        new_triangle.angle_a_label = self.angle_a_label
        new_triangle.angle_b_label = self.angle_b_label
        new_triangle.angle_c_label = self.angle_c_label
        new_triangle.visible = self.visible
        new_triangle.color = self.color
        new_triangle.fill_color = self.fill_color
        new_triangle.line_width = self.line_width
        new_triangle.line_style = self.line_style
        new_triangle.layer = self.layer
        new_triangle.font_size = self.font_size
        new_triangle.text_color = self.text_color
        new_triangle._properties = self._properties.copy()
        return new_triangle