# Phase C Worktree Execution Plan — Hero Artifacts × 10

**Created:** 2026-04-29
**Mode:** Codex worktree fanout, 6 visible iTerm lanes
**Source plan:** `plans/2026-04-29-redesign-c-b-a.md`
**C1 baseline:** `plans/hero-artifacts.md`

## Execution assumption

The latest user instruction says to continue with Codex, plan the whole effort, and execute in worktrees with maximum subagents. Therefore the C1 recommended defaults are treated as approved for implementation unless later corrected:

- Use **10** hero artifacts, not 12.
- Use **National Treasure No. 83** for the pensive bodhisattva.
- Use **National Treasure No. 310** for the moon jar.
- Treat **Danwon Genre Album** as one hero slot with representative paintings inside the page.
- Use semantic IDs such as `hero_pensive_bodhisattva`.

## Non-negotiable constraints

1. Do not hotlink museum/media images in production pages. Images must be local under `docs/images/heroes/<id>/` with source/license metadata.
2. Do not fabricate metadata, dimensions, licenses, or official English titles. If source verification or download is blocked, leave a clear `needs_verification` marker and report `blocked` or partial work.
3. Keep existing fallback 57-item collection intact except where the entry page intentionally adds a new Featured Heroes section/tab.
4. Workers must not push, create PRs, deploy, or publish. Local commits only.
5. Workers are not alone in the codebase: each lane owns a disjoint write surface and must not revert unrelated edits.

## Target file structure

```text
artifacts/heroes/<hero_id>.md          # English curator copy + frontmatter
artifacts/heroes/<hero_id>.hgl         # cleaned Han source
artifacts/heroes/<hero_id>.json        # source-of-truth sidecar for repo

docs/data/heroes/index.json            # web manifest for 10 heroes
docs/data/heroes/<hero_id>.json        # web-consumable copy of sidecar/copy pointers
docs/images/heroes/<hero_id>/...       # local image(s) + image-sources.json

docs/hero.html
docs/hero.css
docs/hero.js
```

## Parallel lanes

| Lane | Branch | Ownership | Goal |
| --- | --- | --- | --- |
| `planning-source` | `phase-c/planning-source` | `plans/hero-artifacts.md`, `plans/hero-source-matrix.md`, `docs/data/heroes/index.json` | Finalize C1 defaults, document source/license candidates, create web manifest skeleton for all 10 heroes. |
| `content-sculpture-metal` | `phase-c/content-sculpture-metal` | `artifacts/heroes/*`, `docs/data/heroes/*`, `docs/images/heroes/*` only for `hero_pensive_bodhisattva`, `hero_baekje_incense_burner`, `hero_divine_bell` | C2–C4 for Buddhist sculpture / Baekje metalwork / Silla bell. |
| `content-ceramics-gold` | `phase-c/content-ceramics-gold` | same per-artifact surfaces for `hero_celadon_maebyeong`, `hero_moon_jar`, `hero_silla_gold_crown` | C2–C4 for celadon, moon jar, Silla crown. |
| `content-records-painting` | `phase-c/content-records-painting` | same per-artifact surfaces for `hero_hunminjeongeum`, `hero_tripitaka`, `hero_celestial_chart`, `hero_genre_album` | C2–C4 for records, astronomy, and painting. |
| `immersive-page` | `phase-c/immersive-page` | `docs/hero.html`, `docs/hero.css`, `docs/hero.js` | Build the standalone immersive hero detail page that consumes `docs/data/heroes/index.json` + per-hero JSON. |
| `featured-entry-qa` | `phase-c/featured-entry-qa` | `docs/index.html`, `docs/app.js`, `docs/style.css`, optional validation script under `pipeline/` | Make Featured Artifacts the first screen and add lightweight validation for hero manifest/local images. |

## Merge/integration order after workers report

1. Merge `planning-source` first to establish manifest/index conventions.
2. Merge content lanes; resolve only additive conflicts in `docs/data/heroes/index.json` if they occur.
3. Merge `immersive-page`.
4. Merge `featured-entry-qa` last because it touches existing entry files.
5. Run final verification from main checkout:
   - JSON parse for all `artifacts/heroes/*.json` and `docs/data/heroes/*.json`.
   - Static link/file existence check for hero image paths.
   - Start `python3 -m http.server --directory docs` and smoke-test `/`, `/hero.html`, and representative `?id=...` URLs if browser tooling is available.

## Definition of done for Phase C in this fanout

- 10 selected heroes are represented in data and UI.
- At least one verified local image per hero, or an explicit `needs_verification` blocker if network/license prevents safe inclusion.
- English copy exists in the 3-section structure: `Why this matters`, `What you're looking at`, `The story`.
- `.hgl` source exists for all 10 hero artifacts and is syntax-highlightable by the page.
- Entry page opens on Featured Artifacts, not Graph.
- Local verification evidence is recorded in worker reports and final main-session summary.
