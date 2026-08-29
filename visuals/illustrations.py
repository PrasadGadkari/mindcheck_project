"""
visuals/illustrations.py
Generates simple, flat-style themed illustrations for each page of the
app (header banner, depression / anxiety / stress icons, calm / methodology
banners) using Pillow. Images are drawn programmatically (no external
downloads needed) and cached to disk under /assets so they are only
generated once.
"""

import os
import math
from PIL import Image, ImageDraw, ImageFilter

from backend.config import (
    ASSETS_DIR, IMG_HEADER, IMG_DEPRESSION, IMG_ANXIETY,
    IMG_STRESS, IMG_CALM, IMG_METHODOLOGY, CATEGORY_COLOR,
)

W, H = 800, 400


def _gradient_bg(size, top_color, bottom_color):
    img = Image.new("RGB", size, top_color)
    draw = ImageDraw.Draw(img)
    r1, g1, b1 = top_color
    r2, g2, b2 = bottom_color
    for y in range(size[1]):
        ratio = y / size[1]
        r = int(r1 + (r2 - r1) * ratio)
        g = int(g1 + (g2 - g1) * ratio)
        b = int(b1 + (b2 - b1) * ratio)
        draw.line([(0, y), (size[0], y)], fill=(r, g, b))
    return img


def _hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def make_header_brain():
    """Calm banner with an abstract brain / mind silhouette for the top of the app."""
    img = _gradient_bg((W, H), (63, 81, 181), (149, 117, 205))
    draw = ImageDraw.Draw(img)
    cx, cy, r = W // 2, H // 2, 120
    # soft glow circle
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    gdraw.ellipse([cx - r - 30, cy - r - 30, cx + r + 30, cy + r + 30],
                  fill=(255, 255, 255, 60))
    glow = glow.filter(ImageFilter.GaussianBlur(25))
    img = Image.alpha_composite(img.convert("RGBA"), glow)
    draw = ImageDraw.Draw(img)
    # stylised "mind" swirl using overlapping arcs
    for i in range(6):
        rr = r - i * 15
        bbox = [cx - rr, cy - rr, cx + rr, cy + rr]
        draw.arc(bbox, start=40 * i, end=40 * i + 260, fill=(255, 255, 255, 200), width=4)
    # small dots representing neural connections
    for angle in range(0, 360, 30):
        x = cx + (r + 40) * math.cos(math.radians(angle))
        y = cy + (r + 40) * math.sin(math.radians(angle))
        draw.ellipse([x - 5, y - 5, x + 5, y + 5], fill=(255, 255, 255, 220))
    img.convert("RGB").save(IMG_HEADER)


def make_wave_illustration(path, color_hex, wave_count=3, seed_offset=0):
    """Generic calming 'wave' illustration used as a base for category icons."""
    top = _hex_to_rgb(color_hex)
    bottom = (255, 255, 255)
    img = _gradient_bg((W, H), top, bottom)
    draw = ImageDraw.Draw(img)
    for w in range(wave_count):
        amplitude = 25 + w * 10
        y_offset = H // 2 + w * 40 - seed_offset
        points = []
        for x in range(0, W + 10, 10):
            y = y_offset + amplitude * math.sin((x / 60) + w)
            points.append((x, y))
        points += [(W, H), (0, H)]
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        odraw = ImageDraw.Draw(overlay)
        alpha = 90 - w * 20 if 90 - w * 20 > 20 else 20
        odraw.polygon(points, fill=top + (alpha,))
        img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    img.save(path)


def make_depression_illustration():
    """Soft rain-cloud motif (low energy / low mood theme)."""
    color = CATEGORY_COLOR["Depression"]
    img = _gradient_bg((W, H), (92, 107, 192), (220, 224, 245))
    draw = ImageDraw.Draw(img)
    cx, cy = W // 2, H // 2 - 30
    # cloud made of overlapping ellipses
    cloud_parts = [(-90, 0, 70), (-30, -30, 90), (40, -20, 80), (100, 10, 60)]
    for dx, dy, rr in cloud_parts:
        draw.ellipse([cx + dx - rr, cy + dy - rr, cx + dx + rr, cy + dy + rr],
                     fill=(255, 255, 255))
    # gentle rain lines
    for i in range(10):
        x = cx - 150 + i * 35
        y1 = cy + 60
        y2 = y1 + 40
        draw.line([(x, y1), (x - 10, y2)], fill=_hex_to_rgb(color), width=4)
    img.save(IMG_DEPRESSION)


def make_anxiety_illustration():
    """Spiral / tangled-thoughts motif (racing thoughts theme)."""
    color = CATEGORY_COLOR["Anxiety"]
    img = _gradient_bg((W, H), (255, 138, 101), (255, 224, 209))
    draw = ImageDraw.Draw(img)
    cx, cy = W // 2, H // 2
    points = []
    for t in range(0, 900):
        angle = t * 0.09
        radius = 0.18 * t
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        points.append((x, y))
    draw.line(points, fill=_hex_to_rgb(color), width=4, joint="curve")
    img.save(IMG_ANXIETY)


def make_stress_illustration():
    """Jagged pressure-line motif (tension / overload theme)."""
    color = CATEGORY_COLOR["Stress"]
    img = _gradient_bg((W, H), (38, 166, 154), (204, 236, 233))
    draw = ImageDraw.Draw(img)
    cy = H // 2
    points = [(0, cy)]
    x = 0
    up = True
    while x < W:
        step = 40
        x += step
        y = cy - 70 if up else cy + 70
        points.append((x, y))
        up = not up
    points.append((W, cy))
    draw.line(points, fill=_hex_to_rgb(color), width=6, joint="curve")
    img.save(IMG_STRESS)


def make_calm_illustration():
    """Calming sunrise / balance motif for the results & self-care section."""
    img = _gradient_bg((W, H), (255, 213, 128), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    cx, cy, r = W // 2, H - 40, 90
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 183, 77))
    for i in range(12):
        angle = math.radians(i * 30)
        x1 = cx + (r + 15) * math.cos(angle)
        y1 = cy + (r + 15) * math.sin(angle)
        x2 = cx + (r + 45) * math.cos(angle)
        y2 = cy + (r + 45) * math.sin(angle)
        draw.line([(x1, y1), (x2, y2)], fill=(255, 213, 128), width=6)
    img.save(IMG_CALM)


def make_methodology_illustration():
    """Simple bar/graph motif for the methodology page."""
    img = _gradient_bg((W, H), (96, 125, 139), (236, 239, 241))
    draw = ImageDraw.Draw(img)
    base_y = H - 60
    bars = [90, 160, 120, 200, 140]
    x = 100
    for i, bh in enumerate(bars):
        draw.rectangle([x, base_y - bh, x + 70, base_y], fill=(255, 255, 255))
        x += 110
    draw.line([(60, base_y), (W - 60, base_y)], fill=(255, 255, 255), width=3)
    img.save(IMG_METHODOLOGY)


def ensure_illustrations():
    """Generate all illustrations once, if they don't already exist on disk."""
    os.makedirs(ASSETS_DIR, exist_ok=True)
    generators = {
        IMG_HEADER: make_header_brain,
        IMG_DEPRESSION: make_depression_illustration,
        IMG_ANXIETY: make_anxiety_illustration,
        IMG_STRESS: make_stress_illustration,
        IMG_CALM: make_calm_illustration,
        IMG_METHODOLOGY: make_methodology_illustration,
    }
    for path, fn in generators.items():
        if not os.path.exists(path):
            fn()
