import os
from PIL import Image

# ─── CONFIG ───────────────────────────────────────────────────────────────
BASE_DIR     = r"C:\Users\ASUS GAMING\Documents\GitHub\Sberatele_Podtacku"
SOURCE_DIR   = os.path.join(BASE_DIR, "images")
OUTPUT_DIR   = os.path.join(BASE_DIR, "images_webp")
QUALITY      = 85  # WebP lossy quality (0–100)
# ──────────────────────────────────────────────────────────────────────────

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Process all PNG files
files = [f for f in os.listdir(SOURCE_DIR) if f.lower().endswith(".png")]

print(f"🔄 Converting {len(files)} PNGs to WEBP (Q{QUALITY})...")

for fname in files:
    input_path = os.path.join(SOURCE_DIR, fname)
    output_path = os.path.join(OUTPUT_DIR, os.path.splitext(fname)[0] + ".webp")

    try:
        img = Image.open(input_path).convert("RGBA")
        img.save(output_path, "WEBP", quality=QUALITY, method=6)
        print(f"✓ {fname} → {os.path.basename(output_path)}")
    except Exception as e:
        print(f"❌ Failed to convert {fname}: {e}")

print("🎉 Done! All images converted to WEBP.")
