# Draft: Museum-as-Code UX Fix

## Requirements (confirmed)
- User complaint (Korean): "뭔 의도인지는 알겠는데 이게 무슨 용도가 있지? 그림도 없고 글씨도 잘 안보이는데. JSON note는 보이지도 않잖아. 글씨를 왜 배경색이랑 같게했어"
- Translation: "I get the intent but what use is this? No images and text is hard to read. JSON notes aren't even visible. Why is the text the same color as the background?"
- User triggered `[analyze-mode]` — wants analysis before fixes

## Research Findings

### CSS Color Analysis (`docs/style.css`)
- `--bg: #fafaf8` (page background — very light cream)
- `--card-bg: #ffffff` (card background — white)
- `--text: #2c2c2c` (body text — dark gray)
- Base contrast is fine (~16:1 ratio), BUT:
- **Duplicate `.detail-code` definitions** at lines 128-135 and 266-278 (cascade conflict)
- First: `color: #d8f2ff` on `background: #111826` (light-on-dark)
- Second (wins): `background: #f5f3ef; color` not explicitly set → inherits or conflicts
- **Card skeleton animation**: `.card-skeleton { opacity: 0 }` — cards start invisible
- Cards only become visible when `IntersectionObserver` fires `.visible { opacity: 1 }`
- If observer doesn't trigger (e.g., all cards in viewport at once), cards may stay invisible

### No Images in Cards (`docs/app.js` lines 286-335)
- `renderCards()` creates: title, subtitle, designation, period — TEXT ONLY
- NO `<img>` element is ever created
- CSS has `.artifact-card img { width: 100%; height: 200px; object-fit: cover; }` but nothing targets it
- **Image data EXISTS**: Sidecar JSON has `image_url` field (e.g., `https://www.emuseum.go.kr/images/relic/11/0001.jpg`)
- But `manifest.json` does NOT include `image_url` — only `name_ko`, `name_en`, `period`, `designation`
- Images would need to be either added to manifest OR fetched from sidecar at card-render time

### JSON Notes Not Visible
- Detail view (`renderDetailContent`, lines 183-225) renders:
  - Korean/English name
  - Metadata list (era, material, size, location, designation)
  - HGL source code in `<pre><code class="detail-code">`
  - Description paragraphs
  - Drama connection (KDH items only)
- The "JSON notes" the user refers to are likely the sidecar metadata — these ARE rendered in the detail view
- But the detail view only opens on card click, and if cards are invisible, user can't reach it
- Also: `description` and `description_en` fields from sidecar may be rendered but could be empty for some artifacts

### Data Structure
- **Manifest** (`docs/manifest.json`): 64 artifacts, fields: `id`, `collection`, `hgl_path`, `json_path`, `name_ko`, `name_en`, `period`, `designation`
- **Sidecar JSON** (e.g., `nb_001.json`): `id`, `name`, `name_en`, `designation`, `era`, `material`, `size`, `location`, `description`, `image_url`, `hgl_file`, `source`
- **KDH sidecar** (e.g., `kdh_001.json`): Same + `drama_connection: { ko, en }`
- **HGL files**: Korean DSL source code (struct + function definitions) — displayed as code block

### Technical Stack
- Pure static HTML/CSS/JS — no build system, no framework
- Deployed to GitHub Pages at `xodn348.github.io/museum-as-code/`
- No test infrastructure exists
- Files: `docs/index.html`, `docs/style.css`, `docs/app.js`, `docs/manifest.json`

## Identified Issues (Priority Order)

1. **CRITICAL — Cards may be invisible**: `card-skeleton` starts at `opacity: 0`, relies on IntersectionObserver. If observer doesn't fire properly, all 64 cards stay invisible.
2. **HIGH — No images on cards**: `renderCards()` never creates `<img>` elements. Image URLs exist in sidecar JSON but not in manifest.
3. **HIGH — CSS duplicate definitions**: `.detail-code` defined twice with conflicting styles.
4. **MEDIUM — No font loaded**: `font-family: 'Noto Sans KR'` referenced but no Google Fonts link in `<head>`.
5. **MEDIUM — Detail view accessibility**: HGL code shown raw without syntax highlighting.

## User Decisions (Round 1)

### Scope: Full redesign with tree view + tabs
- User: "트리 구조로 보여주는것도 없잖아. 문화재끼리의 연관성을 트리로 보여주라니까. 트리를 먼저 보여주고 지금의 인덱스들은 따로 탭을 만들어서 보여주는거 어때?"
- Translation: "There's no tree structure. Show relationships between artifacts as a tree. Show tree first, put current index in a separate tab."
- **Decision**: Tree view as PRIMARY tab (default), Card grid as SECONDARY tab
- **Decision**: Images = Direct eMuseum URLs with fallback placeholder

### Data Analysis for Tree Structure
- **Manifest fields** (available without fetch): `collection`, `period`, `designation`
- **Sidecar fields** (require per-artifact fetch): `category`, `material`, `location`, `era`, `drama_connection`
- **Collections**: 2 — `national-treasures` (57 items), `kdh` (7 items, drama-linked)
- **Periods observed**: 조선시대, 통일신라시대, 삼국시대, etc.
- **NO explicit relationship data** — no parent/child, no related_to fields
- Tree must be DERIVED from shared attributes (period, category, material, location)
- KDH items have unique `drama_connection` field — special relationship axis

### Data Quality Issues
- Duplicate IDs in manifest: `nb_001` appears twice, `nb_006` twice, `nb_009` twice
- Need deduplication or unique key strategy

## User Decisions (Round 2)

### Tree Structure: 복합 트리 (탭 전환)
- User chose: ALL THREE tree views with sub-tab switching
- **시대별 (By Era)**: Period → Category → Artifact
- **카테고리별 (By Category)**: Category → Period → Artifact
- **지역별 (By Location)**: Location → Period → Artifact
- Sub-tabs within the Tree tab to switch between the three views
- Requires fetching ALL 64 sidecar JSONs at startup to extract `category`, `location`, `era` fields

### Test Strategy
- **Infrastructure exists**: NO
- **Automated tests**: NO
- **Agent-Executed QA**: YES (Playwright for UI verification)

## Open Questions
- NONE — all requirements clear

## Scope Boundaries
- INCLUDE: Fix all visibility bugs, add images to cards, build tree view, add tab navigation, fix CSS conflicts, add Google Fonts
- EXCLUDE: New data collection, backend/API changes, new artifact creation, HGL syntax highlighting
- CONSTRAINT: Pure static site (no build system, no framework)
