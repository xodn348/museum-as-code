# Hero Artifacts × 10 — Phase C1 Selection

**Created:** 2026-04-29  
**Updated:** 2026-04-29  
**Plan:** `plans/2026-04-29-redesign-c-b-a.md` (Phase C1)  
**Status:** ✅ Implemented — latest user instruction overrode the review gate and requested C→B→A execution  
**Mode:** Codex-only parallel research. Claude was not used.

---

## Phase C1 gate

Phase C originally required approval for this list; the latest user instruction requested direct C→B→A execution, so these recommended defaults were implemented. The goal is **10 carefully curated hero artifacts**, not a broad catalog. Each later hero page must be backed by verified metadata, local images, license/credit sidecars, English curator copy, and `.hgl` source.

**Approval defaults recommended below:**

- Keep the hero set at **10**, not 12.
- Use **National Treasure No. 83** for the pensive bodhisattva.
- Use a **moon jar with safer public/NMK-family sourcing**; verify the exact National Treasure number during C2 before publishing.
- Treat **Danwon Genre Album** as one hero slot with 2–3 representative paintings inside the page.
- Use semantic IDs such as `hero_pensive_bodhisattva`.

---

## Selection principles

1. **Memorability for non-Korean visitors** — an object a foreign visitor can remember as “Korea = this.”
2. **Visual impact** — strong enough to carry a full dark hero page.
3. **Historical arc** — Three Kingdoms → Unified Silla → Goryeo → Joseon.
4. **Medium diversity** — sculpture, ceramics, metalwork, sound, print/records, astronomy, painting.
5. **Source viability** — likely local-image path from Wikimedia Commons, Korea Heritage Service, national museums, or other open/public sources.
6. **Han-language fit** — at least one artifact must make the `.hgl`/writing-system signature feel conceptually native, not decorative.

---

## Recommended final 10

| # | ID | Korean name | English working title | Designation | Period | Medium | Holding institution / site | Why this belongs in the first 10 |
|---:|---|---|---|---|---|---|---|---|
| 1 | `hero_pensive_bodhisattva` | 금동미륵보살반가사유상 | Pensive Bodhisattva | National Treasure No. 83 | Three Kingdoms, early 7th c. | Gilt bronze | National Museum of Korea | The essential opening hero: a single calm silhouette, a globally legible pose, and the “thousand-year smile” of Korean Buddhist sculpture. |
| 2 | `hero_celadon_maebyeong` | 청자 상감운학문 매병 | Celadon Prunus Vase with Inlaid Cloud and Crane Design | National Treasure No. 68 | Goryeo, 12th c. | Inlaid celadon | Kansong Art Museum | The clearest icon of Goryeo celadon: jade color, crane/cloud rhythm, and a profile that can become a visual identity system. |
| 3 | `hero_moon_jar` | 백자 달항아리 | White Porcelain Moon Jar | National Treasure candidate: No. 310 / public-source equivalent to verify | Joseon, 17th–18th c. | White porcelain | Verify during C2 | Joseon minimalism in one object: asymmetry, restraint, white space, and a form international visitors already associate with Korean design. |
| 4 | `hero_hunminjeongeum` | 훈민정음 해례본 | Hunminjeongeum Manuscript (Haerye Edition) | National Treasure No. 70 / UNESCO Memory of the World | Joseon, 1446 | Printed book / paper | Kansong Art Museum | The conceptual bridge to Han `.hgl`: Korea’s writing system explained by its creators, making language itself a museum object. |
| 5 | `hero_silla_gold_crown` | 금관총 금관 | Gold Crown from Geumgwanchong Tomb | National Treasure No. 87 | Silla, 5th c. | Gold and jade | National Museum of Korea | Immediate “wow” factor: royal gold, tree/antler uprights, jade pendants, and a compact story of Silla ritual kingship. |
| 6 | `hero_baekje_incense_burner` | 백제 금동대향로 | Great Gilt-bronze Incense Burner of Baekje | National Treasure No. 287 | Baekje, 6th–7th c. | Gilt bronze | Buyeo National Museum | A complete cosmology in one object: dragon, lotus, mountain, phoenix, musicians, immortals, animals, Buddhism, and Daoism. |
| 7 | `hero_divine_bell` | 성덕대왕신종 (에밀레종) | Divine Bell of King Seongdeok | National Treasure No. 29 | Unified Silla, 771 | Bronze bell | Gyeongju National Museum | Adds scale and sound: a monumental bell whose reliefs, inscription, resonance, and legend can make the page feel alive. |
| 8 | `hero_tripitaka` | 합천 해인사 대장경판 (팔만대장경) | Printing Woodblocks of the Tripiṭaka Koreana | National Treasure No. 32 / UNESCO heritage context | Goryeo, 1236–1251 | Woodblocks | Haeinsa Temple | Code-before-code: 80,000+ precision-carved blocks, mass knowledge preservation, and a natural partner to `.hgl` as executable cultural memory. |
| 9 | `hero_celestial_chart` | 천상열차분야지도 각석 | Stone Constellation Chart (Cheonsang Yeolcha Bunyajido) | National Treasure No. 228 | Joseon, 1395 | Stone engraving | National Palace Museum of Korea | Science and sovereignty in stone: a star map that turns the hero page from object-viewing into sky-reading. |
| 10 | `hero_genre_album` | 김홍도 필 풍속도 화첩 / 단원풍속도첩 | Album of Genre Paintings by Kim Hong-do (Danwon) | **Treasure No. 527** | Joseon, 18th c. | Ink and light color on paper | National Museum of Korea | Keeps the set human: ordinary people, labor, play, humor, and motion — a needed counterweight to royal and sacred objects. |

---

## Corrections made from the seed plan

- `hero_genre_album` is **Treasure No. 527**, not National Treasure No. 527.
- `hero_moon_jar` should not be published with a fixed number/holding institution until C2 confirms the safest image/license path. National Treasure No. 310 is the current working preference, but the implementation may choose a public-source equivalent if licensing is stronger.
- The C1 list stays faithful to the original C→B→A plan instead of swapping in visually strong alternatives such as Hahoe masks, horse-and-rider vessels, or Gyeongcheonsa pagoda. Those remain Phase A/B expansion candidates.

---

## Coverage check

### Period

- Three Kingdoms / Baekje / Silla: 1, 5, 6
- Unified Silla: 7
- Goryeo: 2, 8
- Joseon: 3, 4, 9, 10

### Medium / genre

- Buddhist sculpture: 1
- Ceramics: 2, 3
- Metalwork / royal craft / ritual sound: 5, 6, 7
- Writing / printing / records: 4, 8
- Science / astronomy: 9
- Painting / daily life: 10

### Visitor rhythm for the final page set

1. Quiet face — bodhisattva  
2. Ceramic atmosphere — celadon  
3. Minimal white space — moon jar  
4. Language/code — Hunminjeongeum  
5. Gold spectacle — Silla crown  
6. Mythic density — Baekje incense burner  
7. Sound/scale — Divine Bell  
8. Knowledge archive — Tripiṭaka Koreana  
9. Cosmos/science — celestial chart  
10. Human life — Danwon genre album

---

## C2 source leads to verify next

These are leads, not publish-ready license claims. C2 must download local images and write `license`, `source_url`, and `credit` sidecars.

| ID | Metadata/source leads | Image/license notes for C2 |
|---|---|---|
| `hero_pensive_bodhisattva` | National Museum of Korea collection highlight; Met essay for international framing | NMK download/credit route likely; verify KOGL/public terms before local use. |
| `hero_celadon_maebyeong` | Kansong/Korea Heritage references; public descriptions widely available | Kansong image licensing may be constrained; Wikimedia/open alternatives must be checked carefully. |
| `hero_moon_jar` | Korea Heritage/NMK moon jar records | Prefer the moon jar with the cleanest public image license, even if the final designation shifts from No. 310. |
| `hero_hunminjeongeum` | Korea Heritage Service UNESCO page; UNESCO nomination PDF; Wikimedia category | Likely text/page scans available; verify whether Commons file license is acceptable. |
| `hero_silla_gold_crown` | NMK/Gyeongju National Museum materials | Verify whether Geumgwanchong crown images can be locally hosted; if blocked, consider Cheonmachong crown only with approval. |
| `hero_baekje_incense_burner` | Buyeo National Museum representative-object page; NMK essay; Wikimedia file lead | Strong candidate for verified Commons or museum source. |
| `hero_divine_bell` | Gyeongju National Museum permanent exhibition page; Wikimedia category | Strong candidate for local image sourcing from Commons or museum source. |
| `hero_tripitaka` | Korea Heritage/Haeinsa/UNESCO context | Likely architectural/block images; ensure the page emphasizes woodblocks, not only the depository. |
| `hero_celestial_chart` | National Palace Museum catalogue / Korea Heritage references | Need careful image-rights verification; source may be catalogue PDF or museum image. |
| `hero_genre_album` | NMK collection pages for individual album leaves; Korea Heritage record | NMK pages provide per-leaf metadata; choose 2–3 representative leaves for the hero page. |

---

## User review requested

Please approve or correct these five C1 decisions:

1. **Pensive Bodhisattva:** keep National Treasure No. 83? *(recommended: yes)*
2. **Moon jar:** allow C2 to choose the safest public-license moon jar image, even if the exact National Treasure number changes? *(recommended: yes)*
3. **Gold crown:** keep Geumgwanchong National Treasure No. 87, not switch to Cheonmachong No. 188? *(recommended: keep No. 87 for plan fidelity)*
4. **Genre painting:** use Danwon Genre Album as one slot, with 2–3 representative leaves? *(recommended: yes)*
5. **Set size:** keep exactly 10 for Phase C? *(recommended: yes)*

After approval, C2 should start with `hero_pensive_bodhisattva` and establish the local image + license + JSON/HGL/copy pattern before fanning out the remaining nine.
