"""
Sub-command for generating mind map visualizations.
"""

import argparse
from pathlib import Path
from typing import NoReturn

from ..visualization import generate_mindmap


def register_command(subparsers: argparse._SubParsersAction):
    """Registers the 'visualize' command and its arguments."""
    parser = subparsers.add_parser(
        "visualize", help="Generate a visualization from a .mm mind map file."
    )
    parser.add_argument(
        "input_file", type=Path, help="Path to the input .mm mind map file."
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Path for the output file. Defaults to a .svg file with the same name as the input.",
    )
    parser.add_argument(
        "--colors",
        nargs="+",
        metavar="COLOR",
        help="A list of hex color codes to use for node depths.",
    )
    parser.add_argument(
        "--direction",
        choices=["LR", "TB"],
        default="LR",
        help="Graph layout direction: LR or TB.",
    )
    parser.add_argument(
        "--splines",
        choices=["ortho", "curved", "spline", "line", "polyline"],
        default="ortho",
        help="Controls the edge line style.",
    )
    parser.add_argument(
        "--fontsize", type=int, default=14, help="Font size for the text in nodes."
    )
    parser.add_argument(
        "--wrap",
        type=int,
        default=30,
        help="Character width before wrapping text in a node.",
    )
    parser.set_defaults(func=execute)


def execute(args: argparse.Namespace) -> NoReturn:
    """The handler function for the 'visualize' command."""
    print(f"\n--- VISUALIZING MIND MAP: {args.input_file} ---")

    # Determine output path and format
    if not args.output:
        output_file_path = args.input_file.with_suffix(".svg")
    else:
        output_file_path = args.output
        if not output_file_path.suffix:
            output_file_path = output_file_path.with_suffix(".svg")

    generate_mindmap(
        xml_file_path=args.input_file,
        output_path=output_file_path,
        custom_palette=args.colors,
        direction=args.direction,
        spline_style=args.splines,
        font_size=args.fontsize,
        text_width=args.wrap,
    )
