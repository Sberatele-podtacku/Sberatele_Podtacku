import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image
import multiprocessing

# ─── CONFIG ───────────────────────────────────────────────────────────────
BASE_DIR = r"C:\Users\ASUS GAMING\Documents\GitHub\Sberatele_Podtacku"
SOURCE_DIR = os.path.join(BASE_DIR, "images")          # Folder with .png
OUTPUT_DIR = os.path.join(BASE_DIR, "images_webp_threaded")  # Output folder
QUALITY = 85
# ──────────────────────────────────────────────────────────────────────────

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Gather all PNGs that haven’t been converted yet
files_to_convert = [
    f for f in os.listdir(SOURCE_DIR)
    if f.lower().endswith(".png") and not os.path.exists(
        os.path.join(OUTPUT_DIR, os.path.splitext(f)[0] + ".webp")
    )
]

print(f"🔍 Found {len(files_to_convert)} PNGs to convert...")

# Convert one file
def convert_to_webp(filename):
    input_path = os.path.join(SOURCE_DIR, filename)
    output_path = os.path.join(OUTPUT_DIR, os.path.splitext(filename)[0] + ".webp")
    try:
        img = Image.open(input_path).convert("RGBA")
        img.save(output_path, "WEBP", quality=QUALITY, method=6)
        return (filename, True, None)
    except Exception as e:
        return (filename, False, str(e))

# Multi-threaded execution
max_threads = multiprocessing.cpu_count()
results = []
failed = []

with ThreadPoolExecutor(max_workers=max_threads) as executor:
    future_map = {executor.submit(convert_to_webp, f): f for f in files_to_convert}
    for future in as_completed(future_map):
        fname, success, error = future.result()
        if success:
            print(f"✓ {fname}")
            results.append(fname)
        else:
            print(f"❌ {fname} — {error}")
            failed.append((fname, error))

# Save failures
if failed:
    log_path = os.path.join(BASE_DIR, "webp_conversion_failed_log.txt")
    with open(log_path, "w", encoding="utf-8") as f:
        for fname, error in failed:
            f.write(f"{fname}: {error}\n")
    print(f"⚠️ Logged {len(failed)} failures to: {log_path}")

print(f"✅ Converted {len(results)} files with {len(failed)} failures.")
