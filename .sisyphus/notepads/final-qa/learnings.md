
## F3 QA Results (2026-03-30)

### Findings
1. `artifacts/artifacts.json` does NOT exist in the repo — app uses `manifest.json` + individual artifact JSON files instead. 404 is expected.
2. The app works perfectly: manifest.json + sidecar JSON files load all 64 cards (57 NT + 7 KDH).
3. 404 redirect correctly goes to `/museum-as-code/` (not `/`).
4. No console errors on clean page load.
5. User site xodn348.github.io/ is completely separate and intact.
