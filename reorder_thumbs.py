#!/usr/bin/env python3
import os
from pathlib import Path

# ────────────────────────────────────────────────────────
# CONFIGURATION: update this if your thumbs folder is elsewhere
THUMBS_DIR = Path("images/thumbs")
# ────────────────────────────────────────────────────────

# 1) Gather all .webp files, sorted by their numeric stem
files = sorted(THUMBS_DIR.glob("*.webp"), key=lambda p: int(p.stem))

# 2) First pass: rename to a temp name (to avoid clobbering)
tmp_paths = []
for idx, path in enumerate(files, start=1):
    # new temporary name: e.g. "__00001__.webp"
    tmp = path.with_name(f"__{idx:05}.webp")
    path.rename(tmp)
    tmp_paths.append(tmp)

# 3) Second pass: strip the temp prefix to final name "00001.webp"
for tmp in tmp_paths:
    final = tmp.with_name(tmp.name.strip("_"))  # "__00001__.webp" → "00001.webp"
    tmp.rename(final)

print(f"✅ Renamed {len(files)} thumbnails sequentially in {THUMBS_DIR}")
