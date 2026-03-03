# Draw.io XML Schema

## File Structure

```xml
<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="agent" version="1.0">
  <diagram name="Page-1" id="unique-id">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10"
                  guides="1" tooltips="1" connect="1" arrows="1"
                  fold="1" page="0" pageScale="1" pageWidth="1100"
                  pageHeight="850" background="#ffffff" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <!-- All diagram elements go here with parent="1" -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

**Required structure**: Cell `id="0"` (root) and cell `id="1" parent="0"` (default layer) must always be present. All user elements have `parent="1"`.

## Cell Types

| Attribute | Meaning |
|-----------|---------|
| `vertex="1"` | Shape (rectangle, ellipse, diamond, text, etc.) |
| `edge="1"` | Connection (arrow, line) |

## Shape Styles (vertex)

All visual properties are in a single semicolon-delimited `style` attribute:

```
style="shape=ellipse;perimeter=ellipsePerimeter;whiteSpace=wrap;html=1;fillColor=#3b82f6;strokeColor=#1e3a5f;strokeWidth=2;fontColor=#374151;fontSize=16;"
```

### Shape Types

| `shape=` value | Use For | Perimeter |
|----------------|---------|-----------|
| *(omitted)* | Rectangle (default) | `rectanglePerimeter` (default) |
| `ellipse` | Entry/exit points, external systems | `ellipsePerimeter` |
| `rhombus` | Decisions, conditionals | `rhombusPerimeter` |
| `cylinder` | Databases | `cylinderPerimeter` |
| `cloud` | Abstract states | — |
| `hexagon` | Special processes | `hexagonPerimeter` |

**Important**: Always include `shape=` prefix (e.g., `shape=ellipse`, not just `ellipse;`). Always pair with the matching `perimeter=` value for correct arrow attachment.

### Common Style Properties

| Property | Type | Description |
|----------|------|-------------|
| `fillColor` | hex or `none` | Shape background color |
| `strokeColor` | hex or `none` | Shape border color |
| `strokeWidth` | number | Border thickness (1, 2, or 3) |
| `rounded` | `0` or `1` | Round corners on rectangles |
| `dashed` | `0` or `1` | Dashed stroke |
| `dashPattern` | string | Custom dash pattern (e.g., `3 3` for dotted) |
| `opacity` | 0-100 | Overall opacity |
| `shadow` | `0` or `1` | Drop shadow |
| `sketch` | `0` or `1` | Hand-drawn look (0 = clean, 1 = sketchy) |

### Text Style Properties

| Property | Description |
|----------|-------------|
| `fontColor` | Text color (hex) |
| `fontSize` | Size in pixels (16-20 recommended) |
| `fontFamily` | Typeface (use `Courier New` for monospace) |
| `fontStyle` | Bitmask: bold=1, italic=2, underline=4 (combine with OR) |
| `align` | Horizontal: `left`, `center`, `right` |
| `verticalAlign` | Vertical: `top`, `middle`, `bottom` |
| `whiteSpace` | Set to `wrap` to enable text wrapping |
| `html` | Set to `1` to enable HTML in labels |
| `spacingTop`, `spacingBottom`, `spacingLeft`, `spacingRight` | Label padding (pixels) |
| `overflow` | `fill`, `width`, `hidden`, `visible` |

### Text in Shapes vs Standalone Text

**Text inside a shape**: Set the `value` attribute on the shape's `<mxCell>`:
```xml
<mxCell id="2" value="Process Step" style="rounded=1;whiteSpace=wrap;html=1;fontSize=16;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="180" height="90" as="geometry" />
</mxCell>
```

**Standalone text** (no container): Use `text;fillColor=none;strokeColor=none;`:
```xml
<mxCell id="3" value="Section Title" style="text;html=1;fillColor=none;strokeColor=none;fontColor=#1e40af;fontSize=20;fontStyle=1;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="50" width="200" height="30" as="geometry" />
</mxCell>
```

## Edge Styles (connections)

```xml
<mxCell id="edge1" style="endArrow=classic;strokeColor=#1e3a5f;strokeWidth=2;"
        edge="1" parent="1" source="shape1" target="shape2">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

### Arrowhead Types

| `endArrow` / `startArrow` | Description |
|---------------------------|-------------|
| `classic` | Standard filled arrow |
| `block` | Filled block/triangle |
| `open` | Open (unfilled) arrow |
| `oval` | Circular endpoint |
| `diamond` | Diamond endpoint |
| `none` | No arrowhead |

Use `endFill=0` to make a filled type hollow.

### Edge Routing

| `edgeStyle=` value | Description |
|-------------------|-------------|
| *(omitted)* | Straight line (direct) |
| `orthogonalEdgeStyle` | Right-angle routing |
| `elbowEdgeStyle` | Simple elbow (one bend) |
| `curved=1` (no edgeStyle) | Smooth curve |

### Waypoints (Intermediate Points)

```xml
<mxCell id="edge1" style="..." edge="1" parent="1" source="s" target="t">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="300" y="200" />
      <mxPoint x="400" y="200" />
    </Array>
  </mxGeometry>
</mxCell>
```

### Connection Points (Fine-Grained)

Control where edges attach to shapes:
```
exitX=0.5;exitY=1;exitPerimeter=1;entryX=0.5;entryY=0;entryPerimeter=1;
```
Values are 0 to 1, relative to shape bounds (0,0 = top-left; 1,1 = bottom-right).

## Geometry

```xml
<mxGeometry x="100" y="50" width="180" height="90" as="geometry" />
```

- Coordinates are absolute pixels from top-left origin
- X increases rightward, Y increases downward
- Edge geometry uses `relative="1"` for label positioning

## Grouping

Use the `parent` attribute to group cells under a container:
```xml
<!-- Container -->
<mxCell id="group1" value="Group" style="group;" vertex="1" parent="1">
  <mxGeometry x="50" y="50" width="300" height="200" as="geometry" />
</mxCell>
<!-- Child inside the container -->
<mxCell id="child1" value="Inside" style="rounded=1;" vertex="1" parent="group1">
  <mxGeometry x="10" y="10" width="100" height="50" as="geometry" />
</mxCell>
```

Child coordinates are relative to their parent container.

## Special Characters in `value`

Use XML entities for special characters:
- `&quot;` for `"`
- `&amp;` for `&`
- `&lt;` for `<`
- `&gt;` for `>`
- `&#xa;` for newline
