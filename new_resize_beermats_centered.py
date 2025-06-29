#!/usr/bin/env python3
from PIL import Image
import os
import numpy as np


# ─── CONFIG ───────────────────────────────────────────────────────────────
SRC_FOLDER = r"C:\Users\ASUS GAMING\Documents\GitHub\Sberatele_Podtacku\recenter_nobg"
OUT_FOLDER = r"C:\Users\ASUS GAMING\Documents\GitHub\Sberatele_Podtacku\recenter_png"
CANVAS_SIZE = (2000, 2000)  # Width, Height
ALPHA_THRESHOLD = 5         # Minimum alpha to consider as content
# ──────────────────────────────────────────────────────────────────────────

os.makedirs(OUT_FOLDER, exist_ok=True)

for fname in os.listdir(SRC_FOLDER):
    if not fname.lower().endswith(".png"):
        continue

    path_in = os.path.join(SRC_FOLDER, fname)
    path_out = os.path.join(OUT_FOLDER, fname)

    # Load image with alpha
    img = Image.open(path_in).convert("RGBA")
    alpha = img.getchannel("A")
    alpha_np = np.array(alpha)
    mask = alpha_np > ALPHA_THRESHOLD

    if not mask.any():
        cropped = img
    else:
        ys, xs = mask.nonzero()
        bbox = (xs.min(), ys.min(), xs.max()+1, ys.max()+1)
        cropped = img.crop(bbox)

    # Resize proportionally to fit within canvas
    max_w, max_h = CANVAS_SIZE
    scale = min(max_w / cropped.width, max_h / cropped.height)
    new_size = (int(cropped.width * scale), int(cropped.height * scale))
    resized = cropped.resize(new_size, Image.LANCZOS)

    # Create transparent canvas and center the image
    canvas = Image.new("RGBA", CANVAS_SIZE, (0, 0, 0, 0))
    x = (CANVAS_SIZE[0] - resized.width) // 2
    y = (CANVAS_SIZE[1] - resized.height) // 2
    canvas.paste(resized, (x, y), resized)

    canvas.save(path_out, "PNG", optimize=True)
    print(f"✓ {fname} resized + centered")

print("✅ All images are now scaled, centered, and on a transparent 2000×2000 canvas.")
