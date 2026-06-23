---
name: Premium Flowchart GIF Generator
description: A skill to transform simple flowchart descriptions into eye-catching, high-definition dark-mode animated GIFs with glowing particles, dynamic card borders, and smooth vector icons.
---

# Premium Flowchart GIF Generator

Use this skill to convert any textual flowchart description (e.g. `Data -> Model -> Prediction -> Feedback -> Data`) into a stunning, high-definition dark-mode animated loop. 

---

## 📥 Input Specification

The input is a list of nodes and optional loops:
```text
Title: My Custom Flow
Nodes:
1. NodeName1 | Subtitle1 | IconType1 | ThemeColor1
2. NodeName2 | Subtitle2 | IconType2 | ThemeColor2
3. NodeName3 | Subtitle3 | IconType3 | ThemeColor3
Loopback: True (from final Node back to Node 1)
```

### Standard Icon Types:
- `database`: Stack of three 2.5D cylinders.
- `cubes`: Shaded 3D isometric cubes.
- `target`: Concentric rings with a solid core.
- `sync`: Clockwise/counter-clockwise circular loops.

### Standard Theme Colors (RGB):
- Cyan: `(0, 240, 255)`
- Blue: `(59, 130, 246)`
- Emerald: `(16, 185, 129)`
- Indigo: `(99, 102, 241)`

---

## 🎨 Visual Specifications & Layout Rules

1. **Canvas Resolution**: Use `2400x1000` (High-definition, retina-ready scale factor `SCALE = 2` on top of a `1200x500` base).
2. **Background Color**: Flat deep dark navy-black: `#080C14` / `(8, 12, 20)`.
3. **Card Styling**: 
   - Cards are rounded rectangles (`radius = 24`).
   - Filled with glassmorphic semi-translucent dark blue: `#111827` / `(17, 24, 39)`.
   - Card size: `440x440` pixels.
   - Default borders are dim gray: `#1F2E4D` / `(31, 46, 77)`, width = `4px`.
4. **Card Positioning**: Distribute card centers `cx_i` symmetrically across the canvas:
   $$\text{cx}_i = \text{left\_margin} + i \times (\text{width} + \text{spacing}) + \frac{\text{width}}{2}$$

---

## 📐 Vector Drawing Recipes (Pillow)

### 1. Pseudo-3D Database Cylinder
Draws a shaded vertical disk structure representing a storage volume:
```python
def draw_cylinder(draw, x, y, w, h, fill, border):
    ellipse_h = h // 2
    # Bottom elliptical base
    draw.ellipse([x, y + h - ellipse_h, x + w, y + h], fill=fill)
    # Side walls
    draw.rectangle([x, y + ellipse_h // 2, x + w, y + h - ellipse_h // 2], fill=fill)
    # Top elliptical lid (lighter tint for 3D look)
    top_fill = tuple(min(255, c + 35) for c in fill[:3]) + (fill[3],) if len(fill) == 4 else tuple(min(255, c + 35) for c in fill)
    draw.ellipse([x, y, x + w, y + ellipse_h], fill=top_fill, outline=border, width=4)
    # Borders
    draw.line([x, y + ellipse_h // 2, x, y + h - ellipse_h // 2], fill=border, width=4)
    draw.line([x + w, y + ellipse_h // 2, x + w, y + h - ellipse_h // 2], fill=border, width=4)
    draw.arc([x, y + h - ellipse_h, x + w, y + h], start=0, end=180, fill=border, width=4)
```

### 2. Shaded Isometric Cubes
Draws three layered isometric blocks:
```python
def draw_isometric_cube(draw, cx, cy, size, top_color, left_color, right_color, border_color):
    w = int(size * 0.866)  # cos(30 deg)
    h = int(size * 0.5)    # sin(30 deg)
    l = size
    
    top_face = [(cx, cy - h), (cx + w, cy), (cx, cy + h), (cx - w, cy)]
    left_face = [(cx - w, cy), (cx, cy + h), (cx, cy + h + l), (cx - w, cy + l)]
    right_face = [(cx, cy + h), (cx + w, cy), (cx + w, cy + l), (cx, cy + h + l)]
    
    draw.polygon(top_face, fill=top_color, outline=border_color, width=2)
    draw.polygon(left_face, fill=left_color, outline=border_color, width=2)
    draw.polygon(right_face, fill=right_color, outline=border_color, width=2)
```

### 3. Bold Counter-Clockwise Sync Icon
Draws a clean, thick clockwise/counter-clockwise refresh loop:
```python
def draw_sync_icon(draw, cx, cy, color):
    r = 44
    draw.arc([cx - r, cy - r, cx + r, cy + r], start=210, end=330, fill=color, width=10)
    draw.arc([cx - r, cy - r, cx + r, cy + r], start=30, end=150, fill=color, width=10)
    
    # Arrowhead 1 (bottom-left)
    x1 = int(cx + r * math.cos(math.radians(210)))
    y1 = int(cy + r * math.sin(math.radians(210)))
    draw.polygon([(x1, y1), (x1 + 6, y1 - 24), (x1 + 24, y1 - 6)], fill=color)
    
    # Arrowhead 2 (top-right)
    x2 = int(cx + r * math.cos(math.radians(30)))
    y2 = int(cy + r * math.sin(math.radians(30)))
    draw.polygon([(x2, y2), (x2 - 24, y2 + 6), (x2 - 6, y2 + 24)], fill=color)
```

---

## ⚙️ Physics-based Animation Guidelines

To achieve premium dynamics, use the following two visual equations:

1. **Gaussian Proximity Glow**:
   Calculate the Euclidean distance $d$ from the particle position $(p_x, p_y)$ to each card's center $(c_{x}, c_{y})$. The border highlight and shadow glow intensity factor is:
   $$\text{glow\_factor} = e^{-\left(\frac{d}{220}\right)^2}$$
   Apply this value to interpolate card border colors and neon glow transparency dynamically.

2. **Layering Rule**:
   - Connection line paths (dim lines and active highlights) MUST be drawn **before** card shapes.
   - Card shapes are drawn on top of the connection lines, naturally masking any internal lines.
   - The glowing particle and its fading trail history are drawn on top of everything.

---

## 🏃 Execution Workflow

1. **Local System Fonts**: Load high-quality system fonts (Helvetica on macOS, Arial as fallback) to avoid internet latency and missing assets:
   - Bold title: `/System/Library/Fonts/Helvetica.ttc` (index 1)
   - Regular body: `/System/Library/Fonts/Helvetica.ttc` (index 0)
2. **GIF Compression**: Save using adaptive color quantization to ensure smooth, noise-free neon gradients:
   ```python
   frames[0].save(
       "output.gif",
       save_all=True,
       append_images=frames[1:],
       duration=50,
       loop=0,
       optimize=True,
       palette=Image.Palette.ADAPTIVE
   )
   ```
