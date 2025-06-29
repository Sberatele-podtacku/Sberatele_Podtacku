import os
import re
import pandas as pd

# ─── CONFIG ───────────────────────────────────────────────────────────────
BASE_DIR       = r"C:\Users\ASUS GAMING\Documents\GitHub\Sberatele_Podtacku"
IMAGES_DIR     = os.path.join(BASE_DIR, "images")
METADATA_CSV   = os.path.join(BASE_DIR, "metadata_updated.csv")
# ──────────────────────────────────────────────────────────────────────────

# Match files like 00001_back.png / 00001_front.png
pattern = re.compile(r"(\d{5})_(back|front)\.png$", re.IGNORECASE)

# Get all unique image IDs from filenames in images/
image_ids = set()
for fname in os.listdir(IMAGES_DIR):
    match = pattern.match(fname)
    if match:
        image_ids.add(match.group(1))

# Read metadata CSV and normalize column names
try:
    df_existing = pd.read_csv(METADATA_CSV)
    df_existing.columns = df_existing.columns.str.strip().str.lower()
    existing_ids = set(df_existing["id"].astype(str))
except FileNotFoundError:
    df_existing = pd.DataFrame(columns=["id"])
    existing_ids = set()

# Identify new IDs
new_ids = sorted(image_ids - existing_ids)

# Append if needed
if new_ids:
    new_rows = pd.DataFrame({"id": new_ids})
    df_final = pd.concat([df_existing, new_rows], ignore_index=True)
    df_final.to_csv(METADATA_CSV, index=False)
    print(f"✅ Added {len(new_ids)} new IDs to metadata_updated.csv")
else:
    print("ℹ️ No new IDs found — CSV already up to date.")
