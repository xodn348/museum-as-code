# Museum Site Update — Rename, English Default, Photos, Deploy

## TL;DR

> **Quick Summary**: Rename site to "Museum as Code", switch to English default, add artifact photos in cards AND as Cytoscape graph image nodes with hover/click interactions, then deploy to GitHub Pages. All artifact data remains in han (`.hgl`) format.
> 
> **Deliverables**:
> - Site title/header updated across all files
> - English as default language on page load
> - Artifact cards display photos from e-museum.go.kr
> - Graph nodes show artifact photos with hover-enlarge + click-for-info
> - All changes pushed to origin/main for GitHub Pages deployment
> 
> **Estimated Effort**: Medium (11 tasks across 4 waves, ~2-3 hours)
> **Parallel Execution**: YES - 4 waves + validation wave + final review
> **Critical Path**: Wave 0 validation → Wave 1 (rename + lang + pipeline) → Wave 2 (cards + graph parallel) → Wave 3 (push) → Final

---

## Context

### Original Request
User wants 4 changes to the museum-as-code static site:
1. Rename from "디지털 국립중앙박물관" to "Museum as Code - National Museum of Korea" — user explicitly said people will think it's an official government site ("우리가 오피셜인줄 착각하잖아")
2. Switch default language from Korean to English
3. Add artifact photos using image URLs from e-museum.go.kr sidecar JSON
4. Push existing + new commits to deploy on GitHub Pages

### Interview Summary
**Key Discussions**:
- **Site name**: "Museum as Code - National Museum of Korea" (user repeated this explicitly)
- **Default language**: English (`currentLang = 'en'`, `<html lang="en">`)
- **Photo source**: `image_url` field in sidecar JSON files (`artifacts/national-treasures/nb_XXX.json`)
- **Photo pipeline**: Add `image_url` to `manifest.json` via pipeline, then render in cards
- **No test infra**: Agent-executed QA only (Playwright)

**Research Findings**:
- i18n uses CSS show/hide: `body[data-lang='ko']` hides `[data-lang='en']` elements and vice versa
- `toggleLang()` in `app.js:403-417` handles switching
- manifest.json lacks `image_url` — only has id, collection, hgl_path, json_path, name_ko, name_en, period, designation
- Sidecar JSON (e.g. `nb_001.json:13`) has `"image_url": "https://www.emuseum.go.kr/images/relic/11/0001.jpg"`
- `style.css:42` has `.artifact-card img { width: 100%; height: 200px; object-fit: cover; }` — already prepared but unused
- Card rendering at `app.js:307-315` — text only, no image

### Metis Review
**Identified Gaps** (addressed):
- **Korean-mode h1 text**: Default applied — "Museum as Code - 국립중앙박물관" for Korean mode
- **e-museum hotlinking**: Added Wave 0 validation gate (curl test + Playwright img load)
- **Missing image_url in some sidecars**: Added Wave 0 validation to count files with/without field
- **Pipeline confirmation**: Added Wave 0 task to verify `generate_graph.py` → `manifest.json` flow
- **Meta tag audit**: Added to Wave 0 — grep for `og:title`, `og:site_name`, `<meta name="description">`
- **Image fallback**: `onerror="this.style.display='none'"` — hide broken images gracefully
- **`loading="lazy"`**: Added as single attribute (not a feature) per Metis recommendation
- **Full 404.html audit**: Check entire file for old name references, not just title

---

## Work Objectives

### Core Objective
Update the museum-as-code site identity (name + language) and enhance artifact cards with photos, then deploy all changes to GitHub Pages.

### Concrete Deliverables
- `docs/index.html` — updated title, h1 data attributes, meta tags, html lang
- `docs/404.html` — updated title and any body references
- `docs/app.js` — `currentLang = 'en'`, image rendering in cards
- `docs/manifest.json` — regenerated with `image_url` field
- `pipeline/generate_graph.py` — modified to extract `image_url` from sidecar JSON
- All changes pushed to `origin/main`

### Definition of Done
- [ ] `grep -r "디지털 국립중앙박물관" docs/` returns 0 results
- [ ] Site loads with English as default language
- [ ] Artifact cards display images from e-museum.go.kr
- [ ] `git log origin/main..HEAD` shows 0 commits (all pushed)
- [ ] GitHub Pages serves updated site

### Must Have
- Site title shows "Museum as Code - National Museum of Korea" in browser tab
- h1 shows "Museum as Code - National Museum of Korea" in English mode
- h1 shows "Museum as Code - 국립중앙박물관" in Korean mode
- Page loads with `body[data-lang="en"]` and `<html lang="en">`
- Language toggle still works bidirectionally (EN↔KO)
- Artifact cards show photos with graceful fallback for missing/broken images
- `loading="lazy"` on all artifact images
- All changes deployed via `git push origin main`
- Graph nodes display artifact photos instead of text labels
- Clicking a graph node opens the detail/info overlay
- Hovering on a graph node enlarges the photo
- Graph visually shows photo-to-photo relationships (edges between image nodes)

### Must NOT Have (Guardrails)
- DO NOT touch the i18n CSS show/hide system — it works, don't "improve" it
- DO NOT proxy, cache, or locally copy external images — direct `<img src>` only
- DO NOT add lazy loading library, lightbox, or image optimization features
- DO NOT refactor app.js card rendering architecture — add image INTO existing template
- DO NOT modify generate_graph.py beyond adding `image_url` field extraction
- DO NOT add retry logic, monitoring, or error handling beyond `onerror` attribute
- DO NOT change other default settings (sort, view, filters)
- DO NOT create new files — all changes go into existing files
- DO NOT update git config user.name or user.email

---

## Verification Strategy (MANDATORY)

> **ZERO HUMAN INTERVENTION** — ALL verification is agent-executed. No exceptions.

### Test Decision
- **Infrastructure exists**: NO
- **Automated tests**: None
- **Framework**: none
- **Agent-Executed QA**: ALWAYS — Playwright for UI, Bash for CLI/grep verification

### QA Policy
Every task MUST include agent-executed QA scenarios.
Evidence saved to `.sisyphus/evidence/task-{N}-{scenario-slug}.{ext}`.

- **Frontend/UI**: Use Playwright — Navigate, interact, assert DOM, screenshot
- **CLI/Pipeline**: Use Bash — Run commands, check output, diff files
- **Data validation**: Use Bash — grep, jq, diff for JSON verification

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 0 (Validation Gate — BLOCKING, all 4 in parallel):
├── Task 0a: Validate e-museum image hotlinking [explore]
├── Task 0b: Validate sidecar JSONs have image_url [explore]
├── Task 0c: Full site name grep + meta tag audit [explore]
└── Task 0d: Confirm generate_graph.py → manifest.json pipeline [explore]

Wave 1 (After Wave 0 — independent changes, 3 in parallel):
├── Task 1: Rename site across all files [quick]
├── Task 2: Switch default language to English [quick]
└── Task 3: Add image_url to manifest.json via pipeline [unspecified-low]

Wave 2 (After Task 3 — rendering depends on manifest data, 2 in parallel):
├── Task 4: Render artifact photos in cards [unspecified-low]
└── Task 5: Graph photo nodes — Cytoscape image nodes + hover/click [unspecified-high]

Wave 3 (After ALL — ship):
└── Task 6: Push to origin/main and verify deployment [quick]

Wave FINAL (After push — 4 parallel reviews):
├── F1: Plan compliance audit [oracle]
├── F2: Code quality review [unspecified-high]
├── F3: Real manual QA [unspecified-high]
└── F4: Scope fidelity check [deep]
→ Present results → Get explicit user okay
```

### Dependency Matrix

| Task | Depends On | Blocks |
|------|-----------|--------|
| 0a   | —         | 3, 4   |
| 0b   | —         | 3      |
| 0c   | —         | 1      |
| 0d   | —         | 3      |
| 1    | 0c        | 6      |
| 2    | —         | 6      |
| 3    | 0a,0b,0d  | 4, 5   |
| 4    | 3         | 6      |
| 5    | 3         | 6      |
| 6    | 1,2,4,5   | F1-F4  |
| F1-F4| 6         | —      |

### Agent Dispatch Summary

- **Wave 0**: **4** — T0a-T0d → `explore` (subagent_type)
- **Wave 1**: **3** — T1 → `quick` (subagent_type), T2 → `quick`, T3 → `unspecified-low`
- **Wave 2**: **2** — T4 → `unspecified-low`, T5 → `unspecified-high`
- **Wave 3**: **1** — T6 → `quick`
- **FINAL**: **4** — F1 → `oracle`, F2 → `unspecified-high`, F3 → `unspecified-high`, F4 → `deep`

Critical Path: 0a/0b/0d → 3 → 4/5 → 6 → F1-F4 → user okay
Parallel Speedup: ~40% vs sequential

---

## TODOs

> Implementation + Test = ONE Task. Never separate.
> EVERY task MUST have: Recommended Agent Profile + Parallelization info + QA Scenarios.

### Wave 0 — Validation Gate (BLOCKING)

- [ ] 0a. Validate e-museum.go.kr Image Hotlinking

  **What to do**:
  - Pick 3 sample image URLs from sidecar JSONs (first, middle, last artifact)
  - `curl -I` each URL — check HTTP status (200 OK), Content-Type (image/*), no redirect to login/block page
  - Load one URL in Playwright `<img>` tag — verify `naturalWidth > 0` (actual image loaded, not placeholder)
  - Check response headers for `X-Frame-Options`, CORS, or referrer restrictions
  - **IF BLOCKED**: Document the block type and stop — escalate to user before proceeding

  **Must NOT do**:
  - Do NOT download or save images locally
  - Do NOT set up a proxy or caching layer

  **Recommended Agent Profile**:
  - **Subagent Type**: `explore`
    - Reason: Validation/research task, no code changes needed
  - **Skills**: [`browse`]
    - `browse`: Needed to test actual image loading in browser context (CORS, referrer policy)

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 0 (with Tasks 0b, 0c, 0d)
  - **Blocks**: Task 3 (manifest pipeline), Task 4 (card images)
  - **Blocked By**: None

  **References**:
  - `artifacts/national-treasures/nb_001.json:13` — Sample `image_url` field: `"https://www.emuseum.go.kr/images/relic/11/0001.jpg"`
  - `docs/style.css:42` — `.artifact-card img` CSS already exists, confirming images were planned

  **QA Scenarios**:
  ```
  Scenario: e-museum images are accessible via direct URL (happy path)
    Tool: Bash (curl)
    Preconditions: Internet connection available
    Steps:
      1. Extract 3 image_url values from nb_001.json, nb_032.json, nb_064.json using grep/jq
      2. curl -I each URL, capture HTTP status code
      3. Assert: all 3 return HTTP 200
      4. Assert: Content-Type header starts with "image/"
    Expected Result: All 3 URLs return HTTP 200 with image Content-Type
    Failure Indicators: HTTP 403/404, redirect to HTML page, Content-Type text/html
    Evidence: .sisyphus/evidence/task-0a-curl-headers.txt

  Scenario: Image actually renders in browser (CORS/referrer check)
    Tool: Playwright (browse skill)
    Preconditions: One valid image URL from step above
    Steps:
      1. Navigate to about:blank
      2. Inject <img src="{url}"> via page.evaluate
      3. Wait 5s for load
      4. Assert: img.naturalWidth > 0 AND img.naturalHeight > 0
    Expected Result: Image dimensions are non-zero (image loaded successfully)
    Failure Indicators: naturalWidth === 0 (blocked by CORS/referrer policy)
    Evidence: .sisyphus/evidence/task-0a-browser-img-load.png
  ```

  **Commit**: NO (validation only, no code changes)

- [ ] 0b. Validate Sidecar JSONs Have image_url Field

  **What to do**:
  - Count total sidecar JSON files in `artifacts/national-treasures/`
  - Count how many contain `"image_url"` field
  - List any files MISSING the field (these artifacts won't show images — that's OK, but we need the count)
  - Verify URL format consistency (all start with `https://www.emuseum.go.kr/`)

  **Must NOT do**:
  - Do NOT modify any sidecar JSON files
  - Do NOT add missing image_url fields

  **Recommended Agent Profile**:
  - **Subagent Type**: `explore`
    - Reason: Data validation task, read-only filesystem inspection
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 0 (with Tasks 0a, 0c, 0d)
  - **Blocks**: Task 3 (manifest pipeline needs to know which fields exist)
  - **Blocked By**: None

  **References**:
  - `artifacts/national-treasures/nb_001.json` — Sample sidecar with `image_url` at line 13
  - `docs/manifest.json` — Current manifest lacks `image_url` (only has id, collection, hgl_path, json_path, name_ko, name_en, period, designation)

  **QA Scenarios**:
  ```
  Scenario: Count sidecar files with image_url (happy path)
    Tool: Bash (grep)
    Preconditions: artifacts/national-treasures/ directory exists
    Steps:
      1. ls artifacts/national-treasures/nb_*.json | wc -l → total count
      2. grep -l "image_url" artifacts/national-treasures/nb_*.json | wc -l → count with field
      3. Compare: total vs with-field
      4. grep -L "image_url" artifacts/national-treasures/nb_*.json → list missing ones
    Expected Result: ≥60 out of 64 files have image_url field
    Failure Indicators: <50% have field (pipeline would produce mostly blank images)
    Evidence: .sisyphus/evidence/task-0b-image-url-audit.txt

  Scenario: URL format consistency check
    Tool: Bash (grep)
    Preconditions: Files with image_url identified
    Steps:
      1. grep "image_url" artifacts/national-treasures/nb_*.json | grep -v "emuseum.go.kr" → find non-standard URLs
    Expected Result: 0 non-standard URLs (all point to emuseum.go.kr)
    Failure Indicators: Any URL pointing to different domain
    Evidence: .sisyphus/evidence/task-0b-url-format-check.txt
  ```

  **Commit**: NO (validation only)

- [ ] 0c. Full Site Name Grep + Meta Tag Audit

  **What to do**:
  - `grep -rn "디지털 국립중앙박물관" docs/` — find ALL occurrences of old name
  - `grep -rn "og:title\|og:site_name\|meta.*description" docs/index.html` — find all meta tags referencing site name
  - Check `docs/404.html` entirely for any old name references (not just title)
  - Document every location that needs renaming with file:line

  **Must NOT do**:
  - Do NOT rename anything yet — this is audit only
  - Do NOT touch files outside `docs/`

  **Recommended Agent Profile**:
  - **Subagent Type**: `explore`
    - Reason: Read-only audit task
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 0 (with Tasks 0a, 0b, 0d)
  - **Blocks**: Task 1 (rename needs complete location list)
  - **Blocked By**: None

  **References**:
  - `docs/index.html:2` — `<html lang="ko">` (known location)
  - `docs/index.html:6` — `<title>` tag (known location)
  - `docs/404.html` — title tag (known location)
  - `docs/index.html` h1 — `data-ko` and `data-en` attributes (known locations)

  **QA Scenarios**:
  ```
  Scenario: Find all old name occurrences (happy path)
    Tool: Bash (grep)
    Preconditions: docs/ directory exists
    Steps:
      1. grep -rn "디지털 국립중앙박물관" docs/ → capture all matches
      2. grep -rn "og:title\|og:site_name\|meta.*description" docs/index.html
      3. cat docs/404.html and manually inspect for any name references
    Expected Result: Complete list of file:line locations needing rename
    Failure Indicators: grep returns 0 results (name already changed — unexpected)
    Evidence: .sisyphus/evidence/task-0c-name-audit.txt

  Scenario: No hidden name references in JS/CSS
    Tool: Bash (grep)
    Preconditions: docs/ directory exists
    Steps:
      1. grep -rn "디지털\|국립중앙박물관" docs/app.js docs/graph.js docs/style.css
    Expected Result: 0 matches in JS/CSS files (name only in HTML)
    Failure Indicators: Matches found in unexpected files
    Evidence: .sisyphus/evidence/task-0c-js-css-check.txt
  ```

  **Commit**: NO (audit only)

- [ ] 0d. Confirm generate_graph.py → manifest.json Pipeline

  **What to do**:
  - Read `pipeline/generate_graph.py` — understand how it reads sidecar JSONs and outputs `docs/manifest.json`
  - Identify the exact code location where manifest fields are assembled (the dict/list that becomes JSON)
  - Verify: can we add `image_url` by just reading the field from sidecar JSON and including it?
  - Run the pipeline once (`python pipeline/generate_graph.py`) to confirm it works in current state
  - Document: input files, output file, field mapping, where to add `image_url`

  **Must NOT do**:
  - Do NOT modify generate_graph.py yet — read-only inspection
  - Do NOT modify manifest.json

  **Recommended Agent Profile**:
  - **Subagent Type**: `explore`
    - Reason: Code inspection + single command execution to verify pipeline works
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 0 (with Tasks 0a, 0b, 0c)
  - **Blocks**: Task 3 (pipeline modification needs this understanding)
  - **Blocked By**: None

  **References**:
  - `pipeline/generate_graph.py` — The pipeline script to inspect (exact line numbers TBD by this task)
  - `docs/manifest.json` — Current output (missing `image_url`)
  - `artifacts/national-treasures/nb_001.json` — Sample input sidecar

  **QA Scenarios**:
  ```
  Scenario: Pipeline runs successfully in current state
    Tool: Bash
    Preconditions: Python 3 available, pipeline/ directory exists
    Steps:
      1. python pipeline/generate_graph.py (or python3)
      2. Check exit code is 0
      3. Verify docs/manifest.json was regenerated (check mtime or diff)
    Expected Result: Pipeline completes without errors, manifest.json updated
    Failure Indicators: Non-zero exit code, Python import errors, missing dependencies
    Evidence: .sisyphus/evidence/task-0d-pipeline-run.txt

  Scenario: Document field mapping for image_url addition
    Tool: Bash (grep/read)
    Preconditions: generate_graph.py readable
    Steps:
      1. Read generate_graph.py, find where sidecar JSON fields are extracted
      2. Identify the dict/object that maps to manifest.json entries
      3. Document: "Add image_url at line X, pattern: entry['image_url'] = sidecar.get('image_url', '')"
    Expected Result: Clear documentation of where and how to add image_url field
    Failure Indicators: Pipeline uses unexpected format (not simple JSON read → write)
    Evidence: .sisyphus/evidence/task-0d-pipeline-analysis.txt
  ```

  **Commit**: NO (inspection only)

### Wave 1 — Core Changes (parallel after Wave 0)

- [x] 1. Rename Site Across All Files

  **What to do**:
  - Replace ALL occurrences of "디지털 국립중앙박물관" found by Task 0c audit
  - `docs/index.html`: Update `<title>` to "Museum as Code - National Museum of Korea"
  - `docs/index.html`: Update h1 `data-en` attribute to "Museum as Code - National Museum of Korea"
  - `docs/index.html`: Update h1 `data-ko` attribute to "Museum as Code - 국립중앙박물관"
  - `docs/index.html`: Update any `og:title`, `og:site_name`, `<meta name="description">` if present
  - `docs/404.html`: Update `<title>` and any body references to old name
  - Verify with `grep -r "디지털 국립중앙박물관" docs/` → 0 results

  **Must NOT do**:
  - Do NOT touch i18n CSS show/hide system
  - Do NOT rename anything outside `docs/` directory
  - Do NOT change the h1 element structure — only change text content in data attributes

  **Recommended Agent Profile**:
  - **Subagent Type**: `explore` (simple text replacements across 2 files)
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 2, 3)
  - **Blocks**: Task 6 (push)
  - **Blocked By**: Task 0c (need complete list of locations)

  **References**:
  - `docs/index.html:6` — `<title>` tag with old name
  - `docs/index.html` h1 element — `data-ko` and `data-en` attributes with old name
  - `docs/404.html` — `<title>` tag with old name
  - Task 0c output — `.sisyphus/evidence/task-0c-name-audit.txt` for complete location list

  **QA Scenarios**:
  ```
  Scenario: Old name completely removed (happy path)
    Tool: Bash (grep)
    Preconditions: All edits applied to docs/index.html and docs/404.html
    Steps:
      1. grep -r "디지털 국립중앙박물관" docs/ → capture output
      2. Assert: output is empty (0 matches)
      3. grep "Museum as Code" docs/index.html → capture output
      4. Assert: matches found in <title> and h1 data-en attribute
    Expected Result: Zero old name occurrences, new name present in title + h1
    Failure Indicators: Any grep match for old name
    Evidence: .sisyphus/evidence/task-1-name-grep.txt

  Scenario: Korean mode h1 shows correct text
    Tool: Playwright (browse skill)
    Preconditions: Site served locally (python -m http.server in docs/)
    Steps:
      1. Navigate to localhost:8000
      2. Query h1 element's data-ko attribute
      3. Assert: data-ko contains "Museum as Code - 국립중앙박물관"
      4. Query <title> element text
      5. Assert: title contains "Museum as Code - National Museum of Korea"
    Expected Result: Both Korean and English names are correct
    Failure Indicators: Old name still visible, or "Museum as Code" prefix missing
    Evidence: .sisyphus/evidence/task-1-playwright-name.png
  ```

  **Commit**: YES
  - Message: `rename: Museum as Code - National Museum of Korea`
  - Files: `docs/index.html`, `docs/404.html`
  - Pre-commit: `grep -r "디지털 국립중앙박물관" docs/` returns 0

- [x] 2. Switch Default Language to English

  **What to do**:
  - `docs/index.html:2`: Change `<html lang="ko">` → `<html lang="en">`
  - `docs/app.js:7`: Change `let currentLang = 'ko'` → `let currentLang = 'en'`
  - `docs/app.js:421-424`: Verify init code sets `body.dataset.lang` from `currentLang` (should auto-follow)
  - Test: page loads → body has `data-lang="en"` → English content visible by default
  - Test: click language toggle → switches to Korean → click again → back to English

  **Must NOT do**:
  - Do NOT modify the `toggleLang()` function logic
  - Do NOT change the CSS show/hide rules in style.css
  - Do NOT change any other default settings (sort, view, filters)

  **Recommended Agent Profile**:
  - **Subagent Type**: `explore` (2 simple string replacements)
  - **Skills**: [`browse`]
    - `browse`: Needed to verify page loads in English and toggle works

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1, 3)
  - **Blocks**: Task 6 (push)
  - **Blocked By**: None (independent of Wave 0 results)

  **References**:
  - `docs/index.html:2` — `<html lang="ko">` to change
  - `docs/app.js:7` — `let currentLang = 'ko'` to change
  - `docs/app.js:403-417` — `toggleLang()` function (DO NOT MODIFY, just verify it works)
  - `docs/app.js:421-424` — Init code that sets `body.dataset.lang` (should auto-follow currentLang change)
  - `docs/style.css` — CSS rules `[data-lang="ko"]`/`[data-lang="en"]` show/hide (DO NOT MODIFY)

  **QA Scenarios**:
  ```
  Scenario: Page loads in English by default (happy path)
    Tool: Playwright (browse skill)
    Preconditions: Local server running (python -m http.server in docs/)
    Steps:
      1. Navigate to localhost:8000
      2. Evaluate: document.documentElement.lang → assert equals "en"
      3. Evaluate: document.body.dataset.lang → assert equals "en"
      4. Query selector [data-lang="en"] elements → assert visible
      5. Query selector [data-lang="ko"] elements → assert hidden (display:none)
    Expected Result: HTML lang="en", body data-lang="en", English content visible
    Failure Indicators: lang="ko", Korean content visible on load
    Evidence: .sisyphus/evidence/task-2-english-default.png

  Scenario: Language toggle still works bidirectionally
    Tool: Playwright (browse skill)
    Preconditions: Page loaded in English (default)
    Steps:
      1. Find and click language toggle button/link
      2. Assert: body.dataset.lang now equals "ko"
      3. Assert: Korean content visible, English content hidden
      4. Click toggle again
      5. Assert: body.dataset.lang back to "en"
      6. Assert: English content visible again
    Expected Result: Toggle switches EN→KO→EN without errors
    Failure Indicators: Toggle doesn't switch, page errors, content stuck
    Evidence: .sisyphus/evidence/task-2-toggle-test.png
  ```

  **Commit**: YES
  - Message: `feat: switch default language to English`
  - Files: `docs/app.js`, `docs/index.html`
  - Pre-commit: Playwright confirms English default

- [x] 3. Add image_url to Manifest via Pipeline

  **What to do**:
  - Modify `pipeline/generate_graph.py` at the location identified by Task 0d
  - Add `image_url` field extraction from sidecar JSON: `entry['image_url'] = sidecar.get('image_url', '')`
  - Run the pipeline: `python pipeline/generate_graph.py` (or python3)
  - Verify `docs/manifest.json` now contains `image_url` fields
  - Verify URL values match sidecar JSON sources (spot-check 3 entries)
  - Handle missing `image_url` gracefully: use empty string `""` as default (not null, not omit)

  **Must NOT do**:
  - Do NOT modify generate_graph.py beyond adding the `image_url` field extraction
  - Do NOT change existing field names or order in manifest.json
  - Do NOT add any other new fields
  - Do NOT download or validate the image URLs in the pipeline

  **Recommended Agent Profile**:
  - **Subagent Type**: `explore` (single field addition to existing pipeline)
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1, 2)
  - **Blocks**: Task 4 (card images), Task 5 (graph images)
  - **Blocked By**: Task 0a (hotlinking OK), Task 0b (field exists), Task 0d (pipeline understood)

  **References**:
  - `pipeline/generate_graph.py` — Pipeline script (exact line from Task 0d analysis)
  - `docs/manifest.json` — Output file to regenerate
  - `artifacts/national-treasures/nb_001.json:13` — Sample sidecar with `image_url`
  - Task 0d output — `.sisyphus/evidence/task-0d-pipeline-analysis.txt` for exact insertion point

  **QA Scenarios**:
  ```
  Scenario: Manifest contains image_url after pipeline run (happy path)
    Tool: Bash
    Preconditions: Pipeline dependencies installed, Task 0d confirmed pipeline works
    Steps:
      1. python pipeline/generate_graph.py → assert exit code 0
      2. grep -c "image_url" docs/manifest.json → capture count
      3. Assert: count ≥ 60 (most of 64 artifacts should have URLs)
      4. python -c "import json; m=json.load(open('docs/manifest.json')); print(m[0].get('image_url','MISSING'))" → assert starts with "https://www.emuseum.go.kr/"
    Expected Result: ≥60 image_url fields in manifest, URLs point to emuseum.go.kr
    Failure Indicators: 0 image_url fields, pipeline error, wrong URL format
    Evidence: .sisyphus/evidence/task-3-manifest-image-urls.txt

  Scenario: Missing image_url in sidecar produces empty string (not crash)
    Tool: Bash
    Preconditions: At least one sidecar might lack image_url (from Task 0b audit)
    Steps:
      1. python -c "import json; m=json.load(open('docs/manifest.json')); missing=[e['id'] for e in m if not e.get('image_url')]; print(f'{len(missing)} entries without image_url: {missing[:5]}')"
      2. Assert: no KeyError — entries without URL have empty string ""
    Expected Result: Graceful handling — empty string for missing URLs, no crashes
    Failure Indicators: KeyError, null values, pipeline crash on missing field
    Evidence: .sisyphus/evidence/task-3-missing-url-handling.txt
  ```

  **Commit**: YES
  - Message: `feat: add image_url to manifest pipeline`
  - Files: `pipeline/generate_graph.py`, `docs/manifest.json`
  - Pre-commit: `grep "image_url" docs/manifest.json | head -3` shows URLs

### Wave 2 — Rendering (parallel, after Task 3)

- [x] 4. Render Artifact Photos in Cards

  **What to do**:
  - In `docs/app.js`, find the card rendering function (lines ~307-315)
  - Add an `<img>` element BEFORE the existing text content in each card
  - Image source: `artifact.image_url` from manifest data
  - Add `loading="lazy"` attribute on every `<img>`
  - Add `onerror="this.style.display='none'"` for graceful fallback on broken images
  - Add `alt` attribute with artifact name for accessibility
  - The existing CSS at `style.css:42` (`.artifact-card img`) already handles sizing — no CSS changes needed

  **Must NOT do**:
  - Do NOT refactor the card rendering architecture — add image INTO existing template literal
  - Do NOT add a lightbox, modal, or image zoom feature
  - Do NOT add lazy loading library — just the native `loading="lazy"` attribute
  - Do NOT add retry logic or image preloading
  - Do NOT modify style.css — the `.artifact-card img` rule already exists

  **Recommended Agent Profile**:
  - **Subagent Type**: `explore` (single function modification in one file)
  - **Skills**: [`browse`]
    - `browse`: Needed to verify images render in browser and fallback works

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Task 5)
  - **Blocks**: Task 6 (push)
  - **Blocked By**: Task 3 (needs manifest with image_url)

  **References**:
  - `docs/app.js:307-315` — Current card rendering (text only, no image) — add `<img>` here
  - `docs/style.css:42` — `.artifact-card img { width: 100%; height: 200px; object-fit: cover; }` — already prepared, DO NOT MODIFY
  - `docs/manifest.json` — After Task 3, will contain `image_url` field per artifact
  - Sample URL format: `https://www.emuseum.go.kr/images/relic/11/0001.jpg`

  **QA Scenarios**:
  ```
  Scenario: Cards display artifact images (happy path)
    Tool: Playwright (browse skill)
    Preconditions: Local server running, manifest.json has image_url fields (Task 3 complete)
    Steps:
      1. Navigate to localhost:8000
      2. Wait for cards to render (wait for selector `.artifact-card`)
      3. Query: document.querySelectorAll('.artifact-card img').length
      4. Assert: count > 0 (at least some cards have images)
      5. Query first card image: document.querySelector('.artifact-card img').naturalWidth
      6. Assert: naturalWidth > 0 (image actually loaded)
      7. Query first card image: getAttribute('loading')
      8. Assert: equals "lazy"
    Expected Result: Cards show images, images load, lazy loading enabled
    Failure Indicators: No <img> elements in cards, naturalWidth === 0, missing lazy attribute
    Evidence: .sisyphus/evidence/task-4-card-images.png

  Scenario: Broken image URL hides gracefully (error handling)
    Tool: Playwright (browse skill)
    Preconditions: At least one artifact has empty/invalid image_url
    Steps:
      1. Navigate to localhost:8000
      2. Evaluate: find a card where img failed to load (naturalWidth === 0)
      3. Assert: that img element has display:none (onerror handler fired)
      4. Assert: card still displays text content correctly (name, period, designation)
    Expected Result: Broken images hidden, card text still readable
    Failure Indicators: Broken image icon visible, card layout broken
    Evidence: .sisyphus/evidence/task-4-broken-image-fallback.png
  ```

  **Commit**: YES
  - Message: `feat: render artifact photos in cards`
  - Files: `docs/app.js`
  - Pre-commit: Playwright confirms `.artifact-card img` elements exist

- [x] 5. Graph Photo Nodes — Cytoscape Image Nodes + Hover/Click

  **What to do**:
  - In `docs/graph.js`, modify node style to use `background-image` property from manifest `image_url`
  - Set node style: `'background-image': 'data(image_url)'`, `'background-fit': 'cover'`, `'background-clip': 'node'`
  - Set node shape to `'ellipse'` or keep existing, sized appropriately for image display (~40-60px)
  - Pass `image_url` as node data when creating Cytoscape elements (read from manifest)
  - **Hover → enlarge**: Use Cytoscape `mouseover`/`mouseout` events to scale node (e.g., `ele.style('width', '80px')` on hover, revert on mouseout)
  - **Click → info**: Use Cytoscape `tap` event on node to trigger the existing detail/info overlay (reuse the card click handler from `app.js` if available, or dispatch a custom event)
  - **Edges stay as-is**: The 1583 existing edges already represent relationships between artifacts — these become photo-to-photo relationships automatically when nodes show photos
  - Add fallback for nodes without image_url: show text label instead

  **Must NOT do**:
  - Do NOT add new edge types or relationship logic — existing edges ARE the photo-to-photo relationships
  - Do NOT add a separate photo graph — enhance the existing graph
  - Do NOT add lightbox or modal for enlarged view — just CSS/Cytoscape scale on hover
  - Do NOT create new files — modify `docs/graph.js` and optionally `docs/style.css` for hover tooltip CSS

  **Recommended Agent Profile**:
  - **Subagent Type**: `explore` (Cytoscape.js API usage, single file focus)
  - **Skills**: [`browse`]
    - `browse`: Needed to verify graph renders with images, hover/click interactions work

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Task 4)
  - **Blocks**: Task 6 (push)
  - **Blocked By**: Task 3 (needs manifest with image_url for node data)

  **References**:
  - `docs/graph.js` (111 lines) — Current Cytoscape.js module, CoSE layout, 64 nodes, 1583 edges
  - `docs/app.js` — Card click handler / detail overlay (reuse for node click → info)
  - `docs/manifest.json` — After Task 3, contains `image_url` per artifact
  - Cytoscape.js docs: `background-image` node style — https://js.cytoscape.org/#style/background-image
  - Cytoscape.js docs: events — https://js.cytoscape.org/#events
  - `docs/style.css` — May need minor additions for hover tooltip if using HTML overlay

  **QA Scenarios**:
  ```
  Scenario: Graph nodes display artifact photos (happy path)
    Tool: Playwright (browse skill)
    Preconditions: Local server running, manifest with image_url (Task 3), graph view active
    Steps:
      1. Navigate to localhost:8000
      2. Switch to graph view (click graph tab/button if needed)
      3. Wait for Cytoscape canvas to render (wait for `#cy` or `.cytoscape-container`)
      4. Evaluate: cy.nodes().length → assert equals 64
      5. Evaluate: cy.nodes()[0].style('background-image') → assert contains "emuseum.go.kr"
      6. Screenshot the graph
    Expected Result: 64 nodes with artifact photos as backgrounds
    Failure Indicators: Nodes show text labels only, background-image empty, canvas blank
    Evidence: .sisyphus/evidence/task-5-graph-photo-nodes.png

  Scenario: Hover enlarges node photo
    Tool: Playwright (browse skill)
    Preconditions: Graph view active with photo nodes
    Steps:
      1. Get position of first node: cy.nodes()[0].renderedPosition()
      2. Get initial width: cy.nodes()[0].style('width')
      3. Mouse hover over node position on canvas
      4. Wait 500ms for animation
      5. Get new width: cy.nodes()[0].style('width')
      6. Assert: new width > initial width (node enlarged)
      7. Mouse move away from node
      8. Wait 500ms
      9. Assert: width returns to initial value
    Expected Result: Node enlarges on hover, returns to normal on mouseout
    Failure Indicators: No size change, node stays enlarged, JavaScript error
    Evidence: .sisyphus/evidence/task-5-hover-enlarge.png

  Scenario: Click node opens info overlay
    Tool: Playwright (browse skill)
    Preconditions: Graph view active with photo nodes
    Steps:
      1. Click on a graph node (via canvas coordinates or Cytoscape tap event)
      2. Wait 500ms for overlay/panel to appear
      3. Assert: detail panel/overlay is visible (check for `.artifact-detail`, `.modal`, or similar selector)
      4. Assert: panel shows artifact name matching the clicked node
    Expected Result: Clicking photo node shows artifact information
    Failure Indicators: No overlay appears, wrong artifact shown, JavaScript error
    Evidence: .sisyphus/evidence/task-5-click-info.png

  Scenario: Node without image_url shows text fallback
    Tool: Playwright (browse skill)
    Preconditions: At least one artifact lacks image_url (from Task 0b audit)
    Steps:
      1. Find node without background-image: cy.nodes().filter(n => !n.data('image_url'))
      2. Assert: node shows text label instead of image
      3. Assert: graph still renders without errors
    Expected Result: Graceful fallback to text label for imageless nodes
    Failure Indicators: Broken image icon in node, graph crashes, blank node
    Evidence: .sisyphus/evidence/task-5-text-fallback.png
  ```

  **Commit**: YES
  - Message: `feat: graph photo nodes with hover/click`
  - Files: `docs/graph.js`, `docs/style.css` (if hover CSS needed)
  - Pre-commit: Playwright confirms graph nodes show images

### Wave 3 — Deploy

- [x] 6. Push All Changes to origin/main

  **What to do**:
  - First push the 5 existing commits that are already ahead of origin/main
  - Then push the new commits from Tasks 1-5
  - Command: `git push origin main`
  - Verify: `git log origin/main..HEAD --oneline` returns empty (all pushed)
  - Verify: `git status` shows "Your branch is up to date with 'origin/main'"

  **Must NOT do**:
  - Do NOT force push (`--force`)
  - Do NOT update git config user.name or user.email
  - Do NOT rebase or squash existing commits
  - Do NOT create a new branch — push directly to main

  **Recommended Agent Profile**:
  - **Subagent Type**: `explore` (single git command)
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Sequential (Wave 3)
  - **Blocks**: F1-F4 (final verification)
  - **Blocked By**: Tasks 1, 2, 4, 5 (all implementation must be committed first)

  **References**:
  - Git log: 5 existing commits ahead of origin/main (from before this plan)
  - New commits from Tasks 1-5 (6 total new commits per Commit Strategy)

  **QA Scenarios**:
  ```
  Scenario: All commits pushed to remote (happy path)
    Tool: Bash
    Preconditions: All Tasks 1-5 committed
    Steps:
      1. git push origin main → assert exit code 0
      2. git log origin/main..HEAD --oneline → assert empty output
      3. git status → assert contains "up to date with 'origin/main'"
    Expected Result: All local commits pushed, local and remote in sync
    Failure Indicators: Push rejected, commits still ahead, auth error
    Evidence: .sisyphus/evidence/task-6-push-result.txt

  Scenario: GitHub Pages will serve updated site
    Tool: Bash
    Preconditions: Push successful
    Steps:
      1. git log origin/main --oneline -5 → verify latest commits are ours
      2. Assert: commit messages match our Commit Strategy (rename, feat: switch, feat: add, feat: render, feat: graph)
    Expected Result: Remote main has all our commits, GitHub Pages will auto-deploy
    Failure Indicators: Commits missing from remote, wrong branch
    Evidence: .sisyphus/evidence/task-6-remote-log.txt
  ```

  **Commit**: NO (this IS the push task)

---

## Final Verification Wave (MANDATORY — after ALL implementation tasks)

> 4 review agents run in PARALLEL. ALL must APPROVE. Present consolidated results to user and get explicit "okay" before completing.

- [ ] F1. **Plan Compliance Audit** — `oracle` (subagent_type)
  Read the plan end-to-end. For each "Must Have": verify implementation exists (read file, grep, Playwright). For each "Must NOT Have": search codebase for forbidden patterns — reject with file:line if found. Check evidence files exist in `.sisyphus/evidence/`. Compare deliverables against plan.
  Output: `Must Have [N/N] | Must NOT Have [N/N] | Tasks [N/N] | VERDICT: APPROVE/REJECT`

- [ ] F2. **Code Quality Review** — `unspecified-high` (subagent_type)
  Review all changed files (`docs/index.html`, `docs/404.html`, `docs/app.js`, `docs/manifest.json`, `pipeline/generate_graph.py`) for: empty catches, console.log in prod, commented-out code, unused imports. Check AI slop: excessive comments, over-abstraction, generic variable names. Vanilla JS — no build step to run.
  Output: `Files [N clean/N issues] | AI Slop [CLEAN/N issues] | VERDICT`

- [ ] F3. **Real Manual QA** — `unspecified-high` (subagent_type, + `browse` skill)
  Start from clean state. Open site locally (`file://` or local server). Execute EVERY QA scenario from EVERY task — follow exact steps, capture evidence. Test cross-task integration: rename + language toggle + photos all working together. Test mobile viewport. Save to `.sisyphus/evidence/final-qa/`.
  Output: `Scenarios [N/N pass] | Integration [N/N] | Edge Cases [N tested] | VERDICT`

- [ ] F4. **Scope Fidelity Check** — `deep` (subagent_type)
  For each task: read "What to do", read actual diff (`git diff`). Verify 1:1 — everything in spec was built (no missing), nothing beyond spec was built (no creep). Check "Must NOT do" compliance. Detect cross-task contamination. Flag unaccounted changes.
  Output: `Tasks [N/N compliant] | Contamination [CLEAN/N issues] | Unaccounted [CLEAN/N files] | VERDICT`

---

## Commit Strategy

| Order | Message | Files | Pre-commit |
|-------|---------|-------|------------|
| 1 | `rename: Museum as Code - National Museum of Korea` | `docs/index.html`, `docs/404.html` | `grep -r "디지털 국립중앙박물관" docs/` returns 0 |
| 2 | `feat: switch default language to English` | `docs/app.js`, `docs/index.html` | Playwright: page loads in English |
| 3 | `feat: add image_url to manifest pipeline` | `pipeline/generate_graph.py`, `docs/manifest.json` | `grep "image_url" docs/manifest.json \| head -3` shows URLs |
| 4 | `feat: render artifact photos in cards` | `docs/app.js` | Playwright: `.artifact-card img` elements exist |
| 5 | `feat: graph photo nodes with hover/click` | `docs/graph.js`, `docs/style.css` | Playwright: Cytoscape nodes show images, hover enlarges |
| 6 | `git push origin main` | — | `git status` shows up to date with remote |

---

## Success Criteria

### Verification Commands
```bash
grep -r "디지털 국립중앙박물관" docs/          # Expected: no output (0 matches)
grep "Museum as Code" docs/index.html        # Expected: matches in title + h1
grep "currentLang = 'en'" docs/app.js        # Expected: 1 match
grep "lang=\"en\"" docs/index.html            # Expected: 1 match  
grep -c "image_url" docs/manifest.json       # Expected: ~64 (one per artifact)
git log origin/main..HEAD --oneline          # Expected: no output (all pushed)
```

### Final Checklist
- [ ] All "Must Have" items present and verified
- [ ] All "Must NOT Have" items absent (no forbidden patterns)
- [ ] Site loads in English by default
- [ ] Language toggle works bidirectionally
- [ ] Artifact cards show photos
- [ ] Broken/missing images hidden gracefully
- [ ] All changes deployed to GitHub Pages
