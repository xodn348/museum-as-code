# Decisions — museum-graph

## Architecture
- Cytoscape.js v3.33.1 via CDN (pinned)
- graph.js: IIFE/global pattern (no ES modules)
- graph.json: Cytoscape-compatible { elements: { nodes, edges } }
- Default edge filter: only "category" checked (prevents edge explosion)
- Lazy init: Cytoscape only initialized on first Graph tab click
- Singleton: cy variable never destroyed, hidden on tab switch

## Data Pipeline
- Python stdlib only (no pip), run from project root
- Era normalization: re.sub(r'\s*\(.*?\)\s*$', '', era)
- Material: split on "," and strip whitespace
- Missing fields: skip that dimension only, print WARNING to stderr
