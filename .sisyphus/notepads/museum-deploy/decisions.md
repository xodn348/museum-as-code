# Decisions — museum-deploy

## 2026-03-30 Task: init
- Deploy as PROJECT site (not user site) — must use /museum-as-code/ base path
- Use GitHub Actions workflow (not gh-pages branch) for deployment
- Merge strategy: copy docs/* and artifacts/ into single deploy directory
- 404.html redirect must use /museum-as-code/ not / (SPA subpath fix)
- Actions versions: checkout@v4, upload-pages-artifact@v3, deploy-pages@v4
- Permissions required: pages: write, id-token: write, contents: read
