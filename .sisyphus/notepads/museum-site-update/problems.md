## 2026-03-31 Task: 0a — BLOCKER: e-museum.go.kr Hotlinking BLOCKED

**Status**: ESCALATED TO USER — plan execution halted pending decision

**Block Type**: Server-side session/bot detection anti-hotlinking

**Evidence** (full details in `.sisyphus/evidence/task-0a-curl-headers.txt`):
- All 3 tested URLs return `HTTP 200` but with `Content-Type: text/html` (1920-byte error page)
- Error message: "존재하지 않는 페이지거나, 오류로 인하여 현재 페이지를 볼 수 없습니다"
- Adding `Referer: https://www.emuseum.go.kr/` header does NOT bypass the block
- Browser Playwright test: `naturalWidth=0`, `naturalHeight=0` — image does not render
- Tested URLs: nb_001 (0001.jpg), nb_287 (0287.jpg), nb_531 (0531.jpg)

**Blocked Tasks**:
- Task 3: pipeline/manifest.py image_url field addition (can still do pipeline change, but images won't load)
- Task 4: Render artifact photos in cards (requires working image URLs)
- Task 5: Graph photo nodes (requires working image URLs)

**Unblocked Tasks** (can still proceed independently):
- Task 1: Rename site in docs/index.html and docs/404.html
- Task 2: Switch default language to English in docs/app.js

**Options for User Decision**:
A. Skip Tasks 3/4/5 entirely — ship without photos for now
B. Download/commit images locally to docs/images/ in the repo (~57 images, ~10-50MB)
C. Set up a CORS proxy or image CDN (GitHub Actions workflow to cache images)
D. Use e-museum.go.kr embed page (iframe), not direct img hotlinks
E. Find alternative public image source for these artifacts

## 2026-04-01 F4 Scope Fidelity Audit — Open Problems
- Plan-task sequence is not cleanly reconstructable as 1 commit per task due to duplicate task commits (`rename`, `switch default language`, `render cards`, `graph photo nodes`).
- 60 changed files in the audited range are unaccounted for by Task 1-6 scope (mostly `docs/images/artifacts/*.jpg`, `pipeline/download_images.py`, and Sisyphus artifacts).
- Guardrail conflict unresolved: plan says direct external image usage only (no local copies/proxy), but execution introduced local image download workflow and local image paths in manifest.

## 2026-04-01 Final Verification Remediation — Open Problem
- Plan file mutability conflict remains: task checklist requested checkbox updates in `.sisyphus/plans/museum-site-update.md`, but orchestration rule declares plan files read-only.
