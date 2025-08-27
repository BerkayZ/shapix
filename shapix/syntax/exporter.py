"""
PNG exporter for shapix geometry engine
"""

import tkinter as tk
from tkinter import Canvas
from typing import List, Tuple
import io
import platform
import subprocess

from ..core.base import GeometricShape
from ..rendering.renderer import ShapeRenderer
from .parser import GeometrySyntaxParser


class GeometryPNGExporter:
    """Export geometry syntax to PNG images"""
    
    def __init__(self, width: int = 800, height: int = 600):
        self.width = width
        self.height = height
        self.origin_x = width // 2
        self.origin_y = height // 2
        self.scale = 1.0
        
        # Create hidden tkinter canvas for rendering
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the window
        self.canvas = Canvas(self.root, width=width, height=height, bg='white')
        
        # Create renderer
        self.renderer = ShapeRenderer(self.canvas, self.world_to_canvas)
    
    def world_to_canvas(self, x: float, y: float) -> Tuple[int, int]:
        """Convert world coordinates to canvas coordinates"""
        return int(self.origin_x + x * self.scale), int(self.origin_y - y * self.scale)
    
    def export_syntax_to_png(self, syntax: str, filename: str, auto_scale: bool = True) -> None:
        """Export geometry syntax to PNG file"""
        try:
            parser = GeometrySyntaxParser()
            shapes = parser.parse(syntax)
            
            if auto_scale:
                self._auto_scale_shapes(shapes)
            
            self._draw_shapes(shapes)
            self._save_canvas_as_png(filename)
        finally:
            self._cleanup()
    
    def _auto_scale_shapes(self, shapes: List[GeometricShape]) -> None:
        """Automatically scale shapes to fit canvas"""
        if not shapes:
            return
        
        # Find bounding box of all shapes
        min_x = min_y = float('inf')
        max_x = max_y = float('-inf')
        
        for shape in shapes:
            points = shape.get_points()
            for point in points:
                if hasattr(point, 'x') and hasattr(point, 'y'):
                    min_x = min(min_x, point.x)
                    max_x = max(max_x, point.x)
                    min_y = min(min_y, point.y)
                    max_y = max(max_y, point.y)
        
        if min_x == float('inf'):
            return
        
        # Add padding
        padding = 50
        content_width = max_x - min_x
        content_height = max_y - min_y
        
        if content_width > 0 and content_height > 0:
            scale_x = (self.width - 2 * padding) / content_width
            scale_y = (self.height - 2 * padding) / content_height
            self.scale = min(scale_x, scale_y, 2.0)  # Max scale of 2.0
        
        # Center the content
        center_x = (min_x + max_x) / 2
        center_y = (min_y + max_y) / 2
        self.origin_x = self.width // 2 - center_x * self.scale
        self.origin_y = self.height // 2 + center_y * self.scale
    
    def _draw_shapes(self, shapes: List[GeometricShape]) -> None:
        """Draw all shapes on canvas"""
        self.canvas.delete("all")
        
        # Draw background
        self.canvas.create_rectangle(0, 0, self.width, self.height, fill='white', outline='white')
        
        # Draw shapes sorted by layer
        for shape in sorted(shapes, key=lambda s: s.layer):
            if shape.visible:
                self._draw_shape(shape)
    
    def _draw_shape(self, shape: GeometricShape) -> None:
        """Draw individual shape using renderer"""
        shape_type = shape.__class__.__name__
        
        # Use dynamic method lookup first
        method_name = f'draw_{shape_type.lower()}'
        if hasattr(self.renderer, method_name):
            getattr(self.renderer, method_name)(shape)
        # Handle specific shape types
        elif 'PointShape' in shape_type:
            self.renderer.draw_point(shape)
        elif 'Triangle' in shape_type:
            self.renderer.draw_triangle(shape)
        elif 'Circle' in shape_type:
            self.renderer.draw_circle(shape)
        elif 'Line' in shape_type:
            self.renderer.draw_line(shape)
        elif 'Angle' in shape_type:
            self.renderer.draw_angle(shape)
    
    def _save_canvas_as_png(self, filename: str) -> None:
        """Save canvas to PNG file"""
        try:
            # Update canvas to ensure all drawing is complete
            self.canvas.update()
            
            # Try PostScript method first
            ps_data = self.canvas.postscript(colormode='color', width=self.width, height=self.height)
            
            # Try to convert PostScript to PNG using PIL
            try:
                from PIL import Image
                img = Image.open(io.BytesIO(ps_data.encode('latin-1')))
                img.save(filename, 'PNG')
                return
            except ImportError:
                print("PIL not available, trying alternative method...")
            except Exception:
                print("PIL conversion failed, trying alternative method...")
            
            # Fallback: Use platform-specific screenshot
            self._save_canvas_screenshot(filename)
            
        except Exception as e:
            print(f"Error saving PNG: {e}")
            # Save as PostScript if all else fails
            ps_filename = filename.replace('.png', '.ps')
            with open(ps_filename, 'w') as f:
                f.write(self.canvas.postscript(colormode='color', width=self.width, height=self.height))
            print(f"Saved as PostScript: {ps_filename}")
    
    def _save_canvas_screenshot(self, filename: str) -> None:
        """Alternative method to save canvas using screenshot"""
        try:
            # Make window visible temporarily
            self.root.deiconify()
            self.root.update()
            
            # Get window position
            x = self.root.winfo_rootx() + self.canvas.winfo_x()
            y = self.root.winfo_rooty() + self.canvas.winfo_y()
            
            # Take screenshot based on platform
            if platform.system() == "Darwin":  # macOS
                subprocess.run([
                    'screencapture', '-R', f'{x},{y},{self.width},{self.height}', filename
                ])
                print(f"Screenshot saved: {filename}")
            elif platform.system() == "Linux":
                subprocess.run([
                    'import', '-window', 'root', '-crop', f'{self.width}x{self.height}+{x}+{y}', filename
                ])
                print(f"Screenshot saved: {filename}")
            elif platform.system() == "Windows":
                print("Windows screenshot method not implemented")
                print(f"Please implement platform-specific screenshot for Windows")
            else:
                print(f"Screenshot method not implemented for {platform.system()}")
            
            self.root.withdraw()
            
        except Exception as e:
            print(f"Error taking screenshot: {e}")
    
    def _cleanup(self) -> None:
        """Clean up resources"""
        try:
            self.canvas.destroy()
            self.root.destroy()
        except Exception:
            pass


def export_geometry_syntax(syntax: str, filename: str, width: int = 800, height: int = 600) -> None:
    """Convenience function to export geometry syntax to PNG"""
    exporter = GeometryPNGExporter(width, height)
    exporter.export_syntax_to_png(syntax, filename)