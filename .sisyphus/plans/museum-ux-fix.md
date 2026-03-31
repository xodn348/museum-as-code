# Museum-as-Code UX Transformation

## TL;DR

> **Quick Summary**: Transform the museum-as-code static site from a broken card grid into a dual-view app (Tree View primary + Card Grid secondary), fix all visibility bugs, add artifact images, and enrich the manifest with tree-building data.
> 
> **Deliverables**:
> - Fixed CSS (no duplicate declarations, proper code block styling)
> - Enriched `docs/manifest.json` (image_url, category, location fields + deduplicated IDs)
> - Artifact images on all cards via eMuseum URLs with fallback
> - Dual-tab layout: Tree View (default) / Card Grid
> - Triple sub-tab tree view: 시대별 / 카테고리별 / 지역별
> - Google Fonts loaded, site title updated to "Museum as Code - 국립중앙 박물관"
> 
> **Estimated Effort**: Medium
> **Parallel Execution**: YES - 4 waves
> **Critical Path**: Task 1 → Task 3 → Task 5 → Task 6

---

## Context

### Original Request
User complained (Korean): "뭔 의도인지는 알겠는데 이게 무슨 용도가 있지? 그림도 없고 글씨도 잘 안보이는데. JSON note는 보이지도 않잖아. 글씨를 왜 배경색이랑 같게했어"

Translation: "I get the intent but what use is this? No images, text is hard to read, JSON notes aren't visible, why is text the same color as background?"

User then expanded scope: wants tree view showing artifact relationships as the PRIMARY view, with card grid moved to a secondary tab.

### Interview Summary
**Key Discussions**:
- **Tree structure**: User chose 복합 트리 (탭 전환) — ALL THREE tree views (시대별/카테고리별/지역별) with sub-tab switching
- **Image strategy**: Direct eMuseum URLs with CSS fallback placeholder on error
- **Tab layout**: Tree View as PRIMARY (default) tab, Card Grid as SECONDARY tab
- **Title**: "Museum as Code - 국립중앙 박물관" (NOT "디지털 국립중앙박물관" — user explicitly stated they're not the official site)
- **Data approach**: Enrich `docs/manifest.json` with fields from sidecar JSONs (avoids 64 runtime fetches)

**Research Findings**:
- CSS has duplicate declarations for `.detail-code`, `.detail-name-ko`, `.detail-name-en`, `.detail-meta`, `.detail-meta li` (lines 92-135 vs 233-278)
- `renderCards()` in app.js creates NO `<img>` elements despite CSS `.artifact-card img` existing
- Manifest has 3 duplicate ID pairs: nb_001, nb_006, nb_009
- Sidecar JSONs contain `image_url`, `category`, `era`, `location` fields needed for tree building
- `fetchWithFallback()` path resolution is critical for GitHub Pages — don't break it

### Metis Review
**Identified Gaps** (addressed):
- **Manifest enrichment strategy**: Metis recommended adding `image_url`, `category`, `location` directly to `docs/manifest.json` instead of 64 runtime sidecar fetches → adopted as Task 1
- **CSS scope broader than expected**: Not just `.detail-code` but also `.detail-name-ko`, `.detail-name-en`, `.detail-meta` have duplicates → included in Task 2
- **Duplicate ID handling**: 3 pairs confirmed (nb_001, nb_006, nb_009) — second entry in each pair needs correct ID based on actual artifact designation
- **eMuseum URL reliability**: Unvalidated — fallback must be robust (`onerror` → hide image, show placeholder)
- **Missing fields in some sidecars**: Some artifacts may lack `category` or `location` — group as "기타" (Other)
- **fetchWithFallback must not be broken**: GitHub Pages path resolution depends on the `./` then `../` fallback pattern

---

## Work Objectives

### Core Objective
Transform the museum-as-code site into a usable dual-view application with working visibility, images, and artifact relationship trees.

### Concrete Deliverables
- `docs/manifest.json` — enriched with `image_url`, `category`, `location` fields; duplicate IDs fixed
- `docs/style.css` — duplicate CSS declarations removed; clean single-source styles
- `docs/index.html` — Google Fonts link added; title updated; dual-tab HTML structure; tree view sub-tabs
- `docs/app.js` — image rendering in cards; tab switching logic; tree view rendering with 3 grouping modes

### Definition of Done
- [ ] All 64 artifact cards render visibly with images (or graceful fallback)
- [ ] `.detail-code` block shows light text on dark background in detail overlay
- [ ] Tree View tab is default, showing collapsible artifact groups
- [ ] All 3 sub-tabs (시대별/카테고리별/지역별) switch tree grouping correctly
- [ ] Card Grid tab shows the existing card index (fixed)
- [ ] No duplicate IDs in manifest
- [ ] Google Fonts loads successfully
- [ ] Site title reads "Museum as Code - 국립중앙 박물관"

### Must Have
- Tree View as default/primary tab
- All 3 tree grouping axes (era, category, location) via sub-tabs
- Artifact images on cards from eMuseum URLs
- Fixed CSS — no invisible text, no duplicate declarations
- Clicking tree leaf or card opens same `#artifact-detail` overlay
- Google Fonts for Noto Sans KR (weights 400, 600, 700)

### Must NOT Have (Guardrails)
- DO NOT modify files under `artifacts/` or `pipeline/`
- DO NOT add npm dependencies, build tools, or bundlers
- DO NOT create separate JS/CSS files — keep single `app.js` + `style.css`
- DO NOT add search/filter within tree view
- DO NOT add animations for tab switching or tree expand/collapse
- DO NOT normalize era names or merge categories — use raw sidecar values
- DO NOT add hash-based URL routing for tabs (hash stays for artifact detail only)
- DO NOT refactor app.js into ES modules
- DO NOT use innerHTML for dynamic content — follow existing createElement pattern
- DO NOT add loading spinners or skeleton UIs beyond existing pattern
- DO NOT break `fetchWithFallback()` path resolution (critical for GitHub Pages)

---

## Verification Strategy (MANDATORY)

> **ZERO HUMAN INTERVENTION** — ALL verification is agent-executed. No exceptions.

### Test Decision
- **Infrastructure exists**: NO
- **Automated tests**: None
- **Framework**: none
- **QA**: Agent-executed via Playwright headless browser

### QA Policy
Every task MUST include agent-executed QA scenarios.
Evidence saved to `.sisyphus/evidence/task-{N}-{scenario-slug}.{ext}`.

- **Frontend/UI**: Use `browse` skill — Navigate to local/deployed site, interact, assert DOM, screenshot
- **Data validation**: Use Bash with `jq` — Validate manifest JSON structure and constraints

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Start Immediately — data + CSS foundation, PARALLEL):
├── Task 1: Enrich docs/manifest.json + fix duplicate IDs [unspecified-high]
└── Task 2: Fix CSS duplicates + Google Fonts + title update [quick]

Wave 2 (After Wave 1 — images + tab layout, PARALLEL):
├── Task 3: Add images to card rendering (depends: 1) [quick]
└── Task 4: Build dual-tab layout structure (depends: 1, 2) [visual-engineering]

Wave 3 (After Wave 2 — tree view implementation):
└── Task 5: Implement triple tree view with sub-tabs (depends: 1, 4) [unspecified-high]

Wave FINAL (After ALL tasks — verification):
├── Task F1: Plan compliance audit (oracle)
├── Task F2: Code quality review (unspecified-high)
├── Task F3: Full QA sweep (unspecified-high + browse skill)
└── Task F4: Scope fidelity check (deep)
→ Present results → Get explicit user okay
```

### Dependency Matrix

| Task | Blocked By | Blocks |
|------|-----------|--------|
| **1** | None | 3, 4, 5 |
| **2** | None | 4 |
| **3** | 1 | F1-F4 |
| **4** | 1, 2 | 5 |
| **5** | 1, 4 | F1-F4 |
| **F1-F4** | 3, 5 | None |

### Agent Dispatch Summary

- **Wave 1**: 2 tasks — T1 → `unspecified-high`, T2 → `quick`
- **Wave 2**: 2 tasks — T3 → `quick`, T4 → `visual-engineering`
- **Wave 3**: 1 task — T5 → `unspecified-high`
- **FINAL**: 4 tasks — F1 → `oracle`, F2 → `unspecified-high`, F3 → `unspecified-high` + `browse`, F4 → `deep`

---

## TODOs

---

## Final Verification Wave (MANDATORY — after ALL implementation tasks)

> 4 review agents run in PARALLEL. ALL must APPROVE. Present consolidated results to user and get explicit "okay" before completing.

- [ ] F1. **Plan Compliance Audit** — `oracle`
  Read the plan end-to-end. For each "Must Have": verify implementation exists (read file, check DOM). For each "Must NOT Have": search codebase for forbidden patterns — reject with file:line if found. Check evidence files exist in `.sisyphus/evidence/`. Compare deliverables against plan.
  Output: `Must Have [N/N] | Must NOT Have [N/N] | Tasks [N/N] | VERDICT: APPROVE/REJECT`

- [ ] F2. **Code Quality Review** — `unspecified-high`
  Review all changed files (`docs/index.html`, `docs/style.css`, `docs/app.js`, `docs/manifest.json`) for: empty catches, console.log in prod, commented-out code, unused CSS rules. Check AI slop: excessive comments, over-abstraction, generic names. Verify no duplicate CSS declarations remain.
  Output: `Files [N clean/N issues] | VERDICT`

- [ ] F3. **Full QA Sweep** — `unspecified-high` + `browse` skill
  Start from clean state. Open site in headless browser. Execute EVERY QA scenario from EVERY task — follow exact steps, capture evidence. Test cross-task integration: card click → detail, tree click → detail, tab switch → state preserved, sub-tab switch → tree re-render. Test edge cases: rapid tab switching, artifact with missing image. Save to `.sisyphus/evidence/final-qa/`.
  Output: `Scenarios [N/N pass] | Integration [N/N] | Edge Cases [N tested] | VERDICT`

- [ ] F4. **Scope Fidelity Check** — `deep`
  For each task: read "What to do", read actual diff. Verify: everything in spec was built, nothing beyond spec was built. Check "Must NOT do" compliance. Detect cross-task contamination. Flag unaccounted changes.
  Output: `Tasks [N/N compliant] | Contamination [CLEAN/N issues] | VERDICT`

---

## Commit Strategy

- **After Task 1**: `fix(data): deduplicate manifest IDs + enrich with image/category/location`
  - Files: `docs/manifest.json`
- **After Task 2**: `fix(css): remove duplicate declarations + add Google Fonts + update title`
  - Files: `docs/style.css`, `docs/index.html`
- **After Task 3**: `feat(cards): add artifact images from eMuseum URLs`
  - Files: `docs/app.js`
- **After Task 4**: `feat(ui): add dual-tab layout (tree view + card grid)`
  - Files: `docs/index.html`, `docs/style.css`, `docs/app.js`
- **After Task 5**: `feat(tree): implement triple tree view with era/category/location sub-tabs`
  - Files: `docs/app.js`, `docs/style.css`, `docs/index.html`

---

## Success Criteria

### Verification Commands
```bash
# No duplicate IDs in manifest
jq '[.artifacts[].id] | group_by(.) | map(select(length > 1)) | length' docs/manifest.json  # Expected: 0

# All artifacts have image_url
jq '[.artifacts[] | select(.image_url == null or .image_url == "")] | length' docs/manifest.json  # Expected: 0

# All artifacts have category
jq '[.artifacts[] | select(.category == null or .category == "")] | length' docs/manifest.json  # Expected: 0 (or small number with "기타")

# No duplicate CSS declarations
grep -c "detail-code" docs/style.css  # Expected: 1 (single rule block)

# Google Fonts link exists
grep -c "fonts.googleapis" docs/index.html  # Expected: 1

# Title updated
grep "Museum as Code" docs/index.html  # Expected: match
```

### Final Checklist
- [ ] All "Must Have" present and verified
- [ ] All "Must NOT Have" absent and verified
- [ ] All 5 implementation tasks completed with evidence
- [ ] Final verification wave (F1-F4) all APPROVE
- [ ] User explicitly okayed completion
