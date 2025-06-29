import os
from PIL import Image

# ─── CONFIG ───────────────────────────────────────────────────────────────
FOLDER = r"C:\Users\ASUS GAMING\Documents\GitHub\Sberatele_Podtacku\rotate"
ANGLE = -90  # Clockwise rotation
# ──────────────────────────────────────────────────────────────────────────

files = [f for f in os.listdir(FOLDER) if f.lower().endswith(".webp")]

print(f"🔄 Found {len(files)} WEBP files to rotate...")

for fname in files:
    path = os.path.join(FOLDER, fname)
    try:
        img = Image.open(path).convert("RGBA")
        rotated = img.rotate(ANGLE, expand=True)
        rotated.save(path, "WEBP", quality=85)
        print(f"✅ Rotated: {fname}")
    except Exception as e:
        print(f"❌ Failed to rotate {fname}: {e}")

print("🎉 All done!")
