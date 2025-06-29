import os
import re
import numpy as np
from PIL import Image

# ─── CONFIG ───────────────────────────────────────────────────────────────
BASE_DIR        = r"C:\Users\ASUS GAMING\Documents\GitHub\Sberatele_Podtacku"
IMAGES_DIR      = os.path.join(BASE_DIR, "images")
THUMBS_DIR      = os.path.join(IMAGES_DIR, "thumbs")
CANVAS_SIZE     = (2000, 2000)
THUMB_SIZE      = (300, 300)
ALPHA_THRESHOLD = 5
MAX_ID          = 733  # Only reprocess 00001 to 00733
# ──────────────────────────────────────────────────────────────────────────

pattern = re.compile(r"(\d{5})_(front|back)\.png$", re.IGNORECASE)

files_to_fix = [
    f for f in os.listdir(IMAGES_DIR)
    if pattern.match(f)
    and f.lower().endswith(".png")
    and int(pattern.match(f).group(1)) <= MAX_ID
]

print(f"🔍 Found {len(files_to_fix)} image(s) to reprocess (IDs up to {MAX_ID})")

for fname in files_to_fix:
    img_path = os.path.join(IMAGES_DIR, fname)
    thumb_name = fname.replace(".png", ".webp")
    thumb_path = os.path.join(THUMBS_DIR, thumb_name)

    # Load + crop using alpha threshold
    img = Image.open(img_path).convert("RGBA")
    alpha = img.getchannel("A")
    mask = np.array(alpha) > ALPHA_THRESHOLD

    if not mask.any():
        cropped = img
    else:
        ys, xs = mask.nonzero()
        bbox = (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)
        cropped = img.crop(bbox)

    # Resize proportionally to fit canvas
    scale = min(CANVAS_SIZE[0] / cropped.width, CANVAS_SIZE[1] / cropped.height)
    new_size = (int(cropped.width * scale), int(cropped.height * scale))
    resized = cropped.resize(new_size, Image.LANCZOS)

    # Create canvas and paste
    canvas = Image.new("RGBA", CANVAS_SIZE, (0, 0, 0, 0))
    x = (CANVAS_SIZE[0] - resized.width) // 2
    y = (CANVAS_SIZE[1] - resized.height) // 2
    canvas.paste(resized, (x, y), resized)

    # Overwrite the PNG image
    canvas.save(img_path, "PNG", optimize=True)
    print(f"✅ Rescaled: {fname}")

    # Create new thumbnail
    thumb = canvas.copy()
    thumb.thumbnail(THUMB_SIZE, Image.LANCZOS)
    thumb.save(thumb_path, "WEBP", quality=85)
    print(f"↪️  Thumb updated: {thumb_name}")

print("🎉 Done! All selected images and thumbnails have been re-centered and scaled.")
