# Final QA Evidence

## Date: 2026-04-01

## Grep Results

### Task 1 - Rename (no 디지털 국립중앙박물관)
```
grep -r "디지털 국립중앙박물관" docs/ → 0 matches (PASS)
```

### Task 2 - h1 data-lang attributes
```
grep "data-lang-ko\|data-lang-en" docs/index.html → Found 7 matches including h1
h1 line: <h1 data-lang-ko="Museum as Code - 국립중앙박물관" data-lang-en="Museum as Code - National Museum of Korea">
```

### Task 2 - 404.html no redirect
```
grep "window.location" docs/404.html → 0 matches (PASS)
```

### Task 3 - Manifest image_url count
```
grep -c "image_url" docs/manifest.json → 64 image_url fields
```

### Task 6 - No unmerged commits
```
git log origin/main..HEAD --oneline → empty (PASS)
```

## Browser Tests

### Task 2 - Default Language
- body.dataset.lang === "en" ✓ (PASS)

### Task 2 - Language Toggle
- Click toggle: ko → en → ko ✓ (PASS)

### Task 4 - Card Images
- First card HTML shows: `<img src="images/artifacts/PS01002001_000010000.jpg" loading="lazy" alt="Heunginjimun Gate">` ✓ (PASS)
- onerror handler in app.js:294 ✓ (PASS)

### Edge Case - 404 Page
- 404.html shows both English and Korean text, no redirect ✓ (PASS)

## Summary
All static checks pass. Browser tests for language toggle pass. Card images show with proper attributes.
