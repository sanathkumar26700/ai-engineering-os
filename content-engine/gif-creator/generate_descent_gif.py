import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ---------------------------------------------------------
# CONSTANTS & STYLING CONFIG (SCALED FOR HD 2400x1350)
# ---------------------------------------------------------
SCALE = 2
WIDTH, HEIGHT = 1200 * SCALE, 675 * SCALE

BG_COLOR = (8, 12, 20, 255)         # Deep dark blue/gray
AXIS_COLOR = (47, 55, 75, 255)      # Sleek gray-blue for axis lines
GRID_COLOR = (18, 25, 41, 255)      # Extremely subtle grid color
PROJ_LINE_COLOR = (255, 255, 255, 50) # Translucent projection line

VALLEY_COLOR_CYAN = (0, 240, 255)     # Glowing Cyan at valley bottom
VALLEY_COLOR_PINK = (236, 72, 153)    # Glowing Pink at valley top edges
HIST_DOT_COLOR = (59, 130, 246)       # Deep blue history dot
BALL_COLOR = (0, 240, 255)            # Cyan active ball

# Parabola parameters
x_0 = 600 * SCALE
y_bottom = 530 * SCALE
a = 0.0018 / SCALE

def get_y(x):
    """Calculates screen y coordinate for a given screen x coordinate on the parabola."""
    return y_bottom - a * (x - x_0)**2

# Gradient descent step positions (base values scaled)
step_x_base = [160, 280, 400, 510, 585, 650, 600]
step_x = [val * SCALE for val in step_x_base]

# Frame mappings for steps (total 60 frames)
step_frames = [0, 8, 16, 24, 32, 40, 48, 60]

# ---------------------------------------------------------
# FONT HANDLING
# ---------------------------------------------------------
def get_fonts():
    mac_helvetica = "/System/Library/Fonts/Helvetica.ttc"
    mac_arial_reg = "/System/Library/Fonts/Supplemental/Arial.ttf"
    mac_arial_bold = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
    
    try:
        if os.path.exists(mac_helvetica):
            font_title = ImageFont.truetype(mac_helvetica, 34 * SCALE, index=1)
            font_label = ImageFont.truetype(mac_helvetica, 18 * SCALE, index=1)
            font_sub = ImageFont.truetype(mac_helvetica, 14 * SCALE, index=0)
            return font_title, font_label, font_sub
        elif os.path.exists(mac_arial_reg) and os.path.exists(mac_arial_bold):
            font_title = ImageFont.truetype(mac_arial_bold, 34 * SCALE)
            font_label = ImageFont.truetype(mac_arial_bold, 18 * SCALE)
            font_sub = ImageFont.truetype(mac_arial_reg, 14 * SCALE)
            return font_title, font_label, font_sub
    except Exception as e:
        print(f"Error loading system fonts: {e}")
        
    font_title = ImageFont.load_default()
    font_label = ImageFont.load_default()
    font_sub = ImageFont.load_default()
    return font_title, font_label, font_sub

# ---------------------------------------------------------
# INTERPOLATION HELPERS
# ---------------------------------------------------------
def get_ball_pos(frame):
    """Calculates smoothstep-interpolated position of the ball at a given frame."""
    interval = 0
    for i in range(len(step_frames) - 1):
        if frame >= step_frames[i] and frame < step_frames[i+1]:
            interval = i
            break
            
    f_start = step_frames[interval]
    f_end = step_frames[interval+1]
    
    if interval >= len(step_x) - 1:
        x = step_x[-1]
        return x, get_y(x)
        
    x_start = step_x[interval]
    x_end = step_x[interval+1]
    
    t = (frame - f_start) / (f_end - f_start)
    t_smooth = t * t * (3 - 2 * t)
    
    x = x_start + (x_end - x_start) * t_smooth
    return int(x), int(get_y(x))

def draw_dashed_line(draw, start, end, fill, width=2, dash_length=12, gap_length=12):
    """Draws a beautiful dashed line in Pillow."""
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1
    distance = math.sqrt(dx*dx + dy*dy)
    if distance == 0:
        return
        
    ux = dx / distance
    uy = dy / distance
    
    steps = int(distance / (dash_length + gap_length))
    for i in range(steps + 1):
        s_dist = i * (dash_length + gap_length)
        e_dist = min(s_dist + dash_length, distance)
        if s_dist > distance:
            break
        sx = int(x1 + ux * s_dist)
        sy = int(y1 + uy * s_dist)
        ex = int(x1 + ux * e_dist)
        ey = int(y1 + uy * e_dist)
        draw.line([(sx, sy), (ex, ey)], fill=fill, width=width)

# ---------------------------------------------------------
# FRAME RENDERING
# ---------------------------------------------------------
def render_frame(frame, font_title, font_label, font_sub):
    # Main image
    img = Image.new("RGBA", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # Get current ball position
    px, py = get_ball_pos(frame)
    
    # 1. Draw Subtle Tech Grid Lines
    grid_spacing = 80 * SCALE
    for gx in range(grid_spacing, WIDTH, grid_spacing):
        draw.line([(gx, 0), (gx, HEIGHT)], fill=GRID_COLOR, width=1)
    for gy in range(grid_spacing, HEIGHT, grid_spacing):
        draw.line([(0, gy), (WIDTH, gy)], fill=GRID_COLOR, width=1)
        
    # 2. Draw Soft Background Radial Glow (bottom center of valley)
    glow_bg = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_bg)
    glow_draw.ellipse([x_0 - 350*SCALE, y_bottom - 250*SCALE, x_0 + 350*SCALE, y_bottom + 450*SCALE], fill=VALLEY_COLOR_CYAN + (12,))
    glow_bg = glow_bg.filter(ImageFilter.GaussianBlur(radius=100))
    img.alpha_composite(glow_bg)
    
    # 3. Draw Title & Subtitle (Aesthetic typography)
    draw.text((WIDTH // 2, 55 * SCALE), "Gradient Descent", font=font_title, fill=(255, 255, 255, 255), anchor="mm")
    draw.text((WIDTH // 2, 95 * SCALE), "Walking downhill toward the minimum loss", font=font_sub, fill=(148, 163, 184, 255), anchor="mm")
    
    # 4. Axes Configurations
    axis_x_start = 140 * SCALE
    axis_x_end = 1060 * SCALE
    axis_y_top = 160 * SCALE
    axis_y_bottom = 580 * SCALE
    
    # 5. Draw Dynamic Dashed Projection Lines (behind curve and ball)
    # Vertical projection (to Weight Axis)
    draw_dashed_line(draw, (px, py), (px, axis_y_bottom), fill=PROJ_LINE_COLOR, width=2)
    # Horizontal projection (to Loss Axis)
    draw_dashed_line(draw, (px, py), (axis_x_start, py), fill=PROJ_LINE_COLOR, width=2)
    
    # 6. Draw Parabolic Valley with custom color gradient
    dx = 4
    # Draw segments of the curve with thickness and soft outer glow
    for cx_val in range(150 * SCALE, 1050 * SCALE, dx):
        x1, y1 = cx_val, get_y(cx_val)
        x2, y2 = cx_val + dx, get_y(cx_val + dx)
        
        # Color shifting based on loss height (normalized distance from valley bottom)
        dist_norm = abs(cx_val - x_0) / (450 * SCALE)
        dist_norm = min(1.0, dist_norm)
        
        # Interpolate between Valley Bottom (Cyan) and top edges (Pink)
        r = int(VALLEY_COLOR_CYAN[0] + (VALLEY_COLOR_PINK[0] - VALLEY_COLOR_CYAN[0]) * dist_norm)
        g = int(VALLEY_COLOR_CYAN[1] + (VALLEY_COLOR_PINK[1] - VALLEY_COLOR_CYAN[1]) * dist_norm)
        b = int(VALLEY_COLOR_CYAN[2] + (VALLEY_COLOR_PINK[2] - VALLEY_COLOR_CYAN[2]) * dist_norm)
        color = (r, g, b)
        
        # Multi-pass line layers to build neon glow
        draw.line([(x1, y1), (x2, y2)], fill=color + (30,), width=16)
        draw.line([(x1, y1), (x2, y2)], fill=color + (80,), width=8)
        draw.line([(x1, y1), (x2, y2)], fill=color + (255,), width=4)
        
    # 7. Draw History Dots and Connecting Optimizing Vectors
    for i in range(len(step_x) - 1):
        if frame >= step_frames[i+1]:
            hx = step_x[i]
            hy = get_y(hx)
            next_x = step_x[i+1]
            next_y = get_y(next_x)
            
            # Solid step vector line
            draw.line([(hx, hy), (next_x, next_y)], fill=HIST_DOT_COLOR + (160,), width=4)
            
            # Glowing history landing dot
            draw.ellipse([hx - 12, hy - 12, hx + 12, hy + 12], fill=HIST_DOT_COLOR + (40,))
            draw.ellipse([hx - 6, hy - 6, hx + 6, hy + 6], fill=HIST_DOT_COLOR + (255,))
            
    # 8. Draw Axes (Sleek gray-blue, sits on top of helper grid lines)
    # Y-Axis (vertical)
    draw.line([(axis_x_start, axis_y_top), (axis_x_start, axis_y_bottom)], fill=AXIS_COLOR, width=4)
    draw.polygon([(axis_x_start, axis_y_top), (axis_x_start - 8, axis_y_top + 16), (axis_x_start + 8, axis_y_top + 16)], fill=AXIS_COLOR)
    
    # X-Axis (horizontal)
    draw.line([(axis_x_start, axis_y_bottom), (axis_x_end, axis_y_bottom)], fill=AXIS_COLOR, width=4)
    draw.polygon([(axis_x_end, axis_y_bottom), (axis_x_end - 16, axis_y_bottom - 8), (axis_x_end - 16, axis_y_bottom + 8)], fill=AXIS_COLOR)
    
    # Axis Labels (Shifted left and bottom to prevent overlap with the ball path)
    draw.text((axis_x_start - 15 * SCALE, axis_y_top + 10 * SCALE), "Loss (Error)", font=font_label, fill=(226, 232, 240, 255), anchor="rm")
    draw.text((axis_x_end - 20 * SCALE, axis_y_bottom - 20 * SCALE), "Weight (W)", font=font_label, fill=(226, 232, 240, 255), anchor="rm")
    
    # 9. Draw Active Ball (3D glossy sphere overlay)
    r = 24 * SCALE
    # Glowing shadow behind ball
    draw.ellipse([px - r - 12, py - r - 12, px + r + 12, py + r + 12], fill=BALL_COLOR + (45,))
    # Main active ball body
    draw.ellipse([px - r, py - r, px + r, py + r], fill=BALL_COLOR + (255,))
    # Glass highlight shine
    hl_r = r // 4
    draw.ellipse([px - r//3 - hl_r, py - r//3 - hl_r, px - r//3 + hl_r, py - r//3 + hl_r], fill=(255, 255, 255, 220))
    
    return img.convert("RGB")

# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------
def main():
    print("Initializing Premium Gradient Descent GIF Generator...")
    font_title, font_label, font_sub = get_fonts()
    
    frames = []
    total_frames = 60
    
    print(f"Rendering {total_frames} frames of size {WIDTH}x{HEIGHT}...")
    for f in range(total_frames):
        pct = int(100 * f / total_frames)
        print(f"Rendering frame {f:02d}/{total_frames} [{pct}%]", end="\r")
        frame_img = render_frame(f, font_title, font_label, font_sub)
        frames.append(frame_img)
        
    print("\nCompiling GIF with adaptive palette...")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "compiled_flow", "descent_visual.gif")
    
    # Ensure folder exists
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
