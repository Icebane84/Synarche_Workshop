import argparse
import textwrap
import xml.etree.ElementTree as ET
from pathlib import Path

import graphviz
from bs4 import BeautifulSoup  # type: ignore


def create_mindmap_visualization(
    xml_file_path: Path,
    output_path: Path,
    custom_palette: list[str] | None = None,
    direction: str = "LR",
    spline_style: str = "ortho",
    font_size: int = 14,
    text_width: int = 30,
):
    """Parses a mind map XML file and generates a graph visualization.

    Args:
        xml_file_path (Path): The path to the .mm XML file.
        output_path (Path): The path for the output file.
        custom_palette (list[str] | None, optional): A list of hex color codes. Defaults to None.
        direction (str, optional): The layout direction ('LR' or 'TB'). Defaults to 'LR'.
        spline_style (str, optional): The edge line style. Defaults to 'ortho'.
        font_size (int, optional): The font size for node text. Defaults to 14.
        text_width (int, optional): The character width at which to wrap node text. Defaults to 30.

    """
    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
    except (ET.ParseError, FileNotFoundError) as e:
        print(f"Error: Could not parse or find the XML file. {e}")
        return

    # Define graph styling attributes
    graph_attrs = {"rankdir": direction, "splines": spline_style}
    node_attrs = {
        "shape": "box",
        "style": "rounded,filled",
        "fillcolor": "#e8f4f8",
        "fontname": "Helvetica",
        "fontsize": str(font_size),
    }
    edge_attrs = {"color": "#555555"}

    # Initialize a directed graph
    dot = graphviz.Digraph("MindMap", comment="Quantum AI Mind Map")
    dot.attr(**graph_attrs)
    dot.attr("node", **node_attrs)
    dot.attr("edge", **edge_attrs)

    # Find the main root node of the mind map
    map_root_node = root.find("node")

    if map_root_node is None:
        print("Error: No root <node> found in the XML file.")
        return

    # Use the provided custom palette or fall back to a default.
    if custom_palette:
        color_palette = custom_palette
    else:
        # Define a default color palette for different depths.
        color_palette = [
            "#e8f4f8",  # Level 0 (Root)
            "#bde0fe",  # Level 1
            "#a2d2ff",  # Level 2
            "#86bbd8",  # Level 3
            "#6a9fb5",  # Level 4+
        ]

    # Use a recursive function to traverse the XML tree
    def add_nodes_and_edges(xml_node, parent_id=None, depth=0):
        node_id = xml_node.get("ID")
        # Wrap text for better readability in the graph
        node_text = "\n".join(
            textwrap.wrap(xml_node.get("TEXT", "No Text"), width=text_width)
        )

        # Determine node color based on depth
        color_index = min(depth, len(color_palette) - 1)
        node_color = color_palette[color_index]

        # Check for rich content (notes) and set shape/tooltip accordingly
        note_node = xml_node.find('richcontent[@TYPE="NOTE"]')
        node_shape = "box"  # Default shape
        tooltip_text = None

        if note_node is not None and note_node.text:
            # Use BeautifulSoup to robustly parse the HTML content of the note
            soup = BeautifulSoup(
                ET.tostring(note_node, encoding="unicode"), "html.parser"
            )
            tooltip_text = " ".join(soup.get_text().split())  # Clean up whitespace
            node_shape = "note"  # Change shape for nodes with notes

        # Add the node to the graph
        dot.node(
            node_id,
            node_text,
            fillcolor=node_color,
            shape=node_shape,
            tooltip=tooltip_text,
        )

        # If it's not the absolute root, draw an edge from its parent
        if parent_id:
            dot.edge(parent_id, node_id)

        # Recurse for all child nodes
        for child_node in xml_node.findall("node"):
            add_nodes_and_edges(child_node, parent_id=node_id, depth=depth + 1)

    # Start the recursive process from the root node
    add_nodes_and_edges(map_root_node)

    # Render the graph to a file (e.g., mindmap.gv.png)
    try:
        # Use the output path stem as the filename for the intermediate .gv file
        output_gv_path = output_path.with_suffix("")
        output_format = output_path.suffix.lstrip(".")
        dot.render(output_gv_path, view=True, format=output_format, cleanup=True)
        print(f"Successfully generated mind map visualization: {output_path}")
    except graphviz.backend.ExecutableNotFound:
        print("\nError: Graphviz executable not found.")
        print(
            "Please ensure Graphviz is installed and that its 'bin' directory is in your system's PATH."
        )


def main():
    """Main function to parse arguments and run the visualization."""
    parser = argparse.ArgumentParser(
        description="Generate a visualization from a FreeMind/Freeplane .mm mind map file."
    )
    parser.add_argument(
        "input_file", type=Path, help="Path to the input .mm mind map file."
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Path for the output file. The extension determines the format (e.g., 'map.svg', 'map.png'). Defaults to a .svg file with the same name as the input.",
    )
    parser.add_argument(
        "--colors",
        nargs="+",
        metavar="COLOR",
        help="A list of hex color codes to use for node depths (e.g., #ffadad #ffd6a5 #fdffb6).",
    )
    parser.add_argument(
        "--direction",
        choices=["LR", "TB"],
        default="LR",
        help="Graph layout direction: LR (Left-to-Right) or TB (Top-to-Bottom).",
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
    args = parser.parse_args()

    # Determine output path and format
    # If no output is specified, create it based on the input file name
    if not args.output:
        # Default to SVG to make tooltips functional
        output_file_path = args.input_file.with_suffix(".svg")
    else:
        output_file_path = args.output
        # Ensure the output path has an extension, default to .svg if not
        if not output_file_path.suffix:
            output_file_path = output_file_path.with_suffix(".svg")

    create_mindmap_visualization(
        args.input_file,
        output_file_path,
        custom_palette=args.colors,
        direction=args.direction,
        spline_style=args.splines,
        font_size=args.fontsize,
        text_width=args.wrap,
    )


if __name__ == "__main__":
    main()
