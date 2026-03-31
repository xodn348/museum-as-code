# Issues — museum-deploy

## 2026-03-30 Task: init
- SPA 404 redirect bug: docs/404.html line 6 hardcodes '/' — breaks on project site subpath
  Fix: change '/' to '/museum-as-code/' on both line 6 (script) and line 9 (anchor)
- .workflows/ directory does not exist yet — must be created
- Existing user site xodn348.github.io must NOT be overwritten
