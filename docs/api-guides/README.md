# API Guides

Vendor-published OpenAPI guides for Korean cultural data services we either consume or are evaluating. Each `.doc` / `.pdf` is the original Microsoft Word / PDF artifact as distributed by the issuing agency; the matching `*-analysis.md` is our condensed reading + integration notes.

| Spec | Provider | Status | Analysis |
|---|---|---|---|
| `한눈에보는문화정보조회서비스_가이드.doc` | 문화체육관광부 / 한국문화정보원 (data.go.kr `B553457`) | **Evaluating** — does NOT replace artifact images, but enables a "current exhibitions" feature | [`cultureinfo-api-analysis.md`](./cultureinfo-api-analysis.md) |

## Adding a new spec

1. Drop the original document as-is into `docs/api-guides/`.
2. Convert to `txt` for searchability: `textutil -convert txt -encoding UTF-8 your_file.doc -output /tmp/out.txt`.
3. Write `your_spec-analysis.md` with: TL;DR, what this is good for, endpoint reference, response shapes, integration plan, open questions.
4. Add a row to the table above.
5. Open a PR.
