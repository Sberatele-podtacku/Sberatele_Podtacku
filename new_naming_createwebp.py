import os
import re
from PIL import Image

# ─── CONFIG ───────────────────────────────────────────────────────────────
BASE_DIR      = r"C:\Users\ASUS GAMING\Documents\GitHub\Sberatele_Podtacku"
IMAGES_DIR    = os.path.join(BASE_DIR, "images")
RECENTER_DIR  = os.path.join(BASE_DIR, "recenter_png")
THUMBS_DIR    = os.path.join(IMAGES_DIR, "thumbs")
THUMB_SIZE    = (300, 300)
# ──────────────────────────────────────────────────────────────────────────

os.makedirs(THUMBS_DIR, exist_ok=True)

# 1. Extract numbers from filenames like 00733_front.jpg
pattern = re.compile(r"(\d+)_([a-z]+)\.(jpg|png|webp)$", re.IGNORECASE)
existing_numbers = []

for f in os.listdir(IMAGES_DIR):
    match = pattern.match(f)
    if match:
        num = int(match.group(1))
        existing_numbers.append(num)

# 2. Get next available number
next_num = max(existing_numbers, default=0) + 1

# 3. Sort files (by filename) to ensure predictable front/back pairing
recenter_files = sorted([f for f in os.listdir(RECENTER_DIR) if f.lower().endswith(".png")])

if len(recenter_files) % 2 != 0:
    raise ValueError("❌ Number of files in recenter_png is not even. Expected front/back pairs.")

# 4. Process in pairs (front first, then back)
for i in range(0, len(recenter_files), 2):
    front_file = recenter_files[i]
    back_file = recenter_files[i + 1]

    for suffix, src_file in zip(["front", "back"], [front_file, back_file]):
        new_base = f"{next_num:05d}_{suffix}"

        # Paths
        src_path = os.path.join(RECENTER_DIR, src_file)
        final_path = os.path.join(IMAGES_DIR, new_base + ".png")
        thumb_path = os.path.join(THUMBS_DIR, new_base + ".webp")

        # Move and rename image into images/
        os.rename(src_path, final_path)
        print(f"✓ Moved: {src_file} → {final_path}")

        # Create thumbnail
        with Image.open(final_path) as img:
            thumb = img.copy()
            thumb.thumbnail(THUMB_SIZE, Image.LANCZOS)
            thumb.save(thumb_path, "WEBP", quality=85)
            print(f"✓ Thumb: {thumb_path}")

    next_num += 1  # One number per front/back pair

print("✅ All images renamed and thumbnails created.")
