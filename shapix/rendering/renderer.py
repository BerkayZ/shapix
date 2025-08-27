"""
Shape rendering utilities for shapix
"""

import tkinter as tk
import math
from typing import TYPE_CHECKING, Tuple, Callable

if TYPE_CHECKING:
    from ..shapes.triangle import Triangle
    from ..shapes.circle import Circle
    from ..shapes.line import Line
    from ..shapes.angle import Angle
    from ..shapes.point import PointShape


class ShapeRenderer:
    """Handles rendering of shapes on tkinter canvas"""
    
    def __init__(self, canvas: tk.Canvas, world_to_canvas_func: Callable[[float, float], Tuple[int, int]]):
        self.canvas = canvas
        self.world_to_canvas = world_to_canvas_func
    
    def draw_point(self, shape: 'PointShape') -> None:
        """Draw point with configurable label positioning"""
        point_x, point_y = self.world_to_canvas(shape.point.x, shape.point.y)
        
        color = "red" if shape.selected else shape.color
        
        # Draw the point circle
        size = getattr(shape, 'point_size', 4)
        self.canvas.create_oval(
            point_x - size, point_y - size, 
            point_x + size, point_y + size, 
            fill=color, outline=color
        )
        
        # Draw label if enabled
        if shape.point.show_label and shape.point.label:
            label_x, label_y = self._calculate_label_position(
                point_x, point_y, shape.point.label_position
            )
            
            # Use contrasting text color for better visibility
            text_color = shape.text_color if shape.text_color != "black" else "darkblue"
            font_size = max(shape.font_size, 10)
            
            self.canvas.create_text(
                label_x, label_y, 
                text=shape.point.label,
                fill=text_color, 
                font=("Arial", font_size, "bold")
            )
    
    def draw_line(self, shape: 'Line') -> None:
        """Draw line with optional labels and endpoints"""
        x1, y1 = self.world_to_canvas(shape.start.x, shape.start.y)
        x2, y2 = self.world_to_canvas(shape.end.x, shape.end.y)
        
        color = "red" if shape.selected else shape.color
        self.canvas.create_line(x1, y1, x2, y2, fill=color, width=shape.line_width)
        
        # Draw endpoints
        if shape.show_endpoints:
            self.canvas.create_oval(x1-2, y1-2, x1+2, y1+2, fill=color)
            self.canvas.create_oval(x2-2, y2-2, x2+2, y2+2, fill=color)
        
        # Draw line label at midpoint
        if hasattr(shape, 'label') and shape.label:
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            # Offset label perpendicular to line
            dx, dy = x2 - x1, y2 - y1
            length = math.sqrt(dx*dx + dy*dy)
            if length > 0:
                # Perpendicular offset
                perp_x, perp_y = -dy / length, dx / length
                label_x = mid_x + perp_x * 15
                label_y = mid_y + perp_y * 15
            else:
                label_x, label_y = mid_x, mid_y
            
            self.canvas.create_text(
                label_x, label_y, 
                text=shape.label,
                fill=shape.text_color, 
                font=("Arial", shape.font_size)
            )
        
        # Draw length if requested
        if shape.show_length:
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            length_text = f"{shape.get_length():.1f}"
            # Position length on opposite side of label
            dx, dy = x2 - x1, y2 - y1
            length = math.sqrt(dx*dx + dy*dy)
            if length > 0:
                perp_x, perp_y = dy / length, -dx / length  # Opposite perpendicular
                label_x = mid_x + perp_x * 15
                label_y = mid_y + perp_y * 15
            else:
                label_x, label_y = mid_x, mid_y - 15
            
            self.canvas.create_text(
                label_x, label_y, 
                text=length_text,
                fill=shape.text_color, 
                font=("Arial", shape.font_size - 1)
            )
    
    def draw_circle(self, shape: 'Circle') -> None:
        """Draw circle with optional center and labels"""
        center_x, center_y = self.world_to_canvas(shape.center.x, shape.center.y)
        radius = shape.radius
        
        color = "red" if shape.selected else shape.color
        fill_color = shape.fill_color if shape.fill_color else ""
        
        bbox = [center_x - radius, center_y - radius, center_x + radius, center_y + radius]
        self.canvas.create_oval(*bbox, fill=fill_color, outline=color, width=shape.line_width)
        
        # Draw center point
        if shape.show_center:
            self.canvas.create_oval(center_x-2, center_y-2, center_x+2, center_y+2, fill=color)
            if shape.center_label and shape.center.label:
                self.canvas.create_text(
                    center_x + 10, center_y - 10, 
                    text=shape.center.label,
                    fill=shape.text_color, 
                    font=("Arial", shape.font_size)
                )
        
        # Draw radius line
        if shape.show_radius_line:
            self.canvas.create_line(
                center_x, center_y, center_x + radius, center_y,
                fill=color, width=1, dash=(3, 3)
            )
            if shape.label:
                self.canvas.create_text(
                    center_x + radius/2, center_y - 10, 
                    text=shape.label,
                    fill=shape.text_color, 
                    font=("Arial", shape.font_size)
                )
    
    def draw_triangle(self, shape: 'Triangle') -> None:
        """Draw triangle with vertices and optional labels"""
        points = []
        for vertex in [shape.vertex_a, shape.vertex_b, shape.vertex_c]:
            canvas_x, canvas_y = self.world_to_canvas(vertex.x, vertex.y)
            points.extend([canvas_x, canvas_y])
        
        color = "red" if shape.selected else shape.color
        fill_color = shape.fill_color if shape.fill_color else ""
        
        # Draw triangle
        self.canvas.create_polygon(points, fill=fill_color, outline=color, width=shape.line_width)
        
        # Draw vertices
        if shape.show_vertices:
            for vertex in [shape.vertex_a, shape.vertex_b, shape.vertex_c]:
                canvas_x, canvas_y = self.world_to_canvas(vertex.x, vertex.y)
                self.canvas.create_oval(canvas_x-3, canvas_y-3, canvas_x+3, canvas_y+3, fill=color)
                
                # Draw vertex label
                if shape.vertex_labels and vertex.label:
                    # Position label outside triangle using centroid
                    centroid_x = (shape.vertex_a.x + shape.vertex_b.x + shape.vertex_c.x) / 3
                    centroid_y = (shape.vertex_a.y + shape.vertex_b.y + shape.vertex_c.y) / 3
                    
                    # Calculate outward direction
                    dx = vertex.x - centroid_x
                    dy = vertex.y - centroid_y
                    length = math.sqrt(dx*dx + dy*dy)
                    
                    if length > 0:
                        unit_x, unit_y = dx/length, dy/length
                        offset = 20
                        label_x = canvas_x + unit_x * offset
                        label_y = canvas_y - unit_y * offset  # Flip Y for canvas
                    else:
                        label_x, label_y = canvas_x + 12, canvas_y - 12
                    
                    self.canvas.create_text(
                        label_x, label_y, 
                        text=vertex.label,
                        fill=shape.text_color, 
                        font=("Arial", shape.font_size)
                    )
        
        # Draw angles if requested
        if shape.show_angles or shape.show_angle_measures:
            self._draw_triangle_angles(shape)
    
    def draw_angle(self, shape: 'Angle') -> None:
        """Draw angle with arc and label"""
        vertex_x, vertex_y = self.world_to_canvas(shape.vertex.x, shape.vertex.y)
        p1_x, p1_y = self.world_to_canvas(shape.point1.x, shape.point1.y)
        p2_x, p2_y = self.world_to_canvas(shape.point2.x, shape.point2.y)
        
        color = "red" if shape.selected else shape.color
        
        # Draw the two rays
        self.canvas.create_line(vertex_x, vertex_y, p1_x, p1_y, fill=color, width=shape.line_width)
        self.canvas.create_line(vertex_x, vertex_y, p2_x, p2_y, fill=color, width=shape.line_width)
        
        # Draw arc if enabled
        if shape.show_arc:
            arc_radius = getattr(shape, 'arc_radius', 30)
            
            # Calculate angles for arc
            angle1 = math.degrees(math.atan2(-(p1_y - vertex_y), p1_x - vertex_x))
            angle2 = math.degrees(math.atan2(-(p2_y - vertex_y), p2_x - vertex_x))
            
            # Normalize angles
            angle1 = angle1 % 360
            angle2 = angle2 % 360
            
            # Calculate extent
            diff = angle2 - angle1
            if diff > 180:
                diff -= 360
            elif diff < -180:
                diff += 360
            
            if abs(diff) <= 180:
                start_angle = angle1
                extent = diff
            else:
                start_angle = angle2
                extent = 360 - abs(diff)
                if diff < 0:
                    extent = -extent
            
            # Draw arc
            bbox = [vertex_x - arc_radius, vertex_y - arc_radius, 
                    vertex_x + arc_radius, vertex_y + arc_radius]
            self.canvas.create_arc(bbox, start=start_angle, extent=extent, 
                                 outline=color, width=2, style="arc")
        
        # Draw label and/or measure
        if (hasattr(shape, 'label') and shape.label) or shape.show_measure:
            # Calculate bisector for label positioning
            v1x, v1y = shape.point1.x - shape.vertex.x, shape.point1.y - shape.vertex.y
            v2x, v2y = shape.point2.x - shape.vertex.x, shape.point2.y - shape.vertex.y
            
            mag1 = math.sqrt(v1x * v1x + v1y * v1y)
            mag2 = math.sqrt(v2x * v2x + v2y * v2y)
            
            if mag1 > 0 and mag2 > 0:
                u_x, u_y = v1x / mag1, v1y / mag1
                v_x, v_y = v2x / mag2, v2y / mag2
                
                bisector_x = u_x + v_x
                bisector_y = u_y + v_y
                bisector_mag = math.sqrt(bisector_x * bisector_x + bisector_y * bisector_y)
                
                if bisector_mag > 0:
                    b_x = bisector_x / bisector_mag
                    b_y = bisector_y / bisector_mag
                    
                    arc_radius = getattr(shape, 'arc_radius', 30)
                    label_distance = arc_radius + 15
                    label_x = vertex_x + label_distance * b_x
                    label_y = vertex_y - label_distance * b_y
                    
                    text_parts = []
                    if hasattr(shape, 'label') and shape.label:
                        text_parts.append(shape.label)
                    if shape.show_measure:
                        text_parts.append(f"{shape.get_measure():.0f}°")
                    
                    if text_parts:
                        display_text = " ".join(text_parts)
                        self.canvas.create_text(
                            label_x, label_y, 
                            text=display_text,
                            fill=shape.text_color, 
                            font=("Arial", shape.font_size)
                        )
    
    def _calculate_label_position(self, point_x: float, point_y: float, position: str) -> Tuple[float, float]:
        """Calculate label position based on position setting"""
        offset = 20
        
        position_map = {
            "top_left": (-offset, -offset),
            "top": (0, -offset),
            "top_right": (offset, -offset),
            "center_left": (-offset, 0),
            "center": (0, 0),
            "center_right": (offset, 0),
            "bottom_left": (-offset, offset),
            "bottom": (0, offset),
            "bottom_right": (offset, offset),
            "left": (-offset, 0),
            "right": (offset, 0)
        }
        
        dx, dy = position_map.get(position, position_map["top_right"])
        return point_x + dx, point_y + dy
    
    def _draw_triangle_angles(self, shape: 'Triangle') -> None:
        """Draw triangle angles with arcs and labels"""
        angles_data = [
            (shape.vertex_a, shape.vertex_b, shape.vertex_c, shape.angle_a_label),
            (shape.vertex_b, shape.vertex_a, shape.vertex_c, shape.angle_b_label),
            (shape.vertex_c, shape.vertex_a, shape.vertex_b, shape.angle_c_label)
        ]
        
        for vertex, p1, p2, label in angles_data:
            vertex_x, vertex_y = self.world_to_canvas(vertex.x, vertex.y)
            
            # Calculate bisector direction
            v1x, v1y = p1.x - vertex.x, p1.y - vertex.y
            v2x, v2y = p2.x - vertex.x, p2.y - vertex.y
            
            mag1 = math.sqrt(v1x * v1x + v1y * v1y)
            mag2 = math.sqrt(v2x * v2x + v2y * v2y)
            
            if mag1 == 0 or mag2 == 0:
                continue
            
            u_x, u_y = v1x / mag1, v1y / mag1
            v_x, v_y = v2x / mag2, v2y / mag2
            
            bisector_x = u_x + v_x
            bisector_y = u_y + v_y
            bisector_mag = math.sqrt(bisector_x * bisector_x + bisector_y * bisector_y)
            
            if bisector_mag == 0:
                continue
            
            b_x = bisector_x / bisector_mag
            b_y = bisector_y / bisector_mag
            
            # Draw arc if requested
            if shape.show_angles:
                arc_radius = 20
                
                p1_canvas_x, p1_canvas_y = self.world_to_canvas(p1.x, p1.y)
                p2_canvas_x, p2_canvas_y = self.world_to_canvas(p2.x, p2.y)
                
                angle1 = math.degrees(math.atan2(-(p1_canvas_y - vertex_y), p1_canvas_x - vertex_x))
                angle2 = math.degrees(math.atan2(-(p2_canvas_y - vertex_y), p2_canvas_x - vertex_x))
                
                angle1 = angle1 % 360
                angle2 = angle2 % 360
                
                diff = angle2 - angle1
                if diff > 180:
                    diff -= 360
                elif diff < -180:
                    diff += 360
                
                if abs(diff) <= 180:
                    start_angle = angle1
                    extent = diff
                else:
                    start_angle = angle2
                    extent = 360 - abs(diff)
                    if diff < 0:
                        extent = -extent
                
                bbox = [vertex_x - arc_radius, vertex_y - arc_radius,
                        vertex_x + arc_radius, vertex_y + arc_radius]
                
                self.canvas.create_arc(bbox, start=start_angle, extent=extent,
                                     outline=shape.color, width=1, style="arc")
            
            # Draw label and/or measure
            label_distance = 25
            label_x = vertex_x + label_distance * b_x
            label_y = vertex_y - label_distance * b_y
            
            text_parts = []
            if shape.angle_labels and label:
                text_parts.append(label)
            if shape.show_angle_measures:
                if vertex == shape.vertex_a:
                    angle_measure = shape.get_angle_measure('a')
                elif vertex == shape.vertex_b:
                    angle_measure = shape.get_angle_measure('b')
                else:
                    angle_measure = shape.get_angle_measure('c')
                text_parts.append(f"{angle_measure:.0f}°")
            
            if text_parts:
                display_text = " ".join(text_parts)
                self.canvas.create_text(
                    label_x, label_y, 
                    text=display_text,
                    fill=shape.text_color, 
                    font=("Arial", shape.font_size)
                )