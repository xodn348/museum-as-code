## F3 QA Decisions (2026-04-01)

1. Treat graph photo verification as a combined evidence check: network image fetch success + graph node `image_url` data population + hover enlargement event change.
2. Mark final verdict as REJECT when any required MUST-DO scenario fails, even if the rest of the scenarios pass.

## F3 QA Decisions (2026-04-01, rerun)

1. Use strict scenario-level pass/fail based on user-provided expected outcomes, not prior QA history.
2. Keep verdict at REJECT due to blocking regressions in language rendering consistency, card image visibility, hover enlargement behavior, and 404 rename expectation.
