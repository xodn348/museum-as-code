# Museum as Code — Han-lang Cultural Archive

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Han Language](https://img.shields.io/badge/han-.hgl-green.svg)](https://github.com/han-lang/han)
[![Artifacts](https://img.shields.io/badge/Artifacts-64-gold.svg)](docs/manifest.json)
[![Hero Artifacts](https://img.shields.io/badge/Hero%20Artifacts-10-d9b45e.svg)](docs/data/heroes/index.json)

**Live site:** https://xodn348.github.io/museum-as-code/<br>
**Repository:** https://github.com/xodn348/museum-as-code

---

## What this is

**Museum as Code** is a digital museum experiment that treats Korean cultural heritage as **Han-lang (`.hgl`) source code**.

The current homepage is intentionally **code-first**: it does not lead with large artifact photos, because some image/object matches still need exact source and license verification. Instead, the public interface foregrounds:

- `.hgl` source snippets as the visual signature,
- provenance and metadata sidecars,
- curated hero pages for 10 representative artifacts,
- room-based navigation and a secondary connection graph,
- a broader 64-record code archive.

한국 문화유산을 사진 카탈로그처럼 보여주기보다, **Han-lang 소스코드·출처·구조화된 메타데이터**를 먼저 보여주는 디지털 박물관입니다. 사진은 정확한 유물/출처/라이선스 매칭이 끝난 항목부터 다시 도입합니다.

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

### Hero artifacts

The curated Phase C set contains 10 hero records under `artifacts/heroes/` and web copies under `docs/data/heroes/`:

1. Pensive Bodhisattva — National Treasure No. 83
2. Celadon Prunus Vase with Inlaid Cloud and Crane Design
3. White Porcelain Moon Jar
4. Hunminjeongeum Haerye
5. Gold Crown from Geumgwanchong Tomb
6. Baekje Gilt-bronze Incense Burner
7. Divine Bell of King Seongdeok
8. Tripitaka Koreana Woodblocks
9. Stone Constellation Chart
10. Danwon Genre Album

Some images remain marked with `needs_verification`; those photos are deliberately hidden from homepage cards until exact matching is resolved.

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

---

## Data pipeline commands

```bash
# Normalize sidecars after metadata/image-source edits
python3 -m pipeline.normalize_sidecars

# Copy artifact .json/.hgl records into GitHub Pages-safe docs/data paths
python3 -m pipeline.sync_docs_artifacts

# Regenerate archive manifest
python3 -m pipeline.manifest

# Regenerate graph data
python3 -m pipeline.generate_graph

# Validate JSON, local paths, hero files, manifest, and graph
python3 -m pipeline.validate_data
```

Recommended verification before pushing:

```bash
node --check docs/app.js
node --check docs/graph.js
node --check docs/hero.js
python3 -m pipeline.validate_data
```

---

## Image/provenance policy

1. **Do not hotlink production artifact images.** Use local files under `docs/images/...`.
2. **Do not show uncertain photos as primary homepage visuals.** If a source match is not exact, leave `needs_verification` and use the code-first presentation.
3. **Record source and license fields** in sidecar JSON and `docs/images/heroes/*/image-sources.json`.
4. **Reintroduce photos per artifact only after verification**, not as broad automatic thumbnails.

---

## Contributing

Contributions are welcome, especially:

- replacing `needs_verification` image placeholders with exact verified sources,
- improving hero artifact metadata and curator copy,
- extending `.hgl` records,
- improving validation scripts,
- refining the code-first design system without making photos the default entry surface again.

Before opening a PR, run:

```bash
node --check docs/app.js
node --check docs/graph.js
node --check docs/hero.js
python3 -m pipeline.validate_data
```

---

## License

This project is distributed under the **MIT License**. See [LICENSE](LICENSE).
