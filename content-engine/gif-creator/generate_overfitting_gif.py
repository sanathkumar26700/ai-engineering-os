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
GRID_COLOR = (18, 25, 41, 255)      # Tech grid
DIVIDER_COLOR = (24, 35, 59, 255)   # Grid borders
AXIS_COLOR = (47, 55, 75, 255)      # Plot axis color

COLOR_MAP = {
    "cyan": (0, 240, 255),
    "blue": (59, 130, 246),
    "emerald": (16, 185, 129),
    "indigo": (99, 102, 241),
    "purple": (168, 85, 247),
    "orange": (249, 115, 22),
    "red": (239, 68, 68),
    "pink": (236, 72, 153),
    "white": (255, 255, 255)
}

# ---------------------------------------------------------
# DATA POINTS CONFIG (Local coordinates, Y inverted for screen space)
# ---------------------------------------------------------
# Symmetrical curves: noisy inverted U-shape parabola
train_pts = [
    (-110, 60),
    (-70, 10),
    (-30, -15),
    (10, -30),
    (50, -5),
    (90, 40),
    (120, 80)
]

test_pts = [
    (-90, 28),
    (-10, -22),
    (30, -15),
    (70, 10),
    (110, 65)
]

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
            font_subtitle = ImageFont.truetype(mac_helvetica, 16 * SCALE, index=0)
            font_panel_label = ImageFont.truetype(mac_helvetica, 20 * SCALE, index=1)
            font_panel_sub = ImageFont.truetype(mac_helvetica, 12 * SCALE, index=0)
            return font_title, font_subtitle, font_panel_label, font_panel_sub
        elif os.path.exists(mac_arial_reg) and os.path.exists(mac_arial_bold):
            font_title = ImageFont.truetype(mac_arial_bold, 36 * SCALE)
            font_subtitle = ImageFont.truetype(mac_arial_reg, 16 * SCALE)
            font_panel_label = ImageFont.truetype(mac_arial_bold, 20 * SCALE)
            font_panel_sub = ImageFont.truetype(mac_arial_reg, 12 * SCALE)
            return font_title, font_subtitle, font_panel_label, font_panel_sub
    except Exception as e:
        print(f"Error loading system fonts: {e}")
        
    font_title = ImageFont.load_default()
    font_subtitle = ImageFont.load_default()
    font_panel_label = ImageFont.load_default()
    font_panel_sub = ImageFont.load_default()
    return font_title, font_subtitle, font_panel_label, font_panel_sub

# ---------------------------------------------------------
# MATH FUNCTIONS & RBF SOLVER
# ---------------------------------------------------------
def get_y_underfit(lx):
    """Linear fit."""
    return 0.08 * lx + 35

def get_y_justright(lx):
    """Quadratic parabola fit."""
    return 0.0055 * lx**2 + 0.05 * lx - 25

def solve_rbf(points, y_base_func, sigma=25):
    """Solves for radial basis function coefficients to match training points exactly."""
    n = len(points)
    A = [[0.0]*n for _ in range(n)]
    b = [0.0]*n
    for i in range(n):
        x_i, y_i = points[i]
        b[i] = y_i - y_base_func(x_i)
        for j in range(n):
            x_j, _ = points[j]
            A[i][j] = math.exp(-((x_i - x_j) / sigma)**2)
            
    # Gaussian elimination with pivoting
    c = list(b)
    for i in range(n):
        pivot = A[i][i]
        for j in range(i+1, n):
            factor = A[j][i] / pivot
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            c[j] -= factor * c[i]
            
    for i in range(n-1, -1, -1):
        for j in range(i+1, n):
            c[i] -= A[i][j] * c[j]
        c[i] /= A[i][i]
        
    return c

# Solve RBF once
c_rbf = solve_rbf(train_pts, get_y_justright, sigma=25)

def get_wiggle(lx):
    """Sum of Gaussian RBFs representing overfitting noise memorization."""
    val = 0.0
    for i in range(len(train_pts)):
        x_i, _ = train_pts[i]
        val += c_rbf[i] * math.exp(-((lx - x_i) / 25.0)**2)
    return val

def get_model_y(panel_idx, lx, t):
    """Calculates curve y value for a given panel, local x, and training time t [0, 1]."""
    # Flat start
    y_start = 50.0
    
    if panel_idx == 0:  # Underfitting
        y_target = get_y_underfit(lx)
        return (1.0 - t) * y_start + t * y_target
    elif panel_idx == 1:  # Just Right
        y_target = get_y_justright(lx)
        return (1.0 - t) * y_start + t * y_target
    else:  # Overfitting
        # Fit general trend first, then start memorizing noise
        t_base = min(1.0, t * 1.4)
        t_wiggle = max(0.0, (t - 0.45) / 0.55)
        
        y_base = (1.0 - t_base) * y_start + t_base * get_y_justright(lx)
        return y_base + t_wiggle * get_wiggle(lx)

# ---------------------------------------------------------
# DRAWING HELPERS
# ---------------------------------------------------------
def draw_dashed_line(draw, start, end, fill, width=2, dash_length=6, gap_length=6):
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

def draw_glow_rect(img, box, radius, color, opacity=0.18):
    glow_img = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(glow_img)
    x0, y0, x1, y1 = box
    glow_box = [x0 - 8, y0 - 8, x1 + 8, y1 + 8]
    draw.rounded_rectangle(glow_box, radius=radius + 8, fill=(color[0], color[1], color[2], int(255 * opacity)))
    glow_img = glow_img.filter(ImageFilter.GaussianBlur(radius=12 * SCALE))
    img.alpha_composite(glow_img)

# ---------------------------------------------------------
# FRAME RENDERING ENGINE
# ---------------------------------------------------------
def render_frame(frame, font_title, font_subtitle, font_panel_label, font_panel_sub):
    img = Image.new("RGBA", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # 1. Subtle Background Tech Grid
    grid_spacing = 80 * SCALE
    for gx in range(grid_spacing, WIDTH, grid_spacing):
        draw.line([(gx, 0), (gx, HEIGHT)], fill=GRID_COLOR, width=1)
    for gy in range(grid_spacing, HEIGHT, grid_spacing):
        draw.line([(0, gy), (WIDTH, gy)], fill=GRID_COLOR, width=1)
        
    # 2. Main Headers
    draw.text((WIDTH // 2, 45 * SCALE), "THE DANGER OF 100% ACCURACY", font=font_title, fill=(255, 255, 255, 255), anchor="mm")
    draw.text((WIDTH // 2, 85 * SCALE), "Real patterns have noise. Perfect training scores mean memorization.", font=font_subtitle, fill=(148, 163, 184, 255), anchor="mm")
    
    # Define phase variables
    # Phase 1: Training (frames 0-29) -> t from 0.0 to 1.0. Test data invisible.
    # Phase 2: Testing (frames 30-59) -> t remains at 1.0. Test data fades in.
    if frame < 30:
        t_train = frame / 29.0
        test_fade = 0.0
        phase_label = "TRAINING MODEL..."
        phase_color = COLOR_MAP["blue"]
    else:
        t_train = 1.0
        test_fade = min(1.0, (frame - 30) / 6.0)
        phase_label = "TESTING UNSEEN DATA"
        phase_color = COLOR_MAP["pink"] if frame < 54 else COLOR_MAP["emerald"]

    # Render Phase HUD indicator
    draw.rounded_rectangle([WIDTH // 2 - 120 * SCALE, 115 * SCALE, WIDTH // 2 + 120 * SCALE, 145 * SCALE], radius=6 * SCALE, fill=(17, 24, 39, 255), outline=phase_color + (180,), width=1 * SCALE)
    draw.text((WIDTH // 2, 130 * SCALE), phase_label, font=font_panel_sub, fill=phase_color, anchor="mm")

    # Panel dimensions
    panel_cy = 350
    panel_w = 320
    panel_h = 320
    panel_centers = [220, 600, 980]
    
    # 3. Draw Panels
    for idx, cx in enumerate(panel_centers):
        cx_s, cy_s = cx * SCALE, panel_cy * SCALE
        pw_s, ph_s = panel_w * SCALE, panel_h * SCALE
        x0, y0 = cx_s - pw_s // 2, cy_s - ph_s // 2
        x1, y1 = cx_s + pw_s // 2, cy_s + ph_s // 2
        
        # Decide border color based on model validation outcome
        if idx == 0:
            border_col = COLOR_MAP["orange"] if test_fade > 0.1 else BORDER_DEFAULT
            card_title = "Underfitting"
            card_sub = "Too Simple (High Loss everywhere)"
            title_col = COLOR_MAP["orange"]
        elif idx == 1:
            border_col = COLOR_MAP["emerald"] if test_fade > 0.1 else BORDER_DEFAULT
            card_title = "Just Right"
            card_sub = "Learns General Pattern"
            title_col = COLOR_MAP["emerald"]
        else:
            border_col = COLOR_MAP["red"] if test_fade > 0.1 else BORDER_DEFAULT
            card_title = "Overfitting"
            card_sub = "Memorizes Noise (Fails Test)"
            title_col = COLOR_MAP["red"] if test_fade > 0.1 else COLOR_MAP["blue"]

        # Glow layer behind active cards in Phase 2
        if test_fade > 0.05:
            draw_glow_rect(img, [x0, y0, x1, y1], 12 * SCALE, border_col, opacity=test_fade * 0.15)
            
        # Draw card container
        draw.rounded_rectangle([x0, y0, x1, y1], radius=12 * SCALE, fill=CARD_BG_COLOR)
        draw.rounded_rectangle([x0, y0, x1, y1], radius=12 * SCALE, outline=border_col, width=2 * SCALE)
        
        # Inner plot boundaries
        plot_w = 260
        plot_h = 200
        px0, py0 = cx_s - (plot_w // 2) * SCALE, cy_s - (plot_h // 2) * SCALE + 20 * SCALE
        px1, py1 = cx_s + (plot_w // 2) * SCALE, cy_s + (plot_h // 2) * SCALE + 20 * SCALE
        
        # Draw internal axes
        draw.line([(px0, py1), (px1, py1)], fill=AXIS_COLOR, width=2 * SCALE)  # X axis
        draw.line([(px0, py0), (px0, py1)], fill=AXIS_COLOR, width=2 * SCALE)  # Y axis
        
        # Draw dynamic curve segments
        curve_pts = []
        dx = 4
        for lx in range(-125, 126, dx):
            ly = get_model_y(idx, lx, t_train)
            
            # Map local coordinates to plot space
            screen_x = cx_s + lx * SCALE
            screen_y = py1 - (120 - ly) * SCALE # 120 is offset so U-shape parabola looks correct
            curve_pts.append((screen_x, screen_y))
            
        # Draw curve line
        curve_color = COLOR_MAP["red"] if idx == 0 else (COLOR_MAP["emerald"] if idx == 1 else COLOR_MAP["blue"])
        if idx == 2 and test_fade > 0.1:
            # Overfit curve turns red to represent invalidity
            curve_color = COLOR_MAP["red"]
            
        draw.line(curve_pts, fill=curve_color + (255,), width=3 * SCALE)

        # Draw Static training scatter dots
        for rx, ry in train_pts:
            dot_x = cx_s + rx * SCALE
            dot_y = py1 - (120 - ry) * SCALE
            
            # Draw blue dots
            draw.ellipse([dot_x - 5 * SCALE, dot_y - 5 * SCALE, dot_x + 5 * SCALE, dot_y + 5 * SCALE], fill=COLOR_MAP["blue"] + (255,))
            draw.ellipse([dot_x - 9 * SCALE, dot_y - 9 * SCALE, dot_x + 9 * SCALE, dot_y + 9 * SCALE], outline=COLOR_MAP["blue"] + (60,), width=2 * SCALE)

        # Draw Dynamic test scatter dots + error indicator lines
        if test_fade > 0.01:
            test_opacity = int(255 * test_fade)
            err_opacity = int(140 * test_fade)
            
            # Error color
            err_color = COLOR_MAP["red"] if idx == 2 else (COLOR_MAP["orange"] if idx == 0 else COLOR_MAP["emerald"])
            
            for tx, ty in test_pts:
                dot_x = cx_s + tx * SCALE
                dot_y = py1 - (120 - ty) * SCALE
                
                # Get curve value at tx
                cy_val = get_model_y(idx, tx, t_train)
                curve_screen_y = py1 - (120 - cy_val) * SCALE
                
                # Draw vertical error projection line
                draw_dashed_line(draw, (dot_x, curve_screen_y), (dot_x, dot_y), fill=err_color + (err_opacity,), width=2 * SCALE, dash_length=4 * SCALE, gap_length=4 * SCALE)
                
                # Draw test dot (Orange/Pink)
                test_col = COLOR_MAP["pink"] if idx == 2 else COLOR_MAP["orange"]
                draw.ellipse([dot_x - 5 * SCALE, dot_y - 5 * SCALE, dot_x + 5 * SCALE, dot_y + 5 * SCALE], fill=test_col + (test_opacity,))
                draw.ellipse([dot_x - 9 * SCALE, dot_y - 9 * SCALE, dot_x + 9 * SCALE, dot_y + 9 * SCALE], outline=test_col + (int(test_opacity * 0.25),), width=2 * SCALE)
                
            # Draw brief performance text
            if idx == 0:
                perf_txt = "Test Loss: High"
                perf_col = COLOR_MAP["orange"]
            elif idx == 1:
                perf_txt = "Test Loss: Low"
                perf_col = COLOR_MAP["emerald"]
            else:
                perf_txt = "Test Loss: Extreme!"
                perf_col = COLOR_MAP["red"]
            draw.text((cx_s, py0 + 20 * SCALE), perf_txt, font=font_panel_sub, fill=perf_col + (test_opacity,), anchor="mm")

        # Typography Card Info
        draw.text((cx_s, cy_s - 120 * SCALE), card_title, font=font_panel_label, fill=title_col, anchor="mm")
        draw.text((cx_s, cy_s - 95 * SCALE), card_sub, font=font_panel_sub, fill=(148, 163, 184, 255), anchor="mm")
        
    return img.convert("RGB")

# ---------------------------------------------------------
# MAIN FUNCTION
# ---------------------------------------------------------
def main():
    print("Initializing Overfitting Comparison GIF Generator...")
    font_title, font_subtitle, font_panel_label, font_panel_sub = get_fonts()
    
    frames = []
    total_frames = 60
    
    print(f"Rendering {total_frames} frames of size {WIDTH}x{HEIGHT}...")
    for f in range(total_frames):
        pct = int(100 * f / total_frames)
        print(f"Rendering frame {f:02d}/{total_frames} [{pct}%]", end="\r")
        frame_img = render_frame(f, font_title, font_subtitle, font_panel_label, font_panel_sub)
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
