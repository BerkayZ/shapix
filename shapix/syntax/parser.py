"""
Geometry syntax parser for shapix
"""

import re
from typing import List, Dict, Any, Optional
from ..core.base import Point, GeometricShape
from ..shapes.triangle import Triangle
from ..shapes.circle import Circle
from ..shapes.line import Line
from ..shapes.angle import Angle
from ..shapes.point import PointShape


class GeometrySyntaxParser:
    """Parses text-based geometry syntax into shape objects"""
    
    def __init__(self):
        self.shapes: List[GeometricShape] = []
        self.points: Dict[str, Point] = {}
        self.named_shapes: Dict[str, GeometricShape] = {}
    
    def parse(self, syntax: str) -> List[GeometricShape]:
        """Parse geometry syntax and return list of shapes"""
        self.shapes.clear()
        self.points.clear()
        self.named_shapes.clear()
        
        lines = [line.strip() for line in syntax.split('\n') if line.strip()]
        
        for line in lines:
            if line.startswith('#') or not line:
                continue
            self._parse_line(line)
        
        return self.shapes
    
    def _parse_line(self, line: str) -> None:
        """Parse a single line of syntax"""
        if line.startswith('POINT'):
            self._parse_point(line)
        elif line.startswith('TRIANGLE'):
            self._parse_triangle(line)
        elif line.startswith('CIRCLE'):
            self._parse_circle(line)
        elif line.startswith('LINE'):
            self._parse_line_shape(line)
        elif line.startswith('ANGLE'):
            self._parse_angle(line)
    
    def _parse_point(self, line: str) -> None:
        """Parse point definition: POINT A 10 20 "Label" show_label=true label_position=top_right"""
        parts = self._split_line(line)
        if len(parts) >= 4:
            name = parts[1]
            x, y = float(parts[2]), float(parts[3])
            
            # Extract label (quoted string or name)
            label = self._extract_quoted_string(line) or name
            
            # Create point
            point = Point(x, y, label)
            
            # Parse properties
            props = self._parse_properties(line)
            if 'show_label' in props:
                point.show_label = self._parse_bool(props['show_label'])
            if 'label_position' in props:
                point.label_position = props['label_position']
            
            # Store point for reference
            self.points[name] = point
            
            # Create point shape for rendering
            point_shape = PointShape(point, f"point_{name}")
            self._apply_common_properties(point_shape, props)
            self.shapes.append(point_shape)
    
    def _parse_circle(self, line: str) -> None:
        """Parse circle definition: CIRCLE O 50 color=blue"""
        parts = self._split_line(line)
        if len(parts) >= 3:
            center_name = parts[1]
            radius = float(parts[2])
            
            # Get or create center point
            if center_name in self.points:
                center = self.points[center_name]
            else:
                center = Point(0, 0, center_name)
                self.points[center_name] = center
            
            # Create circle
            circle = Circle(center, radius, f"circle_{center_name}")
            
            # Parse properties
            props = self._parse_properties(line)
            self._apply_common_properties(circle, props)
            
            if 'show_center' in props:
                circle.show_center = self._parse_bool(props['show_center'])
            if 'show_radius_line' in props:
                circle.show_radius_line = self._parse_bool(props['show_radius_line'])
            
            self.shapes.append(circle)
    
    def _parse_line_shape(self, line: str) -> None:
        """Parse line definition: LINE A B color=red"""
        parts = self._split_line(line)
        if len(parts) >= 3:
            start_name = parts[1]
            end_name = parts[2]
            
            # Get points
            start_point = self.points.get(start_name, Point(0, 0, start_name))
            end_point = self.points.get(end_name, Point(100, 0, end_name))
            
            # Create line
            line_shape = Line(start_point, end_point, f"line_{start_name}_{end_name}")
            
            # Parse properties
            props = self._parse_properties(line)
            self._apply_common_properties(line_shape, props)
            
            if 'show_endpoints' in props:
                line_shape.show_endpoints = self._parse_bool(props['show_endpoints'])
            if 'show_length' in props:
                line_shape.show_length = self._parse_bool(props['show_length'])
            
            self.shapes.append(line_shape)
    
    def _parse_triangle(self, line: str) -> None:
        """Parse triangle definition: TRIANGLE A B C color=green"""
        parts = self._split_line(line)
        if len(parts) >= 4:
            vertex_names = [parts[1], parts[2], parts[3]]
            
            # Get or create vertices
            vertices = []
            for name in vertex_names:
                if name in self.points:
                    vertices.append(self.points[name])
                else:
                    # Create default positioned vertices
                    if len(vertices) == 0:
                        vertices.append(Point(-50, 50, name))
                    elif len(vertices) == 1:
                        vertices.append(Point(50, 50, name))
                    else:
                        vertices.append(Point(0, -50, name))
                    self.points[name] = vertices[-1]
            
            # Create triangle
            triangle = Triangle(vertices[0], vertices[1], vertices[2], f"triangle_{'_'.join(vertex_names)}")
            
            # Parse properties
            props = self._parse_properties(line)
            self._apply_common_properties(triangle, props)
            
            if 'show_vertices' in props:
                triangle.show_vertices = self._parse_bool(props['show_vertices'])
            if 'show_angles' in props:
                triangle.show_angles = self._parse_bool(props['show_angles'])
            
            self.shapes.append(triangle)
    
    def _parse_angle(self, line: str) -> None:
        """Parse angle definition: ANGLE A O B color=red arc=true show_measure=true"""
        parts = self._split_line(line)
        if len(parts) >= 4:
            point1_name = parts[1]
            vertex_name = parts[2]
            point2_name = parts[3]
            
            # Get or create points
            point1 = self.points.get(point1_name, Point(-50, 0, point1_name))
            vertex = self.points.get(vertex_name, Point(0, 0, vertex_name))
            point2 = self.points.get(point2_name, Point(50, 50, point2_name))
            
            # Create angle
            angle = Angle(point1, vertex, point2, f"angle_{point1_name}_{vertex_name}_{point2_name}")
            
            # Parse properties
            props = self._parse_properties(line)
            self._apply_common_properties(angle, props)
            
            if 'arc' in props:
                angle.show_arc = self._parse_bool(props['arc'])
            if 'show_measure' in props:
                angle.show_measure = self._parse_bool(props['show_measure'])
            if 'arc_radius' in props:
                angle.arc_radius = float(props['arc_radius'])
            
            self.shapes.append(angle)
    
    def _split_line(self, line: str) -> List[str]:
        """Split line into parts, handling quoted strings"""
        # Remove quoted strings temporarily
        quoted_pattern = r'"[^"]*"'
        quotes = re.findall(quoted_pattern, line)
        temp_line = re.sub(quoted_pattern, '___QUOTE___', line)
        
        # Split by whitespace
        parts = temp_line.split()
        
        # Restore quoted strings
        quote_index = 0
        for i, part in enumerate(parts):
            if part == '___QUOTE___' and quote_index < len(quotes):
                parts[i] = quotes[quote_index]
                quote_index += 1
        
        return parts
    
    def _extract_quoted_string(self, line: str) -> Optional[str]:
        """Extract the first quoted string from line"""
        match = re.search(r'"([^"]*)"', line)
        return match.group(1) if match else None
    
    def _parse_properties(self, line: str) -> Dict[str, str]:
        """Parse key=value properties from line"""
        props = {}
        
        # Find all key=value pairs
        pattern = r'(\w+)=([^\s]+)'
        matches = re.findall(pattern, line)
        
        for key, value in matches:
            # Remove quotes if present
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            props[key] = value
        
        return props
    
    def _parse_bool(self, value: str) -> bool:
        """Parse boolean value from string"""
        return value.lower() in ('true', '1', 'yes', 'on')
    
    def _apply_common_properties(self, shape: GeometricShape, props: Dict[str, str]) -> None:
        """Apply common properties to a shape"""
        if 'color' in props:
            shape.color = props['color']
        if 'fill_color' in props:
            shape.fill_color = props['fill_color']
        if 'line_width' in props:
            shape.line_width = int(props['line_width'])
        if 'font_size' in props:
            shape.font_size = int(props['font_size'])
        if 'text_color' in props:
            shape.text_color = props['text_color']
        if 'visible' in props:
            shape.visible = self._parse_bool(props['visible'])
        if 'layer' in props:
            shape.layer = int(props['layer'])
    
    def get_point(self, name: str) -> Optional[Point]:
        """Get a point by name"""
        return self.points.get(name)
    
    def get_shape(self, name: str) -> Optional[GeometricShape]:
        """Get a shape by name"""
        return self.named_shapes.get(name)