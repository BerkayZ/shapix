"""
Command line interface for shapix
"""

import argparse
import sys
import os
from .syntax import export_geometry_syntax


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Shapix - Export geometry syntax to PNG images",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  shapix input.geo output.png
  shapix input.geo output.png --width 1200 --height 800
  shapix --help
        """,
    )
    
    parser.add_argument("input", help="Input geometry file (.geo)")
    parser.add_argument("output", help="Output PNG file")
    parser.add_argument(
        "--width", "-w", 
        type=int, 
        default=800, 
        help="Output image width (default: 800)"
    )
    parser.add_argument(
        "--height", "-h", 
        type=int, 
        default=600, 
        help="Output image height (default: 600)"
    )
    parser.add_argument(
        "--no-autoscale", 
        action="store_true",
        help="Disable automatic scaling to fit canvas"
    )
    parser.add_argument(
        "--version", 
        action="version", 
        version="shapix 0.1.0"
    )
    
    args = parser.parse_args()
    
    # Check input file exists
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found", file=sys.stderr)
        sys.exit(1)
    
    # Read input file
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            syntax = f.read()
    except Exception as e:
        print(f"Error reading input file: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Export to PNG
    try:
        print(f"Exporting {args.input} to {args.output}...")
        export_geometry_syntax(
            syntax, 
            args.output, 
            width=args.width, 
            height=args.height
        )
        print(f"Successfully exported to {args.output}")
    except Exception as e:
        print(f"Error exporting: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()