# Analysis · 한눈에보는문화정보조회서비스 (PublicPerformanceDisplayService)

**Source guide:** [`한눈에보는문화정보조회서비스_가이드.doc`](./한눈에보는문화정보조회서비스_가이드.doc)
**Last updated by source:** 2024-12-19 (v1.0, valid through 2099-12-31)
**Provider:** 문화체육관광부 / 한국문화정보원 (data.go.kr 채널 ID `B553457`)
**Analyzed:** 2026-04-30

---

## TL;DR — does this solve our image problem?

**No.** This API serves **current/upcoming performances, exhibitions, festivals, and events** — not artifact reference photos.

| What we needed | What this API gives |
|---|---|
| HD photos of National Treasure No. 83 (금동미륵보살반가사유상) for hero card | A list of CURRENT exhibitions, with `imgUrl` pointing to **event posters** (not the artifact itself) |
| Stable, license-tagged image URLs for 64 archive cards | `thumbnail` per event item, `imgUrl` (poster) per detail — license is data.go.kr's 공공누리, attribution required |
| One-shot bulk download | Real-time event feed; useful for "what's on now," not for a static archive |

**Conclusion:** keep using the existing CHA `khs.go.kr/unisearch/...` mapping (PR #5, 56/57 covered) for the artifact photos. This new API is a **different feature** — a "What's on now / nearby exhibitions" widget that complements the museum.

---

## What this API is actually good for

A "currently showing / upcoming events" feature for the museum site:

- **Hero detail sidebar** — "Exhibitions featuring this artifact or its era right now":
  - Call `/cultrueinfo/realm2?realmCode=D000` (전시) and filter client-side by keyword match against `title` or `place` (e.g., "국립중앙박물관" for hero_pensive_bodhisattva).
- **Homepage banner** — "Top 5 ongoing Korean cultural exhibitions this week":
  - Call `/cultrueinfo/period2?from=YYYYMMDD&to=YYYYMMDD&serviceTp=A` (공연/전시 only) and render the first 5 items with thumbnails.
- **Map view** — `gpsX/gpsY` are present on every item, so a clickable Korean map marking active exhibitions is feasible without geocoding.
- **Static archive build** — at build time, fetch realm=D000 within next 90 days, snapshot to `docs/data/exhibitions.json`, and rebuild weekly via the existing CI workflow. This avoids client-side data.go.kr calls (no key in browser, no CORS issues).

---

## Endpoint reference

**Base URL:** `https://apis.data.go.kr/B553457/cultrueinfo`

> Note: spelling is literally `cultrueinfo` (typo in the published spec — do not "fix" it).

**Auth:** `serviceKey` query param (data.go.kr-issued, encoded). No certificates, no Basic auth, no SSL message-level encryption.
**Format:** REST GET → XML response (data.go.kr usually accepts `&type=json` but the spec doesn't mention it; verify on first call).
**Rate budget per the spec:** 30 TPS, 500ms avg latency, 800KB max message.
**HTTPS:** required (운영환경 URL is `https://`).

| # | Path | Purpose | Required params |
|---|---|---|---|
| 1 | `GET /livelihood2` | Cultural calendar (broad list) | `serviceKey`, `keyword` (optional) |
| 2 | `GET /period2` | List by date range | `serviceKey`, `from`, `to` |
| 3 | `GET /area2` | List by region | `serviceKey`, `sido`, `sigungu` (optional) |
| 4 | `GET /realm2` | List by category | `serviceKey`, `realmCode` |
| 5 | `GET /detail2?seq={id}` | Full record for a single event | `serviceKey`, `seq` |

### Common request params (apply to list endpoints 1–4)

| Param | Type | Default | Notes |
|---|---|---|---|
| `serviceKey` | string | — | data.go.kr-issued, URL-encoded |
| `pageNo` | int | 1 | Pagination |
| `numOfRows` | int | 10 | Max ~100 (spec says 31, but 100 is the platform default) |
| `from` / `to` | YYYYMMDD | — | Date range |
| `keyword` | string | — | Free-text filter on title |
| `serviceTp` | A/B/C | — | A=공연/전시, B=행사/축제, C=교육/체험 |
| `sortStdr` | 1/2/3 | 1 | 1=등록일, 2=공연명, 3=지역 |
| `sido` / `sigungu` | string | — | Korean region names |
| `gpsxfrom` / `gpsxto` / `gpsyfrom` / `gpsyto` | float | — | Bounding-box geo filter |
| `place` | string | — | Venue name filter |
| `realmCode` | code | — | See realm codes table below |

### Realm codes (분야)

| Code | Category |
|---|---|
| `A000` | 연극 (Theater) |
| `B000` | 음악/콘서트 (Music/Concert) |
| `B002` | 국악 (Korean traditional music) |
| `B003` | 뮤지컬/오페라 (Musical/Opera) |
| `C000` | 무용/발레 (Dance/Ballet) |
| `D000` | **전시 (Exhibition)** ← most relevant for us |
| `E000` | 아동/가족 (Kids/Family) |
| `F000` | 행사/축제 (Events/Festivals) |
| `G000` | 교육/체험 (Education/Experience) |
| `H000` | 도서 (Books) |
| `I000` | 체육 (Sports) |
| `L000` | 기타 (Other) |

---

## Response shape

### List endpoints (1–4) — `<items><item>...</item></items>`

| Field | Type | Sample | Use |
|---|---|---|---|
| `seq` | int | `250002` | Primary key for `/detail2` |
| `title` | string | `토비아스 레베르거: 가끔이나마…` | Card title |
| `startDate` / `endDate` | YYYYMMDD | `20180616` / `20251231` | Date chips |
| `place` | string | `부산현대미술관` | Venue |
| `realmName` | string | `전시` | Category label |
| `area` | string | `부산` | 시도 |
| `sigungu` | string | `동래구` | 시군구 |
| `thumbnail` | URL | (CDN) | Card image |
| `gpsX` / `gpsY` | float | `128.94274 / 35.10921` | Map marker |
| `serviceName` | string | `공연/전시` | Used to filter A/B/C client-side |

### Detail endpoint (5)

Adds to the list shape:

| Field | Type | Sample | Use |
|---|---|---|---|
| `contents1` | text | (up to 14,000 chars) | Curator description, render as prose |
| `price` | string | `무료` | Ticket info |
| `url` | URL | (event page) | "More info ↗" link |
| `phone` | string | `02-...` | Contact |
| `imgUrl` | URL | (poster) | Hero image on detail panel |
| `placeUrl` | URL | (venue) | Venue link |
| `placeAddr` | string | `부산광역시 사하구…` | Full venue address |
| `placeSeq` | int | `905593` | 문화예술공간 ID for cross-reference |

---

## How this fits into museum-as-code

### Tier 1 — keep current pipeline (PR #5)

The CHA `khs.go.kr/unisearch/...` images we already wired (56/57 archive cards, 0/10 hero) remain the primary source for **artifact reference photos**. This API does not replace them.

### Tier 2 — net-new feature: "Currently showing"

A small static-build pipeline using this API:

1. New file: `pipeline/fetch_current_exhibitions.py`
   - Loads `serviceKey` from env var `DATA_GO_KR_KEY` (do NOT commit the key)
   - Calls `/realm2?realmCode=D000&from=$today&to=$today+90d&numOfRows=100`
   - For each item: store `seq`, `title`, `place`, `startDate`/`endDate`, `area`, `gpsX`, `gpsY`, `thumbnail`
   - For top N (~20): also call `/detail2` to grab `contents1`, `imgUrl`, `placeAddr`
   - Output: `docs/data/exhibitions.json` (single file, ~50–100KB)

2. Frontend:
   - `docs/exhibitions.html` — new page listing current Korean exhibitions, KPDH-A styled cards
   - On hero detail pages: optional "Related current exhibitions" sidebar — server-side filter by venue keyword (e.g., 국립중앙박물관) so we surface only items relevant to the artifact's home museum

3. CI:
   - GitHub Actions cron `0 6 * * 1` (every Monday 6am UTC) — re-runs the pipeline, commits the refreshed `exhibitions.json` to main. Key stored as `secrets.DATA_GO_KR_KEY`.

### Tier 3 — speculative: map view

Every item carries `gpsX/gpsY`. A new `docs/map.html` could plot ongoing exhibitions on a Korean basemap (Leaflet + free tile provider). Out of scope for v1 but the API supports it without extra calls.

---

## Open questions / blockers

1. **Key issuance.** The data.go.kr 활용신청 process for this dataset (`15121515`) is currently blocked for the project owner from US IP. Wikimedia Commons + emuseum scraping remain the primary fallback for HD images. The "current exhibitions" feature waits on key approval.
2. **JSON format.** Spec only documents XML. Need to verify whether `&_type=json` (data.go.kr platform-wide param) works — if so, we skip XML parsing.
3. **Image hotlinking policy.** `thumbnail` and `imgUrl` are CDN URLs hosted by data.go.kr. Public hotlinking should be acceptable under 공공누리 1유형, but for production we should mirror to `docs/images/exhibitions/` to avoid hot-link breakage and rate limits.
4. **Caching.** `numOfRows=100` per page × ~12 realms × 4 weeks of upcoming events ≈ a few hundred items. Single weekly snapshot is plenty; no client-side calls to data.go.kr needed.

---

## Recommended next step

Wait until the data.go.kr key clears (or use a Korean collaborator's key). Then:

1. Add `pipeline/fetch_current_exhibitions.py` (mirror the structure of `pipeline/fetch_official_images.py`).
2. Build the Tier 2 feature behind a `GENERATE_EXHIBITIONS=1` env flag so the rest of the static site doesn't depend on it.
3. Open as a separate PR — keeps the artifact archive (national treasures) and the events feed cleanly separated.
