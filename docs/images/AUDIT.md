# Artifact Image Audit · 2026-04-30

Generated from `artifacts/heroes/*.json`, `artifacts/national-treasures/*.json`,
`docs/data/image-audit.json`, and `docs/images/` directory scan.

## Summary

- Total artifacts: 74 (10 heroes · 57 national-treasure catalog entries · 7 KDH entries)
- With verified image: 8 (heroes with exact match confirmed)
- With wrong / facsimile image (withheld): 2 (heroes — celadon, hunminjeongeum)
- With image present but license unverified: 57 (all national-treasure catalog entries)
- With no local image file: 7 (all KDH entries)
- Orphan image files (on disk, not referenced by any JSON): 14
- Missing referenced files (JSON path exists, file absent): 0

**Image state key**

| state | meaning |
|---|---|
| `verified` | Exact match confirmed, license clear, safe to display |
| `wrong-image` | File on disk but known to depict a different object |
| `facsimile` | File on disk but confirmed reprint/reproduction, not the original |
| `needs-license` | Image file on disk; `license: needs_verification`, low confidence |
| `no-local-image` | No image file on disk at all |

## Per-artifact table

| id | name | designation | image state | source field | priority for B-track |
|---|---|---|---|---|---|
| hero_baekje_incense_burner | 백제 금동대향로 | 국보 제287호 | verified | commons.wikimedia.org · CC BY-SA 2.5 | OK |
| hero_celadon_maebyeong | 청자 상감운학문 매병 | 국보 제68호 | wrong-image | clevelandart.org · CC0 (similar vase, not Kansong NT68) | P1 (hero) |
| hero_celestial_chart | 천상열차분야지도 각석 | 국보 제228호 | verified | gogung.go.kr · KOGL Type 1 | OK |
| hero_divine_bell | 성덕대왕신종 | 국보 제29호 | verified | commons.wikimedia.org · CC0 | OK |
| hero_genre_album | 김홍도 필 풍속도 화첩 | 보물 제527호 | verified | commons.wikimedia.org · Public domain | OK |
| hero_hunminjeongeum | 훈민정음 해례본 | 국보 제70호 / 유네스코 세계기록유산 | facsimile | commons.wikimedia.org · Public domain (reprint, not original Kansong manuscript) | P1 (hero) |
| hero_moon_jar | 백자 달항아리 | 국보 제310호 | verified | commons.wikimedia.org · KOGL Type 1 | OK |
| hero_pensive_bodhisattva | 금동미륵보살반가사유상 | 국보 제83호 | verified | commons.wikimedia.org · CC BY-SA 4.0 | OK |
| hero_silla_gold_crown | 금관총 금관 | 국보 제87호 | verified | commons.wikimedia.org · KOGL Type 1 | OK |
| hero_tripitaka | 합천 해인사 대장경판 | 국보 제32호 | verified | commons.wikimedia.org · CC0 | OK |
| kdh_001 | 금동미륵보살반가사유상 | 국보 제78호 | no-local-image | emuseum.go.kr · needs_verification | P2 (no-image) |
| kdh_002 | 청동은입사포류수금문정병 | 국보 제92호 | no-local-image | emuseum.go.kr · needs_verification | P2 (no-image) |
| kdh_003 | 금동용두보당 | 국보 제136호 | no-local-image | emuseum.go.kr · needs_verification | P2 (no-image) |
| kdh_004 | 도기 기마인물형 명기 | 국보 제91호 | no-local-image | emuseum.go.kr · needs_verification | P2 (no-image) |
| kdh_005 | 칠지도 | 국보 제369호 | no-local-image | emuseum.go.kr · needs_verification | P2 (no-image) |
| kdh_006 | 금관총 금관 | 국보 제87호 | no-local-image | emuseum.go.kr · needs_verification | P2 (no-image) |
| kdh_007 | 백제 금동대향로 | 국보 제287호 | no-local-image | emuseum.go.kr · needs_verification | P2 (no-image) |
| nb_001 | 흥인지문 | 국보 제1호 | needs-license | emuseum.go.kr · needs_verification, low confidence | P2 (unlicensed) |
| nb_001_2 | 서울 숭례문 | 국보 제1호 | needs-license | emuseum.go.kr · needs_verification, low confidence | P2 (unlicensed) |
| nb_002 | 원각사지십층석탑 | 국보 제2호 | needs-license | emuseum.go.kr · needs_verification, low confidence | P2 (unlicensed) |
| nb_005 | 감은사지동종 | 국보 제5호 | needs-license | emuseum.go.kr · needs_verification, low confidence | P2 (unlicensed) |
| nb_006 | 부석사소조석가여래좌상 | 국보 제6호 | needs-license | emuseum.go.kr · needs_verification, low confidence | P2 (unlicensed) |
| nb_006_2 | 평창대관도 | 국보 제6호 | needs-license | emuseum.go.kr · needs_verification, low confidence | P2 (unlicensed) |
| nb_007 | 부석사석탑 | 국보 제7호 | needs-license | emuseum.go.kr · needs_verification, low confidence | P2 (unlicensed) |
| nb_008 | 흥덕사지현존이층석탑 | 국보 제8호 | needs-license | emuseum.go.kr · needs_verification, low confidence | P2 (unlicensed) |
| nb_009 | 흥왕사지칠층석탑 | 국보 제9호 | needs-license | emuseum.go.kr · needs_verification, low confidence | P2 (unlicensed) |
| nb_009_2 | 용두사지석등 | 국보 제9호 | needs-license | emuseum.go.kr · needs_verification, low confidence | P2 (unlicensed) |
| nb_010 | 정림사지오층석탑 | 국보 제10호 | needs-license | emuseum.go.kr · needs_verification, low confidence | P2 (unlicensed) |
| nb_015 | 금속활자 | 국보 제15호 | needs-license | emuseum.go.kr · needs_verification, low confidence | P2 (unlicensed) |
| nb_016 | 금강문학 | 국보 제16호 | needs-license | emuseum.go.kr · needs_verification, low confidence | P2 (unlicensed) |
| nb_020 | 한석탑 | 국보 제20호 | needs-license | emuseum.go.kr · needs_verification, low confidence | P2 (unlicensed) |
| nb_021 | 불국사석가탑 | 국보 제21호 | needs-license | emuseum.go.kr · needs_verification, low confidence | P2 (unlicensed) |
| nb_022 | 불국사다보탑 | 국보 제22호 | needs-license | emuseum.go.kr · needs_verification, low confidence | P2 (unlicensed) |
| nb_023 | 금은화혜 | 국보 제23호 | needs-license | emuseum.go.kr · needs_verification, low confidence | P2 (unlicensed) |
| nb_030 | 신라인서 | 국보 제30호 | needs-license | emuseum.go.kr · needs_verification, low confidence | P2 (unlicensed) |
| nb_031 | 첨성대 | 국보 제31호 | needs-license | emuseum.go.kr · needs_verification, low confidence | P2 (unlicensed) |
| nb_032 | 팔만대장경 | 국보 제32호 | needs-license | emuseum.go.kr · needs_verification, low confidence | P2 (unlicensed) |
| nb_033 | 신라연화문비단 | 국보 제33호 | needs-license | emuseum.go.kr · needs_verification, low confidence | P2 (unlicensed) |
| nb_037 | 평산토기 | 국보 제37호 | needs-license | emuseum.go.kr · needs_verification, low confidence | P2 (unlicensed) |
| nb_038 | 황토기기 | 국보 제38호 | needs-license | emuseum.go.kr · needs_verification, low confidence | P2 (unlicensed) |
| nb_041 | 경복사지철기 | 국보 제41호 | needs-license | emuseum.go.kr · needs_verification, low confidence | P2 (unlicensed) |
| nb_045 | 백제무녕왕릉석곽 | 국보 제45호 | needs-license | emuseum.go.kr · needs_verification, low confidence | P2 (unlicensed) |
| nb_061 | 고려사찰벽화 | 국보 제61호 | needs-license | emuseum.go.kr · needs_verification, low confidence | P2 (unlicensed) |
| nb_065 | 청자어패문항아리 | 국보 제65호 | needs-license | emuseum.go.kr · needs_verification, low confidence | P2 (unlicensed) |
| nb_066 | 청자상감학문호 | 국보 제66호 | needs-license | emuseum.go.kr · needs_verification, low confidence | P2 (unlicensed) |
| nb_067 | 분청사자수도완 | 국보 제67호 | needs-license | emuseum.go.kr · needs_verification, low confidence | P2 (unlicensed) |
| nb_068 | 금동대향로 | 국보 제68호 | needs-license | emuseum.go.kr · needs_verification, low confidence | P2 (unlicensed) |
| nb_069 | 백자병 | 국보 제69호 | needs-license | emuseum.go.kr · needs_verification, low confidence | P2 (unlicensed) |
| nb_071 | 금책 | 국보 제71호 | needs-license | emuseum.go.kr · needs_verification, low confidence | P2 (unlicensed) |
| nb_078 | 금동미륵보살반가사유상 | 국보 제78호 | needs-license | emuseum.go.kr · needs_verification, low confidence | P2 (unlicensed) |
| nb_079 | 낙엽호랑이 | 국보 제79호 | needs-license | emuseum.go.kr · needs_verification, low confidence | P2 (unlicensed) |
| nb_080 | 칠성도 | 국보 제80호 | needs-license | emuseum.go.kr · needs_verification, low confidence | P2 (unlicensed) |
| nb_081 | 호랑이그림 | 국보 제81호 | needs-license | emuseum.go.kr · needs_verification, low confidence | P2 (unlicensed) |
| nb_082 | 용왕상 | 국보 제82호 | needs-license | emuseum.go.kr · needs_verification, low confidence | P2 (unlicensed) |
| nb_083 | 금동미륵보살반가사유상 | 국보 제83호 | needs-license | emuseum.go.kr · needs_verification, low confidence | P2 (unlicensed) |
| nb_085 | 가야금관 | 국보 제85호 | needs-license | emuseum.go.kr · needs_verification, low confidence | P2 (unlicensed) |
| nb_086 | 남기고분금관 | 국보 제86호 | needs-license | emuseum.go.kr · needs_verification, low confidence | P2 (unlicensed) |
| nb_087 | 신라금관 | 국보 제87호 | needs-license | emuseum.go.kr · needs_verification, low confidence | P2 (unlicensed) |
| nb_088 | 금관총금관 | 국보 제88호 | needs-license | emuseum.go.kr · needs_verification, low confidence | P2 (unlicensed) |
| nb_089 | 금동관음보살좌상 | 국보 제89호 | needs-license | emuseum.go.kr · needs_verification, low confidence | P2 (unlicensed) |
| nb_090 | 금동아미타여래좌상 | 국보 제90호 | needs-license | emuseum.go.kr · needs_verification, low confidence | P2 (unlicensed) |
| nb_091 | 금동보살머리장식 | 국보 제91호 | needs-license | emuseum.go.kr · needs_verification, low confidence | P2 (unlicensed) |
| nb_092 | 청동은입사포류수금문정병 | 국보 제92호 | needs-license | emuseum.go.kr · needs_verification, low confidence | P2 (unlicensed) |
| nb_113 | 마애여래삼존상 | 국보 제113호 | needs-license | emuseum.go.kr · needs_verification, low confidence | P2 (unlicensed) |
| nb_121 | 금동약사여래좌상 | 국보 제121호 | needs-license | emuseum.go.kr · needs_verification, low confidence | P2 (unlicensed) |
| nb_122 | 금동아미타여래입상 | 국보 제122호 | needs-license | emuseum.go.kr · needs_verification, low confidence | P2 (unlicensed) |
| nb_124 | 신라금관 | 국보 제124호 | needs-license | emuseum.go.kr · needs_verification, low confidence | P2 (unlicensed) |
| nb_129 | 고려명종명성왕후묘지 | 국보 제129호 | needs-license | emuseum.go.kr · needs_verification, low confidence | P2 (unlicensed) |
| nb_131 | 조선왕조실록 | 국보 제131호 | needs-license | emuseum.go.kr · needs_verification, low confidence | P2 (unlicensed) |
| nb_132 | 동아시아서예발파도 | 국보 제132호 | needs-license | emuseum.go.kr · needs_verification, low confidence | P2 (unlicensed) |
| nb_136 | 금동용두보당 | 국보 제136호 | needs-license | emuseum.go.kr · needs_verification, low confidence | P2 (unlicensed) |
| nb_197 | 궁예릉 | 국보 제197호 | needs-license | emuseum.go.kr · needs_verification, low confidence | P2 (unlicensed) |
| nb_287 | 백제금동대향로 | 국보 제287호 | needs-license | emuseum.go.kr · needs_verification, low confidence | P2 (unlicensed) |
| nb_531 | 아미타쌍상도 | 국보 제531호 | needs-license | emuseum.go.kr · needs_verification, low confidence | P2 (unlicensed) |

## Wrong / uncertain photos (action items for B-track)

### P1 — Hero cards with images that must NOT be displayed

- **hero_celadon_maebyeong** (`images/heroes/hero_celadon_maebyeong/celadon-cloud-crane.jpg`)
  - Source: Cleveland Museum of Art (CC0), `https://www.clevelandart.org/art/1921.634`
  - Reason: Similar Goryeo cloud-and-crane maebyeong, NOT confirmed as the Kansong NT68 object.
  - JSON flag: `exact_image_verified: false`, `needs_verification` populated, `display: withheld`
  - Action: Locate a reusable image of the exact Kansong Art Museum NT68 specimen, or obtain permission.

- **hero_hunminjeongeum** (`images/heroes/hero_hunminjeongeum/hunminjeongeum-haerye.jpg`)
  - Source: Wikimedia Commons (Public domain), `https://commons.wikimedia.org/wiki/File:Hunminjeongeum_Haerye_10.jpg`
  - Reason: Image is a Kyujanggak/SNU reprint facsimile, not the original Kansong Haerye manuscript.
  - JSON flag: `exact_image_verified: false`, `needs_verification` populated, `display: withheld`
  - Action: Source a reusable photograph of the original Kansong manuscript, or relabel as "reprint edition" with clear disclosure.

### P2 — National treasure catalog: all 57 nb_ entries

All 57 `nb_*` artifacts have:
- Image file present on disk (`docs/images/artifacts/PS01002001_*.jpg`)
- `license: "needs_verification"` — no confirmed reuse rights
- `confidence: "low"` — sourced via e뮤지엄 Open API fallback, not from authoritative cultural-heritage API with explicit license grants
- `credit: "Museum as Code local artifact image; original source requires verification"`

B-track must either:
1. Confirm e뮤지엄 images are reusable under KOGL or equivalent, or
2. Replace with Wikimedia Commons / official CHA/NRICH images that carry explicit free licenses.

### P2 — KDH entries: all 7 kdh_ entries

All 7 `kdh_*` artifacts have no local image file whatsoever. B-track must source and download images.

| kdh id | name | designation | suggested source |
|---|---|---|---|
| kdh_001 | 금동미륵보살반가사유상 | 국보 제78호 | commons.wikimedia.org (multiple CC images exist) |
| kdh_002 | 청동은입사포류수금문정병 | 국보 제92호 | national.museum.go.kr or Wikimedia |
| kdh_003 | 금동용두보당 | 국보 제136호 | national.museum.go.kr |
| kdh_004 | 도기 기마인물형 명기 | 국보 제91호 | commons.wikimedia.org |
| kdh_005 | 칠지도 | 국보 제369호 | commons.wikimedia.org (Shōsōin mirror, verify) |
| kdh_006 | 금관총 금관 | 국보 제87호 | commons.wikimedia.org (KOGL image exists) |
| kdh_007 | 백제 금동대향로 | 국보 제287호 | commons.wikimedia.org CC BY-SA 2.5 exists |

## Data quality notes

The following internal JSON inconsistencies were detected during audit (read-only observation, not fixed):

- `nb_003.json` has `id: "nb_001"` internally (file name vs JSON id mismatch) → manifested as `nb_001_2` in pipeline output.
- `nb_039.json` has `id: "nb_006"` internally (duplicate designation 국보 제6호) → manifested as `nb_006_2`.
- `nb_040.json` has `id: "nb_009"` internally (duplicate designation 국보 제9호) → manifested as `nb_009_2`.
- `nb_004.json` has `id: "nb_005"` internally (file nb_004 → internal id nb_005).
- Several national treasure names appear transliterated or mixed-script (e.g., `浮石寺石탑`, `高麗寺壁画`); Korean-only names should be used throughout.

## Orphan files

Files present in `docs/images/` with no corresponding `image_local` / `image_url` reference in any artifact JSON:

**Hero image-sources.json sidecars (10 files)** — metadata, not images; safe to keep:
- `docs/images/heroes/hero_baekje_incense_burner/image-sources.json`
- `docs/images/heroes/hero_celadon_maebyeong/image-sources.json`
- `docs/images/heroes/hero_celestial_chart/image-sources.json`
- `docs/images/heroes/hero_divine_bell/image-sources.json`
- `docs/images/heroes/hero_genre_album/image-sources.json`
- `docs/images/heroes/hero_hunminjeongeum/image-sources.json`
- `docs/images/heroes/hero_moon_jar/image-sources.json`
- `docs/images/heroes/hero_pensive_bodhisattva/image-sources.json`
- `docs/images/heroes/hero_silla_gold_crown/image-sources.json`
- `docs/images/heroes/hero_tripitaka/image-sources.json`

**Release preview screenshots (4 files)** — documentation assets, safe to keep:
- `docs/images/release-2026-04-30/hero-celadon-desktop.png`
- `docs/images/release-2026-04-30/hero-pensive-desktop.png`
- `docs/images/release-2026-04-30/home-desktop.png`
- `docs/images/release-2026-04-30/home-mobile.png`
