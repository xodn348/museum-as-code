# Museum as Code Design System

**Updated:** 2026-04-29  
**Scope:** Phase C hero pages + Phase A featured/rooms entry.

## Product direction

Museum as Code should feel less like a catalog and more like a sequence of curated rooms. The graph remains available as an expert exploration tool, but the first impression is now:

1. Featured hero artifacts
2. Curated rooms
3. All artifacts
4. Explore connections

## Color

- Museum dark: `#0a0a0a` / `#090909`
- Warm cream text: `#f5f1e8`
- Heritage gold: `#c9a84c`
- Existing institutional blue: `#1a3a5c`
- Paper background: `#f5f1e8`

Use dark backgrounds for immersive single-object storytelling. Use paper backgrounds for room navigation and broad collection browsing.

## Typography

- Narrative headings: Georgia / serif fallback.
- Interface and Korean body text: Apple SD Gothic Neo / Noto Sans KR / system sans.
- `.hgl` code: JetBrains Mono / SFMono / Menlo / monospace.

## Components

### Featured hero card

Large image-first card with dark gradient, room label, English/Korean title, and one-sentence hook. It links directly to `hero.html?id=<hero_id>`.

### Hero detail page

Vertical single-object page:

1. Full-viewport object image
2. Metadata strip
3. Three curator sections
4. Sticky `.hgl` source panel
5. License/credit footer and next/previous hero links

### Room card

Paper-background card grouping hero pages by theme. Room cards are a bridge between curated storytelling and the broader collection.

### Graph

The graph is now “Explore connections.” Node labels should remain visible even when image thumbnails are present.

## Motion

Use restrained fade/scale only. Avoid decorative animation that competes with the object.

## Data rules

- Production images must be local under `docs/images/**`.
- Remote URLs belong in `source_url`, never `image_url`.
- If source verification is incomplete, keep an explicit `needs_verification` marker.

## 2026-04-30 Code-first redesign reset

The homepage no longer uses artifact photographs as the primary visual system. Until exact image/object matches are verified, the public entry experience uses Han-lang source blocks as the visual signature:

- Homepage hero: live `.hgl` preview + GitHub CTA.
- Featured heroes: 10 code cards, no photo thumbnails.
- Rooms: code-snippet links instead of image strips.
- Archive cards: generated Han-like source plates instead of potentially mismatched images.
- Graph: labeled code-style nodes, no photo node backgrounds.

Rationale: incorrect photographs are more damaging than missing photographs. The design now makes provenance and source structure visible first; photos can be reintroduced per object only after exact source/license matching.
