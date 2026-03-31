# Issues — museum-graph

## Known Gotchas
- #cy container MUST have explicit height (not auto/0) or Cytoscape renders invisible
- Do NOT destroy Cytoscape instance on tab switch — hide/show #cy div instead
- KDH sidecars lack 'category' field — handle gracefully (skip dimension, log warning)
- Era values may have parenthetical suffixes: "삼국시대 (6-7세기)" — must normalize
- Material may be comma-separated multi-value: "석재, 목재" — must split
