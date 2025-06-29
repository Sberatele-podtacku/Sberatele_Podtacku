from pathlib import Path
from PIL import Image

# Configuration
SRC_DIR = Path("images")              # folder containing your full-res PNGs named 00001_front.png, etc.
DST_DIR = SRC_DIR / "thumbs"           # new folder to store webp thumbnails
DST_DIR.mkdir(parents=True, exist_ok=True)
MAX_WIDTH = 300                         # desired thumbnail width in pixels

# Gather unique coaster IDs (prefix before underscore)
ids = sorted({p.stem.split('_')[0] for p in SRC_DIR.glob("*_front.png")}, key=lambda x: int(x))

# Loop over each ID, processing front then back
for coaster_id in ids:
    for side in ("front", "back"):
        src_path = SRC_DIR / f"{coaster_id}_{side}.png"
        if not src_path.exists():
            print(f"⚠️ Skipping missing: {src_path.name}")
            continue
        try:
            with Image.open(src_path) as im:
                # maintain aspect ratio
                w, h = im.size
                new_w = min(MAX_WIDTH, w)
                new_h = int(new_w / w * h)
                thumb = im.resize((new_w, new_h), Image.LANCZOS)
                # save as WebP, preserving side in name
                dst_path = DST_DIR / f"{coaster_id}_{side}.webp"
                thumb.save(dst_path, "WEBP", quality=80, method=6)
                print(f"✅ {src_path.name} → {dst_path.name}")
        except Exception as e:
            print(f"❌ Error processing {src_path.name}: {e}")

print("🎉 Thumbnails generated successfully.")
