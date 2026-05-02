# Museum as Code — The National Museum of Korea, rewritten in Han-lang

> **국립중앙박물관을 한언어로 다시 짓다** — a code-first reconstruction of Korea's national collection. 64 treasures, 64 `.hgl` files. The catalog is the codebase.

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Han Language](https://img.shields.io/badge/han-.hgl-green.svg)](https://github.com/xodn348/han)
[![Artifacts](https://img.shields.io/badge/Artifacts-64-gold.svg)](docs/manifest.json)
[![Hero Artifacts](https://img.shields.io/badge/Hero%20Artifacts-10-d9b45e.svg)](docs/data/heroes/index.json)
[![Han Validate](https://github.com/xodn348/museum-as-code/actions/workflows/han-validate.yml/badge.svg)](.github/workflows/han-validate.yml)

**Live site:** https://xodn348.github.io/museum-as-code/<br>
**Museum repo:** https://github.com/xodn348/museum-as-code<br>
**Han-lang repo:** https://github.com/xodn348/han · **Playground:** https://xodn348.github.io/han/playground/

---

<a href="https://xodn348.github.io/museum-as-code/">
  <img src="docs/images/release-2026-04-30/home-desktop.png" alt="Museum as Code — homepage in Han-lang" width="100%">
</a>

---

## 🚨 Han-Lang Only

**Every code block in this project — homepage cards, hero pages, downloadable artifact files, README examples, demo snippets, anything — MUST be valid, executable Han-lang (`.hgl`).** Pseudocode and Korean-keyword-flavored fake syntax are forbidden. If `hgl interpret file.hgl` cannot run it, it does not go in this repo.

This is the project's hardest rule because the museum is simultaneously a Korean cultural archive **and** the canonical real-world demo of the Han programming language. Both jobs require valid Han.

The full mandate, keyword reference, and PR review gates live in [`CLAUDE.md`](./CLAUDE.md). Read it before opening a PR that adds or modifies code in this repo.

---

## What this is

**Museum as Code** is the **National Museum of Korea, rebuilt as source code**. Every page, card, and artifact record is a real Han-lang (`.hgl`) file — homepage cards, hero pages, downloadable artifacts, schema definitions. 64 national treasures rewritten as 64 executable programs that run unchanged in the [Han playground](https://xodn348.github.io/han/playground/).

The official [국립중앙박물관 site](https://www.museum.go.kr/) is the canonical curator's interface — wider catalog, real photographs, scholarly metadata. This site does something the official one cannot: it makes "Korean cultural archive" and "Korean-language programming demo" the **same artifact**. The medium is the message — Hangul appears as 1st-class syntax, not translated chrome around an English codebase.

It also doubles as the canonical real-world showcase of the [Han programming language](https://github.com/xodn348/han). Every code block on this site is parseable, executable Han — no pseudocode, no fake syntax.

The current homepage is intentionally **code-first**: it does not lead with large artifact photos, because some image/object matches still need exact source and license verification. Instead, the public interface foregrounds:

- `.hgl` source snippets as the visual signature,
- provenance and metadata sidecars,
- curated hero pages for 10 representative artifacts,
- room-based navigation and a secondary connection graph,
- a broader 64-record code archive.

Rather than presenting Korean cultural heritage as a photo catalog, the project leads with **Han-lang source code, provenance, and structured metadata**. Photographs are reintroduced only after the exact artifact, source, and license match has been verified.

---

## Current experience

| Surface | Purpose |
| --- | --- |
| `docs/index.html` | Code-first homepage with GitHub CTA, featured code cards, rooms, archive, graph |
| `docs/hero.html?id=<hero_id>` | Immersive single-artifact hero page with curator copy and `.hgl` source panel |
| `docs/data/heroes/index.json` | Web manifest for 10 curated hero artifacts |
| `docs/data/artifacts/` | GitHub Pages-safe copies of artifact `.json` and `.hgl` records |
| `docs/manifest.json` | 64-record archive manifest |
| `docs/data/graph.json` | Artifact relationship graph data |

10 curated hero records under `artifacts/heroes/` (Pensive Bodhisattva, Celadon Maebyeong, Moon Jar, Hunminjeongeum, Gold Crown, Baekje Incense Burner, Divine Bell of King Seongdeok, Tripitaka Koreana, Stone Constellation Chart, Danwon Genre Album). Photos marked `needs_verification` stay hidden from cards until source/license match.

---

## Han-lang example

```hgl
// Real hero-page style source
구조 히어로유물_hero_pensive_bodhisattva {
    이름: 문자열,
    영문명: 문자열,
    지정번호: 문자열,
    시대: 문자열,
    재질: 문자열,
    소장처: 문자열,
    라이선스: 문자열,
}

함수 main() {
    변수 이름 = "금동미륵보살반가사유상"
    변수 영문명 = "Pensive Bodhisattva"
    변수 지정번호 = "국보 제83호"

    출력(형식("{0} — {1}", 이름, 지정번호))
}

main()
```

Han-lang uses Korean keywords such as `구조`, `함수`, `변수`, `문자열`, `정수`, `출력`, and `형식`. In this project, `.hgl` is both data representation and visual identity.

---

## Design System

**KPDH-A · 부적 굿판** — neon talisman aesthetics on a code-first surface. Rose `#ff2e6a` on ink `#0a0612`, Black Han Sans for 한글 display, Noto Sans KR for body, JetBrains Mono for `.hgl`. Full palette, typography, and highlighting notes in [`DESIGN.md`](./DESIGN.md).

---

## Repository layout

```text
museum-as-code/
├── artifacts/
│   ├── heroes/                    # 10 curated hero artifacts: .json + .md + .hgl
│   ├── national-treasures/        # 57 national-treasure records: .json + .hgl
│   └── special/kdh/               # 7 KDH cultural-reference records
├── docs/
│   ├── index.html                 # GitHub Pages homepage
│   ├── hero.html                  # single hero artifact route
│   ├── app.js / graph.js          # frontend behavior
│   ├── style.css / hero.css       # code-first visual system
│   ├── data/
│   │   ├── artifacts/             # Pages-safe artifact record copies
│   │   ├── heroes/                # Pages-safe hero records + .hgl previews
│   │   ├── graph.json
│   │   └── rooms.json
│   └── images/                    # local image assets, not homepage-leading by default
├── pipeline/
│   ├── artifact_io.py             # shared path/data helpers
│   ├── manifest.py                # writes docs/manifest.json
│   ├── sync_docs_artifacts.py     # copies records into docs/data/artifacts
│   ├── normalize_sidecars.py      # normalizes provenance/local-image fields
│   ├── generate_graph.py          # writes docs/data/graph.json
│   └── validate_data.py           # data and asset integrity checks
├── DESIGN.md                      # design rules and code-first rationale
└── plans/                         # redesign planning artifacts
```

---

## Run locally

No frontend build step is required; the site is static.

```bash
cd ~/code/museum-as-code
python3 -m http.server 8765 --directory docs
```

Open: http://127.0.0.1:8765/

Verify a single `.hgl` artifact end-to-end:

```bash
hgl interpret artifacts/heroes/hero_pensive_bodhisattva.hgl
```

---

<details>
<summary><b>Data pipeline + verification</b></summary>

```bash
# Sidecar / manifest / graph regeneration
python3 -m pipeline.normalize_sidecars
python3 -m pipeline.sync_docs_artifacts
python3 -m pipeline.manifest
python3 -m pipeline.generate_graph

# Pull official photo URLs from 국가유산청 (CHA) Open API into the
# national-treasures sidecars. No API key required, ≤2 req/s.
python3 -m pipeline.fetch_official_images          # full sweep
python3 -m pipeline.fetch_official_images --dry-run
python3 -m pipeline.fetch_official_images --limit 5
python3 -m pipeline.fetch_official_images --type 보물

# Validate everything (JSON, local paths, hero files, manifest, graph)
python3 -m pipeline.validate_data

# Pre-push smoke test
node --check docs/app.js
node --check docs/hero.js
```

</details>

<details>
<summary><b>Image / provenance policy</b></summary>

1. No hotlinking — local files under `docs/images/...` only.
2. No uncertain photos as primary visuals — if source match is not exact, leave `needs_verification` and use the code-first card.
3. Record `source` + `license` fields in sidecar JSON.

CHA Open API images carry license `공공누리 제1유형(출처표시)` (attribution required, commercial use OK), credit `국가유산청`. Fields written by `pipeline.fetch_official_images`: `image_official_url`, `image_source_api`, `image_official_license`, `image_official_credit`, `image_official_source_name_ko`, `image_fetched_at`. Cards render `source · license` captions from these fields.

</details>

---

## Contributing

PRs welcome — especially exact-image verifications, curator copy improvements, new `.hgl` records. Before pushing:

```bash
node --check docs/app.js docs/hero.js
python3 -m pipeline.validate_data
```

---

## License

This project is distributed under the **MIT License**. See [LICENSE](LICENSE).
