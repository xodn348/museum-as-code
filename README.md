# Museum as Code — The National Museum of Korea, rewritten in Han-lang

> **국립중앙박물관을 한언어로 다시 짓다** — a code-first reconstruction of Korea's national collection.
> Built with the [Han programming language](https://github.com/xodn348/han). Every page, card, and artifact is a real `.hgl` file — 56 catalog entries plus 10 curated hero pages, all executable in the [Han playground](https://xodn348.github.io/han/playground/).

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Han Language](https://img.shields.io/badge/built%20with-Han%20.hgl-green.svg)](https://github.com/xodn348/han)
[![Artifacts](https://img.shields.io/badge/Catalog-56-gold.svg)](docs/manifest.json)
[![Hero Artifacts](https://img.shields.io/badge/Hero%20Pages-10-d9b45e.svg)](docs/data/heroes/index.json)

**Live site:** https://xodn348.github.io/museum-as-code/
**Han-lang:** https://github.com/xodn348/han · [playground](https://xodn348.github.io/han/playground/)

---

## What this is

A reconstruction of the National Museum of Korea where the **artifact records, hero pages, and demo snippets are all real Han-lang source code**. The official [국립중앙박물관 site](https://www.museum.go.kr/) is the canonical curator's interface; this site does something the official one cannot — it makes "Korean cultural archive" and "Korean-language programming demo" the **same artifact**. Hangul is first-class syntax, not chrome around an English codebase.

It is also the canonical real-world showcase of [Han](https://github.com/xodn348/han). Every code block on the site runs unchanged in `hgl interpret`.

## 🚨 Han-Lang only

Every `.hgl` in this repo must run cleanly under `hgl interpret`. Pseudocode and Korean-keyword-flavored fake syntax are forbidden. Full mandate, keyword reference, and PR review gates: [`CLAUDE.md`](./CLAUDE.md).

## Han-lang example

```hgl
구조 히어로유물_hero_pensive_bodhisattva {
    이름: 문자열,
    영문명: 문자열,
    지정번호: 문자열,
}

함수 main() {
    변수 이름 = "금동미륵보살반가사유상"
    변수 영문명 = "Pensive Bodhisattva"
    변수 지정번호 = "국보 제83호"
    출력(형식("{0} — {1}", 이름, 지정번호))
}

main()
```

## Run locally

```bash
cd ~/code/museum-as-code
python3 -m http.server 8765 --directory docs
# open http://127.0.0.1:8765/

hgl interpret artifacts/heroes/hero_pensive_bodhisattva.hgl
```

## Repository layout

```text
museum-as-code/
├── artifacts/
│   ├── heroes/                    # 10 curated hero artifacts (.json + .md + .hgl)
│   ├── national-treasures/        # national-treasure records (.json + .hgl)
│   └── special/kdh/               # 7 KDH cultural-reference records
├── docs/                          # GitHub Pages site (homepage, hero pages, manifests)
├── pipeline/                      # Python build + validation pipeline
├── DESIGN.md                      # design system notes
└── CLAUDE.md                      # Han-only mandate + PR gates
```

<details>
<summary><b>Data pipeline + verification</b></summary>

```bash
python3 -m pipeline.normalize_sidecars
python3 -m pipeline.sync_docs_artifacts
python3 -m pipeline.manifest
python3 -m pipeline.generate_graph
python3 -m pipeline.validate_data

node --check docs/app.js
node --check docs/hero.js
```

</details>

<details>
<summary><b>Image / provenance policy</b></summary>

1. No hotlinking — local files under `docs/images/...` only.
2. No uncertain photos as primary visuals — if source match is not exact, leave `needs_verification` and the card falls back to the code-first view.
3. Record `source` + `license` fields in sidecar JSON.

CHA Open API images carry license `공공누리 제1유형(출처표시)` (attribution required, commercial use OK), credit `국가유산청`. Cards render `source · license` captions from the sidecar fields.

</details>

## Contributing

PRs welcome — exact-image verifications, curator copy, new `.hgl` records. Before pushing:

```bash
node --check docs/app.js docs/hero.js
python3 -m pipeline.validate_data
```

## License

MIT. See [LICENSE](LICENSE).
