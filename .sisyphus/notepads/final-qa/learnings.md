
## F3 QA Results (2026-03-30)

### Findings
1. `artifacts/artifacts.json` does NOT exist in the repo — app uses `manifest.json` + individual artifact JSON files instead. 404 is expected.
2. The app works perfectly: manifest.json + sidecar JSON files load all 64 cards (57 NT + 7 KDH).
3. 404 redirect correctly goes to `/museum-as-code/` (not `/`).
4. No console errors on clean page load.
5. User site xodn348.github.io/ is completely separate and intact.

## F3 QA Results (2026-04-01)

### Findings
1. Local HTTP serving via `python3 -m http.server 8787 --directory docs` is required; file protocol would break data fetches.
2. `manifest.json` contains 64 `image_url` entries and artifacts image directory has local JPG assets available.
3. Title is correctly `Museum as Code - National Museum of Korea` and default language state is `en` on initial load.
4. Language toggle works bidirectionally (`en -> ko -> en`) and switches visible localized content.
5. Card view renders `<img>` elements for artifacts; sample load check shows actual successfully loaded photos in-browser.
6. Broken image handling is graceful: card image `onerror` path hides the image (`display: none`) rather than leaving a broken icon.
7. Graph data loads with image URLs (`dataWithImg: 54/61` graph nodes) and hover event increases image-node size (`50px -> 80px`).
8. Mobile viewport check at `375x812` shows no horizontal overflow in tested state.

## F3 QA Results (2026-04-01, rerun)

### Findings
1. Local page title is correct (`Museum as Code - National Museum of Korea`) and `body.dataset.lang` initializes to `en`.
2. Language toggle flips state `en -> ko -> en`, but visible localized content remains mixed (both EN/KO blocks visible in DOM checks) and H1 remains mixed-language (`Museum as Code - 국립중앙박물관`).
3. Cards view currently has 64 `<img>` tags but they render with empty `src` and `display:none` in this run (`visibleCardImgs=0`).
4. Graph container initializes (`#cy` present) and node style inspection shows photo backgrounds on a subset of nodes (`withBackgroundImage=54/61`).
5. Forced image error path still hides images (`display:none`), so no broken icon appears in tested element.
6. Mobile viewport at `375x812` remains responsive (`scrollWidth == innerWidth`).
