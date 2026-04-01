
## 2026-03-31 Task: 0a
e-museum hotlinking status: **BLOCK**
HTTP status: 200 (server reachable, but returns error page)
Content-Type: text/html (NOT image/* — HTML error page returned instead of image)
Browser load: NOT POSSIBLE — text/html cannot render as image
Referrer spoofing: Tested with -e flag pointing to GitHub Pages — does NOT bypass block
Block type: Server-side referrer check or bot blocking that intercepts image requests and returns Korean error page ("서비스 이용에 불편을 드려 죄송합니다")
Notes: All 3 tested URLs (nb_001, nb_032/nb_287, nb_057/nb_531) return identical HTML error page (1920 bytes). This is a hard block — images cannot be hotlinked directly on museum-as-code GitHub Pages. Mitigation required: must use e-museum.go.kr's official embed API, OR download/cache images locally, OR use a proxy/caching layer.

## 2026-03-31 Task: 0a (VALIDATION COMPLETE)
e-museum hotlinking status: BLOCK
HTTP status: 200 (but Content-Type: text/html — error page, not image)
Content-Type: text/html (NOT image/* — server returns 1920-byte error HTML)
Browser load: naturalWidth=0, naturalHeight=0 (all 3 URLs confirmed)
Notes: Referrer spoofing (with -H "Referer: https://www.emuseum.go.kr/") does NOT bypass block. Block is session/cookie-based or server-side bot detection. Full evidence at: .sisyphus/evidence/task-0a-curl-headers.txt
Action: STOP — do not proceed with hotlinking-based image embedding. Must use local copy, proxy, or official embed API.

## 2026-04-01 F4 Scope Fidelity Audit Issues
- Task commit contamination detected: commits with task messages touched `.sisyphus/notepads/museum-site-update/learnings.md`, outside declared task file scopes.
- Task 2 scope bleed: `feat: switch default language to English` commit (`1ea704e`) modified `docs/404.html`, which was not in Task 2 declared scope (`docs/app.js`, `docs/index.html`).
- Task 6 not currently satisfied at HEAD: `git status -sb` shows `main...origin/main [ahead 1]`.


## 2026-04-01 Task: F2 (Code Quality Review)
Verdict: REJECT
Files reviewed: docs/index.html, docs/404.html, docs/app.js, docs/graph.js, docs/manifest.json, pipeline/manifest.py
Issue 1: docs/manifest.json contains duplicate artifact ids (nb_001 at lines 6/17, nb_006 at 50/61, nb_009 at 94/105). These are not safe as unique graph keys.
Issue 2: docs/graph.js maps images by artifact id (lines 13-16, 37-38), so duplicate ids overwrite earlier entries and can attach the wrong image to a node.
Issue 3: pipeline/manifest.py trusts sidecar id as the manifest id without a uniqueness check (lines 122-126), allowing invalid manifest output for downstream consumers keyed by id.
Minor AI slop: docs/app.js still has stale scaffold comments referencing T12/T13/T14 (lines 227-231, 268-271, 354-357, 471).

## 2026-04-01 Code quality review (F2)
- `docs/manifest.json`: duplicate artifact ids (`nb_001`, `nb_006`, `nb_009`) create non-unique keys for card/detail/hash/graph flows.
- `pipeline/manifest.py`: `_find_local_image_url` is unused dead code while `_load_artifact_entry()` duplicates a simpler image lookup path.
- `docs/graph.js`: manifest fetch failure is swallowed by `.catch(function () { return {}; })`, which hides data-loading problems.
- AI slop/task-residue comments remain in `docs/index.html` and `docs/app.js` (`T12`/`T13`/`T14` markers).

## 2026-04-01 Final Verification Remediation Issues
- Work-context conflict detected: remediation checklist requested editing `.sisyphus/plans/museum-site-update.md`, but orchestration guardrail marks plan files as read-only.

## 2026-04-01 Final Verification Wave Remediation Follow-up
- Duplicate manifest ids issue is resolved by pipeline-level deduplication and manifest regeneration.
- Stale `T12/T13/T14` scaffold-comment issue in `docs/app.js` is resolved (no matches).
