## F3 QA Issues (2026-04-01)

1. Scenario 8 failed: `http://localhost:8787/404.html` returns default Python server 404 page (`File not found`) instead of a project-branded renamed 404 page.
2. In graph mode, photo styling and node image visibility are state-sensitive in automated checks; direct style inspection can return `none` unless graph initialization fully settles.

## F3 QA Issues (2026-04-01, rerun)

1. Scenario 2 partial failure: language state toggles, but visible EN/KO content segregation is broken (both language blocks visible simultaneously in checks).
2. Scenario 3 failure: artifact card photos are not visibly rendered (`totalCardImgs=64`, `visibleImgs=0`, `loaded=0`) in local QA run.
3. Scenario 6 failure: graph hover enlargement check did not change node size (`50px -> 50px`), indicating hover zoom effect is not active in tested state.
4. Scenario 8 failure: `docs/404.html` content does not reflect renamed title target (`404 — Museum as Code`) and performs immediate redirect, preventing in-page rename verification.
