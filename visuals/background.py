"""
visuals/background.py
Generates ONE large, thematically-related background illustration for the
whole app: a soft dusk-to-dawn sky with gentle clouds, calming waves along
the bottom, faint brain-wave / neural lines drifting across the middle, and
a scattering of soft stars - all tying back to the "calm mind" theme of a
mental-health screening tool. Pure Pillow, no internet required, generated
once and cached to disk.
"""

import os
import math
import random
from PIL import Image, ImageDraw, ImageFilter

from backend.config import ASSETS_DIR

IMG_BACKGROUND = os.path.join(ASSETS_DIR, "app_background.png")

BG_W, BG_H = 1920, 1080


def _hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _gradient_bg(size, stops):
    """stops: list of (position 0-1, (r,g,b)) sorted by position."""
    img = Image.new("RGB", size)
    draw = ImageDraw.Draw(img)
    h = size[1]
    for y in range(h):
        t = y / h
        # find surrounding stops
        for i in range(len(stops) - 1):
            p0, c0 = stops[i]
            p1, c1 = stops[i + 1]
            if p0 <= t <= p1:
                local_t = (t - p0) / (p1 - p0) if p1 > p0 else 0
                r = int(c0[0] + (c1[0] - c0[0]) * local_t)
                g = int(c0[1] + (c1[1] - c0[1]) * local_t)
                b = int(c0[2] + (c1[2] - c0[2]) * local_t)
                draw.line([(0, y), (size[0], y)], fill=(r, g, b))
                break
    return img


def _draw_soft_cloud(base, cx, cy, scale, opacity):
    """Draws one fluffy cloud made of overlapping blurred ellipses onto an RGBA layer."""
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    parts = [(-1.2, 0.1, 0.55), (-0.5, -0.35, 0.75), (0.3, -0.25, 0.85),
             (1.0, 0.05, 0.6), (0.1, 0.15, 0.9)]
    for dx, dy, rr in parts:
        r = rr * scale
        x = cx + dx * scale
        y = cy + dy * scale
        draw.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, opacity))
    layer = layer.filter(ImageFilter.GaussianBlur(18))
    return Image.alpha_composite(base, layer)


def _draw_waves(base, color, y_base, amplitude, wavelength, opacity):
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    w, h = base.size
    points = []
    for x in range(0, w + 20, 12):
        y = y_base + amplitude * math.sin(x / wavelength)
        points.append((x, y))
    points += [(w, h), (0, h)]
    draw.polygon(points, fill=color + (opacity,))
    return Image.alpha_composite(base, layer)


def _draw_brainwave_lines(base, color, opacity, seed=0):
    """Faint neural / calm brain-wave style lines drifting across the middle band."""
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    w, h = base.size
    rnd = random.Random(seed)
    for i in range(5):
        y0 = h * 0.32 + i * 34
        pts = []
        phase = rnd.uniform(0, math.pi)
        for x in range(0, w + 20, 8):
            y = y0 + 14 * math.sin((x / 140) + phase) + 4 * math.sin(x / 37 + i)
            pts.append((x, y))
        draw.line(pts, fill=color + (opacity,), width=2, joint="curve")
    layer = layer.filter(ImageFilter.GaussianBlur(0.6))
    return Image.alpha_composite(base, layer)


def _draw_stars(base, count, seed=1):
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    w, h = base.size
    rnd = random.Random(seed)
    for _ in range(count):
        x = rnd.uniform(0, w)
        y = rnd.uniform(0, h * 0.45)
        r = rnd.uniform(1, 2.4)
        alpha = rnd.randint(90, 200)
        draw.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, alpha))
    return Image.alpha_composite(base, layer)


def make_app_background():
    """Build the full themed background: dusk sky -> soft clouds -> brainwave
    lines -> calm rolling waves at the base. Saved once to assets/."""
    # Soft dusk/dawn gradient: deep indigo -> lavender -> peach -> mint (matches app palette)
    stops = [
        (0.00, (63, 81, 181)),    # indigo (top)
        (0.30, (121, 134, 203)),  # soft violet
        (0.55, (206, 190, 230)),  # lavender
        (0.75, (255, 224, 209)),  # peach
        (1.00, (224, 247, 240)),  # mint (bottom)
    ]
    img = _gradient_bg((BG_W, BG_H), stops).convert("RGBA")

    # stars in the upper (darker) portion
    img = _draw_stars(img, count=140, seed=7)

    # soft clouds drifting across upper-middle
    cloud_specs = [
        (BG_W * 0.15, BG_H * 0.18, 140, 60),
        (BG_W * 0.55, BG_H * 0.10, 170, 55),
        (BG_W * 0.85, BG_H * 0.22, 130, 50),
        (BG_W * 0.35, BG_H * 0.30, 110, 45),
    ]
    for cx, cy, scale, op in cloud_specs:
        img = _draw_soft_cloud(img, cx, cy, scale, op)

    # faint calming brain-wave lines across the middle band (ties to "mind" theme)
    img = _draw_brainwave_lines(img, (255, 255, 255), 70, seed=3)

    # gentle rolling waves near the bottom (layered, teal tones - calm/stress-relief theme)
    img = _draw_waves(img, _hex_to_rgb("#26A69A"), BG_H * 0.86, 22, 220, 55)
    img = _draw_waves(img, _hex_to_rgb("#4DB6AC"), BG_H * 0.90, 18, 260, 70)
    img = _draw_waves(img, _hex_to_rgb("#80CBC4"), BG_H * 0.95, 14, 300, 90)

    img.convert("RGB").save(IMG_BACKGROUND, quality=92)


def ensure_background():
    os.makedirs(ASSETS_DIR, exist_ok=True)
    if not os.path.exists(IMG_BACKGROUND):
        make_app_background()
    return IMG_BACKGROUND
