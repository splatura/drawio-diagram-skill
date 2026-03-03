"""Render draw.io XML to PNG using Playwright + headless Chromium.

Usage:
    cd .claude/skills/drawio-diagram/references
    uv run python render_drawio.py <path-to-file.drawio> [--output path.png] [--scale 2] [--width 1920]

First-time setup:
    cd .claude/skills/drawio-diagram/references
    uv sync
    uv run playwright install chromium
"""

from __future__ import annotations

import argparse
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def validate_drawio(xml_str: str) -> list[str]:
    """Validate draw.io XML structure. Returns list of errors (empty = valid)."""
    errors: list[str] = []

    try:
        root = ET.fromstring(xml_str)
    except ET.ParseError as e:
        errors.append(f"Invalid XML: {e}")
        return errors

    # Accept both <mxfile> wrapper and bare <mxGraphModel>
    if root.tag == "mxfile":
        diagram = root.find(".//diagram")
        if diagram is None:
            errors.append("Missing <diagram> element inside <mxfile>")
            return errors
        graph_model = diagram.find("mxGraphModel")
        if graph_model is None:
            # Check if diagram content is encoded (base64)
            if diagram.text and diagram.text.strip():
                # Encoded content — skip deeper validation, renderer will handle it
                return errors
            errors.append("Missing <mxGraphModel> inside <diagram>")
            return errors
    elif root.tag == "mxGraphModel":
        graph_model = root
    else:
        errors.append(f"Expected root element 'mxfile' or 'mxGraphModel', got '{root.tag}'")
        return errors

    root_el = graph_model.find("root")
    if root_el is None:
        errors.append("Missing <root> element inside <mxGraphModel>")
        return errors

    cells = root_el.findall("mxCell")
    if len(cells) < 2:
        errors.append("Expected at least 2 mxCell elements (root cell 0 and layer cell 1)")
        return errors

    # Check for user-created cells (beyond the required root and layer cells)
    user_cells = [c for c in cells if c.get("id") not in ("0", "1")]
    if len(user_cells) == 0:
        errors.append("No diagram elements found — only root/layer cells present")

    return errors


def compute_bounding_box_from_xml(xml_str: str) -> tuple[float, float, float, float]:
    """Compute bounding box from draw.io XML geometry elements."""
    min_x = float("inf")
    min_y = float("inf")
    max_x = float("-inf")
    max_y = float("-inf")

    try:
        root = ET.fromstring(xml_str)
    except ET.ParseError:
        return (0, 0, 800, 600)

    for geom in root.iter("mxGeometry"):
        # Skip relative geometries (edge labels)
        if geom.get("relative") == "1":
            # Check for waypoints
            for point in geom.iter("mxPoint"):
                px = float(point.get("x", 0))
                py = float(point.get("y", 0))
                min_x = min(min_x, px)
                min_y = min(min_y, py)
                max_x = max(max_x, px)
                max_y = max(max_y, py)
            continue

        x = float(geom.get("x", 0))
        y = float(geom.get("y", 0))
        w = float(geom.get("width", 0))
        h = float(geom.get("height", 0))

        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_x = max(max_x, x + w)
        max_y = max(max_y, y + h)

    if min_x == float("inf"):
        return (0, 0, 800, 600)

    return (min_x, min_y, max_x, max_y)


def render(
    drawio_path: Path,
    output_path: Path | None = None,
    scale: int = 2,
    max_width: int = 1920,
) -> Path:
    """Render a .drawio file to PNG. Returns the output PNG path."""
    # Import playwright here so validation errors show before import errors
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("ERROR: playwright not installed.", file=sys.stderr)
        print("Run: cd .claude/skills/drawio-diagram/references && uv sync && uv run playwright install chromium", file=sys.stderr)
        sys.exit(1)

    # Read and validate
    raw = drawio_path.read_text(encoding="utf-8")

    errors = validate_drawio(raw)
    if errors:
        print("ERROR: Invalid draw.io file:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)

    # Compute viewport size from element bounding box
    min_x, min_y, max_x, max_y = compute_bounding_box_from_xml(raw)
    padding = 80
    diagram_w = max_x - min_x + padding * 2
    diagram_h = max_y - min_y + padding * 2

    # Cap viewport width, let height be natural
    vp_width = min(int(diagram_w), max_width)
    vp_height = max(int(diagram_h), 600)

    # Output path
    if output_path is None:
        output_path = drawio_path.with_suffix(".png")

    # Template path (same directory as this script)
    template_path = Path(__file__).parent / "render_template.html"
    if not template_path.exists():
        print(f"ERROR: Template not found at {template_path}", file=sys.stderr)
        sys.exit(1)

    template_url = template_path.as_uri()

    # Escape the XML for injection into JavaScript
    escaped_xml = raw.replace("\\", "\\\\").replace("`", "\\`").replace("$", "\\$")

    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
        except Exception as e:
            if "Executable doesn't exist" in str(e) or "browserType.launch" in str(e):
                print("ERROR: Chromium not installed for Playwright.", file=sys.stderr)
                print("Run: cd .claude/skills/drawio-diagram/references && uv run playwright install chromium", file=sys.stderr)
                sys.exit(1)
            raise

        page = browser.new_page(
            viewport={"width": vp_width, "height": vp_height},
            device_scale_factor=scale,
        )

        # Load the template
        page.goto(template_url)

        # Wait for mxGraph library to load
        page.wait_for_function("window.__moduleReady === true", timeout=30000)

        # Inject the diagram data and render
        result = page.evaluate(f"window.renderDiagram(`{escaped_xml}`)")

        if not result or not result.get("success"):
            error_msg = result.get("error", "Unknown render error") if result else "renderDiagram returned null"
            print(f"ERROR: Render failed: {error_msg}", file=sys.stderr)
            browser.close()
            sys.exit(1)

        # Wait for render completion signal
        page.wait_for_function("window.__renderComplete === true", timeout=15000)

        # Screenshot the root container
        root_el = page.query_selector("#root svg")
        if root_el is None:
            # Fall back to the container div
            root_el = page.query_selector("#root")

        if root_el is None:
            print("ERROR: No rendered content found.", file=sys.stderr)
            browser.close()
            sys.exit(1)

        root_el.screenshot(path=str(output_path))
        browser.close()

    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Render draw.io XML to PNG")
    parser.add_argument("input", type=Path, help="Path to .drawio XML file")
    parser.add_argument("--output", "-o", type=Path, default=None, help="Output PNG path (default: same name with .png)")
    parser.add_argument("--scale", "-s", type=int, default=2, help="Device scale factor (default: 2)")
    parser.add_argument("--width", "-w", type=int, default=1920, help="Max viewport width (default: 1920)")
    args = parser.parse_args()

    if not args.input.exists():
        print(f"ERROR: File not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    png_path = render(args.input, args.output, args.scale, args.width)
    print(str(png_path))


if __name__ == "__main__":
    main()
