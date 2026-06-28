import os
import sys
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ---------------------------------------------------------
# CONSTANTS & STYLING CONFIG (SCALED FOR HD 2400x1200)
# ---------------------------------------------------------
SCALE = 2
WIDTH, HEIGHT = 1200 * SCALE, 600 * SCALE

BG_COLOR = (8, 12, 20, 255)         # Deep dark blue/gray
CARD_BG_COLOR = (17, 24, 39, 255)    # Translucent glass dark blue
BORDER_DEFAULT = (31, 46, 77, 255)   # Dim card border
GRID_COLOR = (18, 25, 41, 255)      # Subtlest grid line
DIVIDER_COLOR = (24, 35, 59, 255)   # Middle vertical divider
PROJ_LINE_COLOR = (255, 255, 255, 30)

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

# Card shape configuration
CARD_W = 140
CARD_H = 140
CARD_R = 70

# ---------------------------------------------------------
# FONT HELPER
# ---------------------------------------------------------
def get_fonts():
    mac_helvetica = "/System/Library/Fonts/Helvetica.ttc"
    mac_arial_reg = "/System/Library/Fonts/Supplemental/Arial.ttf"
    mac_arial_bold = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
    
    try:
        if os.path.exists(mac_helvetica):
            font_title = ImageFont.truetype(mac_helvetica, 36 * SCALE, index=1)
            font_side_title = ImageFont.truetype(mac_helvetica, 22 * SCALE, index=1)
            font_name = ImageFont.truetype(mac_helvetica, 16 * SCALE, index=1)
            font_desc = ImageFont.truetype(mac_helvetica, 11 * SCALE, index=0)
            return font_title, font_side_title, font_name, font_desc
        elif os.path.exists(mac_arial_reg) and os.path.exists(mac_arial_bold):
            font_title = ImageFont.truetype(mac_arial_bold, 36 * SCALE)
            font_side_title = ImageFont.truetype(mac_arial_bold, 22 * SCALE)
            font_name = ImageFont.truetype(mac_arial_bold, 16 * SCALE)
            font_desc = ImageFont.truetype(mac_arial_reg, 11 * SCALE)
            return font_title, font_side_title, font_name, font_desc
    except Exception as e:
        print(f"Error loading system fonts: {e}")
        
    font_title = ImageFont.load_default()
    font_side_title = ImageFont.load_default()
    font_name = ImageFont.load_default()
    font_desc = ImageFont.load_default()
    return font_title, font_side_title, font_name, font_desc

# ---------------------------------------------------------
# VECTOR DRAWING RECIPES
# ---------------------------------------------------------
def draw_cylinder(draw, cx, cy, fill, border):
    """Draws database cylinder stack."""
    w = 40 * SCALE
    h = 22 * SCALE
    ellipse_h = h // 2
    
    offsets = [18 * SCALE, 0, -18 * SCALE]
    for dy in offsets:
        x = cx - w // 2
        y = cy + dy - h // 2
        
        # Bottom ellipse
        draw.ellipse([x, y + h - ellipse_h, x + w, y + h], fill=fill)
        # Rectangle body
        draw.rectangle([x, y + ellipse_h // 2, x + w, y + h - ellipse_h // 2], fill=fill)
        # Top ellipse
        top_fill = tuple(min(255, c + 35) for c in fill[:3]) + (fill[3],) if len(fill) == 4 else tuple(min(255, c + 35) for c in fill)
        draw.ellipse([x, y, x + w, y + ellipse_h], fill=top_fill, outline=border, width=2 * SCALE)
        # Lines
        draw.line([x, y + ellipse_h // 2, x, y + h - ellipse_h // 2], fill=border, width=2 * SCALE)
        draw.line([x + w, y + ellipse_h // 2, x + w, y + h - ellipse_h // 2], fill=border, width=2 * SCALE)
        draw.arc([x, y + h - ellipse_h, x + w, y + h], start=0, end=180, fill=border, width=2 * SCALE)

def draw_isometric_cubes(draw, cx, cy, color):
    """Draws three isometric 3D cubes."""
    size = 10 * SCALE
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
        
        draw.polygon(top_face, fill=top_c, outline=border_color, width=1 * SCALE)
        draw.polygon(left_face, fill=left_c, outline=border_color, width=1 * SCALE)
        draw.polygon(right_face, fill=right_c, outline=border_color, width=1 * SCALE)

    draw_cube(cx, cy - 10 * SCALE)
    draw_cube(cx - 10 * SCALE, cy + 5 * SCALE)
    draw_cube(cx + 10 * SCALE, cy + 5 * SCALE)

def draw_target(draw, cx, cy, color):
    """Concentric rings with solid core."""
    r_outer = 18 * SCALE
    r_mid = 11 * SCALE
    r_inner = 4 * SCALE
    draw.ellipse([cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer], outline=color, width=3 * SCALE)
    draw.ellipse([cx - r_mid, cy - r_mid, cx + r_mid, cy + r_mid], outline=color, width=3 * SCALE)
    draw.ellipse([cx - r_inner, cy - r_inner, cx + r_inner, cy + r_inner], fill=color)

def draw_sync(draw, cx, cy, color):
    """Refresh loop arrows."""
    r = 15 * SCALE
    draw.arc([cx - r, cy - r, cx + r, cy + r], start=210, end=330, fill=color, width=3 * SCALE)
    draw.arc([cx - r, cy - r, cx + r, cy + r], start=30, end=150, fill=color, width=3 * SCALE)
    
    x1 = int(cx + r * math.cos(math.radians(210)))
    y1 = int(cy + r * math.sin(math.radians(210)))
    draw.polygon([(x1, y1), (x1 + 2 * SCALE, y1 - 8 * SCALE), (x1 + 8 * SCALE, y1 - 2 * SCALE)], fill=color)
    
    x2 = int(cx + r * math.cos(math.radians(30)))
    y2 = int(cy + r * math.sin(math.radians(30)))
    draw.polygon([(x2, y2), (x2 - 8 * SCALE, y2 + 2 * SCALE), (x2 - 2 * SCALE, y2 + 8 * SCALE)], fill=color)

def draw_check(draw, cx, cy, color):
    """Green checkmark."""
    r = 15 * SCALE
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=2 * SCALE)
    p1 = (cx - 6 * SCALE, cy - 1 * SCALE)
    p2 = (cx - 1 * SCALE, cy + 4 * SCALE)
    p3 = (cx + 6 * SCALE, cy - 4 * SCALE)
    draw.line([p1, p2, p3], fill=color, width=3 * SCALE, joint="round")

def draw_alert(draw, cx, cy, color):
    """Red exclamation mark."""
    r = 15 * SCALE
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=2 * SCALE)
    draw.line([(cx, cy - 6 * SCALE), (cx, cy + 1 * SCALE)], fill=color, width=3 * SCALE)
    draw.ellipse([cx - 1 * SCALE, cy + 4 * SCALE, cx + 1 * SCALE, cy + 6 * SCALE], fill=color)

# ---------------------------------------------------------
# GENERAL DRAWING HELPERS
# ---------------------------------------------------------
def draw_glow_rect(img, box, radius, color, opacity=0.18):
    glow_img = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(glow_img)
    x0, y0, x1, y1 = box
    glow_box = [x0 - 8, y0 - 8, x1 + 8, y1 + 8]
    draw.rounded_rectangle(glow_box, radius=radius + 8, fill=(color[0], color[1], color[2], int(255 * opacity)))
    glow_img = glow_img.filter(ImageFilter.GaussianBlur(radius=16 * SCALE))
    img.alpha_composite(glow_img)

def draw_arrow(draw, start, end, target_r, color, width=3):
    x1, y1 = start[0] * SCALE, start[1] * SCALE
    x2, y2 = end[0] * SCALE, end[1] * SCALE
    target_r = target_r * SCALE
    
    dx = x2 - x1
    dy = y2 - y1
    dist = math.sqrt(dx*dx + dy*dy)
    if dist == 0:
        return
        
    ux = dx / dist
    uy = dy / dist
    
    ex = x2 - ux * target_r
    ey = y2 - uy * target_r
    
    draw.line([(x1, y1), (ex, ey)], fill=color, width=width)
    
    arrow_len = 10 * SCALE
    arrow_w = 6 * SCALE
    
    ox = -uy
    oy = ux
    
    p1 = (ex, ey)
    p2 = (ex - ux * arrow_len + ox * arrow_w, ey - uy * arrow_len + oy * arrow_w)
    p3 = (ex - ux * arrow_len - ox * arrow_w, ey - uy * arrow_len - oy * arrow_w)
    
    draw.polygon([p1, p2, p3], fill=color)

# ---------------------------------------------------------
# CARD RENDERER
# ---------------------------------------------------------
def render_card(draw, font_name, font_desc, cx, cy, title, subtitle, color_name, icon_type, glow_val):
    w, h = CARD_W * SCALE, CARD_H * SCALE
    cx_s, cy_s = cx * SCALE, cy * SCALE
    x0, y0 = cx_s - w // 2, cy_s - h // 2
    x1, y1 = cx_s + w // 2, cy_s + h // 2
    
    rgb = COLOR_MAP.get(color_name, (0, 240, 255))
    
    # Card background
    draw.rounded_rectangle([x0, y0, x1, y1], radius=8 * SCALE, fill=CARD_BG_COLOR)
    
    # Border
    border_r = int(BORDER_DEFAULT[0] + (rgb[0] - BORDER_DEFAULT[0]) * glow_val)
    border_g = int(BORDER_DEFAULT[1] + (rgb[1] - BORDER_DEFAULT[1]) * glow_val)
    border_b = int(BORDER_DEFAULT[2] + (rgb[2] - BORDER_DEFAULT[2]) * glow_val)
    border_color = (border_r, border_g, border_b, 255)
    
    b_width = 2 * SCALE if glow_val < 0.1 else 3 * SCALE
    draw.rounded_rectangle([x0, y0, x1, y1], radius=8 * SCALE, outline=border_color, width=b_width)
    
    # Icon
    icon_cy = cy_s - 15 * SCALE
    if icon_type == "database":
        draw_cylinder(draw, cx_s, icon_cy, (0, 30, 40, 255), rgb + (255,))
    elif icon_type == "cubes":
        draw_isometric_cubes(draw, cx_s, icon_cy, rgb)
    elif icon_type == "target":
        draw_target(draw, cx_s, icon_cy, rgb)
    elif icon_type == "sync":
        draw_sync(draw, cx_s, icon_cy, rgb)
    elif icon_type == "check":
        draw_check(draw, cx_s, icon_cy, rgb)
    elif icon_type == "alert":
        draw_alert(draw, cx_s, icon_cy, rgb)
        
    # Text
    text_color = (255, 255, 255, 255) if glow_val > 0.2 else (226, 232, 240, 255)
    draw.text((cx_s, cy_s + 30 * SCALE), title, font=font_name, fill=text_color, anchor="mm")
    draw.text((cx_s, cy_s + 48 * SCALE), subtitle, font=font_desc, fill=(148, 163, 184, 255), anchor="mm")

# ---------------------------------------------------------
# PHYSICS TRAIL RENDERING
# ---------------------------------------------------------
def draw_particle(draw, px, py, particle_color, trail_history):
    trail_history.append((px, py))
    if len(trail_history) > 8:
        trail_history.pop(0)
        
    for idx, (tx, ty) in enumerate(trail_history):
        alpha = int(255 * ((idx + 1) / len(trail_history)))
        radius = int(6 * SCALE * ((idx + 1) / len(trail_history)))
        if radius < 1:
            radius = 1
            
        glow_rad = radius + 4 * SCALE
        draw.ellipse([tx - glow_rad, ty - glow_rad, tx + glow_rad, ty + glow_rad], 
                     fill=particle_color + (int(alpha * 0.35),))
        draw.ellipse([tx - radius, ty - radius, tx + radius, ty + radius], 
                     fill=particle_color + (alpha,))

# ---------------------------------------------------------
# MAIN RENDER FUNCTION
# ---------------------------------------------------------
def render_frame(frame, font_title, font_side_title, font_name, font_desc, trail_left, trail_right):
    img = Image.new("RGBA", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # 1. Subtle Background Tech Grid
    grid_spacing = 80 * SCALE
    for gx in range(grid_spacing, WIDTH, grid_spacing):
        draw.line([(gx, 0), (gx, HEIGHT)], fill=GRID_COLOR, width=1)
    for gy in range(grid_spacing, HEIGHT, grid_spacing):
        draw.line([(0, gy), (WIDTH, gy)], fill=GRID_COLOR, width=1)
        
    # 2. Main Center Divider and Headers
    draw.line([(WIDTH // 2, 100 * SCALE), (WIDTH // 2, HEIGHT - 30 * SCALE)], fill=DIVIDER_COLOR, width=2 * SCALE)
    draw.text((WIDTH // 2, 45 * SCALE), "PROMPTING VS LOOPING IN PRODUCTION", font=font_title, fill=(255, 255, 255, 255), anchor="mm")
    
    # Left Headers
    draw.text((300 * SCALE, 125 * SCALE), "PROMPTING (Probabilistic)", font=font_side_title, fill=(255, 255, 255, 255), anchor="mm")
    draw.text((300 * SCALE, 160 * SCALE), "Single Inference Pass (85% Reliability)", font=font_desc, fill=(148, 163, 184, 255), anchor="mm")
    
    # Right Headers
    draw.text((900 * SCALE, 125 * SCALE), "LOOPING (Deterministic)", font=font_side_title, fill=(255, 255, 255, 255), anchor="mm")
    draw.text((900 * SCALE, 160 * SCALE), "Self-Correcting Loop (98%+ Reliability)", font=font_desc, fill=(148, 163, 184, 255), anchor="mm")
    
    # 3. Particle math
    # LEFT PARTICLE (PROMPTING)
    px_l, py_l = 0, 0
    p_color_l = (0, 240, 255)
    is_left_phase_2 = (frame >= 30)
    left_t = (frame % 30) / 29.0
    
    if left_t < 0.5:
        local_t = left_t / 0.5
        px_l = int(120 + (300 - 120) * local_t)
        py_l = 340
        p_color_l = COLOR_MAP["cyan"]
    else:
        local_t = (left_t - 0.5) / 0.5
        px_l = int(300 + (480 - 300) * local_t)
        py_l = 340
        p_color_l = COLOR_MAP["blue"] if local_t < 0.5 else (COLOR_MAP["red"] if is_left_phase_2 else COLOR_MAP["emerald"])

    # RIGHT PARTICLE (LOOPING)
    px_r, py_r = 0, 0
    p_color_r = (0, 240, 255)
    
    # 6 segments on the right side
    if frame < 10:  # Seg 1: Input to Model
        t = frame / 9.0
        px_r = int(720 + (900 - 720) * t)
        py_r = int(340 + (245 - 340) * t)
        p_color_r = COLOR_MAP["cyan"]
    elif frame < 20:  # Seg 2: Model to Validation
        t = (frame - 10) / 9.0
        px_r = int(900 + (1080 - 900) * t)
        py_r = int(245 + (340 - 245) * t)
        p_color_r = COLOR_MAP["blue"]
    elif frame < 30:  # Seg 3: Validation to Feedback
        t = (frame - 20) / 9.0
        px_r = int(1080 + (900 - 1080) * t)
        py_r = int(340 + (435 - 340) * t)
        p_color_r = COLOR_MAP["orange"]
    elif frame < 40:  # Seg 4: Feedback to Model
        t = (frame - 30) / 9.0
        px_r = 900
        py_r = int(435 + (245 - 435) * t)
        p_color_r = COLOR_MAP["indigo"]
    elif frame < 50:  # Seg 5: Model to Validation (re-run)
        t = (frame - 40) / 9.0
        px_r = int(900 + (1080 - 900) * t)
        py_r = int(245 + (340 - 245) * t)
        p_color_r = COLOR_MAP["blue"]
    else:  # Seg 6: Validation to Success Exit
        t = (frame - 50) / 9.0
        px_r = int(1080 + (1160 - 1080) * t)
        py_r = 340
        p_color_r = COLOR_MAP["emerald"]

    # Multiply coordinates by scale for exact canvas usage
    px_l_s, py_l_s = px_l * SCALE, py_l * SCALE
    px_r_s, py_r_s = px_r * SCALE, py_r * SCALE

    # 4. Proximity glows calculation
    # LEFT
    left_centers = [(120, 340), (300, 340), (480, 340)]
    glow_l = []
    for cx, cy in left_centers:
        dist = math.sqrt((px_l - cx)**2 + (py_l - cy)**2)
        glow_l.append(math.exp(-(dist / 110.0)**2))
        
    # RIGHT
    right_centers = [(720, 340), (900, 245), (1080, 340), (900, 435)]
    glow_r = []
    for cx, cy in right_centers:
        dist = math.sqrt((px_r - cx)**2 + (py_r - cy)**2)
        glow_r.append(math.exp(-(dist / 110.0)**2))

    # 5. Draw Glow Layer (behind cards)
    # Left Card Glows
    for idx, (cx, cy) in enumerate(left_centers):
        glow_val = glow_l[idx]
        if glow_val > 0.05:
            # Color map for the cards
            color_name = "cyan" if idx == 0 else ("blue" if idx == 1 else ("red" if is_left_phase_2 else "emerald"))
            rgb = COLOR_MAP[color_name]
            box = [(cx - CARD_R) * SCALE, (cy - CARD_R) * SCALE, (cx + CARD_R) * SCALE, (cy + CARD_R) * SCALE]
            draw_glow_rect(img, box, CARD_R * SCALE, rgb, opacity=glow_val * 0.22)
            
    # Right Card Glows
    for idx, (cx, cy) in enumerate(right_centers):
        glow_val = glow_r[idx]
        if glow_val > 0.05:
            if idx == 0:
                color_name = "cyan"
            elif idx == 1:
                color_name = "blue"
            elif idx == 2:
                # Validation card glows orange in phase 1 (failure) and green in phase 2 (success)
                color_name = "orange" if (frame >= 20 and frame < 40) else "emerald"
            else:
                color_name = "indigo"
            rgb = COLOR_MAP[color_name]
            box = [(cx - CARD_R) * SCALE, (cy - CARD_R) * SCALE, (cx + CARD_R) * SCALE, (cy + CARD_R) * SCALE]
            draw_glow_rect(img, box, CARD_R * SCALE, rgb, opacity=glow_val * 0.22)

    # 6. Static Connection Lines (Dim connectors)
    # Left connectors
    draw_arrow(draw, (120, 340), (300, 340), CARD_R, BORDER_DEFAULT, width=3 * SCALE)
    draw_arrow(draw, (300, 340), (480, 340), CARD_R, BORDER_DEFAULT, width=3 * SCALE)
    
    # Right connectors
    draw_arrow(draw, (720, 340), (900, 245), CARD_R, BORDER_DEFAULT, width=3 * SCALE)
    draw_arrow(draw, (900, 245), (1080, 340), CARD_R, BORDER_DEFAULT, width=3 * SCALE)
    # validation to feedback
    draw_arrow(draw, (1080, 340), (900, 435), CARD_R, BORDER_DEFAULT, width=3 * SCALE)
    # feedback to model
    draw_arrow(draw, (900, 435), (900, 245), CARD_R, BORDER_DEFAULT, width=3 * SCALE)
    # validation to exit
    draw_arrow(draw, (1080, 340), (1170, 340), CARD_R, BORDER_DEFAULT, width=3 * SCALE)

    # 7. Active Connection Highlights
    # Left side active
    if px_l > 120:
        h_end = min(px_l, 300)
        draw_arrow(draw, (120, 340), (h_end, 340), CARD_R, COLOR_MAP["cyan"] + (255,), width=3 * SCALE)
        if px_l > 300:
            h_end2 = min(px_l, 480)
            col = COLOR_MAP["red"] if is_left_phase_2 else COLOR_MAP["emerald"]
            draw_arrow(draw, (300, 340), (h_end2, 340), CARD_R, col + (255,), width=3 * SCALE)

    # Right side active highlights based on frame segments
    if frame >= 0 and frame < 10:
        draw_arrow(draw, (720, 340), (px_r, py_r), CARD_R, COLOR_MAP["cyan"] + (255,), width=3 * SCALE)
    elif frame >= 10:
        draw_arrow(draw, (720, 340), (900, 245), CARD_R, COLOR_MAP["cyan"] + (255,), width=3 * SCALE)
        
        if frame < 20:
            draw_arrow(draw, (900, 245), (px_r, py_r), CARD_R, COLOR_MAP["blue"] + (255,), width=3 * SCALE)
        else:
            draw_arrow(draw, (900, 245), (1080, 340), CARD_R, COLOR_MAP["blue"] + (255,), width=3 * SCALE)
            
            if frame < 30:
                draw_arrow(draw, (1080, 340), (px_r, py_r), CARD_R, COLOR_MAP["orange"] + (255,), width=3 * SCALE)
            else:
                draw_arrow(draw, (1080, 340), (900, 435), CARD_R, COLOR_MAP["orange"] + (255,), width=3 * SCALE)
                
                if frame < 40:
                    draw_arrow(draw, (900, 435), (px_r, py_r), CARD_R, COLOR_MAP["indigo"] + (255,), width=3 * SCALE)
                else:
                    draw_arrow(draw, (900, 435), (900, 245), CARD_R, COLOR_MAP["indigo"] + (255,), width=3 * SCALE)
                    
                    if frame < 50:
                        draw_arrow(draw, (900, 245), (px_r, py_r), CARD_R, COLOR_MAP["blue"] + (255,), width=3 * SCALE)
                    else:
                        draw_arrow(draw, (900, 245), (1080, 340), CARD_R, COLOR_MAP["blue"] + (255,), width=3 * SCALE)
                        draw_arrow(draw, (1080, 340), (px_r, py_r), CARD_R, COLOR_MAP["emerald"] + (255,), width=3 * SCALE)

    # 8. Draw Cards (drawn on top to mask connection lines)
    # Left Cards
    render_card(draw, font_name, font_desc, 120, 340, "Input Prompt", "Task specs", "cyan", "database", glow_l[0])
    render_card(draw, font_name, font_desc, 300, 340, "Model Inference", "One-shot guess", "blue", "cubes", glow_l[1])
    
    if is_left_phase_2:
        render_card(draw, font_name, font_desc, 480, 340, "JSON Error!", "Malformed structure", "red", "alert", glow_l[2])
    else:
        render_card(draw, font_name, font_desc, 480, 340, "Output Success", "Parsed JSON", "emerald", "check", glow_l[2])

    # Right Cards
    render_card(draw, font_name, font_desc, 720, 340, "Input Prompt", "Task specs", "cyan", "database", glow_r[0])
    render_card(draw, font_name, font_desc, 900, 245, "Model Inference", "Processes input", "blue", "cubes", glow_r[1])
    
    # Validation state toggles
    if frame >= 20 and frame < 40:
        render_card(draw, font_name, font_desc, 1080, 340, "Checking...", "Failed validation", "orange", "alert", glow_r[2])
    elif frame >= 50:
        render_card(draw, font_name, font_desc, 1080, 340, "Valid!", "Verified success", "emerald", "check", glow_r[2])
    else:
        render_card(draw, font_name, font_desc, 1080, 340, "Validation", "Rules & schema", "emerald", "target", glow_r[2])
        
    render_card(draw, font_name, font_desc, 900, 435, "Feedback", "Add error trace", "indigo", "sync", glow_r[3])

    # 9. Draw Particle Trail
    draw_particle(draw, px_l_s, py_l_s, p_color_l, trail_left)
    draw_particle(draw, px_r_s, py_r_s, p_color_r, trail_right)

    return img.convert("RGB")

# ---------------------------------------------------------
# MAIN ENGINE
# ---------------------------------------------------------
def main():
    print("Initializing Custom Comparison GIF Generator...")
    font_title, font_side_title, font_name, font_desc = get_fonts()
    
    frames = []
    trail_left = []
    trail_right = []
    total_frames = 60
    
    print(f"Rendering {total_frames} frames of size {WIDTH}x{HEIGHT}...")
    for f in range(total_frames):
        pct = int(100 * f / total_frames)
        print(f"Rendering frame {f:02d}/{total_frames} [{pct}%]", end="\r")
        frame_img = render_frame(f, font_title, font_side_title, font_name, font_desc, trail_left, trail_right)
        frames.append(frame_img)
        
    print("\nCompiling GIF with adaptive palette...")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "compiled_flow", "compiled_flow.gif")
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
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
