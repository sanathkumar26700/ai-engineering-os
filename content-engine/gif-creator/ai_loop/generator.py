import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ---------------------------------------------------------
# CONSTANTS & STYLING CONFIG (SCALED FOR HD 2400x1000)
# ---------------------------------------------------------
SCALE = 2
WIDTH, HEIGHT = 1200 * SCALE, 500 * SCALE

BG_COLOR = (8, 12, 20, 255)         # Deep dark blue/gray
CARD_BG_COLOR = (17, 24, 39, 255)    # Translucent glass dark blue
BORDER_DEFAULT = (31, 46, 77, 255)   # Dim card border

# Themes for cards: (R, G, B)
THEME_CYAN = (0, 240, 255)
THEME_BLUE = (59, 130, 246)
THEME_EMERALD = (16, 185, 129)
THEME_INDIGO = (99, 102, 241)

CARDS_CONFIG = [
    {
        "name": "Data",
        "desc": "Start with examples",
        "color": THEME_CYAN,
        "cx": 180 * SCALE,
    },
    {
        "name": "Model",
        "desc": "A function with knobs",
        "color": THEME_BLUE,
        "cx": 460 * SCALE,
    },
    {
        "name": "Prediction",
        "desc": "Make a guess",
        "color": THEME_EMERALD,
        "cx": 740 * SCALE,
    },
    {
        "name": "Feedback",
        "desc": "Measure the error",
        "color": THEME_INDIGO,
        "cx": 1020 * SCALE,
    }
]

CARD_Y = 130 * SCALE
CARD_W = 220 * SCALE
CARD_H = 220 * SCALE
CARD_CY = CARD_Y + CARD_H // 2  # 480

# ---------------------------------------------------------
# PATH INTERPOLATION FUNCTIONS (SCALED)
# ---------------------------------------------------------
def get_return_path_pos(t):
    """
    Interpolates coordinates along the outer bottom return loop.
    Starts at Feedback center (2040, 480), exits right, loops under,
    and enters Data center (360, 480) from the left.
    """
    x_feed, y_feed = 2040, 480
    x_data, y_data = 360, 480
    
    if t <= 0.083:
        # Segment 1: Horizontal right
        local_t = t / 0.083
        return int(x_feed + 260 * local_t), y_feed
    elif t <= 0.159:
        # Segment 2: Vertical down
        local_t = (t - 0.083) / 0.076
        return 2300, int(y_feed + 240 * local_t)
    elif t <= 0.219:
        # Segment 3: Arc bottom-right
        local_t = (t - 0.159) / 0.060
        theta = local_t * (math.pi / 2)
        return int(2180 + 120 * math.cos(theta)), int(720 + 120 * math.sin(theta))
    elif t <= 0.844:
        # Segment 4: Horizontal left
        local_t = (t - 0.219) / 0.625
        return int(2180 - 1960 * local_t), 840
    elif t <= 0.904:
        # Segment 5: Arc bottom-left
        local_t = (t - 0.844) / 0.060
        theta = math.pi / 2 + local_t * (math.pi / 2)
        return int(220 + 120 * math.cos(theta)), int(720 + 120 * math.sin(theta))
    elif t <= 0.980:
        # Segment 6: Vertical up
        local_t = (t - 0.904) / 0.076
        return 100, int(720 - 240 * local_t)
    else:
        # Segment 7: Horizontal right (enter Data)
        local_t = (t - 0.980) / (1.0 - 0.980)
        return int(100 + 260 * local_t), y_data


def get_particle_pos(frame):
    """
    Returns (x, y) coordinates of the particle for a given frame (0 to 59).
    """
    if frame <= 11:
        # Phase 1: Data -> Model
        t = frame / 11.0
        return int(360 + (920 - 360) * t), 480
    elif frame <= 23:
        # Phase 2: Model -> Prediction
        t = (frame - 12) / 11.0
        return int(920 + (1480 - 920) * t), 480
    elif frame <= 35:
        # Phase 3: Prediction -> Feedback
        t = (frame - 24) / 11.0
        return int(1480 + (2040 - 1480) * t), 480
    else:
        # Phase 4: Feedback -> Data (Loopback)
        t = (frame - 36) / 23.0
        return get_return_path_pos(t)


# ---------------------------------------------------------
# FONT HANDLING
# ---------------------------------------------------------
def get_fonts():
    mac_helvetica = "/System/Library/Fonts/Helvetica.ttc"
    mac_arial_reg = "/System/Library/Fonts/Supplemental/Arial.ttf"
    mac_arial_bold = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
    
    try:
        if os.path.exists(mac_helvetica):
            print("Loading system font: Helvetica")
            font_title = ImageFont.truetype(mac_helvetica, 34 * SCALE, index=1)  # Helvetica Bold
            font_name = ImageFont.truetype(mac_helvetica, 22 * SCALE, index=1)   # Helvetica Bold
            font_desc = ImageFont.truetype(mac_helvetica, 14 * SCALE, index=0)   # Helvetica Regular
            return font_title, font_name, font_desc
        elif os.path.exists(mac_arial_reg) and os.path.exists(mac_arial_bold):
            print("Loading system font: Arial")
            font_title = ImageFont.truetype(mac_arial_bold, 34 * SCALE)
            font_name = ImageFont.truetype(mac_arial_bold, 22 * SCALE)
            font_desc = ImageFont.truetype(mac_arial_reg, 14 * SCALE)
            return font_title, font_name, font_desc
    except Exception as e:
        print(f"Error loading system fonts: {e}")
        
    print("Falling back to default font.")
    font_title = ImageFont.load_default()
    font_name = ImageFont.load_default()
    font_desc = ImageFont.load_default()
    return font_title, font_name, font_desc

# ---------------------------------------------------------
# DRAWING HELPER FUNCTIONS (SCALED)
# ---------------------------------------------------------
def draw_cylinder(draw, x, y, w, h, fill, border):
    """Draws a premium pseudo-3D cylinder with a shaded top cap face."""
    ellipse_h = h // 2
    # Bottom elliptical base (solid fill)
    draw.ellipse([x, y + h - ellipse_h, x + w, y + h], fill=fill)
    # Side walls (solid fill)
    draw.rectangle([x, y + ellipse_h // 2, x + w, y + h - ellipse_h // 2], fill=fill)
    # Top elliptical lid (slightly lighter to convey 2.5D light source)
    top_fill = tuple(min(255, c + 35) for c in fill[:3]) + (fill[3],) if len(fill) == 4 else tuple(min(255, c + 35) for c in fill)
    draw.ellipse([x, y, x + w, y + ellipse_h], fill=top_fill, outline=border, width=4)
    # Side borders
    draw.line([x, y + ellipse_h // 2, x, y + h - ellipse_h // 2], fill=border, width=4)
    draw.line([x + w, y + ellipse_h // 2, x + w, y + h - ellipse_h // 2], fill=border, width=4)
    # Bottom curved border
    draw.arc([x, y + h - ellipse_h, x + w, y + h], start=0, end=180, fill=border, width=4)


def draw_isometric_cube(draw, cx, cy, size, top_color, left_color, right_color, border_color):
    """Draws an isometric 3D cube with custom face lighting."""
    w = int(size * 0.866)  # cos(30 deg)
    h = int(size * 0.5)    # sin(30 deg)
    l = size               # height
    
    top_face = [(cx, cy - h), (cx + w, cy), (cx, cy + h), (cx - w, cy)]
    left_face = [(cx - w, cy), (cx, cy + h), (cx, cy + h + l), (cx - w, cy + l)]
    right_face = [(cx, cy + h), (cx + w, cy), (cx + w, cy + l), (cx, cy + h + l)]
    
    draw.polygon(top_face, fill=top_color, outline=border_color, width=2)
    draw.polygon(left_face, fill=left_color, outline=border_color, width=2)
    draw.polygon(right_face, fill=right_color, outline=border_color, width=2)


def draw_target_icon(draw, cx, cy, color):
    """Draws a beautiful target/bullseye icon."""
    r_outer = 52
    r_mid = 32
    r_inner = 12
    
    # Outer ring
    draw.ellipse([cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer], outline=color, width=8)
    # Middle ring
    draw.ellipse([cx - r_mid, cy - r_mid, cx + r_mid, cy + r_mid], outline=color, width=8)
    # Center dot
    draw.ellipse([cx - r_inner, cy - r_inner, cx + r_inner, cy + r_inner], fill=color)


def draw_sync_icon(draw, cx, cy, color):
    """Draws circular sync arrows in a bold, counter-clockwise loop matching the target image."""
    r = 44
    # Bolder width (10px) to match the premium flat aesthetic
    draw.arc([cx - r, cy - r, cx + r, cy + r], start=210, end=330, fill=color, width=10)
    draw.arc([cx - r, cy - r, cx + r, cy + r], start=30, end=150, fill=color, width=10)
    
    # Arrowhead 1 (at 210 degrees - bottom-left end of top arc)
    x1 = int(cx + r * math.cos(math.radians(210)))
    y1 = int(cy + r * math.sin(math.radians(210)))
    draw.polygon([
        (x1, y1),
        (x1 + 6, y1 - 24),
        (x1 + 24, y1 - 6)
    ], fill=color)
    
    # Arrowhead 2 (at 30 degrees - top-right end of bottom arc)
    x2 = int(cx + r * math.cos(math.radians(30)))
    y2 = int(cy + r * math.sin(math.radians(30)))
    draw.polygon([
        (x2, y2),
        (x2 - 24, y2 + 6),
        (x2 - 6, y2 + 24)
    ], fill=color)


def draw_glow_rect(img, box, radius, color, opacity=0.18):
    """Draws a blurred neon-glow rectangle behind a card."""
    glow_img = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(glow_img)
    x0, y0, x1, y1 = box
    
    glow_box = [x0 - 8, y0 - 8, x1 + 8, y1 + 8]
    
    draw.rounded_rectangle(glow_box, radius=radius + 8, fill=(color[0], color[1], color[2], int(255 * opacity)))
    # Apply Gaussian blur
    glow_img = glow_img.filter(ImageFilter.GaussianBlur(radius=32))
    
    # Composite the glow onto the main image
    img.alpha_composite(glow_img)


# ---------------------------------------------------------
# FRAME RENDERING
# ---------------------------------------------------------
def render_frame(frame, font_title, font_name, font_desc, trail_history):
    # Create main RGBA image
    img = Image.new("RGBA", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # 1. Draw Title
    title_text = "Almost every AI system runs the same loop"
    draw.text((WIDTH // 2, 110), title_text, font=font_title, fill=(255, 255, 255, 255), anchor="mm")
    
    # Get current particle position
    px, py = get_particle_pos(frame)
    trail_history.append((px, py))
    if len(trail_history) > 8:
        trail_history.pop(0)
        
    # Calculate glow factors for cards based on particle proximity
    glow_factors = []
    for card in CARDS_CONFIG:
        cx, cy = card["cx"], CARD_CY
        dist = math.sqrt((px - cx)**2 + (py - cy)**2)
        # Scaled proximity bell curve
        glow_val = math.exp(- (dist / 220.0)**2)
        glow_factors.append(glow_val)
        
    # 2. Draw Glow Layer (behind lines and cards)
    for i, card in enumerate(CARDS_CONFIG):
        cx = card["cx"]
        color = card["color"]
        glow_val = glow_factors[i]
        
        if glow_val > 0.05:
            x0 = cx - CARD_W // 2
            y0 = CARD_Y
            x1 = cx + CARD_W // 2
            y1 = CARD_Y + CARD_H
            draw_glow_rect(img, [x0, y0, x1, y1], 12 * SCALE, color, opacity=glow_val * 0.25)
            
    # 3. Draw Static Connection Lines & Loopback Path (dim background)
    # Loopback line
    loopback_points = []
    for step in range(101):
        loopback_points.append(get_return_path_pos(step / 100.0))
    draw.line(loopback_points, fill=(24, 35, 59, 255), width=6)
    
    # Inter-card arrows (dim base)
    arrow_gaps = [
        (580, 700),    # Data -> Model
        (1140, 1260),  # Model -> Prediction
        (1700, 1820)   # Prediction -> Feedback
    ]
    for start_x, end_x in arrow_gaps:
        draw.line([(start_x, 480), (end_x, 480)], fill=(24, 35, 59, 255), width=6)
        draw.polygon([(end_x, 480), (end_x - 16, 470), (end_x - 16, 490)], fill=(24, 35, 59, 255))
        
    # 4. Draw Glowing Connection Line Highlights (only outside cards)
    if frame <= 11:
        # Highlight Arrow 0 (Data -> Model)
        if px > 580:
            h_end = min(px, 700)
            draw.line([(580, 480), (h_end, 480)], fill=(0, 240, 255, 255), width=6)
            if h_end >= 700:
                draw.polygon([(700, 480), (684, 470), (684, 490)], fill=(0, 240, 255, 255))
    elif frame <= 23:
        # Highlight Arrow 1 (Model -> Prediction)
        if px > 1140:
            h_end = min(px, 1260)
            draw.line([(1140, 480), (h_end, 480)], fill=(59, 130, 246, 255), width=6)
            if h_end >= 1260:
                draw.polygon([(1260, 480), (1244, 470), (1244, 490)], fill=(59, 130, 246, 255))
    elif frame <= 35:
        # Highlight Arrow 2 (Prediction -> Feedback)
        if px > 1700:
            h_end = min(px, 1820)
            draw.line([(1700, 480), (h_end, 480)], fill=(16, 185, 129, 255), width=6)
            if h_end >= 1820:
                draw.polygon([(1820, 480), (1804, 470), (1804, 490)], fill=(16, 185, 129, 255))
    else:
        # Highlight return path dynamically
        t = (frame - 36) / 23.0
        highlight_points = []
        steps = int(t * 100)
        for s in range(steps + 1):
            highlight_points.append(get_return_path_pos(s / 100.0))
        if len(highlight_points) > 1:
            draw.line(highlight_points, fill=(99, 102, 241, 255), width=6)

    # 5. Draw Cards (drawn after lines to cover parts inside the card)
    for i, card in enumerate(CARDS_CONFIG):
        cx = card["cx"]
        color = card["color"]
        glow_val = glow_factors[i]
        
        x0 = cx - CARD_W // 2
        y0 = CARD_Y
        x1 = cx + CARD_W // 2
        y1 = CARD_Y + CARD_H
        
        # Draw card background (covers any lines behind it)
        draw.rounded_rectangle([x0, y0, x1, y1], radius=12 * SCALE, fill=CARD_BG_COLOR)
        
        # Draw border (interpolated color)
        border_r = int(BORDER_DEFAULT[0] + (color[0] - BORDER_DEFAULT[0]) * glow_val)
        border_g = int(BORDER_DEFAULT[1] + (color[1] - BORDER_DEFAULT[1]) * glow_val)
        border_b = int(BORDER_DEFAULT[2] + (color[2] - BORDER_DEFAULT[2]) * glow_val)
        border_color = (border_r, border_g, border_b, 255)
        
        b_width = 4 if glow_val < 0.1 else 6
        draw.rounded_rectangle([x0, y0, x1, y1], radius=12 * SCALE, outline=border_color, width=b_width)
        
        # 6. Draw Card Content (Icons & Text)
        icon_cy = CARD_Y + 130
        
        if i == 0:  # Data: database stack
            cyl_fill = (0, 30, 40, 255)
            cyl_border = (0, int(150 + 105 * glow_val), int(160 + 95 * glow_val), 255)
            draw_cylinder(draw, cx - 56, icon_cy + 30, 112, 32, cyl_fill, cyl_border)
            draw_cylinder(draw, cx - 56, icon_cy, 112, 32, cyl_fill, cyl_border)
            draw_cylinder(draw, cx - 56, icon_cy - 30, 112, 32, cyl_fill, cyl_border)
            
        elif i == 1:  # Model: 3D cubes
            border_c = (int(30 + 150 * glow_val), int(50 + 130 * glow_val), int(120 + 120 * glow_val), 255)
            top_c = (110, 170, 250, 255) if glow_val > 0.5 else (70, 120, 200, 255)
            left_c = (59, 130, 246, 255) if glow_val > 0.5 else (40, 90, 180, 255)
            right_c = (29, 78, 216, 255) if glow_val > 0.5 else (20, 50, 140, 255)
            
            draw_isometric_cube(draw, cx, icon_cy - 30, 28, top_c, left_c, right_c, border_c)
            draw_isometric_cube(draw, cx - 28, icon_cy + 16, 28, top_c, left_c, right_c, border_c)
            draw_isometric_cube(draw, cx + 28, icon_cy + 16, 28, top_c, left_c, right_c, border_c)
            
        elif i == 2:  # Prediction: Bullseye
            p_color = (int(16 + 200 * glow_val), int(185 + 70 * glow_val), int(129 + 100 * glow_val), 255)
            draw_target_icon(draw, cx, icon_cy, p_color)
            
        elif i == 3:  # Feedback: Sync
            f_color = (int(99 + 130 * glow_val), int(102 + 130 * glow_val), int(241 + 14 * glow_val), 255)
            draw_sync_icon(draw, cx, icon_cy, f_color)
            
        # Draw Card Text
        text_color = (255, 255, 255, 255) if glow_val > 0.2 else (226, 232, 240, 255)
        # Title
        draw.text((cx, CARD_Y + 280), card["name"], font=font_name, fill=text_color, anchor="mm")
        # Subtitle
        draw.text((cx, CARD_Y + 350), card["desc"], font=font_desc, fill=(148, 163, 184, 255), anchor="mm")

    # 7. Draw Particle Motion Trail (drawn on top of cards)
    particle_color = CARDS_CONFIG[0]["color"] if frame <= 11 else (
        CARDS_CONFIG[1]["color"] if frame <= 23 else (
            CARDS_CONFIG[2]["color"] if frame <= 35 else CARDS_CONFIG[3]["color"]
        )
    )
    
    for idx, (tx, ty) in enumerate(trail_history):
        alpha = int(255 * ((idx + 1) / len(trail_history)))
        radius = int(10 * ((idx + 1) / len(trail_history)))
        if radius < 1:
            radius = 1
        
        # Soft outer glow
        glow_rad = radius + 6
        draw.ellipse([tx - glow_rad, ty - glow_rad, tx + glow_rad, ty + glow_rad], 
                     fill=(particle_color[0], particle_color[1], particle_color[2], int(alpha * 0.3)))
        
        # Bright core
        draw.ellipse([tx - radius, ty - radius, tx + radius, ty + radius], 
                     fill=(particle_color[0], particle_color[1], particle_color[2], alpha))
                     
    return img.convert("RGB")

# ---------------------------------------------------------
# MAIN EXECUTION
# ---------------------------------------------------------
def main():
    print("Initializing HD GIF Generation...")
    font_title, font_name, font_desc = get_fonts()
    
    frames = []
    trail_history = []
    
    total_frames = 60
    print(f"Rendering {total_frames} frames...")
    
    for f in range(total_frames):
        pct = int(100 * f / total_frames)
        print(f"Rendering frame {f:02d}/{total_frames} [{pct}%]", end="\r")
        
        frame_img = render_frame(f, font_title, font_name, font_desc, trail_history)
        frames.append(frame_img)
        
    print("\nCompiling HD GIF...")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "ai_loop.gif")
    
    # Save animated GIF using adaptive color quantization
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=50,
        loop=0,
        optimize=True,
        palette=Image.Palette.ADAPTIVE
    )
    
    print(f"Success! Saved HD AI Loop animation to: {os.path.abspath(output_path)}")

if __name__ == "__main__":
    main()
