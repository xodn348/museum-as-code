# Museum Graph Visualization

## TL;DR

> **Quick Summary**: Add interactive Cytoscape.js force-directed graph as the PRIMARY view for 64 Korean national treasure artifacts, with edges connecting artifacts sharing era, category, location, or material. Existing card grid becomes a secondary tab.
> 
> **Deliverables**:
> - `pipeline/generate_graph.py` — Python script generating Cytoscape-compatible graph JSON from sidecar metadata
> - `docs/data/graph.json` — Generated graph data (64 nodes, ~200-600 edges)
> - `docs/graph.js` — Cytoscape.js graph rendering module with CoSE layout + edge filtering
> - `docs/index.html` — Updated with tab navigation (Graph/Cards) + Cytoscape CDN + graph container
> - `docs/style.css` — Extended with tab, graph container, and filter panel styles
> - `docs/app.js` — Minimal changes for tab-switching hooks
> 
> **Estimated Effort**: Medium
> **Parallel Execution**: YES — 3 waves + Final Verification
> **Critical Path**: Task 1 → Task 3 → Task 4 → Task 5 → F1-F4

---

## Context

### Original Request
"그래프로 표현하는것도 하자" — User wants to add interactive graph visualization to the museum-as-code project. Graph should be the primary landing view, with the existing card grid as a secondary tab.

### Interview Summary
**Key Discussions**:
- **Graph type**: Force-directed network (nodes = artifacts, edges = shared attributes)
- **Edge types**: ALL 4 — same era, same category, same location, same material (with toggle filters)
- **Integration**: Graph becomes PRIMARY view (user: "그래프로 먼저 보여주고 인덱스는 그냥 다른탭으로")
- **Library**: Cytoscape.js (CSS-like styling, CoSE layout, good for 50-100 nodes)
- **Test strategy**: No unit tests. Agent QA only (Playwright for browser verification)
- **Data flow**: Python pipeline generates graph JSON → Cytoscape.js renders in browser

**Research Findings**:
- 64 artifacts: 57 national treasures (nb_001~057) + 7 KDH special collection
- Sidecar JSON fields: `era`, `category` (sometimes missing on KDH), `material` (comma-separated multi-value), `location`
- Era values not normalized: "삼국시대 (6-7세기)" vs "조선시대" — needs normalization
- manifest.json has `period` but sidecars have `era` — graph generator must read full sidecar files
- Existing app.js: 465 lines vanilla JS, card grid + detail overlay, hash navigation
- No npm/bundling — vanilla JS via `<script>` tags
- Cytoscape.js: Pin v3.33.1 via CDN, CoSE layout with `nodeRepulsion: 6000`, `animate: false`

### Metis Review
**Identified Gaps** (addressed):
- **Edge explosion**: 40+ artifacts from same era → 780+ era edges alone. Default to only "category" edge type checked.
- **Multi-value material splitting**: "석재, 목재" must be split on "," for individual matching
- **Era normalization**: Strip parenthetical suffixes to canonical era groups
- **Missing `category` on KDH sidecars**: Python script handles gracefully (skip that dimension, log warning)
- **Lazy initialization**: Don't init Cytoscape on page load — only on first Graph tab click
- **Cytoscape instance lifecycle**: Keep alive across tab switches (hide container, don't destroy)
- **`#cy` container height**: Must have explicit CSS height or graph renders invisible
- **Hash navigation preservation**: `#artifact-{id}` deep linking must work from both tabs

---

## Work Objectives

### Core Objective
Add an interactive force-directed graph visualization as the primary landing page view, allowing users to explore relationships between 64 Korean national treasure artifacts by era, category, location, and material — while preserving the existing card grid as a secondary tab.

### Concrete Deliverables
- `pipeline/generate_graph.py` — Reads 64 sidecar JSONs, outputs `docs/data/graph.json`
- `docs/data/graph.json` — Cytoscape-compatible JSON with 64 nodes + computed edges
- `docs/graph.js` — Cytoscape.js initialization, layout, styling, event handling, edge filtering
- `docs/index.html` — Tab bar, `#cy` container, edge filter panel, Cytoscape CDN script
- `docs/style.css` — Tab styles, `#cy` height, filter panel, responsive adjustments
- `docs/app.js` — Minimal tab-switching logic added (NOT refactored)

### Definition of Done
- [ ] `python pipeline/generate_graph.py` produces `docs/data/graph.json` with exactly 64 nodes
- [ ] Edge count is between 50 and 2000 (not 0, not explosive)
- [ ] Graph tab shows interactive force-directed graph on page load
- [ ] Cards tab shows existing card grid (all 64 cards)
- [ ] Edge filter checkboxes toggle visibility of each edge type
- [ ] Node click opens existing detail overlay with correct artifact data
- [ ] `#artifact-{id}` hash navigation still works
- [ ] Mobile viewport (375×667) renders graph with non-zero dimensions
- [ ] Language toggle (ko/en) works on graph node labels

### Must Have
- Graph as PRIMARY tab (shown by default on page load)
- All 4 edge types (era, category, location, material) with checkbox filters
- Default: only "category" (분류) checkbox checked on load (prevents edge explosion)
- Node click → existing `showDetail(artifactId)` overlay
- Tab navigation: 그래프 (Graph) | 카드 (Cards)
- Cytoscape.js v3.33.1 via CDN (pinned)
- Python graph generator as separate script (`pipeline/generate_graph.py`)
- Era normalization in Python script (strip parenthetical suffixes)
- Multi-value material splitting on `","`
- Graceful handling of missing `category`/`era` fields in sidecar JSONs
- Lazy Cytoscape initialization (first Graph tab click only)
- `[data-lang]` support for graph node labels (ko/en toggle)

### Must NOT Have (Guardrails)
- Do NOT refactor `app.js` — only add minimal tab-switching hooks
- Do NOT add npm, webpack, vite, or any bundler
- Do NOT add a CSS framework — extend existing `style.css` custom properties
- Do NOT modify `pipeline/manifest.py` — graph generator is a separate script
- Do NOT break existing `#artifact-{id}` hash navigation
- Do NOT add node tooltips, zoom controls, animated layout, or search in graph
- Do NOT add node sizing by degree, edge weight/thickness, or graph analytics
- Do NOT store duplicate artifact data in `graph.json` — only IDs, labels, edge connections
- Do NOT destroy/recreate Cytoscape instance on tab switch — hide container, keep instance alive
- Do NOT add excessive error handling to Python script (runs locally, not in production)

---

## Verification Strategy (MANDATORY)

> **ZERO HUMAN INTERVENTION** — ALL verification is agent-executed. No exceptions.

### Test Decision
- **Infrastructure exists**: NO
- **Automated tests**: None
- **Framework**: none
- **Agent-Executed QA**: YES — Playwright for all browser verification, Bash for Python script

### QA Policy
Every task MUST include agent-executed QA scenarios.
Evidence saved to `.sisyphus/evidence/task-{N}-{scenario-slug}.{ext}`.

- **Frontend/UI**: Use Playwright — Navigate, interact, assert DOM, screenshot
- **Pipeline/Script**: Use Bash — Run Python script, validate JSON output
- **Data validation**: Use Bash — Parse JSON, assert node/edge counts

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Start Immediately — no dependencies between them):
├── Task 1: Python Graph Data Generator [unspecified-high]
└── Task 2: Tab Navigation UI — HTML + CSS [visual-engineering]

Wave 2 (After Wave 1 — needs graph.json + tab UI):
├── Task 3: Graph.js — Cytoscape Integration Module [unspecified-high]
└── Task 4: Tab Switching + App.js Integration [unspecified-high]

Wave 3 (After Wave 2 — end-to-end verification):
└── Task 5: End-to-End QA + Polish [unspecified-high]

Wave FINAL (After ALL tasks — 4 parallel reviews, then user okay):
├── F1: Plan Compliance Audit (oracle)
├── F2: Code Quality Review (unspecified-high)
├── F3: Real Manual QA (unspecified-high + browse)
└── F4: Scope Fidelity Check (deep)
→ Present results → Get explicit user okay

Critical Path: Task 1 → Task 3 → Task 4 → Task 5 → F1-F4 → user okay
Parallel Speedup: ~50% faster than sequential
Max Concurrent: 2 (Waves 1 & 2)
```

### Dependency Matrix

| Task | Blocked By | Blocks |
|------|-----------|--------|
| **1** | — | 3, 4, 5 |
| **2** | — | 3, 4, 5 |
| **3** | 1, 2 | 4, 5 |
| **4** | 2, 3 | 5 |
| **5** | 3, 4 | F1-F4 |
| **F1-F4** | 5 | — |

### Agent Dispatch Summary

- **Wave 1** (2 tasks): T1 → `unspecified-high`, T2 → `visual-engineering`
- **Wave 2** (2 tasks): T3 → `unspecified-high`, T4 → `unspecified-high`
- **Wave 3** (1 task): T5 → `unspecified-high` + `browse`
- **FINAL** (4 tasks): F1 → `oracle`, F2 → `unspecified-high`, F3 → `unspecified-high` + `browse`, F4 → `deep`

---

## TODOs

> Implementation + Test = ONE Task. Never separate.
> EVERY task MUST have: Recommended Agent Profile + Parallelization info + QA Scenarios.

- [x] 1. Python Graph Data Generator (`pipeline/generate_graph.py` + `docs/data/graph.json`)

  **What to do**:
  - Create `pipeline/generate_graph.py` that:
    1. Walks `artifacts/national-treasures/nb_*.json` (57 files) and `artifacts/special/kdh/kdh_*.json` (7 files)
    2. For each sidecar JSON, extracts: `id`, `name` (ko + en), `era`, `category`, `material`, `location`
    3. **Era normalization**: Strip parenthetical suffixes — `"삼국시대 (6-7세기)"` → `"삼국시대"` using regex `re.sub(r'\s*\(.*?\)\s*$', '', era)`
    4. **Multi-value material splitting**: Split `material` field on `","` and strip whitespace — `"석재, 목재"` → `["석재", "목재"]`
    5. **Missing field handling**: If `category`, `era`, `material`, or `location` is missing/empty, skip that artifact for that dimension only (don't skip the whole artifact). Print warning to stderr: `"WARNING: {artifact_id} missing {field}"`
    6. Build **nodes array**: Each node = `{ "data": { "id": "{artifact_id}", "label_ko": "{name.ko}", "label_en": "{name.en}" } }`
    7. Build **edges array**: For each pair of artifacts sharing a normalized attribute value, create edge = `{ "data": { "source": "{id_a}", "target": "{id_b}", "type": "{era|category|location|material}", "value": "{shared_value}" } }`. Deduplicate: only create edge (a,b) where a < b alphabetically
    8. Output Cytoscape-compatible JSON: `{ "elements": { "nodes": [...], "edges": [...] } }`
    9. Write output to `docs/data/graph.json` (create `docs/data/` directory if not exists)
  - Script must use **stdlib only** — `json`, `os`, `re`, `glob`, `sys`. No pip dependencies.
  - Run the script to generate the initial `docs/data/graph.json`

  **Must NOT do**:
  - Do NOT use `networkx`, `pandas`, or any pip-installable library
  - Do NOT modify `pipeline/manifest.py` or any existing pipeline scripts
  - Do NOT store full artifact metadata in graph.json — only IDs, labels, edge connections
  - Do NOT add excessive error handling (try/except around every line) — simple if-checks suffice
  - Do NOT add argparse CLI — hardcode relative paths from project root

  **Recommended Agent Profile**:
  - **Subagent Type**: `unspecified-high`
    - Reason: Python script with data processing logic, not trivial but not architectural
  - **Skills**: `[]`
    - No special skills needed — standard Python file I/O and JSON processing
  - **Skills Evaluated but Omitted**:
    - `oracle`: Not needed — no debugging or architecture analysis
    - `librarian`: Not needed — stdlib-only, no external library docs required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Task 2)
  - **Blocks**: Tasks 3, 4, 5 (they need `docs/data/graph.json` to exist)
  - **Blocked By**: None (can start immediately)

  **References** (CRITICAL):

  **Pattern References** (existing code to follow):
  - `artifacts/national-treasures/nb_001.json` — Sample national treasure sidecar. Fields: `era: "조선시대"`, `material: "석재, 목재"`, `location: "서울특별시 종로구"`, `category: "유적건조물"`. Use this as the canonical field mapping.
  - `artifacts/special/kdh/kdh_001.json` — Sample KDH sidecar. Note: `era: "삼국시대 (6-7세기)"` (needs normalization), `material: "금동"`, `location: "국립중앙박물관"`, **NO `category` field** (must handle gracefully). Has `drama_connection` field — ignore it.
  - `pipeline/manifest.py` — Existing Python pipeline script. Follow same coding style (stdlib, simple functions, no classes). Do NOT modify this file — just match its conventions.

  **Data References** (schema to process):
  - `docs/manifest.json` — 64 artifact entries. Has `period` field but NOT `era/category/material/location`. Do NOT read this file — read individual sidecar JSONs instead. Only useful to verify you found all 64 artifacts.

  **External References**:
  - Cytoscape.js JSON format: `{ "elements": { "nodes": [{ "data": { "id": "..." } }], "edges": [{ "data": { "source": "...", "target": "...", ... } }] } }` — This is the exact output schema required.

  **WHY Each Reference Matters**:
  - `nb_001.json`: Shows the "happy path" sidecar with all fields present — use as template for field extraction
  - `kdh_001.json`: Shows edge cases — missing `category`, era needing normalization — test your missing-field handling against this
  - `manifest.json`: Cross-reference your node count against this (must be exactly 64)

  **Acceptance Criteria**:
  - [ ] `python pipeline/generate_graph.py` exits with code 0
  - [ ] `docs/data/graph.json` exists and is valid JSON
  - [ ] Node count is exactly 64 (verified by JSON parse)
  - [ ] Edge count is between 50 and 2000
  - [ ] Every edge has `type` field with value in `["era", "category", "location", "material"]`
  - [ ] Every edge has `value` field (the shared attribute value)
  - [ ] Every node has `label_ko` and `label_en` fields
  - [ ] No era value contains parenthetical suffixes (no `(` character in any era edge value)
  - [ ] Material edges use individual values (no `","` in any material edge value)

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: Happy path — generate graph.json from 64 sidecar files
    Tool: Bash
    Preconditions: Working directory is project root (`museum-as-code/`)
    Steps:
      1. Run `python pipeline/generate_graph.py`
      2. Assert exit code is 0
      3. Run `python3 -c "import json; d=json.load(open('docs/data/graph.json')); print(f'nodes:{len(d[\"elements\"][\"nodes\"])}, edges:{len(d[\"elements\"][\"edges\"])}')"`
      4. Assert output contains "nodes:64"
      5. Assert edge count N where 50 < N < 2000
    Expected Result: Script runs without errors, outputs JSON with exactly 64 nodes and reasonable edge count
    Failure Indicators: Non-zero exit code, node count ≠ 64, edge count 0 or >2000, JSON parse error
    Evidence: .sisyphus/evidence/task-1-generate-graph.txt

  Scenario: Era normalization — no parenthetical suffixes in output
    Tool: Bash
    Preconditions: `docs/data/graph.json` exists (from previous scenario)
    Steps:
      1. Run `python3 -c "import json; d=json.load(open('docs/data/graph.json')); era_edges=[e for e in d['elements']['edges'] if e['data']['type']=='era']; bad=[e for e in era_edges if '(' in e['data']['value']]; print(f'era_edges:{len(era_edges)}, bad:{len(bad)}'); assert len(bad)==0, f'Found unnormalized eras: {[e[\"data\"][\"value\"] for e in bad[:3]]}'"`
      2. Assert output shows `bad:0`
    Expected Result: Zero era edges contain parenthetical suffixes
    Failure Indicators: Any era edge value containing "(" character
    Evidence: .sisyphus/evidence/task-1-era-normalization.txt

  Scenario: Material splitting — no comma-separated values in edges
    Tool: Bash
    Preconditions: `docs/data/graph.json` exists
    Steps:
      1. Run `python3 -c "import json; d=json.load(open('docs/data/graph.json')); mat_edges=[e for e in d['elements']['edges'] if e['data']['type']=='material']; bad=[e for e in mat_edges if ',' in e['data']['value']]; print(f'material_edges:{len(mat_edges)}, bad:{len(bad)}'); assert len(bad)==0"`
      2. Assert output shows `bad:0`
    Expected Result: Zero material edges contain comma-separated values
    Failure Indicators: Any material edge value containing ","
    Evidence: .sisyphus/evidence/task-1-material-splitting.txt

  Scenario: Edge case — missing category field on KDH artifacts
    Tool: Bash
    Preconditions: `docs/data/graph.json` exists
    Steps:
      1. Run `python3 -c "import json; d=json.load(open('docs/data/graph.json')); cat_edges=[e for e in d['elements']['edges'] if e['data']['type']=='category']; kdh_in_cat=[e for e in cat_edges if 'kdh' in e['data']['source'] or 'kdh' in e['data']['target']]; print(f'category_edges:{len(cat_edges)}, kdh_in_category:{len(kdh_in_cat)}')"`
      2. Verify KDH artifacts are NOT in category edges (since they lack `category` field) — `kdh_in_category` should be 0 or very low
    Expected Result: KDH artifacts excluded from category edges (graceful skip, not crash)
    Failure Indicators: Script crashed on missing field, or KDH artifacts incorrectly included in category edges
    Evidence: .sisyphus/evidence/task-1-missing-category.txt
  ```

  **Evidence to Capture:**
  - [ ] `task-1-generate-graph.txt` — Full script output + node/edge counts
  - [ ] `task-1-era-normalization.txt` — Era edge validation output
  - [ ] `task-1-material-splitting.txt` — Material edge validation output
  - [ ] `task-1-missing-category.txt` — KDH category edge check output

  **Commit**: YES (C1)
  - Message: `feat(graph): add graph data generator for artifact relationships`
  - Files: `pipeline/generate_graph.py`, `docs/data/graph.json`
  - Pre-commit: `python pipeline/generate_graph.py && python3 -c "import json; d=json.load(open('docs/data/graph.json')); assert len(d['elements']['nodes'])==64"`

- [x] 2. Tab Navigation UI — HTML + CSS (`docs/index.html` + `docs/style.css`)

  **What to do**:
  - Edit `docs/index.html` to add:
    1. **Cytoscape.js CDN script** before existing `app.js` script: `<script src="https://cdnjs.cloudflare.com/ajax/libs/cytoscape/3.33.1/cytoscape.min.js"></script>`
    2. **Tab bar** inside `<main>` before `#card-grid`: Two buttons — `<button class="tab-btn active" data-tab="graph" data-lang-ko="그래프" data-lang-en="Graph">그래프</button>` and `<button class="tab-btn" data-tab="cards" data-lang-ko="카드" data-lang-en="Cards">카드</button>`
    3. **Graph container**: `<div id="cy" class="tab-content active"></div>` — placed before `#card-grid`
    4. **Edge filter panel** inside or adjacent to `#cy`: Checkboxes for 4 edge types — `<div id="edge-filters"><label><input type="checkbox" data-edge-type="category" checked> <span data-lang-ko="분류" data-lang-en="Category">분류</span></label><label><input type="checkbox" data-edge-type="era"> <span data-lang-ko="시대" data-lang-en="Era">시대</span></label><label><input type="checkbox" data-edge-type="location"> <span data-lang-ko="소장처" data-lang-en="Location">소장처</span></label><label><input type="checkbox" data-edge-type="material"> <span data-lang-ko="재질" data-lang-en="Material">재질</span></label></div>`
    5. **Only "category" checked by default** — other 3 unchecked
    6. Add `class="tab-content"` to `#card-grid` (initially hidden, shown when Cards tab clicked)
    7. **Script tag placeholder** for graph.js: `<script src="graph.js"></script>` after cytoscape CDN, before app.js
  - Edit `docs/style.css` to add:
    1. **Tab bar styles**: `.tab-bar` flex container, `.tab-btn` styling (border-bottom highlight for active), consistent with existing header aesthetic
    2. **`#cy` container**: `width: 100%; height: calc(100vh - 200px); min-height: 400px;` — CRITICAL: explicit height or Cytoscape renders invisible
    3. **Tab content visibility**: `.tab-content { display: none; }` and `.tab-content.active { display: block; }`
    4. **Edge filter panel**: `.edge-filters` positioned over graph (absolute or fixed), semi-transparent background, checkbox labels styled
    5. **Responsive**: `@media (max-width: 768px)` — reduce `#cy` min-height to 300px, stack filters vertically
  - Do NOT add any JavaScript logic — that's Tasks 3 and 4

  **Must NOT do**:
  - Do NOT add JavaScript event handlers — HTML + CSS only in this task
  - Do NOT add a CSS framework (Bootstrap, Tailwind, etc.)
  - Do NOT modify existing styles that affect the card grid or detail overlay
  - Do NOT remove or restructure existing HTML elements — only ADD new ones
  - Do NOT add `type="button"` to existing buttons (pre-existing LSP warning, not our concern)

  **Recommended Agent Profile**:
  - **Subagent Type**: `visual-engineering`
    - Reason: HTML structure + CSS styling task — visual-engineering category is purpose-built for UI/layout work
  - **Skills**: `[]`
    - No special skills needed — standard HTML/CSS editing
  - **Skills Evaluated but Omitted**:
    - `browse`: Not needed yet — no interactive behavior to test (that's Wave 2+)
    - `gstack`: Not needed — no running dev server to verify against

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Task 1)
  - **Blocks**: Tasks 3, 4, 5 (they need tab structure and #cy container)
  - **Blocked By**: None (can start immediately)

  **References** (CRITICAL):

  **Pattern References** (existing code to follow):
  - `docs/index.html` (full file, 29 lines) — Current HTML structure. Add tab bar inside `<main>` before `#card-grid`. Add `#cy` div before `#card-grid`. Add Cytoscape CDN script before existing `<script src="app.js">`. Note existing elements: `<header>`, `<main>`, `#card-grid`, `#artifact-detail` overlay.
  - `docs/style.css` (full file) — Current styles. Follow existing custom property conventions (if any). Add new styles at END of file, not interspersed. Check existing media queries and extend them rather than creating new breakpoints.
  - `docs/app.js:1-20` — Check how `currentLang` and `[data-lang]` attributes work — your new HTML elements must use the same `data-lang-ko`/`data-lang-en` pattern so the existing `toggleLang()` function picks them up automatically.

  **External References**:
  - Cytoscape.js CDN: `https://cdnjs.cloudflare.com/ajax/libs/cytoscape/3.33.1/cytoscape.min.js` — Pinned version. Use this exact URL.

  **WHY Each Reference Matters**:
  - `index.html`: Must understand current DOM structure to insert tab bar, #cy, and filters at correct positions without breaking layout
  - `style.css`: Must extend existing styles consistently — don't introduce conflicting patterns
  - `app.js:1-20`: The `[data-lang-ko]`/`[data-lang-en]` pattern must be followed exactly for language toggle to work on new elements

  **Acceptance Criteria**:
  - [ ] `docs/index.html` contains `<div id="cy"` with appropriate class
  - [ ] `docs/index.html` contains Cytoscape CDN script tag with version 3.33.1
  - [ ] `docs/index.html` contains `#edge-filters` with 4 checkboxes (era, category, location, material)
  - [ ] Only `category` checkbox has `checked` attribute
  - [ ] `docs/index.html` contains tab buttons with `data-lang-ko`/`data-lang-en` attributes
  - [ ] `docs/style.css` has `#cy` rule with explicit `height` (not auto, not 0)
  - [ ] `docs/style.css` has `.tab-content` display toggle rules
  - [ ] `docs/index.html` contains `<script src="graph.js"></script>` tag
  - [ ] All new elements use `data-lang-ko`/`data-lang-en` pattern matching existing convention

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: Happy path — HTML structure contains all required elements
    Tool: Bash
    Preconditions: `docs/index.html` has been edited
    Steps:
      1. Run `grep -c 'id="cy"' docs/index.html` — assert output is "1"
      2. Run `grep -c 'cytoscape/3.33.1' docs/index.html` — assert output is "1"
      3. Run `grep -c 'data-edge-type=' docs/index.html` — assert output is "4"
      4. Run `grep -c 'data-tab=' docs/index.html` — assert output is "2"
      5. Run `grep -c 'graph.js' docs/index.html` — assert output is "1"
    Expected Result: All 5 grep counts match expected values
    Failure Indicators: Any count is 0 or wrong number
    Evidence: .sisyphus/evidence/task-2-html-structure.txt

  Scenario: CSS height — #cy has explicit non-zero height
    Tool: Bash
    Preconditions: `docs/style.css` has been edited
    Steps:
      1. Run `grep -A5 '#cy' docs/style.css` — look for `height:` property
      2. Assert height is NOT `auto` and NOT `0` — should contain `vh` or `px` value
    Expected Result: #cy has explicit height like `calc(100vh - 200px)` or similar
    Failure Indicators: No height rule, or height: auto/0
    Evidence: .sisyphus/evidence/task-2-cy-height.txt

  Scenario: Default checkbox state — only category checked
    Tool: Bash
    Preconditions: `docs/index.html` has been edited
    Steps:
      1. Run `grep 'data-edge-type="category"' docs/index.html` — assert contains `checked`
      2. Run `grep 'data-edge-type="era"' docs/index.html` — assert does NOT contain `checked`
      3. Run `grep 'data-edge-type="location"' docs/index.html` — assert does NOT contain `checked`
      4. Run `grep 'data-edge-type="material"' docs/index.html` — assert does NOT contain `checked`
    Expected Result: Only category checkbox is checked by default
    Failure Indicators: Multiple checkboxes checked, or category not checked
    Evidence: .sisyphus/evidence/task-2-default-checkboxes.txt

  Scenario: Edge case — language attributes on all new UI text
    Tool: Bash
    Preconditions: `docs/index.html` has been edited
    Steps:
      1. Run `grep -c 'data-lang-ko=' docs/index.html` — count total language-tagged elements
      2. Verify tab buttons have `data-lang-ko`/`data-lang-en` attributes
      3. Verify filter labels have `data-lang-ko`/`data-lang-en` attributes
    Expected Result: All user-visible text in new elements has both ko and en language attributes
    Failure Indicators: Any new visible text missing language attributes
    Evidence: .sisyphus/evidence/task-2-lang-attributes.txt
  ```

  **Evidence to Capture:**
  - [ ] `task-2-html-structure.txt` — Grep results for all required HTML elements
  - [ ] `task-2-cy-height.txt` — CSS height rule verification
  - [ ] `task-2-default-checkboxes.txt` — Default checkbox state verification
  - [ ] `task-2-lang-attributes.txt` — Language attribute coverage check

  **Commit**: YES (C2)
  - Message: `feat(graph): add tab navigation UI with graph container and edge filters`
  - Files: `docs/index.html`, `docs/style.css`
  - Pre-commit: `grep 'id="cy"' docs/index.html && grep 'cytoscape/3.33.1' docs/index.html`

- [x] 3. Graph.js — Cytoscape Integration Module (`docs/graph.js`)

  **What to do**:
  - Create `docs/graph.js` as a self-contained Cytoscape.js graph module that:
    1. Exports/exposes an `initGraph()` function (called lazily on first Graph tab click)
    2. `initGraph()` does:
       a. `fetch('data/graph.json')` to load graph data
       b. Initialize Cytoscape instance on `#cy` container
       c. Load nodes and edges from fetched JSON
       d. Apply **CoSE layout** with config: `{ name: 'cose', nodeRepulsion: function(node){ return 6000; }, animate: false, randomize: true }`
       e. Style nodes: circular, labeled with `label_ko` (default) or `label_en` based on `currentLang` global
       f. Style edges: colored by type — different color per edge type (era=blue, category=green, location=orange, material=purple)
       g. Apply initial edge visibility: only show edges where `type === 'category'` (matches default checkbox state from Task 2)
    3. Expose `filterEdges(activeTypes)` function:
       - Takes array of active edge type strings, e.g. `['category', 'era']`
       - Shows edges matching any active type, hides others
       - Uses Cytoscape `ele.show()`/`ele.hide()` or `display` style
    4. Expose `updateGraphLabels(lang)` function:
       - Switches node labels between `label_ko` and `label_en` based on `lang` parameter ('ko' or 'en')
       - Called by existing `toggleLang()` in app.js
    5. Node tap event handler:
       - On node tap/click, call `showDetail(node.data('id'))` (existing function in app.js)
       - This opens the existing artifact detail overlay
    6. Store Cytoscape instance in module-level variable (e.g., `let cy = null;`)
       - `initGraph()` checks if `cy` already exists → skip re-initialization (lazy + singleton)
       - Instance stays alive across tab switches (never destroyed)
    7. Expose `getGraphInstance()` for external access if needed

  **Must NOT do**:
  - Do NOT add zoom controls, minimap, or navigation UI
  - Do NOT add node tooltips or hover effects beyond cursor:pointer
  - Do NOT add animated layout transitions (`animate: false`)
  - Do NOT add search/filter by node name
  - Do NOT add node sizing by degree or edge weight/thickness
  - Do NOT use ES modules (`import`/`export`) — use vanilla `<script>` tag pattern (IIFE or global functions)
  - Do NOT add `console.log` statements in production code (use sparingly for errors only)
  - Do NOT duplicate data from graph.json — only reference it

  **Recommended Agent Profile**:
  - **Subagent Type**: `unspecified-high`
    - Reason: Core integration module with Cytoscape.js API usage — moderately complex, needs careful API handling
  - **Skills**: `[]`
    - No special skills needed — Cytoscape.js API is well-documented, CDN already loaded by Task 2
  - **Skills Evaluated but Omitted**:
    - `browse`: Not needed during implementation — browser testing is Task 5
    - `librarian`: Cytoscape.js API is straightforward enough from plan references

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Task 4)
  - **Blocks**: Tasks 4 (needs graph functions), 5 (needs graph rendering)
  - **Blocked By**: Tasks 1 (needs graph.json), 2 (needs #cy container + CDN)

  **References** (CRITICAL):

  **Pattern References** (existing code to follow):
  - `docs/app.js:1-30` — How globals are declared and functions are structured. Graph.js must follow the same vanilla JS pattern (no modules, functions at top level or in IIFE). Key globals to reference: `currentLang`, `showDetail(artifactId)`.
  - `docs/app.js` `showDetail()` function — This is what `graph.js` calls on node tap. Read the function signature to understand expected parameter format (artifact ID string like `"nb_001"`).
  - `docs/app.js` `toggleLang()` function — Graph.js `updateGraphLabels()` will be called from here. Understand the `currentLang` global ('ko'/'en') pattern.

  **Data References** (contracts to implement against):
  - `docs/data/graph.json` (generated by Task 1) — Cytoscape-compatible JSON: `{ "elements": { "nodes": [{ "data": { "id": "nb_001", "label_ko": "숭례문", "label_en": "Sungnyemun" } }], "edges": [{ "data": { "source": "nb_001", "target": "nb_002", "type": "category", "value": "유적건조물" } }] } }`

  **External References**:
  - Cytoscape.js initialization: `cytoscape({ container: document.getElementById('cy'), elements: data.elements, style: [...], layout: {...} })`
  - Cytoscape.js CoSE layout docs: `{ name: 'cose', nodeRepulsion: 6000, animate: false }`
  - Cytoscape.js events: `cy.on('tap', 'node', function(evt){ var node = evt.target; ... })`
  - Cytoscape.js styling: `{ selector: 'node', style: { 'label': 'data(label_ko)', 'background-color': '#666' } }`
  - Cytoscape.js show/hide: `cy.edges('[type="era"]').show()` / `.hide()`

  **WHY Each Reference Matters**:
  - `app.js` globals: Must not clash with existing variable names; must call `showDetail()` correctly
  - `graph.json` schema: The node `data.id` format must match what `showDetail()` expects
  - Cytoscape.js API: Core library interactions — initialization, styling, events, filtering

  **Acceptance Criteria**:
  - [ ] `docs/graph.js` exists and defines `initGraph()`, `filterEdges()`, `updateGraphLabels()` functions
  - [ ] `initGraph()` creates Cytoscape instance on `#cy` with CoSE layout
  - [ ] Node tap calls `showDetail()` with correct artifact ID
  - [ ] `filterEdges(['category'])` shows only category edges, hides others
  - [ ] `filterEdges([])` hides all edges
  - [ ] `filterEdges(['era', 'category', 'location', 'material'])` shows all edges
  - [ ] `updateGraphLabels('en')` switches node labels to English
  - [ ] Second call to `initGraph()` does NOT re-create Cytoscape instance (singleton check)
  - [ ] No `import`/`export` statements (vanilla script pattern)

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: Happy path — graph.js defines required functions
    Tool: Bash
    Preconditions: `docs/graph.js` has been created
    Steps:
      1. Run `grep -c 'function initGraph' docs/graph.js` — assert output is "1"
      2. Run `grep -c 'function filterEdges' docs/graph.js` OR `grep -c 'filterEdges' docs/graph.js` — assert at least "1"
      3. Run `grep -c 'function updateGraphLabels' docs/graph.js` OR `grep -c 'updateGraphLabels' docs/graph.js` — assert at least "1"
      4. Run `grep -c 'showDetail' docs/graph.js` — assert at least "1" (node tap handler calls it)
      5. Run `grep -c 'cose' docs/graph.js` — assert at least "1" (CoSE layout)
    Expected Result: All 5 function/pattern checks pass
    Failure Indicators: Any function missing, no CoSE layout reference, no showDetail call
    Evidence: .sisyphus/evidence/task-3-graph-functions.txt

  Scenario: Singleton pattern — initGraph guards against double initialization
    Tool: Bash
    Preconditions: `docs/graph.js` has been created
    Steps:
      1. Run `grep -c 'cy.*null\|cy.*=.*null\|if.*cy\b' docs/graph.js` — assert at least "1"
      2. Verify there is a guard check like `if (cy) return;` or `if (cy !== null)` near the top of initGraph
    Expected Result: Singleton guard exists preventing double Cytoscape instantiation
    Failure Indicators: No null check for cy variable, no early return guard
    Evidence: .sisyphus/evidence/task-3-singleton-guard.txt

  Scenario: Edge case — no ES module syntax
    Tool: Bash
    Preconditions: `docs/graph.js` has been created
    Steps:
      1. Run `grep -c '^import \|^export ' docs/graph.js` — assert output is "0"
      2. Run `grep -c 'require(' docs/graph.js` — assert output is "0"
    Expected Result: Zero ES module or CommonJS syntax (vanilla script only)
    Failure Indicators: Any import/export/require statements found
    Evidence: .sisyphus/evidence/task-3-no-modules.txt

  Scenario: Edge case — animate:false in layout config
    Tool: Bash
    Preconditions: `docs/graph.js` has been created
    Steps:
      1. Run `grep 'animate.*false' docs/graph.js` — assert match found
    Expected Result: Layout config includes animate: false
    Failure Indicators: No animate:false, or animate:true present
    Evidence: .sisyphus/evidence/task-3-no-animation.txt
  ```

  **Evidence to Capture:**
  - [ ] `task-3-graph-functions.txt` — Function definition checks
  - [ ] `task-3-singleton-guard.txt` — Double-init guard verification
  - [ ] `task-3-no-modules.txt` — ES module syntax absence check
  - [ ] `task-3-no-animation.txt` — Animation disabled verification

  **Commit**: YES (C3)
  - Message: `feat(graph): add Cytoscape.js force-directed graph module`
  - Files: `docs/graph.js`
  - Pre-commit: `grep 'function initGraph' docs/graph.js && grep 'cose' docs/graph.js`

- [x] 4. Tab Switching + App.js Integration (`docs/app.js` minimal changes)

  **What to do**:
  - Add **minimal** tab-switching logic to `docs/app.js`:
    1. Tab click handler: When `.tab-btn[data-tab]` is clicked:
       a. Remove `active` class from all `.tab-btn` and `.tab-content` elements
       b. Add `active` class to clicked tab button and corresponding `.tab-content`
       c. If switching to graph tab AND graph not yet initialized → call `initGraph()` (lazy init)
    2. Edge filter checkbox handler: When `#edge-filters input[type="checkbox"]` changes:
       a. Collect all checked checkbox `data-edge-type` values into array
       b. Call `filterEdges(activeTypes)` from graph.js
    3. Extend existing `toggleLang()` to also call `updateGraphLabels(currentLang)` if graph is initialized
    4. Handle `#artifact-{id}` hash navigation:
       a. If URL has `#artifact-{id}` hash on load, call `showDetail(id)` regardless of active tab
       b. This preserves existing deep-link behavior
  - **ONLY append new code** to app.js — do NOT refactor, rename, or restructure existing functions
  - New code should be added at the END of the file (after existing code), not interspersed

  **Must NOT do**:
  - Do NOT refactor existing functions in app.js (loadManifest, renderCards, showDetail, closeDetail, toggleLang) — only ADD to toggleLang
  - Do NOT rename any existing variables or functions
  - Do NOT reorganize the file structure
  - Do NOT add more than ~40 lines of new code
  - Do NOT add event delegation on document — attach directly to tab buttons and checkboxes
  - Do NOT destroy/recreate Cytoscape instance on tab switch

  **Recommended Agent Profile**:
  - **Subagent Type**: `unspecified-high`
    - Reason: Integration task bridging graph.js with existing app.js — needs careful understanding of both
  - **Skills**: `[]`
    - No special skills needed — vanilla JS DOM manipulation
  - **Skills Evaluated but Omitted**:
    - `browse`: Not needed during implementation — testing is Task 5
    - `oracle`: Not architecture-level — simple event wiring

  **Parallelization**:
  - **Can Run In Parallel**: YES (partially — needs Task 3 functions to exist, but can code against expected API)
  - **Parallel Group**: Wave 2 (with Task 3)
  - **Blocks**: Task 5 (needs full integration working)
  - **Blocked By**: Tasks 2 (needs tab HTML), 3 (needs graph.js functions)

  **References** (CRITICAL):

  **Pattern References** (existing code to follow):
  - `docs/app.js` (full file, 465 lines) — Read ENTIRE file to understand: global state (`allArtifacts`, `currentLang`, `currentFilter`, `currentDetailArtifactId`), event binding patterns (direct DOM query + addEventListener), function naming conventions. Append new code at END of file.
  - `docs/app.js` `toggleLang()` function — Must ADD one line calling `updateGraphLabels(currentLang)` inside this function (with guard: `if (typeof updateGraphLabels === 'function')`). Do NOT rewrite the function.
  - `docs/app.js` `showDetail(artifactId)` — Understand how it works so tab switching doesn't interfere. Detail overlay (`#artifact-detail`) is global, shared between both tabs.

  **API References** (contracts from other tasks):
  - `docs/graph.js` `initGraph()` — Call once on first graph tab click. No parameters. Returns nothing. Safe to call multiple times (singleton guard).
  - `docs/graph.js` `filterEdges(activeTypes)` — Call with array of strings: `['category']`, `['era', 'category']`, `[]`, etc.
  - `docs/graph.js` `updateGraphLabels(lang)` — Call with `'ko'` or `'en'`.

  **HTML References** (DOM structure from Task 2):
  - `.tab-btn[data-tab="graph"]` / `.tab-btn[data-tab="cards"]` — Tab buttons to attach click handlers
  - `.tab-content` — Content panels (graph + card-grid) toggled by active class
  - `#edge-filters input[type="checkbox"][data-edge-type]` — Filter checkboxes
  - `#cy` — Graph container (already in DOM from Task 2)

  **WHY Each Reference Matters**:
  - `app.js` full file: Must understand EVERY existing pattern to avoid conflicts. New code appended at end.
  - `toggleLang()`: Only function being modified (one line added). Must guard against graph.js not loaded yet.
  - Graph.js API: The exact function names and signatures to call — no guessing.
  - HTML selectors: Must match exactly what Task 2 creates.

  **Acceptance Criteria**:
  - [ ] Tab buttons switch active class between graph and cards panels
  - [ ] First graph tab click triggers `initGraph()` (lazy initialization)
  - [ ] Subsequent graph tab clicks do NOT re-trigger `initGraph()`
  - [ ] Edge filter checkboxes call `filterEdges()` with correct active types array
  - [ ] `toggleLang()` now also calls `updateGraphLabels()` (with guard)
  - [ ] `#artifact-{id}` hash navigation still works on page load
  - [ ] New code is appended at END of app.js (not interspersed)
  - [ ] No existing functions were renamed, deleted, or restructured
  - [ ] Total new lines added ≤ 40

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: Happy path — tab switching code exists in app.js
    Tool: Bash
    Preconditions: `docs/app.js` has been edited
    Steps:
      1. Run `grep -c 'tab-btn\|data-tab' docs/app.js` — assert at least "2" (tab switching logic)
      2. Run `grep -c 'initGraph' docs/app.js` — assert at least "1" (lazy init call)
      3. Run `grep -c 'filterEdges' docs/app.js` — assert at least "1" (checkbox handler calls it)
      4. Run `grep -c 'updateGraphLabels' docs/app.js` — assert at least "1" (added to toggleLang)
    Expected Result: All 4 integration points present in app.js
    Failure Indicators: Any integration point missing
    Evidence: .sisyphus/evidence/task-4-integration-points.txt

  Scenario: Minimal changes — app.js not heavily modified
    Tool: Bash
    Preconditions: `docs/app.js` has been edited
    Steps:
      1. Run `wc -l docs/app.js` — assert line count is between 470 and 510 (was 465, adding ~5-40 lines)
      2. Run `grep -c 'function loadManifest\|function renderCards\|function showDetail\|function closeDetail' docs/app.js` — assert "4" (all original functions still exist unchanged)
    Expected Result: File grew by ≤45 lines, all original functions intact
    Failure Indicators: Line count >510 (too much added) or <465 (code deleted), or original function count ≠ 4
    Evidence: .sisyphus/evidence/task-4-minimal-changes.txt

  Scenario: Guard on updateGraphLabels call
    Tool: Bash
    Preconditions: `docs/app.js` has been edited
    Steps:
      1. Run `grep -B1 -A1 'updateGraphLabels' docs/app.js` — check for typeof guard or null check
      2. Assert the call is wrapped in `if (typeof updateGraphLabels` or similar guard
    Expected Result: updateGraphLabels call is guarded against graph.js not being loaded
    Failure Indicators: Bare `updateGraphLabels()` call without any guard
    Evidence: .sisyphus/evidence/task-4-lang-guard.txt

  Scenario: Edge case — no existing function signatures changed
    Tool: Bash
    Preconditions: `docs/app.js` has been edited
    Steps:
      1. Run `grep 'function loadManifest' docs/app.js` — assert exists
      2. Run `grep 'function renderCards' docs/app.js` — assert exists
      3. Run `grep 'function showDetail' docs/app.js` — assert exists
      4. Run `grep 'function closeDetail' docs/app.js` — assert exists
      5. Run `grep 'function toggleLang' docs/app.js` — assert exists
    Expected Result: All 5 original function signatures preserved exactly
    Failure Indicators: Any original function missing or renamed
    Evidence: .sisyphus/evidence/task-4-preserved-functions.txt
  ```

  **Evidence to Capture:**
  - [ ] `task-4-integration-points.txt` — All 4 integration points verified
  - [ ] `task-4-minimal-changes.txt` — Line count and original function preservation
  - [ ] `task-4-lang-guard.txt` — Guard check on updateGraphLabels call
  - [ ] `task-4-preserved-functions.txt` — Original function signatures intact

  **Commit**: YES (C4)
  - Message: `feat(graph): integrate graph/cards tab switching with detail overlay`
  - Files: `docs/app.js`
  - Pre-commit: `grep 'initGraph' docs/app.js && grep 'filterEdges' docs/app.js`

---

## Final Verification Wave (MANDATORY — after ALL implementation tasks)

> 4 review agents run in PARALLEL. ALL must APPROVE. Present consolidated results to user and get explicit "okay" before completing.

- [x] F1. **Plan Compliance Audit** — `oracle`
  Read the plan end-to-end. For each "Must Have": verify implementation exists (read file, run command). For each "Must NOT Have": search codebase for forbidden patterns — reject with file:line if found. Check evidence files exist in `.sisyphus/evidence/`. Compare deliverables against plan.
  Output: `Must Have [N/N] | Must NOT Have [N/N] | Tasks [N/N] | VERDICT: APPROVE/REJECT`

- [x] F2. **Code Quality Review** — `unspecified-high`
  Review all changed/new files for: empty catches, console.log in prod, commented-out code, unused imports. Check AI slop: excessive comments, over-abstraction, generic names (data/result/item/temp). Verify Python script is stdlib-only (no pip dependencies). Verify JS uses vanilla patterns matching existing app.js conventions.
  Output: `Files [N clean/N issues] | VERDICT`

- [x] F3. **Real Manual QA** — `unspecified-high` (+ `browse` skill)
  Start from clean state. Execute EVERY QA scenario from EVERY task — follow exact steps, capture evidence. Test cross-task integration: graph tab → node click → detail overlay → close → switch to cards tab → click card → detail overlay. Test edge cases: all filters unchecked (0 edges), rapid tab switching, mobile viewport. Save to `.sisyphus/evidence/final-qa/`.
  Output: `Scenarios [N/N pass] | Integration [N/N] | Edge Cases [N tested] | VERDICT`

- [x] F4. **Scope Fidelity Check** — `deep`
  For each task: read "What to do", read actual diff (git log/diff). Verify 1:1 — everything in spec was built, nothing beyond spec was built. Check "Must NOT do" compliance: no npm added, no app.js refactor, no manifest.py changes. Detect cross-task contamination. Flag unaccounted changes.
  Output: `Tasks [N/N compliant] | Contamination [CLEAN/N issues] | Unaccounted [CLEAN/N files] | VERDICT`

---

## Commit Strategy

| Commit | Contents | Message |
|--------|----------|---------|
| C1 | `pipeline/generate_graph.py` + `docs/data/graph.json` | `feat(graph): add graph data generator for artifact relationships` |
| C2 | `docs/index.html` + `docs/style.css` tab/container changes | `feat(graph): add tab navigation UI with graph container and edge filters` |
| C3 | `docs/graph.js` | `feat(graph): add Cytoscape.js force-directed graph module` |
| C4 | `docs/app.js` tab integration | `feat(graph): integrate graph/cards tab switching with detail overlay` |
| C5 | QA fixes (if any) | `fix(graph): resolve QA issues from end-to-end testing` |

---

## Success Criteria

### Verification Commands
```bash
python pipeline/generate_graph.py  # Expected: generates docs/data/graph.json without errors
python3 -c "import json; d=json.load(open('docs/data/graph.json')); print(f'nodes:{len(d[\"elements\"][\"nodes\"])}, edges:{len(d[\"elements\"][\"edges\"])}'); assert len(d['elements']['nodes'])==64; assert 50 < len(d['elements']['edges']) < 2000"
# Expected: nodes:64, edges:XXX (between 50-2000)
```

### Final Checklist
- [ ] All "Must Have" items present and verified
- [ ] All "Must NOT Have" guardrails respected
- [ ] Graph renders 64 nodes with interactive CoSE layout
- [ ] Edge filters work (check/uncheck toggles visibility)
- [ ] Tab switching preserves both views without destroying state
- [ ] Node click opens detail overlay, ESC/close dismisses it
- [ ] Hash navigation `#artifact-{id}` works from both tabs
- [ ] Mobile viewport (375×667) renders graph properly
- [ ] Language toggle changes node labels (ko↔en)
