# Museum as Code — Redesign Plan (C → B → A)

**Created:** 2026-04-29
**Audience:** 국립중앙박물관을 방문하고 싶지만 갈 수 없는 외국인 방문자
**Differentiator:** Han 언어(.hgl)로 작성된 코드가 매체이자 시각적 시그니처
**Repo:** https://github.com/xodn348/museum-as-code

---

## Why this order (C → B → A)

현재 사이트의 핵심 문제는 "양은 많은데 각각이 부실"하다는 것:
- 57개 국보 모두 fallback 데이터(이름 깨짐, 중복, 의심스러운 항목)
- 이미지가 e뮤지엄 hotlink → 차단되어 무관한 이미지(공지/광고) 표시
- 그래프가 입구로 잡혀있어 첫 방문자 경험이 카탈로그 같음

**C(범위 축소+깊이) 먼저** → 히어로 10~12점만 손으로 정확히, 몰입형 단일 페이지로 만든다. 한 점이 잘 만들어지면 그게 나머지의 템플릿이 된다.
**B(데이터 기반)** → C에서 검증된 데이터 수집/정제 패턴을 자동화. 나머지 47점도 정상 데이터로 채운다.
**A(갤러리 재설계)** → 데이터가 신뢰 가능해진 후, 테마 룸 큐레이션/그래프 보조탭으로 전체 UX 재구성.

---

## Phase C — Hero artifacts × 10 (가장 시급, 2~3일)

### C1. 히어로 유물 10점 선정 (Day 1, 30분)
**선정 기준:** 외국인이 "한국 = 이것"이라고 기억하면 좋을 작품 / 시각적 임팩트 / 시대·재질·문화권 다양성

**제안 리스트 (확정 전 검토 필요):**
1. **금동미륵보살반가사유상** (국보 78호 또는 83호) — 한국 불교조각의 정수
2. **청자 상감운학문 매병** (국보 68호) — 고려청자의 대표
3. **백자 달항아리** (국보 309호 등) — 조선 미니멀리즘
4. **훈민정음 해례본** (국보 70호) — 한글 창제 원본, Han 언어 프로젝트와 사상적 연결
5. **금관총 금관** (국보 87호) — 신라 황금문화
6. **백제 금동대향로** (국보 287호) — 백제 공예 정점
7. **신라 성덕대왕신종(에밀레종)** (국보 29호) — 음향·주조기술
8. **고려 팔만대장경** (국보 32호) — 세계기록유산
9. **천상열차분야지도** (국보 228호) — 천문학 유산
10. **반가사유상의 미소** 또는 **김홍도 풍속화첩** (국보 527호) — 회화 1점 추가

**Deliverable:** `plans/hero-artifacts.md` — 10점 확정 리스트 + 각 유물의 "왜 이걸 골랐나" 1줄

### C2. 이미지·메타데이터 수급 (Day 1~2, 6시간)
각 유물별로:
- **고해상도 이미지 1~3장** — 우선순위: ① Wikimedia Commons (PD-Korea 또는 CC), ② 국립중앙박물관 공공누리 1유형, ③ Smithsonian Open Access (호암미술관 등 협력 소장품)
- **원본 라이선스/출처 명시** (sidecar JSON에 `license`, `source_url`, `credit` 필드)
- **로컬 다운로드 → `docs/images/heroes/<id>/`**, hotlink 절대 금지
- **메타데이터 정확화** — 한자 표기, 영문 공식명(국립중앙박물관 영문 도록 기준), 시대(서기 연도 포함), 재질, 크기(미터/센티), 소장처

**Deliverable:** `artifacts/heroes/<id>.json` × 10, `docs/images/heroes/<id>/*.jpg` 검증된 이미지

### C3. 영문 큐레이터 카피 (Day 2, 4시간)
유물 1점당 **3섹션, 총 ~400단어 영문**:
1. **Why this matters** (1단락) — 외국인이 "왜 봐야 하는가"
2. **What you're looking at** (1~2단락) — 형태·기법·도상의 핵심 포인트
3. **The story** (1단락) — 만들어진 시대 배경·인물·전설

작성 절차: AI 초안 (Claude) → 1차 자체 검수 → 박물관 영문 공식 자료(`emuseum.go.kr/en`, 도록 PDF) 대조 검증 → 사실관계만 확정. 수사적 표현은 자유.

**Deliverable:** `artifacts/heroes/<id>.md` × 10 (frontmatter에 `lang: en`)

### C4. Han `.hgl` 소스 정제 (Day 2, 2시간)
각 유물의 `.hgl`을 **사람이 읽기 좋게** 손질:
- 필드명 일관성 (`이름`, `영문명`, `시대`, `재질`, `크기`, `소장처`, `제작연도`, `의의`)
- 주석으로 시적인 한 줄 추가 가능 (`// 천 년의 미소를 머금은 보살`)
- syntax highlighting이 잘 보이도록 들여쓰기 정리

**Deliverable:** `artifacts/heroes/<id>.hgl` × 10, `hgl check` 통과

### C5. 몰입형 유물 페이지 컴포넌트 (Day 2~3, 8시간)
신규 라우트: `/hero/<id>` (또는 `?artifact=<id>`)

**페이지 구조 (위→아래 스크롤):**
1. **Hero shot** — 풀스크린 다크 배경, 유물 이미지 가운데, 페이드인. 우측 상단에 유물 이름(한/영 토글)
2. **Why this matters** 섹션 — 큰 영문 한 단락, 사이드에 작은 디테일 이미지
3. **What you're looking at** — 좌: 큰 이미지 + 핫스팟 라벨(선택), 우: 영문 설명
4. **The story** — 타임라인 또는 지도 위 위치 표시(Optional, Phase A로 미뤄도 됨)
5. **"이 유물의 소스 코드" / "Source code of this artifact"** — `.hgl` 코드를 전폭 패널로 syntax-highlighted 렌더링. 스크롤 sticky로 시각적 시그니처
6. **Footer** — 라이선스/출처/credit, 다음 유물 버튼

**디자인 톤:**
- 다크 배경(#0a0a0a) + 크림 텍스트(#f5f1e8) — 박물관 조명 느낌
- 세리프 영문 (예: EB Garamond, Cormorant) for narrative
- 한글은 본명조 / Apple SD Gothic
- 코드 블록은 등폭(JetBrains Mono) + 한국어 키워드 컬러
- 모션은 절제 — fade/parallax 정도, 화려한 애니메이션 금지

**구현:**
- 기존 `docs/index.html`은 건드리지 않고, 새로 `docs/hero.html` + `docs/hero.js` + `docs/hero.css` 생성 (혹은 기존 SPA에 라우트 추가)
- Phase A에서 통합 결정

**Deliverable:** 10개 유물 페이지 모두 로컬 `python -m http.server` 또는 `npx serve docs`로 시연 가능

### C6. 입구 변경 (Day 3, 1시간)
현재 `index.html`의 기본 탭을 그래프에서 **"Featured Artifacts" 갤러리**로 변경.
- 10개 유물의 큰 카드(이미지 + 이름 + 1줄 영문 후크) 그리드
- 클릭 → 위 C5 몰입형 페이지로
- 기존 그래프/카드 탭은 "All artifacts" 보조 탭으로 유지 (Phase B 후 정상 데이터로)

**Deliverable:** 사이트 첫 화면이 카탈로그가 아닌 갤러리

### C7. 검증 + 배포 (Day 3, 1시간)
- 모바일/데스크톱 반응형 (브라우저 dev tools)
- 영어/한국어 토글 모든 페이지에서 작동
- Lighthouse 성능/접근성 90+
- `gh-pages` 배포 후 실제 URL에서 확인
- `/qa` 또는 `/design-review` skill로 자동 검수

**Deliverable:** main 머지, GitHub Pages 배포, 시연 URL

---

## Phase B — Data foundation (Phase C 검증 후, 3~4일)

### B1. 데이터 소스 결정
- **e뮤지엄 OpenAPI 정상화** 시도 → 공공데이터포털 키 재발급, `pipeline/api_client.py` 디버깅
- 동시에 **Wikimedia Commons API**(`MediaWiki API`)로 국보 이미지 일괄 수집 파이프라인
- 두 소스를 **병합**: 메타는 e뮤지엄, 이미지는 Wikimedia 우선

### B2. 데이터 스키마 정규화
- 현재 `.json` 사이드카에 `license`, `source_url`, `credit`, `confidence` 필드 추가
- `source: "fallback"` 항목 모두 제거 또는 재수집
- 중복 detect (`금동미륵보살반가사유상`, `신라금관` 등) → merge 또는 별도 ID 부여

### B3. 이미지 자산 파이프라인
- `pipeline/download_images.py` 강화: 라이선스 검증 → 로컬 다운로드 → WebP 변환 → 다중 해상도(thumbnail/medium/full) → manifest 갱신
- `docs/images/`를 정식 자산으로 (현재 1개뿐)
- CDN 또는 Git LFS 검토 (이미지 크기에 따라)

### B4. Han `.hgl` 일괄 재생성
- 정제된 데이터로 템플릿 재실행 → 57개 모두 정확한 `.hgl`
- `hgl check` CI 통과
- 보물(treasures) 컬렉션도 시작 (현재 0개)

### B5. CI/품질 게이트
- GitHub Action으로: `.hgl` syntax check, JSON schema validation, broken image link 검출, 라이선스 누락 검출
- PR마다 실행

**Deliverable:** 신뢰 가능한 데이터 베이스 위에서 다음 단계 가능

---

## Phase A — Gallery redesign (Phase B 후, 4~5일)

### A1. 테마 룸 설계
"Rooms" 패러다임:
- **Buddhist Sculpture** — 반가사유상, 보살상 등
- **Goryeo Celadon** — 청자, 도자기
- **Joseon Court** — 백자, 의궤, 어진
- **Three Kingdoms Gold** — 신라 금관, 백제 금공예
- **Records & Writing** — 훈민정음, 팔만대장경, 천상열차분야지도
- **Painting** — 김홍도, 신윤복, 정선

각 룸:
- 가로 스크롤 또는 매스컬링 그리드
- 룸 입구에 "큐레이터 노트" (룸 자체의 1단락 영문 인트로)
- 룸 안에서 유물 클릭 → C5 몰입형 페이지

### A2. 그래프 강등
- 그래프는 "Explore connections" 보조 탭으로 (전문가 도구 톤)
- 가시성 개선: 노드 라벨 항상 표시(현재 hover만), edge 색상 의미 범례, zoom-to-fit, 카테고리 필터 강화
- 또는 그래프 자체 폐기 검토 (사용자 가치 vs 유지비용)

### A3. 인덱스 페이지 통합
- 첫 화면: Featured(C에서) + Rooms(A에서) + (선택) Connections
- 영문/한글 토글 글로벌 유지

### A4. 디자인 시스템 문서화
`DESIGN.md` 작성 (Phase A 완료 시점) — 색상, 타이포, 모션, 컴포넌트 카탈로그. 향후 보물 컬렉션 추가 시 일관성 유지용.

**Deliverable:** 디지털 박물관 v1.0

---

## 작업 규칙

1. **Phase C가 끝나기 전엔 Phase B/A 손대지 않는다.** 한 점이라도 완성도 있게 만드는 게 우선.
2. **이미지는 무조건 로컬 다운로드 + 라이선스 명시.** Hotlink 절대 금지.
3. **데이터에 의심이 가면 박물관 공식 영문 자료(emuseum.go.kr/en) 대조 후 확정.** AI 추정으로 게시 금지.
4. **Phase C 각 유물 페이지가 완성될 때마다 PR로 머지** (10번의 작은 PR > 1번의 거대한 PR).
5. **`/go` skill로 ship.** verify (lint/test/browser) → simplify → push → PR.
6. **Phase 종료 시점마다 `/design-review` 또는 `/qa` 자동 검수.**

---

## 첫 실행 단계 (이 plan을 받은 다른 탭이 할 일)

1. 이 plan 읽기: `~/code/museum-as-code/plans/2026-04-29-redesign-c-b-a.md`
2. **C1부터 시작**: 히어로 유물 10점 확정 → `plans/hero-artifacts.md` 생성, 사용자 승인 받기
3. C2: 첫 1점(추천: **금동미륵보살반가사유상 국보 83호**)으로 데이터/이미지 수급 + Wikimedia Commons 활용 패턴 검증
4. C3~C5: 그 1점에 대해 카피 + .hgl + 페이지 끝까지 만들어 시연 → **사용자 리뷰 후** 나머지 9점 병렬 진행 (`/sisyphus` 또는 worktree 분할)
5. C6~C7: 입구 변경 + 배포

**프로세스 권장:** `/prometheus`로 상세 task 분해 → `/sisyphus`로 병렬 실행 → 각 유물 완성 시 `/go`.
