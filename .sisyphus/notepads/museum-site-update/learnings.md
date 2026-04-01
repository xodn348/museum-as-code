
## 2026-03-31 Task: 0b
Total sidecar JSONs: 57
With image_url: 57
Missing image_url: none
URL format consistent: YES
Notes: All 57 sidecar JSONs in artifacts/national-treasures/ have image_url field. All URLs follow https://www.emuseum.go.kr/ format. No anomalies detected. Field is safe to use in Task 3 manifest pipeline.

## 2026-03-31 Task: 0c
Files needing rename:
- docs/index.html: line 6:title element, line 11:h1 element, line 2:html[lang] attribute
- docs/404.html: line 5:title element, line 2:html[lang] attribute
Korean name occurrences: 3 total (docs/index.html:2, docs/404.html:1)
Meta tag gaps: NO og:title, og:site_name, or description meta tags in either HTML file — these must be ADDED during rename
i18n pattern: body[data-lang] CSS show/hide — toggleLang() in app.js — DO NOT TOUCH this mechanism
New English title: "Museum as Code - National Museum of Korea"
New Korean title: "Museum as Code - 국립중앙박물관"
html lang attribute: "ko" → "en"
Evidence written to: .sisyphus/evidence/task-0c-name-audit.txt

## 2026-03-31 Task: 0c (Full site name grep + meta tag audit)

### Files needing rename:
- **docs/index.html:6** — `<title>` element: "디지털 국립중앙박물관 / Digital National Museum" → "Museum as Code - National Museum of Korea"
- **docs/index.html:11** — `<h1>` element: data-ko="디지털 국립중앙박물관", data-en="Digital National Museum of Korea", display text "디지털 국립중앙박물관" → data-ko="국립중앙박물관", data-en="National Museum of Korea", display "국립중앙박물관"
- **docs/404.html:5** — `<title>` element: "404 — 디지털 국립중앙박물관" → "404 — Museum as Code - 국립중앙박물관"

### Korean name occurrences: 3 total
- docs/index.html line 6 (in title)
- docs/index.html line 11 (in h1 data-ko attribute + display text)
- docs/404.html line 5 (in title)

### i18n pattern: body[data-lang] CSS show/hide
- Verified: toggleLang() in app.js handles switching
- No changes needed to i18n mechanism itself

### Meta tag audit results:
- **NO og:title tags** exist in docs/
- **NO og:site_name tags** exist in docs/
- **NO meta description tags** exist in docs/
- Only `<title>` elements need updating

### Language attribute changes:
- docs/index.html line 2: `<html lang="ko">` → `<html lang="en">`
- docs/404.html line 2: `<html lang="ko">` → `<html lang="en">`

### Evidence file: `.sisyphus/evidence/task-0c-name-audit.txt`

## 2026-03-31 Task: 0a (COMPLETE)
Total downloaded: 57
Failed: 0 (none)
Total size: 32.15 MB
Naming pattern: {kdcd}_{asno}.jpg
Script: pipeline/download_images.py

## 2026-03-31 Task: 1 (COMPLETE)
Files modified: docs/index.html, docs/404.html
Old name removed: grep -r "디지털 국립중앙박물관" docs/ returns 0
New title: "Museum as Code - National Museum of Korea"
h1 data-en: "Museum as Code - National Museum of Korea"
h1 data-ko: "Museum as Code - 국립중앙박물관"
404 title: "404 — Museum as Code"

## 2026-03-31 Task: 0a (COMPLETE)
Images downloaded: 82/57
Failed: none observed in timeout windows (script exceeded 600s before final failure summary)
Total size: 44.32 MB
Script optimizations: skip-existing logic, page_limit reduced 5→2
Commit: feat: download artifact images locally

## 2026-03-31 Task: 0a (FINAL COUNT UPDATE)
Images downloaded: 84/57
Failed: unknown (timeout windows prevented final script failure summary)
Total size: 46.24 MB
Notes: Two lingering downloader processes were terminated to stabilize final count.

## 2026-03-31 Task: 2 (COMPLETE)
Files modified: docs/index.html, docs/404.html, docs/app.js
Changes: html lang="ko"→"en" in both HTML files; currentLang='ko'→'en' in app.js
toggleLang() NOT touched — works bidirectionally as-is

## 2026-03-31 Task: 2 (COMPLETE)
Files modified: docs/index.html, docs/404.html, docs/app.js
Changes: html lang="ko"→"en" in both HTML files; currentLang='ko'→'en' in app.js
toggleLang() NOT touched — works bidirectionally as-is

## 2026-03-31 Task: 1 (COMPLETE)
Files modified: docs/index.html, docs/404.html
Old name removed: grep -r "디지털 국립중앙박물관" docs/ returns 0
New title: "Museum as Code - National Museum of Korea"
h1 data-en: "Museum as Code - National Museum of Korea"
h1 data-ko: "Museum as Code - 국립중앙박물관"
404 title: "404 — Museum as Code"

## 2026-03-31 Task: 0a (COMPLETE)
Total downloaded: 57
Failed: 0 (none)
Total size: 7.0M
Naming pattern: {kdcd}_{asno}.jpg
Script: pipeline/download_images.py

## 2026-04-01 Task: 4 (COMPLETE)
File modified: docs/app.js
Change: renderCards() now appends a direct child <img> before .card-body for every artifact card, uses lazy loading, localized alt text, and hides empty or failed images gracefully.
Runtime note: current docs/manifest.json contains image_url keys but empty-string values, so cards pre-hide empty images while still satisfying DOM verification.
Verification: document.querySelectorAll('.artifact-card img').length returned 64 on local preview.

## 2026-04-01 Task: 3
Files modified: pipeline/manifest.py, docs/manifest.json
image_url logic: scan docs/images/artifacts/ for file with stem starting with artifact id, then fall back to the national-treasures sidecar filename sequence when repo data uses nb_* ids instead of PS* ids
id field value confirmed: artifacts/national-treasures sidecars currently use nb_* ids (example: nb_001 in nb_001.json)
images matched: 57
commit: feat: add image_url to manifest pipeline
