# Shapix

A geometry engine for Python with text-based syntax and PNG export capabilities.

## Features

- **Simple text-based syntax** for defining geometric shapes
- **Multiple shape types**: Points, Lines, Circles, Triangles, Angles
- **PNG export** with automatic scaling and positioning
- **Flexible rendering** with customizable colors, labels, and styling
- **Mathematical operations** like area, perimeter, angle calculations
- **Clean object-oriented API** for programmatic use

## Installation

```bash
pip install shapix
```

## Quick Start

### Using Text Syntax

```python
from shapix.syntax import export_geometry_syntax

# Define geometry using simple text syntax
geometry = '''
POINT O 0 0 "O" show_label=true label_position=bottom_right
POINT A 0 100 "A" show_label=true label_position=top
POINT B -87 50 "B" show_label=true label_position=top_left
CIRCLE O 100 color=blue
TRIANGLE A B O color=green
ANGLE B O A color=red arc=true show_measure=true
'''

# Export to PNG
export_geometry_syntax(geometry, "my_diagram.png", width=800, height=600)
```

### Using Python API

```python
from shapix.core import Point
from shapix.shapes import Circle, Triangle
from shapix.rendering import ShapeRenderer

# Create shapes programmatically  
center = Point(0, 0, "O")
circle = Circle(center, radius=100)
circle.color = "blue"

vertex_a = Point(0, 100, "A")
vertex_b = Point(-87, 50, "B") 
triangle = Triangle(vertex_a, vertex_b, center)
triangle.color = "green"

# Render to canvas or export
# ... (rendering code)
```

## Syntax Reference

### Points
```
POINT name x y "label" show_label=true label_position=top_right
```

### Circles
```
CIRCLE center_point radius color=blue show_center=true
```

### Lines
```
LINE start_point end_point color=red show_endpoints=true
```

### Triangles  
```
TRIANGLE point1 point2 point3 color=green show_vertices=true
```

### Angles
```
ANGLE point1 vertex point2 color=red arc=true show_measure=true
```

## Shape Properties

All shapes support common properties:
- `color` - Outline color
- `fill_color` - Fill color  
- `line_width` - Line thickness
- `font_size` - Label font size
- `text_color` - Label text color
- `visible` - Show/hide shape
- `layer` - Drawing order

## Label Positions

Points and labels can be positioned using:
- `top_left`, `top`, `top_right`
- `center_left`, `center`, `center_right` 
- `bottom_left`, `bottom`, `bottom_right`
- `left`, `right`

## Requirements

- Python 3.8+
- Pillow (for PNG export)
- tkinter (usually included with Python)

## License

MIT License