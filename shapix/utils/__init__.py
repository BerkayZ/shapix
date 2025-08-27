"""
Utility functions for shapix
"""

import math
from typing import Tuple
from ..core import Point


def distance(p1: Point, p2: Point) -> float:
    """Calculate distance between two points"""
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)


def angle_between_points(p1: Point, vertex: Point, p2: Point) -> float:
    """Calculate angle at vertex between two points in degrees"""
    v1x, v1y = p1.x - vertex.x, p1.y - vertex.y
    v2x, v2y = p2.x - vertex.x, p2.y - vertex.y
    
    dot_product = v1x * v2x + v1y * v2y
    mag1 = math.sqrt(v1x * v1x + v1y * v1y)
    mag2 = math.sqrt(v2x * v2x + v2y * v2y)
    
    if mag1 == 0 or mag2 == 0:
        return 0
    
    cos_angle = dot_product / (mag1 * mag2)
    cos_angle = max(-1, min(1, cos_angle))  # Clamp to valid range
    return math.degrees(math.acos(cos_angle))


def midpoint(p1: Point, p2: Point) -> Point:
    """Calculate midpoint between two points"""
    return Point((p1.x + p2.x) / 2, (p1.y + p2.y) / 2)


def rotate_point(point: Point, center: Point, angle_degrees: float) -> Point:
    """Rotate a point around a center by given angle"""
    angle_rad = math.radians(angle_degrees)
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)
    
    # Translate to origin
    px = point.x - center.x
    py = point.y - center.y
    
    # Rotate
    new_x = px * cos_a - py * sin_a
    new_y = px * sin_a + py * cos_a
    
    # Translate back
    return Point(new_x + center.x, new_y + center.y, point.label)


def point_to_line_distance(point: Point, line_start: Point, line_end: Point) -> float:
    """Calculate perpendicular distance from point to line segment"""
    A = line_end.x - line_start.x
    B = line_end.y - line_start.y
    C = point.x - line_start.x
    D = point.y - line_start.y
    
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
    
    return math.sqrt((point.x - xx)**2 + (point.y - yy)**2)


def degrees_to_radians(degrees: float) -> float:
    """Convert degrees to radians"""
    return math.radians(degrees)


def radians_to_degrees(radians: float) -> float:
    """Convert radians to degrees"""
    return math.degrees(radians)


__all__ = [
    'distance',
    'angle_between_points', 
    'midpoint',
    'rotate_point',
    'point_to_line_distance',
    'degrees_to_radians',
    'radians_to_degrees'
]