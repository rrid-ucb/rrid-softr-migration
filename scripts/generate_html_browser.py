#!/usr/bin/env python3
"""
Generate HTML browser for output directory.

Usage:
    python scripts/generate_html_browser.py [--output-dir output]
"""

import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.output_generator.html_browser import HTMLBrowserGenerator


def main():
    parser = argparse.ArgumentParser(
        description="Generate self-contained HTML browser for output directory"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="output",
        help="Output directory to scan (default: output)"
    )
    
    args = parser.parse_args()
    
    output_dir = Path(args.output_dir)
    if not output_dir.exists():
        print(f"Error: Output directory not found: {output_dir}")
        sys.exit(1)
    
    print(f"Generating HTML browser for: {output_dir}")
    
    generator = HTMLBrowserGenerator(output_dir)
    index_path = generator.generate_html_browser()
    
    print(f"\n✓ HTML browser generated: {index_path}")
    print(f"\nOpen in browser:")
    print(f"  open {index_path}")
    print(f"\nOr view at:")
    print(f"  file://{index_path.resolve()}")


if __name__ == "__main__":
    main()

