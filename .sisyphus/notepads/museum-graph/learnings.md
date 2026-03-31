# Learnings — museum-graph

## Project Setup
- Working dir: /Users/jnnj92/museum-as-code/
- Static site: docs/ served on GitHub Pages
- No npm/bundler — vanilla JS via <script> tags
- 64 artifacts: 57 national treasures (nb_001~057) + 7 KDH special (kdh_001~007)

## Conventions
- HTML/CSS/JS in docs/
- Pipeline scripts in pipeline/
- Sidecar JSONs in artifacts/national-treasures/nb_*.json and artifacts/special/kdh/kdh_*.json
- app.js: 465 lines, vanilla JS, globals: allArtifacts, currentLang, currentFilter, currentDetailArtifactId
- Language toggle: data-lang-ko / data-lang-en attributes, toggleLang() function
- Hash navigation: #artifact-{id} deep links via showDetail()

## Pre-existing LSP Warnings (IGNORE)
- docs/index.html: button elements missing type attribute — pre-existing, plan says ignore
- docs/style.css: duplicate properties — pre-existing, ignore
- Cytoscape CDN source in /tmp — external library, ignore

## [2026-03-31] Task: T1
- Added pipeline/generate_graph.py to read 57 nb_*.json + 7 kdh_*.json and emit Cytoscape graph JSON at docs/data/graph.json.
- Implemented era normalization via re.sub(r'\s*\(.*?\)\s*$', '', era), material splitting on comma, and per-dimension missing-field warnings to stderr.
- Graph output is constrained to node labels + relationship edges only; verified output has 64 nodes and 1583 edges with QA evidence files under .sisyphus/evidence/.

## [2026-03-31] Task: T1
- Rebuilt `docs/data/graph.json` from 64 sidecars using `pipeline/generate_graph.py` with deterministic pairwise edges where `source < target` by artifact id ordering.
- Confirmed era edge values are normalized (no parenthetical suffixes), material edges are split to single values (no commas), and KDH category omissions only emit stderr warnings while skipping category linking.
- Captured scenario evidence in `.sisyphus/evidence/task-1-generate-graph.txt`, `task-1-era-normalization.txt`, `task-1-material-splitting.txt`, and `task-1-missing-category.txt`.


## [2026-03-31] Task: T2
- Added graph tab UI scaffolding in `docs/index.html`: tab bar, `#cy` graph container, and `#edge-filters` with 4 relationship checkboxes using `data-lang-ko`/`data-lang-en` labels.
- Inserted Cytoscape CDN `3.33.1` and `graph.js` placeholder script tags before existing `app.js` to keep load order ready for future graph logic.
- Added tab/graph CSS at end of `docs/style.css` including `.tab-content` visibility toggles and explicit `#cy` height (`calc(100vh - 200px)`, `min-height: 400px`, mobile `300px`) to prevent invisible Cytoscape rendering.
- Saved QA evidence under `.sisyphus/evidence/` for structure, checkbox defaults, language attributes, and `#cy` height verification.
- Task 2 UI scaffold: Added `.tab-bar` with bilingual `data-lang-ko`/`data-lang-en` tab buttons (`graph`, `cards`) in `docs/index.html` before `#card-grid`.
- Added graph panel scaffold: `#cy.tab-content.active` with `#edge-filters` containing exactly 4 edge-type checkboxes; only `category` is checked by default.
- Script loading order for graph support: Cytoscape CDN `3.33.1` then `graph.js`, both inserted before existing `app.js` script tag.
- Card grid now uses `class="tab-content"` so it starts hidden until JS tab switching is implemented.
- Critical rendering rule confirmed: `#cy` has explicit `height: calc(100vh - 200px)` and `min-height: 400px` with mobile `min-height: 300px` at `max-width: 768px`.

## [2026-03-31] Task: T3
- Created docs/graph.js with initGraph(), filterEdges(), updateGraphLabels(), getGraphInstance().
- Singleton guard implemented as `if (cy) { return; }` at the top of initGraph().
- CoSE layout configured with nodeRepulsion 6000, animate:false, randomize:true.
- Edge colors: era=blue(#6699cc), category=green(#66aa77), location=orange(#cc9944), material=purple(#9966cc).
- Initial edge visibility after initGraph(): only category edges shown.
- Node tap behavior calls showDetail(evt.target.data('id')).
- updateGraphLabels() switches label field via cy.nodes().style('label', fn) for label_ko/label_en.

## [2026-03-31] Task: T4
- Appended ~30 lines to end of docs/app.js (was 465 lines)
- Tab switching: IIFE wrapping querySelectorAll('.tab-btn').forEach + addEventListener('click')
- Lazy graph init: local `graphInitialized` flag, calls initGraph() on first graph tab click only
- Edge filter: querySelectorAll('#edge-filters input:checked') → push data-edge-type → filterEdges(active)
- toggleLang() extended with guard: if (typeof updateGraphLabels === 'function') { updateGraphLabels(currentLang); }
- All 5 original functions (loadManifest, renderCards, showDetail, closeDetail, toggleLang) preserved unchanged
- card-grid panel selected by id (not class) to avoid ambiguity: document.getElementById('card-grid')

## [2026-03-31] Task: T3
- Created docs/graph.js with initGraph(), filterEdges(), updateGraphLabels(), getGraphInstance()
- Singleton guard: `if (cy) { return; }` at top of initGraph()
- CoSE layout: nodeRepulsion 6000, animate:false, randomize:true
- Edge colors: era=blue(#6699cc), category=green(#66aa77), location=orange(#cc9944), material=purple(#9966cc)
- Initial edge visibility: only category edges shown after initGraph()
- Node tap: calls showDetail(evt.target.data('id'))
- updateGraphLabels() uses cy.nodes().style('label', fn) to switch between label_ko/label_en

## [2026-03-31] Task: T4
- Appended ~30 lines to end of docs/app.js (was 465 lines)
- Tab switching: IIFE wrapping querySelectorAll('.tab-btn').forEach + addEventListener('click')
- Lazy graph init: local `graphInitialized` flag, calls initGraph() on first graph tab click only
- Edge filter: querySelectorAll('#edge-filters input:checked') → push data-edge-type → filterEdges(active)
- toggleLang() extended with guard: if (typeof updateGraphLabels === 'function') { updateGraphLabels(currentLang); }
- All 5 original functions (loadManifest, renderCards, showDetail, closeDetail, toggleLang) preserved unchanged
- card-grid panel selected by id (not class) to avoid ambiguity: document.getElementById('card-grid')
