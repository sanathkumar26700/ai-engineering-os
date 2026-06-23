# Premium Flowchart GIF Generator

An elegant, high-definition flowchart animation generator that produces dark-mode loops with glassmorphic cards, custom vector-drawn icons, active particle trails, and interactive Gaussian-proximity neon glowing borders.

Designed to showcase AI systems and developer workflows, the generator compiles smooth 60-frame loops with custom color themes and adaptive color quantization.

---

## 🚀 Quick Start & Installation

This project is built using Python 3.12+ and uses [Pillow](https://python-pillow.org/) for vector drawing and GIF compilation. 

### 1. Prerequisites
Ensure you have [uv](https://github.com/astral-sh/uv) (a fast Python package manager) installed. If you don't have it, install it via:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
Alternatively, you can use regular Python virtual environments (`venv`) and `pip`.

### 2. Setup Dependencies
If using `uv` (recommended), dependencies are managed automatically through [pyproject.toml](file:///Users/sanathkumar/Documents/ai-engineering-os/gif-creator/pyproject.toml) and [uv.lock](file:///Users/sanathkumar/Documents/ai-engineering-os/gif-creator/uv.lock).

If you prefer to set up a manual virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r pyproject.toml
```

### 3. Generate the Default GIF
To run the default generator which produces `ai_loop.gif`:
```bash
# Using uv
uv run generator.py

# Using standard python
python generator.py
```

### 4. Generate from a Custom JSON Configuration
To render a custom flowchart layout using a config file (such as [example_flow.json](file:///Users/sanathkumar/Documents/ai-engineering-os/gif-creator/example_flow.json)):
```bash
# Using uv
uv run render_from_config.py example_flow.json

# Using standard python
python render_from_config.py example_flow.json
```
This compiles the custom layout into `compiled_flow.gif`.

---

## 🛠️ How it Works (Under the Hood)

The animation pipeline executes in the following stages:

### 1. Dynamic Resolution & Grid Calculation
- **HD Scaling**: The canvas base resolution is `1200x500` scaled by `SCALE = 2` for a sharp, retina-ready `2400x1000` final image.
- **Auto-Spacing**: The layout engine in [render_from_config.py](file:///Users/sanathkumar/Documents/ai-engineering-os/gif-creator/render_from_config.py) automatically calculates margins, card spacing, and path loops based on the number of nodes defined in the JSON configuration.

### 2. Rendering Order (Z-Indexing)
To prevent visual overlap and artifacts, layers are compiled from back to front:
1. **Background Canvas**: Painted deep dark navy-black (`#080C14`).
2. **Glow Layer**: Semi-translucent blurred neon shapes drawn behind active cards.
3. **Static Connection Lines & Loopback**: Dim connectors (`#1F2E4D`) showing the base flowchart structure.
4. **Active Connection Highlights**: Vibrant colors drawn dynamically behind/along the active particle's current coordinates.
5. **Card Backdrops**: Rounded glassmorphic rectangles (`#111827`) that act as a mask, hiding any connection lines underneath them.
6. **Card Content**: Custom vector-drawn icons and labels (e.g., node titles and subtitles) using system-loaded Helvetica or Arial fonts.
7. **Moving Particle & Trail**: A bright colored core particle with a trailing decay path overlaying the entire canvas.

### 3. Visual & Mathematical Equations
* **Gaussian Proximity Glow**: As the active particle travels, its distance $d$ to each card center is measured. The card's neon highlight border and shadow glow are interpolated dynamically using:
  $$\text{glow\_factor} = e^{-\left(\frac{d}{220}\right)^2}$$
  This ensures a smooth, organic breathing effect as the particle passes through or near a card.
* **Return Loop Path Interpolation**: The loopback path uses parameterized Bezier-like linear segment and arc calculations to glide the particle smoothly from the last card back to the start.

### 4. Vector Icon Recipes (Pillow)
Rather than using static png images, the generator draws premium clean shapes mathematically:
- **`database`**: Vertically stacked cylinders with shaded top caps for a pseudo-3D look.
- **`cubes`**: Three shaded isometric 3D blocks with face lighting highlights.
- **`target`**: Concentric rings with a solid core (bullseye).
- **`sync`**: Clean clockwise/counter-clockwise loop with custom-drawn polygon arrowheads.

### 5. Adaptive Quantization Compression
Neon gradients are notoriously hard to render in standard GIFs, often leading to heavy banding and noise. The generator uses Pillow's `ADAPTIVE` palette quantization:
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
This maps the color palette to the exact colors used, ensuring smooth neon transitions.

---

## 📋 JSON Configuration Schema

You can define custom flowcharts by creating a JSON configuration file. Here is the structure:

```json
{
  "title": "Custom Flow Title",
  "loopback": true,
  "nodes": [
    {
      "name": "Data Source",
      "desc": "Collect raw inputs",
      "color": "cyan",
      "icon": "database"
    },
    {
      "name": "Processing",
      "desc": "Clean and filter",
      "color": "blue",
      "icon": "cubes"
    },
    {
      "name": "Analysis",
      "desc": "Extract patterns",
      "color": "emerald",
      "icon": "target"
    }
  ]
}
```

### Options:
- **`title`**: Header string displayed on top of the GIF.
- **`loopback`**: Boolean (`true`/`false`). If true, a bottom looping path is drawn back to the start.
- **`color`**: Theme accent color for the node. Supported values: `cyan`, `blue`, `emerald`, `indigo`, `purple`, `orange`, `red`, `green`, `pink`.
- **`icon`**: Graphic style for the node. Supported values: `database`, `cubes`, `target`, `sync`. Fallback is a simple outlined circle.

---

For design guidelines and technical specs, read the companion [SKILL.md](file:///Users/sanathkumar/Documents/ai-engineering-os/gif-creator/SKILL.md) file.
