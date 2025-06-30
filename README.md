# 🍺 Beer Coaster Collection & Gallery

A streamlined image workflow and static web gallery to showcase my personal collection of beer coasters. Built for efficiency, consistency, and style — all powered by Python and GitHub Pages. All thanks to ChatGPT

---

## 📸 First Phase: Capture & Organize

1. Photographed the **first 730 coasters** (front and back).
2. Processed them using a series of Python scripts:
   - **Resized and centered** on uniform white backgrounds.
   - **Removed backgrounds** using `rembg`.
   - **Renamed** all files sequentially as `00001_front`, `00001_back`, etc.
   - **Detected duplicates** with SSIM comparison (`check_duplicates.py`).
   - **Created thumbnails** for fast web loading.
   - **Generated CSV metadata**, later enriched manually and exported to JSON.

---

## 🌐 GitHub Pages Gallery

Once the `/images/`, `/thumbs/`, and `metadata.json` are in place, publishing is easy:

1. Add the following to the root of your repo:
   - `/images/` — Final WEBP front/back coasters
   - `/images/thumbs/` — Thumbnail previews
   - `/logos/` — Branding
   - `index.html` — Static gallery interface
   - `metadata.json` — Manually curated info
   - `sw.js` — Service worker
   - `README.md` — This file

2. Preview locally with:
   ```bash
   python -m http.server
   # or:
   npx http-server
   ```

3. Push to GitHub and enjoy automatic publication via GitHub Pages.

---

## 🧪 Second Phase: Final 130 Coasters

After validating the initial workflow and gallery structure:

1. Photographed and **processed the final 130 coasters**, ensuring none were duplicated.
2. **Consolidated** all processing steps into a single script: `new_coasters.py`.
3. **Converted all PNGs to WEBP** to reduce file size and improve performance.
4. Automatically:
   - Removed BG
   - Resized + centered
   - Converted to `.webp`
   - Renamed as the next sequential ID
   - Generated thumbnails
   - Updated metadata CSV


---

## 📁 Directory Structure

```text
/ (root)
├── images/                # final .webp images (front/back)
│   └── thumbs/            # smaller webp thumbs
├── logos/                 # header logos
├── metadata.json          # enriched data per coaster
├── index.html             # gallery HTML (static)
├── sw.js                  # caching for offline usage
├── new_coasters.py        # main all-in-one processing pipeline
├── [archived_scripts]/    # older scripts: remove_bg, resize, rename, check_duplicates
└── README.md              # this file
```

---

## 🔁 Adding New Coasters

For any future updates:

1. Drop new JPGs into the `new_coaster/` folder.
2. Run:
   ```bash
   python new_coasters.py
   ```
3. Script will:
   - Clean images
   - Rename + generate thumbs
   - Update `metadata_updated.csv`
4. Update manually metadata file to add description and country.
5. Convert it to JSON.
6. Update the web gallery by committing & pushing to GitHub.

---

Built with ❤️ using Python, `rembg`, `Pillow`, `pandas`, `scikit-image`, and hosted on GitHub Pages.  
Special thanks to **ChatGPT** for code generation and optimization guidance!
