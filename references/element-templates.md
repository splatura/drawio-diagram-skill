# Element Templates

Copy-paste XML templates for each draw.io element type. The `fillColor`, `strokeColor`, and `fontColor` values are placeholders — always pull actual colors from `color-palette.md` based on the element's semantic purpose.

**Important**: All elements require the root structure with cells `id="0"` and `id="1"` — see `json-schema.md` for the full file wrapper.

## Free-Floating Text (no container)
```xml
<mxCell id="label1" value="Section Title"
        style="text;html=1;align=left;verticalAlign=top;fillColor=none;strokeColor=none;fontColor=<title color from palette>;fontSize=20;fontFamily=Courier New;fontStyle=1;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="200" height="30" as="geometry" />
</mxCell>
```

## Line (structural, not arrow)
```xml
<mxCell id="line1"
        style="endArrow=none;startArrow=none;strokeColor=<structural line color from palette>;strokeWidth=2;"
        edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="100" y="100" as="sourcePoint" />
    <mxPoint x="100" y="300" as="targetPoint" />
  </mxGeometry>
</mxCell>
```

## Small Marker Dot
```xml
<mxCell id="dot1" value=""
        style="shape=ellipse;perimeter=ellipsePerimeter;fillColor=<marker dot color from palette>;strokeColor=<marker dot color from palette>;strokeWidth=1;"
        vertex="1" parent="1">
  <mxGeometry x="94" y="94" width="12" height="12" as="geometry" />
</mxCell>
```

## Rectangle
```xml
<mxCell id="elem1" value="Process"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=<fill from palette>;strokeColor=<stroke from palette>;strokeWidth=2;fontColor=<text color>;fontSize=16;fontFamily=Courier New;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="180" height="90" as="geometry" />
</mxCell>
```

## Ellipse
```xml
<mxCell id="elem2" value="Start"
        style="shape=ellipse;perimeter=ellipsePerimeter;whiteSpace=wrap;html=1;fillColor=<fill from palette>;strokeColor=<stroke from palette>;strokeWidth=2;fontColor=<text color>;fontSize=16;fontFamily=Courier New;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="140" height="80" as="geometry" />
</mxCell>
```

## Diamond (Decision)
```xml
<mxCell id="elem3" value="Decision"
        style="shape=rhombus;perimeter=rhombusPerimeter;whiteSpace=wrap;html=1;fillColor=<fill from palette>;strokeColor=<stroke from palette>;strokeWidth=2;fontColor=<text color>;fontSize=14;fontFamily=Courier New;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="110" height="70" as="geometry" />
</mxCell>
```

## Arrow (connection)
```xml
<mxCell id="arrow1"
        style="endArrow=classic;strokeColor=<arrow color from palette>;strokeWidth=2;"
        edge="1" parent="1" source="elem1" target="elem2">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

For curved arrows, add `curved=1`:
```xml
<mxCell id="arrow2"
        style="endArrow=classic;curved=1;strokeColor=<arrow color>;strokeWidth=2;"
        edge="1" parent="1" source="elem1" target="elem2">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

For arrows with waypoints:
```xml
<mxCell id="arrow3"
        style="endArrow=classic;strokeColor=<arrow color>;strokeWidth=2;"
        edge="1" parent="1" source="elem1" target="elem2">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="300" y="200" />
    </Array>
  </mxGeometry>
</mxCell>
```

## Evidence Artifact (code/data block)
```xml
<mxCell id="evidence1" value="{&#xa;  &quot;key&quot;: &quot;value&quot;&#xa;}"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1e293b;strokeColor=#1e293b;strokeWidth=1;fontColor=#22c55e;fontSize=13;fontFamily=Courier New;align=left;verticalAlign=middle;spacingLeft=15;spacingTop=5;spacingBottom=5;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="380" height="80" as="geometry" />
</mxCell>
```

Use `&#xa;` for newlines and `&quot;` for quotes in the `value` attribute.
