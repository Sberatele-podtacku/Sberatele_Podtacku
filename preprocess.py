#!/usr/bin/env python3
from PIL import Image
import os

# ─── CONFIG ───────────────────────────────────────────────────────────────
SRC_FOLDER = r"C:\Users\ASUS GAMING\Documents\GitHub\Sberatele_Podtacku\recenter_nobg"
OUT_FOLDER = r"C:\Users\ASUS GAMING\Documents\GitHub\Sberatele_Podtacku\recenter_review"
CANVAS_SIZE = 2000   # final square side in px
# ─────────────────────────────────────────────────────────────────────────────

os.makedirs(OUT_FOLDER, exist_ok=True)

for fname in os.listdir(SRC_FOLDER):
    if not fname.lower().endswith('.png'):
        continue

    path_in  = os.path.join(SRC_FOLDER, fname)
    path_out = os.path.join(OUT_FOLDER, fname)

    # 1) Load RGBA
    img = Image.open(path_in).convert("RGBA")
    pix = img.split()[-1]  # alpha channel

    # 2) Compute bounding box of *non*-transparent pixels
    bbox = pix.getbbox()
    if not bbox:
        # totally blank? just center the whole thing
        cropped = img
    else:
        cropped = img.crop(bbox)

    # 3) Create a white square canvas
    canvas = Image.new("RGBA", (CANVAS_SIZE, CANVAS_SIZE), (255,255,255,255))

    # 4) Compute center offset
    x = (CANVAS_SIZE - cropped.width) // 2
    y = (CANVAS_SIZE - cropped.height) // 2

    # 5) Paste cropped coaster into center of canvas
    canvas.paste(cropped, (x,y), cropped)

    # 6) Save out as PNG
    canvas.convert("RGB").save(path_out, "PNG", optimize=True)
    print(f"✓ {fname}")

print("✅ Done! All thumbnails are now centered on a uniform 200×200 white canvas.")
