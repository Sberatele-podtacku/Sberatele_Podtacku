# 🍻 Beer Coaster Collection & Gallery

A workflow and static web gallery for managing, deduplicating, and showcasing my beer coaster scans.

---

## 🛠 Pre-GitHub Preprocessing (Desktop)

Before publishing to GitHub Pages, use the Python helper scripts to:

1. **Take pictures of all current collection
2. **Resize & center** raw scans to a uniform size.
3. **Remove backgrounds** (using `remove_bg.py`).
4. **Rename** files sequentially (e.g. `00001_front.png`, `00001_back.png`).
5. **Detect & flag duplicates** (SSIM-based) so you only keep unique coasters.
6. **Generate WebP thumbnails** for faster loading: `images/thumbs/*.webp`.

All of the above is automated by:

```bash
git clone .../beer-mats-scripts
cd beer-mats-scripts
python process_and_merge_and_check.py
```

This single script pipelines raw → cleaned → deduped → renamed → thumbnailed → updated metadata.

---

## 🌐 GitHub Pages Gallery

Once you have your cleaned `images/`, `images/thumbs/`, and updated `metadata.json`, deploy your gallery:

1. Copy/commit the following into your **GitHub repo** root:

   * `/images/` (coaster PNGs)
   * `/images/thumbs/` (WebP thumbnails)
   * `/logos/` (site logos)
   * `index.html` (gallery page)
   * `sw.js` (service-worker)
   * `metadata.json`
   * **README.md** (this file)

2. Preview locally:

   ```bash
   python -m http.server
   # or: npx http-server
   ```

   Browse to [http://localhost:8000](http://localhost:8000)

3. Push to GitHub:

   ```bash
   git add .
   git commit -m "Add gallery & metadata"
   git push
   ```

GitHub Pages will automatically build and publish from your `main` branch.

---

## 🔧 Repo Structure

```text
/ (root)
├── images/                # original PNGs (front/back)
│   └── thumbs/            # lightweight WebP thumbnails
├── logos/                 # gallery header logos
├── metadata.json          # [{ id, description, country }, ...]
├── index.html             # static gallery + lightbox + filters
├── sw.js                  # service-worker for caching
├── remove_bg.py           # remove background from raw scans
├── sequential_rename.py   # rename images sequentially
├── check_duplicates.py    # SSIM-based duplicate finder
├── generate_thumbs.py     # WebP thumbnail generator
├── process_and_merge_and_check.py # all-in-one pipeline
└── README.md              # this file
```

---

## 🚀 Continuous Updates

Whenever you get new coasters:

1. Add raw scans to `NEW_COASTERS/`
2. Run the pipeline script:

   ```bash
   python manage_new.py
   ```
3. Review flagged duplicates in the CLI/Streamlit app.
4. Move any genuinely new coasters into `images/`, let the script append metadata.
5. Commit & push: `git add . && git commit -m "Import new coasters" && git push`.

Your gallery will stay up‑to‑date automatically.

---

Built with ❤️ using Python, **rembg**, **Pillow**, **scikit‑image**, & GitHub Pages.
Special thanks to **ChatGPT** for guidance and code snippets!
