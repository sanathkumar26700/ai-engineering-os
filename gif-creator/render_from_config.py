import os
import sys
import json
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ---------------------------------------------------------
# STYLING CONSTANTS (SCALED FOR HD)
# ---------------------------------------------------------
SCALE = 2
BG_COLOR = (8, 12, 20, 255)         # Deep dark blue/gray
CARD_BG_COLOR = (17, 24, 39, 255)    # Translucent glass dark blue
BORDER_DEFAULT = (31, 46, 77, 255)   # Dim card border

COLOR_MAP = {
    "cyan": (0, 240, 255),
    "blue": (59, 130, 246),
    "emerald": (16, 185, 129),
    "indigo": (99, 102, 241),
    "purple": (168, 85, 247),
    "orange": (249, 115, 22),
    "red": (239, 68, 68),
    "green": (34, 197, 94),
    "pink": (236, 72, 153)
}

# ---------------------------------------------------------
# FONT HELPER
# ---------------------------------------------------------
def get_fonts():
    mac_helvetica = "/System/Library/Fonts/Helvetica.ttc"
    mac_arial_reg = "/System/Library/Fonts/Supplemental/Arial.ttf"
    mac_arial_bold = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
    
    try:
        if os.path.exists(mac_helvetica):
            font_title = ImageFont.truetype(mac_helvetica, 34 * SCALE, index=1)
            font_name = ImageFont.truetype(mac_helvetica, 22 * SCALE, index=1)
            font_desc = ImageFont.truetype(mac_helvetica, 14 * SCALE, index=0)
            return font_title, font_name, font_desc
        elif os.path.exists(mac_arial_reg) and os.path.exists(mac_arial_bold):
            font_title = ImageFont.truetype(mac_arial_bold, 34 * SCALE)
            font_name = ImageFont.truetype(mac_arial_bold, 22 * SCALE)
            font_desc = ImageFont.truetype(mac_arial_reg, 14 * SCALE)
            return font_title, font_name, font_desc
    except Exception as e:
        print(f"Error loading system fonts: {e}")
        
    font_title = ImageFont.load_default()
    font_name = ImageFont.load_default()
    font_desc = ImageFont.load_default()
    return font_title, font_name, font_desc

# ---------------------------------------------------------
# VECTOR DRAWING HELPERS
# ---------------------------------------------------------
def draw_cylinder(draw, cx, cy, fill, border):
    """Draws three stacked database cylinders centered at (cx, cy)."""
    w = 56 * SCALE
    h = 32 * SCALE
    ellipse_h = h // 2
    
    # Render three cylinders stacked vertically
    offsets = [30 * SCALE, 0, -30 * SCALE]
    for dy in offsets:
        x = cx - w // 2
        y = cy + dy - h // 2
        
        # Bottom elliptical base
        draw.ellipse([x, y + h - ellipse_h, x + w, y + h], fill=fill)
        # Side walls
        draw.rectangle([x, y + ellipse_h // 2, x + w, y + h - ellipse_h // 2], fill=fill)
        # Top elliptical lid (lighter top shade for 3D depth)
        top_fill = tuple(min(255, c + 35) for c in fill[:3]) + (fill[3],) if len(fill) == 4 else tuple(min(255, c + 35) for c in fill)
        draw.ellipse([x, y, x + w, y + ellipse_h], fill=top_fill, outline=border, width=4)
        # Side borders
        draw.line([x, y + ellipse_h // 2, x, y + h - ellipse_h // 2], fill=border, width=4)
        draw.line([x + w, y + ellipse_h // 2, x + w, y + h - ellipse_h // 2], fill=border, width=4)
        # Bottom curved border
        draw.arc([x, y + h - ellipse_h, x + w, y + h], start=0, end=180, fill=border, width=4)


def draw_isometric_cubes(draw, cx, cy, color):
    """Draws three layered isometric 3D blocks centered at (cx, cy)."""
    size = 28
    w = int(size * 0.866)
    h = int(size * 0.5)
    l = size
    
    top_c = tuple(min(255, c + 80) for c in color)
    left_c = color
    right_c = tuple(max(0, c - 60) for c in color)
    border_color = tuple(max(0, c - 100) for c in color)
    
    def draw_cube(x, y):
        top_face = [(x, y - h), (x + w, y), (x, y + h), (x - w, y)]
        left_face = [(x - w, y), (x, y + h), (x, y + h + l), (x - w, y + l)]
        right_face = [(x, y + h), (x + w, y), (x + w, y + l), (x, y + h + l)]
        
        draw.polygon(top_face, fill=top_c, outline=border_color, width=2)
        draw.polygon(left_face, fill=left_c, outline=border_color, width=2)
        draw.polygon(right_face, fill=right_c, outline=border_color, width=2)

    # Layer order: back-top, bottom-left, bottom-right
    draw_cube(cx, cy - 30)
    draw_cube(cx - 28, cy + 16)
    draw_cube(cx + 28, cy + 16)


def draw_target(draw, cx, cy, color):
    """Draws concentric target rings centered at (cx, cy)."""
    r_outer = 52
    r_mid = 32
    r_inner = 12
    draw.ellipse([cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer], outline=color, width=8)
    draw.ellipse([cx - r_mid, cy - r_mid, cx + r_mid, cy + r_mid], outline=color, width=8)
    draw.ellipse([cx - r_inner, cy - r_inner, cx + r_inner, cy + r_inner], fill=color)


def draw_sync(draw, cx, cy, color):
    """Draws circular sync arrows in a counter-clockwise loop centered at (cx, cy)."""
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


def draw_fallback(draw, cx, cy, color):
    """Fallback shape: a simple clean circle."""
    draw.ellipse([cx - 40, cy - 40, cx + 40, cy + 40], outline=color, width=8)


def draw_glow_rect(img, box, radius, color, opacity=0.18):
    glow_img = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(glow_img)
    x0, y0, x1, y1 = box
    glow_box = [x0 - 8, y0 - 8, x1 + 8, y1 + 8]
    draw.rounded_rectangle(glow_box, radius=radius + 8, fill=(color[0], color[1], color[2], int(255 * opacity)))
    glow_img = glow_img.filter(ImageFilter.GaussianBlur(radius=32))
    img.alpha_composite(glow_img)

# ---------------------------------------------------------
# ENGINE CLASS
# ---------------------------------------------------------
class ConfigFlowchartEngine:
    def __init__(self, config_path):
        with open(config_path, "r") as f:
            self.config = json.load(f)
            
        self.nodes = self.config["nodes"]
        self.loopback = self.config.get("loopback", True)
        self.title = self.config.get("title", "Flowchart")
        
        # Canvas dimensions calculations based on node count
        self.num_nodes = len(self.nodes)
        self.card_w = 220 * SCALE
        self.card_h = 220 * SCALE
        self.card_y = 130 * SCALE
        self.card_cy = self.card_y + self.card_h // 2  # 480
        
        self.margin = 140  # margins on sides
        self.spacing = 120  # spacing between cards
        
        # Calculate required width dynamically
        self.width = 2 * self.margin + self.num_nodes * self.card_w + (self.num_nodes - 1) * self.spacing
        self.height = 500 * SCALE
        
        # Assign centers to nodes
        for i, node in enumerate(self.nodes):
            node["cx"] = self.margin + i * (self.card_w + self.spacing) + self.card_w // 2
            node["rgb"] = COLOR_MAP.get(node.get("color", "cyan").lower(), (0, 240, 255))
            
        # Define loopback parameters dynamically
        self.x_feed = self.nodes[-1]["cx"]
        self.x_data = self.nodes[0]["cx"]
        self.limit_right = self.width - 100
        self.limit_left = 100
        self.limit_y_bottom = 840
        self.y_limit_v = 720
        self.radius = 120
        
        # Setup gap connections
        self.arrow_gaps = []
        for i in range(self.num_nodes - 1):
            start_x = self.nodes[i]["cx"] + self.card_w // 2
            end_x = self.nodes[i+1]["cx"] - self.card_w // 2
            self.arrow_gaps.append((start_x, end_x, self.nodes[i]["rgb"]))

    def get_return_path_pos(self, t):
        """Dynamic parameterized return loopback path."""
        if t <= 0.083:
            local_t = t / 0.083
            return int(self.x_feed + 260 * local_t), self.card_cy
        elif t <= 0.159:
            local_t = (t - 0.083) / 0.076
            return self.limit_right, int(self.card_cy + 240 * local_t)
        elif t <= 0.219:
            local_t = (t - 0.159) / 0.060
            theta = local_t * (math.pi / 2)
            return int((self.limit_right - self.radius) + self.radius * math.cos(theta)), int(self.y_limit_v + self.radius * math.sin(theta))
        elif t <= 0.844:
            local_t = (t - 0.219) / 0.625
            return int((self.limit_right - self.radius) - (self.width - 2 * self.limit_left - 2 * self.radius) * local_t), self.limit_y_bottom
        elif t <= 0.904:
            local_t = (t - 0.844) / 0.060
            theta = math.pi / 2 + local_t * (math.pi / 2)
            return int((self.limit_left + self.radius) + self.radius * math.cos(theta)), int(self.y_limit_v + self.radius * math.sin(theta))
        elif t <= 0.980:
            local_t = (t - 0.904) / 0.076
            return self.limit_left, int(self.y_limit_v - 240 * local_t)
        else:
            local_t = (t - 0.980) / (1.0 - 0.980)
            return int(self.limit_left + 260 * local_t), self.card_cy

    def get_particle_pos(self, frame):
        """Finds the coordinates of the particle for any frame (0 to 59)."""
        if self.loopback:
            # Split: 36 frames for linear segment, 24 for return
            if frame < 36:
                # Active segment logic
                t_linear = frame / 35.0
                total_span = self.x_feed - self.x_data
                return int(self.x_data + total_span * t_linear), self.card_cy
            else:
                t_loop = (frame - 36) / 23.0
                return self.get_return_path_pos(t_loop)
        else:
            # Linear only (loops back and forth, or simply jumps)
            t = frame / 59.0
            total_span = self.x_feed - self.x_data
            return int(self.x_data + total_span * t), self.card_cy

    def render_frame(self, frame, font_title, font_name, font_desc, trail_history):
        img = Image.new("RGBA", (self.width, self.height), BG_COLOR)
        draw = ImageDraw.Draw(img)
        
        # 1. Draw Title
        draw.text((self.width // 2, 110), self.title, font=font_title, fill=(255, 255, 255, 255), anchor="mm")
        
        # Get particle position
        px, py = self.get_particle_pos(frame)
        trail_history.append((px, py))
        if len(trail_history) > 8:
            trail_history.pop(0)
            
        # Calculate proximity card glow factor
        glow_factors = []
        for node in self.nodes:
            dist = math.sqrt((px - node["cx"])**2 + (py - self.card_cy)**2)
            glow_factors.append(math.exp(- (dist / 220.0)**2))
            
        # 2. Draw Glow Layer (behind cards)
        for idx, node in enumerate(self.nodes):
            glow_val = glow_factors[idx]
            if glow_val > 0.05:
                x0 = node["cx"] - self.card_w // 2
                y0 = self.card_y
                x1 = node["cx"] + self.card_w // 2
                y1 = self.card_y + self.card_h
                draw_glow_rect(img, [x0, y0, x1, y1], 12 * SCALE, node["rgb"], opacity=glow_val * 0.25)
                
        # 3. Draw Static Connection Lines & Loopback (dim background)
        if self.loopback:
            loopback_points = [self.get_return_path_pos(s / 100.0) for s in range(101)]
            draw.line(loopback_points, fill=(24, 35, 59, 255), width=6)
            
        for start_x, end_x, _ in self.arrow_gaps:
            draw.line([(start_x, self.card_cy), (end_x, self.card_cy)], fill=(24, 35, 59, 255), width=6)
            draw.polygon([(end_x, self.card_cy), (end_x - 16, self.card_cy - 10), (end_x - 16, self.card_cy + 10)], fill=(24, 35, 59, 255))
            
        # 4. Draw Active Glowing Connections
        if self.loopback and frame >= 36:
            # Active return loopback highlight
            t_loop = (frame - 36) / 23.0
            highlight_points = [self.get_return_path_pos(s / 100.0) for s in range(int(t_loop * 100) + 1)]
            if len(highlight_points) > 1:
                draw.line(highlight_points, fill=(99, 102, 241, 255), width=6)
        else:
            # Active gap line highlight
            for start_x, end_x, rgb in self.arrow_gaps:
                if px > start_x:
                    h_end = min(px, end_x)
                    draw.line([(start_x, self.card_cy), (h_end, self.card_cy)], fill=rgb + (255,), width=6)
                    if h_end >= end_x:
                        draw.polygon([(end_x, self.card_cy), (end_x - 16, self.card_cy - 10), (end_x - 16, self.card_cy + 10)], fill=rgb + (255,))

        # 5. Draw Cards (covers lines underneath)
        for idx, node in enumerate(self.nodes):
            cx = node["cx"]
            rgb = node["rgb"]
            glow_val = glow_factors[idx]
            
            x0 = cx - self.card_w // 2
            y0 = self.card_y
            x1 = cx + self.card_w // 2
            y1 = self.card_y + self.card_h
            
            # Card background
            draw.rounded_rectangle([x0, y0, x1, y1], radius=12 * SCALE, fill=CARD_BG_COLOR)
            
            # Card border (dynamic color interpolation)
            border_r = int(BORDER_DEFAULT[0] + (rgb[0] - BORDER_DEFAULT[0]) * glow_val)
            border_g = int(BORDER_DEFAULT[1] + (rgb[1] - BORDER_DEFAULT[1]) * glow_val)
            border_b = int(BORDER_DEFAULT[2] + (rgb[2] - BORDER_DEFAULT[2]) * glow_val)
            border_color = (border_r, border_g, border_b, 255)
            
            b_width = 4 if glow_val < 0.1 else 6
            draw.rounded_rectangle([x0, y0, x1, y1], radius=12 * SCALE, outline=border_color, width=b_width)
            
            # 6. Draw Node Icons
            icon_cy = self.card_y + 130
            icon_type = node.get("icon", "fallback").lower()
            
            if icon_type == "database":
                cyl_fill = (0, 30, 40, 255)
                cyl_border = (0, int(150 + 105 * glow_val), int(160 + 95 * glow_val), 255)
                draw_cylinder(draw, cx, icon_cy, cyl_fill, cyl_border)
            elif icon_type == "cubes":
                draw_isometric_cubes(draw, cx, icon_cy, rgb + (255,))
            elif icon_type == "target":
                p_color = (int(16 + 200 * glow_val), int(185 + 70 * glow_val), int(129 + 100 * glow_val), 255)
                draw_target(draw, cx, icon_cy, p_color)
            elif icon_type == "sync":
                f_color = (int(99 + 130 * glow_val), int(102 + 130 * glow_val), int(241 + 14 * glow_val), 255)
                draw_sync(draw, cx, icon_cy, f_color)
            else:
                draw_fallback(draw, cx, icon_cy, rgb + (255,))
                
            # Node Text
            text_color = (255, 255, 255, 255) if glow_val > 0.2 else (226, 232, 240, 255)
            draw.text((cx, self.card_y + 280), node["name"], font=font_name, fill=text_color, anchor="mm")
            draw.text((cx, self.card_y + 350), node["desc"], font=font_desc, fill=(148, 163, 184, 255), anchor="mm")

        # 7. Draw Particle Trail
        # Determine particle color based on current position
        particle_color = (99, 102, 241) # Loopback color default
        if self.loopback and frame < 36:
            # Map particle to active node color
            active_seg = int((frame / 35.0) * (self.num_nodes - 1))
            active_seg = min(active_seg, self.num_nodes - 1)
            particle_color = self.nodes[active_seg]["rgb"]
        elif not self.loopback:
            active_seg = int((frame / 59.0) * (self.num_nodes - 1))
            particle_color = self.nodes[active_seg]["rgb"]
            
        for idx, (tx, ty) in enumerate(trail_history):
            alpha = int(255 * ((idx + 1) / len(trail_history)))
            radius = int(10 * ((idx + 1) / len(trail_history)))
            if radius < 1:
                radius = 1
            
            glow_rad = radius + 6
            draw.ellipse([tx - glow_rad, ty - glow_rad, tx + glow_rad, ty + glow_rad], 
                         fill=particle_color + (int(alpha * 0.3),))
            draw.ellipse([tx - radius, ty - radius, tx + radius, ty + radius], 
                         fill=particle_color + (alpha,))
                         
        return img.convert("RGB")

# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------
def main():
    config_file = sys.argv[1] if len(sys.argv) > 1 else "example_flow.json"
    if not os.path.exists(config_file):
        print(f"Error: Configuration file '{config_file}' not found.")
        sys.exit(1)
        
    print(f"Loading diagram configuration: {config_file}")
    engine = ConfigFlowchartEngine(config_file)
    
    font_title, font_name, font_desc = get_fonts()
    
    frames = []
    trail_history = []
    total_frames = 60
    
    print(f"Rendering {total_frames} frames ({engine.width}x{engine.height})...")
    for f in range(total_frames):
        pct = int(100 * f / total_frames)
        print(f"Rendering frame {f:02d}/{total_frames} [{pct}%]", end="\r")
        frame_img = engine.render_frame(f, font_title, font_name, font_desc, trail_history)
        frames.append(frame_img)
        
    print("\nCompiling GIF with adaptive palette...")
    output_path = "compiled_flow.gif"
    
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=50,
        loop=0,
        optimize=True,
        palette=Image.Palette.ADAPTIVE
    )
    print(f"Success! Generated animated GIF: {os.path.abspath(output_path)}")

if __name__ == "__main__":
    main()
