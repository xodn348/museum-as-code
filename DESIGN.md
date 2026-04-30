# Museum as Code · Design System

**Updated:** 2026-04-30
**Current direction:** KPDH-A · 부적 굿판 / Talisman Ritual
**Reference mockup:** `~/.gstack/projects/museum-as-code/designs/homepage-20260429-235551/variant-A.html`

This is the live design source of truth. Newest direction at the top; historical resets retained at the bottom for context.

---

## 1. Direction: 부적 굿판 / Talisman Ritual (KPDH-A)

The site is simultaneously a Korean cultural archive and the canonical real-world demo of Han-lang. The visual system reflects both jobs: **code is the primary visual surface**, and that surface is dressed in **saturated neon talisman aesthetics** drawn from public-domain Korean folk motifs (단청, 부적, 까치, 연꽃, 호랑이).

KPDH-inspired in vibe only — neon rose + dark ink + paper cream + heavy 한글 display type. **Zero copyright lift.** No KPDH photos, characters, or trademarked marks. No K-pop iconography. Reference public-domain motifs only.

The "code as visual" principle from the 2026-04-30 code-first reset is preserved: every artifact is shown as real, runnable Han-lang. The talisman layer is added on top — neon stamps, dashed seal borders, film grain, blink-only motion — to make the code surface feel ritual and intentional rather than developer-default.

---

## 2. Color tokens

CSS custom properties (use these names verbatim across `docs/style.css`, `docs/hero.css`, etc.):

| Token         | Hex       | Use                                                        |
| ------------- | --------- | ---------------------------------------------------------- |
| `--ink`       | `#0a0612` | Primary background. Near-black with violet bias.           |
| `--rose`      | `#ff2e6a` | Primary accent. Borders, seals, accent type, glow.         |
| `--rose-deep` | `#b3083d` | Hover/pressed states, deeper rose for layering.            |
| `--paper`     | `#f6efe3` | Body text on ink, paper-mode backgrounds.                  |
| `--gold`      | `#ffd60a` | Han-lang keyword highlight in code (`구조`, `함수`, etc.). |
| `--violet`    | `#8b3dff` | Han-lang type highlight in code (`문자열`, `정수`, etc.).  |

Code syntax accent palette (used inside `<pre>` blocks):

- Keyword (`.k`): `--gold`
- Type (`.t`): `--violet`
- String (`.s`): `#9be29b` (mint, only used inside code)
- Comment (`.c`): `rgba(246,239,227,.4)` (faded paper)
- Function name (`.fn`): `--rose`

Background ambience (fixed, behind everything, `pointer-events:none`):

- Two radial gradients — rose at top-left (`15% 20%`, alpha .18), violet at mid-right (`85% 60%`, alpha .10).
- SVG film-grain overlay, `mix-blend-mode: overlay`, opacity ~.5.

---

## 3. Typography

All fonts are OFL-licensed and loaded from Google Fonts:

```
Black Han Sans            — display Korean (logo, h1, seals, card titles)
Noto Sans KR (400/700/900) — body Korean + Latin
JetBrains Mono (400/700)   — code, file tags, mono UI chrome
```

Scale (desktop, 1440 reference width):

| Role                | Family          | Size    | Weight | Letter-spacing |
| ------------------- | --------------- | ------- | ------ | -------------- |
| Hero h1             | Black Han Sans  | 160px   | —      | -.02em         |
| Section divider h2  | Black Han Sans  | 48px    | —      | normal         |
| Hero seal (韓)      | Black Han Sans  | 200px   | —      | normal         |
| Card title (EN)     | Black Han Sans  | 20px    | —      | normal         |
| Logo (한)           | Black Han Sans  | 28px    | —      | .04em          |
| Hero body p         | Noto Sans KR    | 20px    | 400    | normal         |
| Card title (KR)     | Noto Sans KR    | 14px    | 400    | normal         |
| Eyebrow / lang-badge | Noto Sans KR   | 13px    | 900    | .4em           |
| Nav links           | Noto Sans KR    | 13px    | 700    | .18em (UPPER)  |
| Han-only banner     | JetBrains Mono  | 11px    | 900    | .32em (UPPER)  |
| GH chip             | JetBrains Mono  | 11px    | 700    | .18em (UPPER)  |
| Code (`<pre>`)      | JetBrains Mono  | 11–13px | 400/700 | normal        |
| File tag            | JetBrains Mono  | 9px     | 400    | .15em          |

Korean display always Black Han Sans. Never substitute serif. Never hint at copyrighted K-pop typefaces (no "Pretendard Black knockoff" effects).

---

## 4. Components

### 4.1 Han-only banner (top)

Full-width strip, `--rose` background, `--ink` text, JetBrains Mono caps.

- Left: `● 100% Han-lang policy · 모든 코드는 .hgl 로 작성 · No pseudocode allowed` (dot blinks).
- Right: `view source ↗ github.com/xodn348/han`.
- 2px `--ink` bottom border.

This is a manifesto bar. Always visible, always at the very top, above nav.

### 4.2 Nav

- Logo: `한` in `--rose` Black Han Sans + `MUSEUM AS CODE` caps in `--paper`.
- Links: `Featured · Rooms · Archive · Graph` (caps, .18em, opacity .7 → 1 + rose on hover).
- **Dual GH chips** (right side, `gh-pair`): two side-by-side JetBrains Mono buttons:
  - `● Museum ↗` — links to `github.com/xodn348/museum-as-code`.
  - `● Han-lang ↗` (rose-tinted variant `.gh-han`) — links to `github.com/xodn348/han`.
  Both must always render. The Han-lang chip exists to make the language's repo a one-click destination from every page; it is not optional.
- Lang switcher: `EN / 한` rose-bordered chip.

### 4.3 Hero

Two-column grid (`1fr 480px`), 80px top padding.

Left column:

1. Eyebrow: `— Built with Han-lang · 한언어로 새겨진 디지털 박물관`.
2. **h1**: two-line Black Han Sans 160px. Last word uses `<span class="accent">` in `--rose` with rose glow `text-shadow`.
3. Body `<p>`: 20px, max 560px wide. `<strong>` rose-glowed, inline `<code>` wrapped in rose-tinted box.
4. **lang-badge**: small rose-bordered pill — `● WRITTEN IN HAN-LANG · 한언어 v0.4 · OPEN SOURCE`. Dot blinks.
5. CTA row: solid rose primary + two ghost buttons (Museum repo, Han-lang repo).

Right column:

- **Hero stamp**: 340×340 square, 3px `--rose` border, rotated `-8deg`, with rose glow shadow.
- Inner 1px **rose dashed border**, inset 14px, opacity .6 — the talisman seal feel.
- Center: `韓` glyph in Black Han Sans 200px, rose with glow.
- Below glyph: `HAN-LANG · 한언어` micro-caps label.

### 4.4 Schema panel (`schema.hgl`)

A single panel directly under each grid section header. It defines the struct **once**, so individual cards can show pure instances without redefining the schema 64 times.

- Background: `rgba(20,10,30,.7)` over the page ambience, 1px `--rose` border, backdrop-blur 6px, rose glow shadow.
- Header strip: rose-tinted, file glyph + filename `📜 schema.hgl` on the left, badge `● SHARED STRUCT · 한 번 정의 · 64회 인스턴스화` on the right (dot blinks).
- `<pre>` body: full Han-lang struct definition + at least one helper function (e.g. `설명출력`). Syntax-highlighted with `.k .t .s .c .fn` spans.

### 4.5 Code cards (artifact grid)

Three-column grid, 24px gap.

- Card background: `rgba(20,10,30,.6)`, 1px `rgba(255,46,106,.3)` border, backdrop-blur 6px.
- Hover: border → `--rose`, 30px rose glow shadow.
- **Seal**: 48×48 square, rose background, ink text, rotated `+8deg`, sits at top-right pinned outside the card edge. Shows the hero number in Black Han Sans (`01`, `02`, …).
- Number line: `// HERO_NN · CATEGORY` in JetBrains Mono rose caps.
- File tag: `heroes/<name>.hgl` in 9px rose mono.
- `<pre>`: 11px JetBrains Mono, 170px tall, dark inner background `rgba(0,0,0,.45)`, **2px rose left border** (the rose stripe is the card's spine).
- Title block under code: EN title in Black Han Sans 20px, KR title in Noto Sans KR 14px faded.
- Footer meta: `→ source-backed · .hgl` rose caps.

### 4.6 Section dividers

Horizontal rose-fade rule, then 48px Black Han Sans h2, then a rose-caps han-label with the count + filename hint:
`Ten Hero Artifacts · 히어로유물 · 10 · written in .hgl`

### 4.7 Film grain + ambience

Two `body::before` / `body::after` fixed layers — gradients and SVG turbulence grain. Always on, never animated, `pointer-events:none`. They are the talisman texture.

---

## 5. Han code rendering rules

**The code on the page IS the artifact.** It must always be valid `.hgl` that parses with `hgl interpret`.

Hard rules:

1. **Schema appears once per grid**, in a `schema.hgl` panel above the cards. It contains the `구조` definition + any helper `함수` used in the cards.
2. **Each card is an instance**, written as `변수 <snake_name> = <StructName> { 필드: 값, ... }` and followed by a single helper call (e.g. `설명출력(<snake_name>)`). No `구조` redefinition inside cards.
3. **Field syntax inside `구조`**: `이름: 타입` (no values). Field syntax inside instances: `이름: 값` (no types).
4. **String values** wrapped in `"..."` and rendered via the `.s` span (mint).
5. **Boolean literals**: `참` / `거짓`, rendered via the `.t` span.
6. **Comments**: `//`, rendered via the `.c` span.
7. **Code in cards must mirror a real file** under `artifacts/heroes/*.hgl` or `artifacts/national-treasures/*.hgl`. The `file-tag` text IS the path. No demo-only Han.
8. **Never** invent keywords. Allowed keyword set is the one listed in `CLAUDE.md`.
9. **Never** show `변수 X = "..."` inside `구조 { ... }` — that is invalid.

Syntax highlighting class contract (used in both schema and card `<pre>` blocks):

```
.k  → keyword       구조 함수 변수 반환 만약 ...
.t  → type / bool   문자열 정수 실수 불 참 거짓
.s  → string lit    "..."
.c  → comment       // ...
.fn → fn name       설명출력, 출력, 형식, main, ...
```

---

## 6. Motion

Minimal, ritual-only. The page should feel like a printed talisman, not a SaaS landing.

- **Allowed**: `@keyframes blink` on status dots only — `0%,100% {opacity:1} 50% {opacity:.3}`, 1.6s ease-in-out infinite. Used on the Han-only banner dot, lang-badge dot, schema badge dot.
- **Hover transitions**: 0.15s–0.2s on chips and cards (border color, box-shadow). No transforms, no scaling, no parallax.
- **No** scroll-triggered animation. **No** marquees. **No** confetti. **No** Lottie.

---

## 7. Aesthetics positioning

KPDH-inspired = **saturated neon + Korean folk talisman**. Concretely:

- Palette is loud (rose + violet + gold on near-black) but typography is restrained and ritualistic.
- Decoration comes from public-domain Korean motifs only:
  - 단청 — color logic (rose / violet / gold layering).
  - 부적 — rotated stamps with dashed inner borders.
  - 까치 / 호랑이 / 연꽃 — acceptable as future SVG illustration if needed.
- **Banned**:
  - Any KPDH photo, lyric, character, or trademarked mark.
  - K-pop iconography, idol silhouettes, fan colors as branding.
  - Lifted layouts from copyrighted album sites.
  - Stock "Asian aesthetic" cliches (cherry blossoms, generic kanji, dragon clipart).
- The site reads as a **museum that ships in source code**, not a fan page.

---

## 8. Data rules (carried forward)

- Production images, when reintroduced, must be local under `docs/images/**`.
- Remote URLs belong in `source_url`, never `image_url`.
- If source verification is incomplete, keep an explicit `needs_verification` marker on the artifact.
- Show a photograph only when `exact_image_verified: true` is present on the hero/image record and the file is local under `docs/images/**`.
- For unverified records, render an "IMAGE WITHHELD" panel plus the Han-lang code fallback instead of a photo.
- Current hero status: 8/10 hero photos are exact-image verified; `hero_celadon_maebyeong` and `hero_hunminjeongeum` remain intentionally withheld until exact reusable sources are confirmed.

---

## 9. Direction history

### 2026-04-30 · KPDH-A reset (current)

Replaces the prior "code-first reset" as the live direction, but **retains its core principle**: code is the primary visual. The talisman-ritual layer (neon rose + dark ink + paper cream + heavy 한글 display + dashed seal borders + film grain) is added on top so the page reads as intentional museum design rather than a code dump. The dual GH chips (Museum + Han-lang) and the `schema.hgl` panel are new structural commitments.

### 2026-04-30 · Code-first reset (superseded, principle retained)

The homepage stopped using unverified artifact photographs as the primary visual system. Exact matches can now return as photographs, but only behind the `exact_image_verified` gate; pending objects continue to use Han-lang source blocks and explicit image-withheld states. Rationale: incorrect photographs are more damaging than missing photographs. **This principle is retained under KPDH-A.**

### 2026-04-29 · Phase C hero pages + Phase A featured/rooms entry (superseded)

Earlier direction: museum dark `#0a0a0a`, warm cream `#f5f1e8`, heritage gold `#c9a84c`, institutional blue `#1a3a5c`, Georgia serif headings, Apple SD Gothic Neo body. Featured hero card → hero detail page (full-viewport image + sticky `.hgl` panel) → room cards → graph as "Explore connections". Superseded once it became clear that unverified photographs were the bottleneck and that the language demo job needed equal weight with the archive job.
