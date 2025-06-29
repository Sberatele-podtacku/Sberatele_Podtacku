#!/usr/bin/env python3
"""
manage_new_coasters.py

Pipeline:
 1) Preprocess (crop & center)
 2) Remove background
 3) Rename front/back pairs sequentially in New_Coaster
 4) Optionally check for duplicates against images/ using 256×256 thumbnails + SSIM/ORB
 5) Pause for manual moves
 6) Generate WebP thumbnails for truly new ones
 7) Append to metadata_updated.csv
 8) Clean up New_Coaster
"""
import os, io, sys, csv
from pathlib import Path
from PIL import Image
from rembg import remove
import numpy as np
import cv2
from skimage.metrics import structural_similarity as ssim

# === CONFIG ===
REPO_ROOT      = Path(r"C:\Users\ASUS GAMING\Documents\GitHub\Sberatele_Podtacku")
NEW_DIR        = REPO_ROOT / "New_Coaster"
IMAGES_DIR     = REPO_ROOT / "images"
THUMBS_DIR     = IMAGES_DIR / "thumbs"
METADATA_CSV   = REPO_ROOT / "metadata_updated.csv"
CANVAS_SIZE    = (2000, 2000)
PAD_WIDTH      = 5
SSIM_THRESH    = 0.90
ORB_THRESH     = 30
THUMB_WIDTH    = 300
WHITE_CUTOFF   = 0.95  # threshold for cropping whitespace

# ── Helpers ───────────────────────────────────────────
def preprocess_image(img: Image.Image, canvas_size: tuple) -> Image.Image:
    """Crop to non-transparent bbox and center on white canvas."""
    img = img.convert("RGBA")
    alpha = img.split()[-1]
    bbox = alpha.getbbox()
    cropped = img.crop(bbox) if bbox else img
    canvas = Image.new("RGBA", canvas_size, (255,255,255,255))
    x = (canvas_size[0] - cropped.width) // 2
    y = (canvas_size[1] - cropped.height) // 2
    canvas.paste(cropped, (x, y), cropped)
    return canvas

def load_thumb(p: Path):
    """Load a grayscale crop of non-white, resized to 256×256 float array."""
    img = Image.open(p).convert("L")
    arr = np.array(img, np.float32) / 255.0
    mask = arr < WHITE_CUTOFF
    if mask.any():
        ys, xs = np.where(mask)
        arr = arr[ys.min():ys.max()+1, xs.min():xs.max()+1]
    th = Image.fromarray((arr*255).astype("uint8")).resize((256,256), Image.LANCZOS)
    return np.array(th, np.float32) / 255.0

def orb_score(a, b) -> int:
    i1, i2 = (a*255).astype("uint8"), (b*255).astype("uint8")
    orb = cv2.ORB_create(nfeatures=500)
    _, d1 = orb.detectAndCompute(i1, None)
    _, d2 = orb.detectAndCompute(i2, None)
    if d1 is None or d2 is None:
        return 0
    matches = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True).match(d1, d2)
    return sum(1 for m in matches if m.distance < 50)

# ── Main ─────────────────────────────────────────────
if __name__ == "__main__":
    # 1) RAW INPUT
    raws = sorted(NEW_DIR.glob("*.*"))
    if not raws:
        print(f"[!] No files in {NEW_DIR}.")
        sys.exit(0)

    # 2) PREPROCESS & REMOVE BACKGROUND
    print(f"🔄 Preprocessing and removing background for {len(raws)} raw images…")
    for f in raws:
        img = Image.open(f)
        prep = preprocess_image(img, CANVAS_SIZE)
        buf = io.BytesIO()
        prep.save(buf, "PNG", optimize=True)
        no_bg = remove(buf.getvalue())
        out = NEW_DIR / f.with_suffix(".png").name
        Image.open(io.BytesIO(no_bg)).convert("RGBA").save(out)
        print(f" ✓ {f.name} → {out.name}")

    # 3) RENAME SEQUENTIAL FRONT/BACK
    existing = sorted({p.stem.split("_")[0]
        for p in IMAGES_DIR.glob("*_front.png")}, key=int)
    last = int(existing[-1]) if existing else 0

    pngs = sorted(NEW_DIR.glob("*.png"))
    if len(pngs) % 2:
        print("[!] Found odd number of PNGs.")
        sys.exit(1)

    new_ids = []
    print("🔢 Renaming new pairs…")
    for i in range(0, len(pngs), 2):
        idx = last + (i//2) + 1
        tag = f"{idx:0{PAD_WIDTH}d}"
        f_dst = NEW_DIR / f"{tag}_front.png"
        b_dst = NEW_DIR / f"{tag}_back.png"
        pngs[i].rename(f_dst)
        pngs[i+1].rename(b_dst)
        new_ids.append(tag)
        print(f" ✓ Assigned {tag}")

    # 4) PRELOAD EXISTING THUMBNAILS
    main_ids    = sorted(existing, key=int)
    main_thumbs = {}
    for mid in main_ids:
        try:
            main_thumbs[mid] = (
                load_thumb(IMAGES_DIR/f"{mid}_front.png"),
                load_thumb(IMAGES_DIR/f"{mid}_back.png")
            )
        except FileNotFoundError:
            pass

    # 5) OPTIONAL DUPLICATE CHECK
    choice = input("\n🔍 Perform duplicate check against existing images? [Y/n]: ")
    unique, dupes = [], []
    if choice.lower().startswith('n'):
        unique = new_ids.copy()
        print("⚡ Skipping duplicate check. All new IDs marked as unique.")
    else:
        print(f"\n🔍 Checking {len(new_ids)} new coasters for duplicates…")
        for nid in new_ids:
            nf = load_thumb(NEW_DIR/f"{nid}_front.png")
            nb = load_thumb(NEW_DIR/f"{nid}_back.png")
            found = []
            for mid, (mf, mb) in main_thumbs.items():
                sf = ssim(nf, mf, data_range=1.0)
                sb = ssim(nb, mb, data_range=1.0)
                av = (sf + sb) / 2
                of = orb_score(nf, mf)
                ob = orb_score(nb, mb)
                if av >= SSIM_THRESH or (of >= ORB_THRESH and ob >= ORB_THRESH):
                    found.append((mid, av, of, ob))
            if not found:
                unique.append(nid)
                print(f" ✅ {nid} is unique.")
            else:
                dupes.append(nid)
                print(f" ⚠️ {nid} possible duplicates:")
                for mid,av,of,ob in sorted(found, key=lambda x: x[1], reverse=True):
                    print(f"    • main {mid}: avg={av:.3f}, orb={of}/{ob}")

    # 6) PAUSE FOR MOVING UNIQUES
    print("\n👉 Move the UNIQUE front/back pairs into:")
    print("      ", IMAGES_DIR)
    print("   IDs:", unique)
    input("   Press Enter when done…")

    # 7) GENERATE WEBP THUMBNAILS
    THUMBS_DIR.mkdir(exist_ok=True, parents=True)
    thumbs_done = []
    print("\n🖼️ Generating WebP thumbnails…")
    for nid in unique:
        src = IMAGES_DIR/f"{nid}_front.png"
        if not src.exists():
            print(f"  (!) {src.name} missing, skipping")
            continue
        img = Image.open(src)
        h = int((THUMB_WIDTH / img.width) * img.height)
        thumb = img.resize((THUMB_WIDTH, h), Image.LANCZOS)
        tgt = THUMBS_DIR/f"{nid}.webp"
        thumb.save(tgt, "WEBP", quality=80)
        thumbs_done.append(nid)
        print(f" ✓ {tgt.name}")

    # 8) APPEND METADATA
    if thumbs_done:
        print("\n📝 Appending to metadata_updated.csv…")
        with open(METADATA_CSV, "a", newline="", encoding="utf-8") as csvf:
            w = csv.writer(csvf)
            for nid in thumbs_done:
                w.writerow([nid, "??", "??", "??"] )
                print(f"   • Added row for {nid}")
    else:
        print("\nℹ️ No new thumbnails → skipping CSV update.")

    # 9) CLEANUP
    print("\n🧹 Cleaning up New_Coaster…")
    for f in NEW_DIR.iterdir():
        try: f.unlink()
        except: pass

    print("\n✅ All done!")
