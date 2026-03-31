# Museum-as-Code: GitHub Pages 배포

## TL;DR

> **Quick Summary**: museum-as-code 프로젝트를 GitHub Pages 프로젝트 사이트(`xodn348.github.io/museum-as-code/`)에 배포. `docs/` + `artifacts/`를 GitHub Actions로 병합 배포하고, 서브패스 리다이렉트 버그를 수정.
> 
> **Deliverables**:
> - 404.html 서브패스 리다이렉트 수정
> - GitHub Actions 배포 워크플로우 (`.github/workflows/deploy.yml`)
> - GitHub 원격 저장소 생성 및 연결
> - Pages 활성화 및 라이브 사이트 검증
> 
> **Estimated Effort**: Short (30-60분)
> **Parallel Execution**: YES - 2 waves
> **Critical Path**: Task 1,2 (parallel) → Task 3 → Task 4 → Task 5

---

## Context

### Original Request
사용자가 museum-as-code 프로젝트를 GitHub Pages에 배포하고 싶어함. 이미 `xodn348.github.io` 유저 사이트가 운영 중이므로, **프로젝트 사이트**(`xodn348.github.io/museum-as-code/`)로 배포하여 기존 사이트를 덮어쓰지 않아야 함.

### Interview Summary
**Key Discussions**:
- GitHub Pages 프로젝트 사이트는 유저 사이트와 독립적으로 운영 가능 — 충돌 없음
- `docs/`와 `artifacts/`가 분리되어 있어 GitHub Actions로 병합 배포 필요
- app.js의 `fetchWithFallback`는 `./artifacts/...` 경로를 사용하므로 artifacts/가 배포 루트에 있으면 수정 불필요

**Research Findings (Metis)**:
- 404.html 라인 6, 9에 `/` 하드코딩 → `/museum-as-code/`로 수정 필요
- app.js 수정 불필요 — `normalizePath()`가 `./` 접두사를 붙여 상대경로로 해결
- `.nojekyll` 파일이 이미 `docs/`에 존재 — 배포 루트에도 복사 필요
- manifest.json에 `nb_001` 중복 ID 존재 — 배포 범위 밖, 별도 처리

### Metis Review
**Identified Gaps** (addressed):
- 404.html 서브패스 버그 → Task 1로 수정
- GitHub Actions 워크플로우 필요 → Task 2로 생성
- `.nojekyll` 배포 루트 포함 필요 → Task 2 워크플로우에서 처리

---

## Work Objectives

### Core Objective
museum-as-code 웹사이트를 `xodn348.github.io/museum-as-code/`에 배포하여, 기존 유저 사이트를 건드리지 않고 독립 프로젝트 사이트로 운영.

### Concrete Deliverables
- `docs/404.html` — 서브패스 리다이렉트 수정
- `.github/workflows/deploy.yml` — GitHub Actions 배포 워크플로우
- GitHub remote `xodn348/museum-as-code` 생성 및 연결
- 라이브 사이트 `https://xodn348.github.io/museum-as-code/` 접근 가능

### Definition of Done
- [ ] `curl -s -o /dev/null -w "%{http_code}" https://xodn348.github.io/museum-as-code/` → `200`
- [ ] 메인 페이지에서 유물 카드 그리드 렌더링 확인
- [ ] 유물 상세 보기에서 .hgl 및 .json 데이터 로드 확인
- [ ] 404 페이지 접근 시 `/museum-as-code/`로 리다이렉트 확인

### Must Have
- 기존 `xodn348.github.io` 유저 사이트에 영향 없음
- `docs/` 내 모든 웹 파일 배포 (index.html, app.js, style.css, manifest.json, .nojekyll)
- `artifacts/` 디렉토리 전체 배포 (114개 .hgl + .json 파일)
- GitHub Actions를 통한 자동 배포 (main 브랜치 push 트리거)

### Must NOT Have (Guardrails)
- app.js 수정 금지 — fetchWithFallback 로직은 이미 정상 동작
- 유저 사이트(`xodn348.github.io` 루트) 변경 금지
- manifest.json 수정 금지 — 중복 ID 문제는 별도 이슈
- 불필요한 빌드 스텝 추가 금지 — 정적 파일 복사만 수행

---

## Verification Strategy (MANDATORY)

> **ZERO HUMAN INTERVENTION** — ALL verification is agent-executed. No exceptions.

### Test Decision
- **Infrastructure exists**: NO (정적 HTML/JS 프로젝트, 테스트 프레임워크 없음)
- **Automated tests**: None
- **Framework**: none
- **Agent-Executed QA**: Playwright + curl로 라이브 사이트 검증

### QA Policy
Every task MUST include agent-executed QA scenarios.
Evidence saved to `.sisyphus/evidence/task-{N}-{scenario-slug}.{ext}`.

- **Frontend/UI**: Playwright — 사이트 접속, 카드 그리드 확인, 상세 페이지 확인
- **API/Backend**: curl — HTTP 상태 코드 확인, 리다이렉트 동작 확인

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Start Immediately — 코드 수정, 독립 작업):
├── Task 1: 404.html 서브패스 리다이렉트 수정 [quick]
├── Task 2: GitHub Actions 배포 워크플로우 생성 [quick]
└── Task 3: GitHub 원격 저장소 생성 및 연결 [quick]

Wave 2 (After Wave 1 — 배포 및 검증):
├── Task 4: 코드 푸시 및 Pages 배포 트리거 [quick]
└── Task 5: 라이브 사이트 QA 검증 [deep]

Wave FINAL (After ALL tasks):
├── Task F1: Plan compliance audit (oracle)
├── Task F2: Code quality review (unspecified-high)
├── Task F3: Real manual QA (unspecified-high + playwright)
└── Task F4: Scope fidelity check (deep)
-> Present results -> Get explicit user okay
```

### Dependency Matrix

| Task | Blocked By | Blocks |
|------|-----------|--------|
| 1 | — | 4 |
| 2 | — | 4 |
| 3 | — | 4 |
| 4 | 1, 2, 3 | 5 |
| 5 | 4 | F1-F4 |

### Agent Dispatch Summary

- **Wave 1**: **3 tasks** — T1 → `quick`, T2 → `quick`, T3 → `quick`
- **Wave 2**: **2 tasks** — T4 → `quick`, T5 → `deep` (+ `browse` skill)
- **FINAL**: **4 tasks** — F1 → `oracle`, F2 → `unspecified-high`, F3 → `unspecified-high` (+ `browse`), F4 → `deep`

---

## TODOs

- [x] 1. 404.html 서브패스 리다이렉트 수정

  **What to do**:
  - `docs/404.html` 라인 6: `window.location.href = '/'` → `window.location.href = '/museum-as-code/'`로 변경
  - `docs/404.html` 라인 9: `<a href="/">홈으로 돌아가기</a>` → `<a href="/museum-as-code/">홈으로 돌아가기</a>`로 변경
  - 총 2줄 변경, 나머지는 그대로 유지

  **Must NOT do**:
  - 404.html의 구조나 스타일 변경 금지
  - 다른 파일 수정 금지

  **Recommended Agent Profile**:
  - **Subagent Type**: `quick` (via subagent_type parameter)
    - Reason: 단일 파일, 2줄 변경의 trivial 작업
  - **Skills**: []
    - 별도 스킬 불필요

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 2, 3)
  - **Blocks**: Task 4
  - **Blocked By**: None (can start immediately)

  **References**:
  - `docs/404.html:6` — `<script>window.location.href = '/';</script>` — 이 줄의 `/`를 `/museum-as-code/`로 변경
  - `docs/404.html:9` — `<a href="/">홈으로 돌아가기</a>` — 이 href의 `/`를 `/museum-as-code/`로 변경
  - GitHub Pages 프로젝트 사이트는 `/{repo-name}/` 서브패스에서 서빙됨

  **Acceptance Criteria**:
  - [ ] `grep 'museum-as-code' docs/404.html` → 2개 매치 (라인 6, 9)
  - [ ] `grep "href = '/'" docs/404.html` → 0개 매치 (하드코딩 `/` 없음)

  **QA Scenarios**:

  ```
  Scenario: 404.html에 서브패스 리다이렉트가 올바르게 설정됨
    Tool: Bash (grep)
    Preconditions: docs/404.html 수정 완료
    Steps:
      1. grep -c 'museum-as-code' docs/404.html
      2. Assert output is "2"
      3. grep -c "= '/'" docs/404.html
      4. Assert output is "0"
    Expected Result: museum-as-code 2회 매치, 하드코딩 '/' 0회 매치
    Failure Indicators: museum-as-code 매치 수 != 2, 또는 '/' 매치 > 0
    Evidence: .sisyphus/evidence/task-1-404-subpath-grep.txt

  Scenario: 404.html이 유효한 HTML 구조를 유지함
    Tool: Bash (cat)
    Preconditions: docs/404.html 수정 완료
    Steps:
      1. cat docs/404.html
      2. Assert contains "<!DOCTYPE html>"
      3. Assert contains "</html>"
      4. Assert contains "/museum-as-code/" (not just "/")
    Expected Result: 유효한 HTML with 올바른 서브패스
    Failure Indicators: HTML 태그 깨짐 또는 서브패스 누락
    Evidence: .sisyphus/evidence/task-1-404-html-valid.txt
  ```

  **Commit**: YES (groups with Task 2)
  - Message: `fix(deploy): fix 404.html subpath redirect for GitHub Pages project site`
  - Files: `docs/404.html`

- [x] 2. GitHub Actions 배포 워크플로우 생성

  **What to do**:
  - `.github/workflows/deploy.yml` 생성
  - 트리거: `push` to `main` branch
  - 스텝 구성:
    1. `actions/checkout@v4`
    2. 배포 디렉토리 구성: `docs/` 내용을 배포 루트에 복사, `artifacts/` 디렉토리를 배포 루트에 복사, `.nojekyll` 파일 포함 확인
    3. `actions/upload-pages-artifact@v3` — 배포 디렉토리 업로드
    4. `actions/deploy-pages@v4` — GitHub Pages에 배포
  - `permissions: pages: write, id-token: write, contents: read` 설정
  - `environment: github-pages` 설정

  **Must NOT do**:
  - 빌드 스텝 추가 금지 (npm, webpack 등) — 순수 정적 파일 복사만
  - Node.js 설치 스텝 불필요
  - 기존 소스 파일 수정 금지

  **Recommended Agent Profile**:
  - **Subagent Type**: `quick` (via subagent_type parameter)
    - Reason: 단일 YAML 파일 생성, GitHub Actions 표준 패턴
  - **Skills**: []
    - 별도 스킬 불필요

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1, 3)
  - **Blocks**: Task 4
  - **Blocked By**: None (can start immediately)

  **References**:
  - `docs/` 디렉토리 구조: `index.html`, `app.js`, `style.css`, `manifest.json`, `404.html`, `.nojekyll` — 이 6개 파일이 배포 루트에 위치해야 함
  - `artifacts/national-treasures/` — 57 `.hgl` + 57 `.json` 파일
  - `artifacts/special/kdh/` — 7 `.hgl` + 7 `.json` 파일
  - `docs/app.js`의 `fetchWithFallback()` — primary 경로 `./artifacts/...`를 사용하므로, artifacts/가 배포 루트에 있어야 함
  - GitHub Actions Pages 배포 공식 문서: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site#publishing-with-a-custom-github-actions-workflow

  **Acceptance Criteria**:
  - [ ] `.github/workflows/deploy.yml` 파일 존재
  - [ ] `grep 'actions/deploy-pages' .github/workflows/deploy.yml` → 매치
  - [ ] `grep 'actions/upload-pages-artifact' .github/workflows/deploy.yml` → 매치
  - [ ] YAML 구문 유효 (yamllint 또는 수동 검증)

  **QA Scenarios**:

  ```
  Scenario: 워크플로우 파일이 올바른 구조를 가짐
    Tool: Bash (grep + cat)
    Preconditions: .github/workflows/deploy.yml 생성 완료
    Steps:
      1. cat .github/workflows/deploy.yml
      2. Assert contains "on:" with "push:" and "branches:" and "main"
      3. Assert contains "actions/checkout@v4"
      4. Assert contains "actions/upload-pages-artifact"
      5. Assert contains "actions/deploy-pages"
      6. Assert contains "permissions:"
      7. Assert YAML contains step that copies docs/ contents to deploy directory
      8. Assert YAML contains step that copies artifacts/ to deploy directory
    Expected Result: 모든 필수 GitHub Actions 구성 요소가 존재
    Failure Indicators: 필수 action 누락 또는 트리거 조건 오류
    Evidence: .sisyphus/evidence/task-2-workflow-structure.txt

  Scenario: 워크플로우에 .nojekyll이 배포에 포함됨
    Tool: Bash (grep)
    Preconditions: .github/workflows/deploy.yml 생성 완료
    Steps:
      1. grep -c 'nojekyll' .github/workflows/deploy.yml
      2. Assert output >= 1 (nojekyll이 언급됨)
    Expected Result: .nojekyll 파일이 배포 과정에 포함
    Failure Indicators: nojekyll 관련 스텝 없음
    Evidence: .sisyphus/evidence/task-2-nojekyll-check.txt
  ```

  **Commit**: YES (groups with Task 1)
  - Message: `ci(deploy): add GitHub Actions workflow for Pages deployment`
  - Files: `.github/workflows/deploy.yml`

- [x] 3. GitHub 원격 저장소 생성 및 연결

  **What to do**:
  - `gh repo create xodn348/museum-as-code --public --source=. --push` 실행
    - `--public`: 공개 저장소 (GitHub Pages 무료 사용을 위해)
    - `--source=.`: 현재 디렉토리를 소스로 사용
    - `--push`: 즉시 push (초기 push만, 이후는 Task 4에서)
  - 만약 이미 존재하면: `git remote add origin https://github.com/xodn348/museum-as-code.git` 사용
  - `git remote -v`로 연결 확인

  **Must NOT do**:
  - private 저장소 생성 금지 (Pages 무료 사용 불가)
  - 기존 `xodn348.github.io` 저장소 수정 금지
  - git config user.name/email 변경 금지

  **Recommended Agent Profile**:
  - **Subagent Type**: `quick` (via subagent_type parameter)
    - Reason: CLI 명령어 실행, 단순 저장소 생성
  - **Skills**: [`git-master`]
    - `git-master`: git remote 설정 및 push 작업에 필요

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1, 2)
  - **Blocks**: Task 4
  - **Blocked By**: None (can start immediately)

  **References**:
  - GitHub 계정: `xodn348` — `gh auth status`로 확인됨
  - 현재 git remote: 없음 (`git remote -v` 결과 빈 값)
  - Working directory: `/Users/jnnj92/museum-as-code/`

  **Acceptance Criteria**:
  - [ ] `gh repo view xodn348/museum-as-code` → 저장소 정보 출력
  - [ ] `git remote -v` → `origin` remote가 `github.com/xodn348/museum-as-code` 포함

  **QA Scenarios**:

  ```
  Scenario: GitHub 저장소가 생성되고 remote가 연결됨
    Tool: Bash (gh + git)
    Preconditions: gh CLI 인증 완료 (xodn348 계정)
    Steps:
      1. gh repo view xodn348/museum-as-code --json name,visibility
      2. Assert JSON contains "name": "museum-as-code"
      3. Assert JSON contains "visibility": "PUBLIC"
      4. git remote -v
      5. Assert output contains "github.com/xodn348/museum-as-code"
    Expected Result: 공개 저장소 존재, origin remote 연결됨
    Failure Indicators: 저장소 없음 또는 remote 미설정
    Evidence: .sisyphus/evidence/task-3-repo-created.txt

  Scenario: 기존 저장소가 있을 경우 graceful 처리
    Tool: Bash (gh)
    Preconditions: 저장소가 이미 존재할 수 있음
    Steps:
      1. gh repo create 실패 시 → git remote add origin 사용
      2. git remote -v로 연결 확인
    Expected Result: 어느 경우든 remote가 올바르게 연결됨
    Failure Indicators: remote 연결 실패
    Evidence: .sisyphus/evidence/task-3-repo-fallback.txt
  ```

  **Commit**: NO (저장소 생성은 코드 변경 아님)

- [x] 1. 404.html 서브패스 리다이렉트 수정

  **What to do**:
  - `docs/404.html` 라인 6: `window.location.href = '/'` → `window.location.href = '/museum-as-code/'`로 변경
  - `docs/404.html` 라인 9: `<a href="/">홈으로 돌아가기</a>` → `<a href="/museum-as-code/">홈으로 돌아가기</a>`로 변경
  - 총 2줄 변경, 나머지는 그대로 유지

  **Must NOT do**:
  - 404.html의 구조나 스타일 변경 금지
  - 다른 파일 수정 금지

  **Recommended Agent Profile**:
  - **Subagent Type**: `quick` (via subagent_type parameter)
    - Reason: 단일 파일, 2줄 변경의 trivial 작업
  - **Skills**: []
    - 별도 스킬 불필요

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 2, 3)
  - **Blocks**: Task 4
  - **Blocked By**: None (can start immediately)

  **References**:
  - `docs/404.html:6` — `<script>window.location.href = '/';</script>` — 이 줄의 `/`를 `/museum-as-code/`로 변경
  - `docs/404.html:9` — `<a href="/">홈으로 돌아가기</a>` — 이 href의 `/`를 `/museum-as-code/`로 변경
  - GitHub Pages 프로젝트 사이트는 `/{repo-name}/` 서브패스에서 서빙됨

  **Acceptance Criteria**:
  - [ ] `grep 'museum-as-code' docs/404.html` → 2개 매치 (라인 6, 9)
  - [ ] `grep "href = '/'" docs/404.html` → 0개 매치 (하드코딩 `/` 없음)

  **QA Scenarios**:

  ```
  Scenario: 404.html에 서브패스 리다이렉트가 올바르게 설정됨
    Tool: Bash (grep)
    Preconditions: docs/404.html 수정 완료
    Steps:
      1. grep -c 'museum-as-code' docs/404.html
      2. Assert output is "2"
      3. grep -c "= '/'" docs/404.html
      4. Assert output is "0"
    Expected Result: museum-as-code 2회 매치, 하드코딩 '/' 0회 매치
    Failure Indicators: museum-as-code 매치 수 != 2, 또는 '/' 매치 > 0
    Evidence: .sisyphus/evidence/task-1-404-subpath-grep.txt

  Scenario: 404.html이 유효한 HTML 구조를 유지함
    Tool: Bash (cat)
    Preconditions: docs/404.html 수정 완료
    Steps:
      1. cat docs/404.html
      2. Assert contains "<!DOCTYPE html>"
      3. Assert contains "</html>"
      4. Assert contains "/museum-as-code/" (not just "/")
    Expected Result: 유효한 HTML with 올바른 서브패스
    Failure Indicators: HTML 태그 깨짐 또는 서브패스 누락
    Evidence: .sisyphus/evidence/task-1-404-html-valid.txt
  ```

  **Commit**: YES (groups with Task 2)
  - Message: `fix(deploy): fix 404.html subpath redirect for GitHub Pages project site`
  - Files: `docs/404.html`

- [x] 2. GitHub Actions 배포 워크플로우 생성

  **What to do**:
  - `.github/workflows/deploy.yml` 생성
  - 트리거: `push` to `main` branch
  - 스텝 구성:
    1. `actions/checkout@v4`
    2. 배포 디렉토리 구성: `docs/` 내용을 배포 루트에 복사, `artifacts/` 디렉토리를 배포 루트에 복사, `.nojekyll` 파일 포함 확인
    3. `actions/upload-pages-artifact@v3` — 배포 디렉토리 업로드
    4. `actions/deploy-pages@v4` — GitHub Pages에 배포
  - `permissions: pages: write, id-token: write, contents: read` 설정
  - `environment: github-pages` 설정

  **Must NOT do**:
  - 빌드 스텝 추가 금지 (npm, webpack 등) — 순수 정적 파일 복사만
  - Node.js 설치 스텝 불필요
  - 기존 소스 파일 수정 금지

  **Recommended Agent Profile**:
  - **Subagent Type**: `quick` (via subagent_type parameter)
    - Reason: 단일 YAML 파일 생성, GitHub Actions 표준 패턴
  - **Skills**: []
    - 별도 스킬 불필요

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1, 3)
  - **Blocks**: Task 4
  - **Blocked By**: None (can start immediately)

  **References**:
  - `docs/` 디렉토리 구조: `index.html`, `app.js`, `style.css`, `manifest.json`, `404.html`, `.nojekyll` — 이 6개 파일이 배포 루트에 위치해야 함
  - `artifacts/national-treasures/` — 57 `.hgl` + 57 `.json` 파일
  - `artifacts/special/kdh/` — 7 `.hgl` + 7 `.json` 파일
  - `docs/app.js`의 `fetchWithFallback()` — primary 경로 `./artifacts/...`를 사용하므로, artifacts/가 배포 루트에 있어야 함
  - GitHub Actions Pages 배포 공식 문서: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site#publishing-with-a-custom-github-actions-workflow

  **Acceptance Criteria**:
  - [ ] `.github/workflows/deploy.yml` 파일 존재
  - [ ] `grep 'actions/deploy-pages' .github/workflows/deploy.yml` → 매치
  - [ ] `grep 'actions/upload-pages-artifact' .github/workflows/deploy.yml` → 매치
  - [ ] YAML 구문 유효 (yamllint 또는 수동 검증)

  **QA Scenarios**:

  ```
  Scenario: 워크플로우 파일이 올바른 구조를 가짐
    Tool: Bash (grep + cat)
    Preconditions: .github/workflows/deploy.yml 생성 완료
    Steps:
      1. cat .github/workflows/deploy.yml
      2. Assert contains "on:" with "push:" and "branches:" and "main"
      3. Assert contains "actions/checkout@v4"
      4. Assert contains "actions/upload-pages-artifact"
      5. Assert contains "actions/deploy-pages"
      6. Assert contains "permissions:"
      7. Assert YAML contains step that copies docs/ contents to deploy directory
      8. Assert YAML contains step that copies artifacts/ to deploy directory
    Expected Result: 모든 필수 GitHub Actions 구성 요소가 존재
    Failure Indicators: 필수 action 누락 또는 트리거 조건 오류
    Evidence: .sisyphus/evidence/task-2-workflow-structure.txt

  Scenario: 워크플로우에 .nojekyll이 배포에 포함됨
    Tool: Bash (grep)
    Preconditions: .github/workflows/deploy.yml 생성 완료
    Steps:
      1. grep -c 'nojekyll' .github/workflows/deploy.yml
      2. Assert output >= 1 (nojekyll이 언급됨)
    Expected Result: .nojekyll 파일이 배포 과정에 포함
    Failure Indicators: nojekyll 관련 스텝 없음
    Evidence: .sisyphus/evidence/task-2-nojekyll-check.txt
  ```

  **Commit**: YES (groups with Task 1)
  - Message: `ci(deploy): add GitHub Actions workflow for Pages deployment`
  - Files: `.github/workflows/deploy.yml`

- [x] 3. GitHub 원격 저장소 생성 및 연결

  **What to do**:
  - `gh repo create xodn348/museum-as-code --public --source=. --push` 실행
    - `--public`: 공개 저장소 (GitHub Pages 무료 사용을 위해)
    - `--source=.`: 현재 디렉토리를 소스로 사용
    - `--push`: 즉시 push (초기 push만, 이후는 Task 4에서)
  - 만약 이미 존재하면: `git remote add origin https://github.com/xodn348/museum-as-code.git` 사용
  - `git remote -v`로 연결 확인

  **Must NOT do**:
  - private 저장소 생성 금지 (Pages 무료 사용 불가)
  - 기존 `xodn348.github.io` 저장소 수정 금지
  - git config user.name/email 변경 금지

  **Recommended Agent Profile**:
  - **Subagent Type**: `quick` (via subagent_type parameter)
    - Reason: CLI 명령어 실행, 단순 저장소 생성
  - **Skills**: [`git-master`]
    - `git-master`: git remote 설정 및 push 작업에 필요

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1, 2)
  - **Blocks**: Task 4
  - **Blocked By**: None (can start immediately)

  **References**:
  - GitHub 계정: `xodn348` — `gh auth status`로 확인됨
  - 현재 git remote: 없음 (`git remote -v` 결과 빈 값)
  - Working directory: `/Users/jnnj92/museum-as-code/`

  **Acceptance Criteria**:
  - [ ] `gh repo view xodn348/museum-as-code` → 저장소 정보 출력
  - [ ] `git remote -v` → `origin` remote가 `github.com/xodn348/museum-as-code` 포함

  **QA Scenarios**:

  ```
  Scenario: GitHub 저장소가 생성되고 remote가 연결됨
    Tool: Bash (gh + git)
    Preconditions: gh CLI 인증 완료 (xodn348 계정)
    Steps:
      1. gh repo view xodn348/museum-as-code --json name,visibility
      2. Assert JSON contains "name": "museum-as-code"
      3. Assert JSON contains "visibility": "PUBLIC"
      4. git remote -v
      5. Assert output contains "github.com/xodn348/museum-as-code"
    Expected Result: 공개 저장소 존재, origin remote 연결됨
    Failure Indicators: 저장소 없음 또는 remote 미설정
    Evidence: .sisyphus/evidence/task-3-repo-created.txt

  Scenario: 기존 저장소가 있을 경우 graceful 처리
    Tool: Bash (gh)
    Preconditions: 저장소가 이미 존재할 수 있음
    Steps:
      1. gh repo create 실패 시 → git remote add origin 사용
      2. git remote -v로 연결 확인
    Expected Result: 어느 경우든 remote가 올바르게 연결됨
    Failure Indicators: remote 연결 실패
    Evidence: .sisyphus/evidence/task-3-repo-fallback.txt
  ```

  **Commit**: NO (저장소 생성은 코드 변경 아님)

- [x] 4. 코드 커밋, 푸시 및 GitHub Pages 활성화

  **What to do**:
  - Task 1, 2의 변경사항을 커밋 (404.html 수정 + workflow 생성)
  - `git add docs/404.html .github/workflows/deploy.yml && git commit -m "fix(deploy): fix 404 redirect and add Pages workflow"`
  - `git push origin main` (Task 3에서 remote 설정 완료된 상태)
  - GitHub Pages 설정 활성화: `gh api repos/xodn348/museum-as-code/pages -X POST -f build_type=workflow` 또는 GitHub Settings에서 Source를 "GitHub Actions"로 설정
  - Actions 탭에서 워크플로우 실행 확인 — 성공할 때까지 대기 (최대 5분)

  **Must NOT do**:
  - git config user.name/email 변경 금지
  - force push 금지
  - main 이외 브랜치 사용 금지 (워크플로우가 main push 트리거)

  **Recommended Agent Profile**:
  - **Subagent Type**: `quick` (via subagent_type parameter)
    - Reason: git 명령어 + gh API 호출, 표준 배포 작업
  - **Skills**: [`git-master`]
    - `git-master`: git commit/push 작업에 필요

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 2 (Sequential — after Wave 1)
  - **Blocks**: Task 5
  - **Blocked By**: Tasks 1, 2, 3

  **References**:
  - Task 1 결과: `docs/404.html` 수정됨
  - Task 2 결과: `.github/workflows/deploy.yml` 생성됨
  - Task 3 결과: `origin` remote가 `github.com/xodn348/museum-as-code`으로 설정됨
  - GitHub Pages API: `gh api repos/{owner}/{repo}/pages -X POST -f build_type=workflow` — Pages를 GitHub Actions 소스로 활성화
  - GitHub Actions 상태 확인: `gh run list --limit 1` — 최근 워크플로우 실행 상태

  **Acceptance Criteria**:
  - [ ] `git log --oneline -1` → 커밋 메시지 포함
  - [ ] `gh run list --limit 1 --json status,conclusion` → `"status": "completed"`, `"conclusion": "success"`
  - [ ] `gh api repos/xodn348/museum-as-code/pages --jq '.status'` → `"built"` 또는 유사 성공 상태

  **QA Scenarios**:

  ```
  Scenario: 코드가 성공적으로 푸시되고 워크플로우가 실행됨
    Tool: Bash (git + gh)
    Preconditions: Tasks 1-3 완료, 변경사항 커밋 준비됨
    Steps:
      1. git status → 변경된 파일 확인 (docs/404.html, .github/workflows/deploy.yml)
      2. git add + commit + push
      3. gh run list --limit 1 --json status,name
      4. Wait up to 300s for workflow to complete: gh run watch (최근 run)
      5. gh run list --limit 1 --json conclusion → Assert "success"
    Expected Result: push 성공, 워크플로우 실행 완료 (conclusion: success)
    Failure Indicators: push 거부, 워크플로우 실패 (conclusion: failure)
    Evidence: .sisyphus/evidence/task-4-push-and-workflow.txt

  Scenario: GitHub Pages가 GitHub Actions 소스로 활성화됨
    Tool: Bash (gh api)
    Preconditions: 워크플로우 성공 완료
    Steps:
      1. gh api repos/xodn348/museum-as-code/pages --jq '.build_type'
      2. Assert output is "workflow"
      3. gh api repos/xodn348/museum-as-code/pages --jq '.html_url'
      4. Assert output contains "xodn348.github.io/museum-as-code"
    Expected Result: Pages 활성화, build_type이 "workflow"
    Failure Indicators: 404 응답 (Pages 미활성화) 또는 build_type이 "legacy"
    Evidence: .sisyphus/evidence/task-4-pages-activated.txt
  ```

  **Commit**: YES
  - Message: `fix(deploy): fix 404 redirect and add Pages workflow`
  - Files: `docs/404.html`, `.github/workflows/deploy.yml`

- [x] 5. 라이브 사이트 QA 검증

  **What to do**:
  - `https://xodn348.github.io/museum-as-code/` 접속하여 메인 페이지 로드 확인
  - 유물 카드 그리드 렌더링 확인 (manifest.json 로드 → 카드 생성)
  - 유물 상세 보기 클릭 → .hgl 및 .json 데이터 로드 확인
  - 404 리다이렉트 테스트: 존재하지 않는 경로 접속 → `/museum-as-code/`로 리다이렉트
  - artifacts 파일 직접 접근 테스트: `curl` 으로 `.json`, `.hgl` 파일 200 응답 확인
  - 기존 `xodn348.github.io` 사이트가 영향받지 않았는지 확인

  **Must NOT do**:
  - 소스 코드 수정 금지 — 순수 검증 태스크
  - 배포 워크플로우 재실행 금지 (Task 4 결과 검증만)

  **Recommended Agent Profile**:
  - **Subagent Type**: `deep` (via subagent_type parameter)
    - Reason: 다중 시나리오 QA, Playwright 브라우저 테스트 포함
  - **Skills**: [`browse`]
    - `browse`: 라이브 사이트 접속, DOM 검증, 스크린샷 캡처에 필요

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 2 (Sequential — after Task 4)
  - **Blocks**: F1-F4
  - **Blocked By**: Task 4

  **References**:
  - 배포 URL: `https://xodn348.github.io/museum-as-code/`
  - `docs/index.html` — 메인 페이지 구조, `<div id="app">` 컨테이너
  - `docs/app.js` — `fetchWithFallback()` 함수가 `./artifacts/...` 경로로 데이터 fetch
  - `docs/manifest.json` — 64개 유물 항목, `hgl_path`와 `json_path` 필드
  - `docs/404.html` — `/museum-as-code/`로 리다이렉트하는 SPA 폴백
  - 기존 유저 사이트: `https://xodn348.github.io/` — 영향 없음 확인용

  **Acceptance Criteria**:
  - [ ] `curl -s -o /dev/null -w "%{http_code}" https://xodn348.github.io/museum-as-code/` → `200`
  - [ ] `curl -s -o /dev/null -w "%{http_code}" https://xodn348.github.io/museum-as-code/artifacts/national-treasures/nb_001.json` → `200`
  - [ ] Playwright: 메인 페이지에서 `.card` 또는 유물 카드 요소 ≥ 1개 존재
  - [ ] `curl -s -o /dev/null -w "%{http_code}" https://xodn348.github.io/` → `200` (기존 사이트 무사)

  **QA Scenarios**:

  ```
  Scenario: 메인 페이지가 정상 로드되고 유물 카드가 렌더링됨
    Tool: Playwright (browse skill)
    Preconditions: GitHub Pages 배포 완료 (Task 4)
    Steps:
      1. Navigate to https://xodn348.github.io/museum-as-code/
      2. Wait for page load (timeout: 15s)
      3. Assert page title contains "디지털 국립중앙박물관" or "museum"
      4. Assert document.querySelectorAll('.card, .artifact-card, [data-artifact]').length >= 1
      5. Take screenshot
    Expected Result: 페이지 200 로드, 유물 카드 최소 1개 렌더링
    Failure Indicators: 404 페이지, 빈 페이지, JavaScript 에러
    Evidence: .sisyphus/evidence/task-5-main-page.png

  Scenario: 유물 상세 페이지에서 데이터가 로드됨
    Tool: Playwright (browse skill)
    Preconditions: 메인 페이지 정상 로드
    Steps:
      1. Navigate to https://xodn348.github.io/museum-as-code/
      2. Click first artifact card element
      3. Wait for detail view to appear (timeout: 10s)
      4. Assert detail content is not empty (text length > 0)
      5. Take screenshot
    Expected Result: 상세 뷰 표시, 유물 데이터 로드됨
    Failure Indicators: 데이터 로드 실패, fetch 에러, 빈 상세 뷰
    Evidence: .sisyphus/evidence/task-5-detail-view.png

  Scenario: artifacts 파일이 직접 접근 가능함
    Tool: Bash (curl)
    Preconditions: GitHub Pages 배포 완료
    Steps:
      1. curl -s -o /dev/null -w "%{http_code}" https://xodn348.github.io/museum-as-code/artifacts/national-treasures/nb_001.json
      2. Assert status code is 200
      3. curl -s https://xodn348.github.io/museum-as-code/artifacts/national-treasures/nb_001.json | head -1
      4. Assert response contains valid JSON (starts with "{")
    Expected Result: HTTP 200, valid JSON 응답
    Failure Indicators: 404 (파일 없음), 403 (권한), HTML 에러 페이지
    Evidence: .sisyphus/evidence/task-5-artifacts-curl.txt

  Scenario: 404 리다이렉트가 서브패스로 정상 동작
    Tool: Bash (curl)
    Preconditions: 404.html 수정 완료 및 배포됨
    Steps:
      1. curl -s -L -o /dev/null -w "%{url_effective}" https://xodn348.github.io/museum-as-code/nonexistent-path
      2. Assert redirected URL contains "/museum-as-code/"
      3. Assert final HTTP status is 200
    Expected Result: 존재하지 않는 경로 → /museum-as-code/로 리다이렉트
    Failure Indicators: 리다이렉트가 /로 가거나, 404 에러 그대로 표시
    Evidence: .sisyphus/evidence/task-5-404-redirect.txt

  Scenario: 기존 유저 사이트가 영향받지 않음
    Tool: Bash (curl)
    Preconditions: museum-as-code 배포 완료
    Steps:
      1. curl -s -o /dev/null -w "%{http_code}" https://xodn348.github.io/
      2. Assert status code is 200
      3. curl -s https://xodn348.github.io/ | head -5
      4. Assert response does NOT contain "museum" or "박물관" (기존 사이트 콘텐츠 유지)
    Expected Result: 기존 유저 사이트 200 응답, museum 콘텐츠 아님
    Failure Indicators: 404 또는 museum-as-code 콘텐츠로 덮어씌워짐
    Evidence: .sisyphus/evidence/task-5-user-site-intact.txt
  ```

  **Commit**: NO (검증 태스크, 코드 변경 없음)

- [x] 4. 코드 커밋, 푸시 및 GitHub Pages 활성화

  **What to do**:
  - Task 1, 2의 변경사항을 커밋 (404.html 수정 + workflow 생성)
  - `git add docs/404.html .github/workflows/deploy.yml && git commit -m "fix(deploy): fix 404 redirect and add Pages workflow"`
  - `git push origin main` (Task 3에서 remote 설정 완료된 상태)
  - GitHub Pages 설정 활성화: `gh api repos/xodn348/museum-as-code/pages -X POST -f build_type=workflow` 또는 GitHub Settings에서 Source를 "GitHub Actions"로 설정
  - Actions 탭에서 워크플로우 실행 확인 — 성공할 때까지 대기 (최대 5분)

  **Must NOT do**:
  - git config user.name/email 변경 금지
  - force push 금지
  - main 이외 브랜치 사용 금지 (워크플로우가 main push 트리거)

  **Recommended Agent Profile**:
  - **Subagent Type**: `quick` (via subagent_type parameter)
    - Reason: git 명령어 + gh API 호출, 표준 배포 작업
  - **Skills**: [`git-master`]
    - `git-master`: git commit/push 작업에 필요

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 2 (Sequential — after Wave 1)
  - **Blocks**: Task 5
  - **Blocked By**: Tasks 1, 2, 3

  **References**:
  - Task 1 결과: `docs/404.html` 수정됨
  - Task 2 결과: `.github/workflows/deploy.yml` 생성됨
  - Task 3 결과: `origin` remote가 `github.com/xodn348/museum-as-code`으로 설정됨
  - GitHub Pages API: `gh api repos/{owner}/{repo}/pages -X POST -f build_type=workflow` — Pages를 GitHub Actions 소스로 활성화
  - GitHub Actions 상태 확인: `gh run list --limit 1` — 최근 워크플로우 실행 상태

  **Acceptance Criteria**:
  - [ ] `git log --oneline -1` → 커밋 메시지 포함
  - [ ] `gh run list --limit 1 --json status,conclusion` → `"status": "completed"`, `"conclusion": "success"`
  - [ ] `gh api repos/xodn348/museum-as-code/pages --jq '.status'` → `"built"` 또는 유사 성공 상태

  **QA Scenarios**:

  ```
  Scenario: 코드가 성공적으로 푸시되고 워크플로우가 실행됨
    Tool: Bash (git + gh)
    Preconditions: Tasks 1-3 완료, 변경사항 커밋 준비됨
    Steps:
      1. git status → 변경된 파일 확인 (docs/404.html, .github/workflows/deploy.yml)
      2. git add + commit + push
      3. gh run list --limit 1 --json status,name
      4. Wait up to 300s for workflow to complete: gh run watch (최근 run)
      5. gh run list --limit 1 --json conclusion → Assert "success"
    Expected Result: push 성공, 워크플로우 실행 완료 (conclusion: success)
    Failure Indicators: push 거부, 워크플로우 실패 (conclusion: failure)
    Evidence: .sisyphus/evidence/task-4-push-and-workflow.txt

  Scenario: GitHub Pages가 GitHub Actions 소스로 활성화됨
    Tool: Bash (gh api)
    Preconditions: 워크플로우 성공 완료
    Steps:
      1. gh api repos/xodn348/museum-as-code/pages --jq '.build_type'
      2. Assert output is "workflow"
      3. gh api repos/xodn348/museum-as-code/pages --jq '.html_url'
      4. Assert output contains "xodn348.github.io/museum-as-code"
    Expected Result: Pages 활성화, build_type이 "workflow"
    Failure Indicators: 404 응답 (Pages 미활성화) 또는 build_type이 "legacy"
    Evidence: .sisyphus/evidence/task-4-pages-activated.txt
  ```

  **Commit**: YES
  - Message: `fix(deploy): fix 404 redirect and add Pages workflow`
  - Files: `docs/404.html`, `.github/workflows/deploy.yml`

- [x] 5. 라이브 사이트 QA 검증

  **What to do**:
  - `https://xodn348.github.io/museum-as-code/` 접속하여 메인 페이지 로드 확인
  - 유물 카드 그리드 렌더링 확인 (manifest.json 로드 → 카드 생성)
  - 유물 상세 보기 클릭 → .hgl 및 .json 데이터 로드 확인
  - 404 리다이렉트 테스트: 존재하지 않는 경로 접속 → `/museum-as-code/`로 리다이렉트
  - artifacts 파일 직접 접근 테스트: `curl` 으로 `.json`, `.hgl` 파일 200 응답 확인
  - 기존 `xodn348.github.io` 사이트가 영향받지 않았는지 확인

  **Must NOT do**:
  - 소스 코드 수정 금지 — 순수 검증 태스크
  - 배포 워크플로우 재실행 금지 (Task 4 결과 검증만)

  **Recommended Agent Profile**:
  - **Subagent Type**: `deep` (via subagent_type parameter)
    - Reason: 다중 시나리오 QA, Playwright 브라우저 테스트 포함
  - **Skills**: [`browse`]
    - `browse`: 라이브 사이트 접속, DOM 검증, 스크린샷 캡처에 필요

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 2 (Sequential — after Task 4)
  - **Blocks**: F1-F4
  - **Blocked By**: Task 4

  **References**:
  - 배포 URL: `https://xodn348.github.io/museum-as-code/`
  - `docs/index.html` — 메인 페이지 구조, `<div id="app">` 컨테이너
  - `docs/app.js` — `fetchWithFallback()` 함수가 `./artifacts/...` 경로로 데이터 fetch
  - `docs/manifest.json` — 64개 유물 항목, `hgl_path`와 `json_path` 필드
  - `docs/404.html` — `/museum-as-code/`로 리다이렉트하는 SPA 폴백
  - 기존 유저 사이트: `https://xodn348.github.io/` — 영향 없음 확인용

  **Acceptance Criteria**:
  - [ ] `curl -s -o /dev/null -w "%{http_code}" https://xodn348.github.io/museum-as-code/` → `200`
  - [ ] `curl -s -o /dev/null -w "%{http_code}" https://xodn348.github.io/museum-as-code/artifacts/national-treasures/nb_001.json` → `200`
  - [ ] Playwright: 메인 페이지에서 `.card` 또는 유물 카드 요소 ≥ 1개 존재
  - [ ] `curl -s -o /dev/null -w "%{http_code}" https://xodn348.github.io/` → `200` (기존 사이트 무사)

  **QA Scenarios**:

  ```
  Scenario: 메인 페이지가 정상 로드되고 유물 카드가 렌더링됨
    Tool: Playwright (browse skill)
    Preconditions: GitHub Pages 배포 완료 (Task 4)
    Steps:
      1. Navigate to https://xodn348.github.io/museum-as-code/
      2. Wait for page load (timeout: 15s)
      3. Assert page title contains "디지털 국립중앙박물관" or "museum"
      4. Assert document.querySelectorAll('.card, .artifact-card, [data-artifact]').length >= 1
      5. Take screenshot
    Expected Result: 페이지 200 로드, 유물 카드 최소 1개 렌더링
    Failure Indicators: 404 페이지, 빈 페이지, JavaScript 에러
    Evidence: .sisyphus/evidence/task-5-main-page.png

  Scenario: 유물 상세 페이지에서 데이터가 로드됨
    Tool: Playwright (browse skill)
    Preconditions: 메인 페이지 정상 로드
    Steps:
      1. Navigate to https://xodn348.github.io/museum-as-code/
      2. Click first artifact card element
      3. Wait for detail view to appear (timeout: 10s)
      4. Assert detail content is not empty (text length > 0)
      5. Take screenshot
    Expected Result: 상세 뷰 표시, 유물 데이터 로드됨
    Failure Indicators: 데이터 로드 실패, fetch 에러, 빈 상세 뷰
    Evidence: .sisyphus/evidence/task-5-detail-view.png

  Scenario: artifacts 파일이 직접 접근 가능함
    Tool: Bash (curl)
    Preconditions: GitHub Pages 배포 완료
    Steps:
      1. curl -s -o /dev/null -w "%{http_code}" https://xodn348.github.io/museum-as-code/artifacts/national-treasures/nb_001.json
      2. Assert status code is 200
      3. curl -s https://xodn348.github.io/museum-as-code/artifacts/national-treasures/nb_001.json | head -1
      4. Assert response contains valid JSON (starts with "{")
    Expected Result: HTTP 200, valid JSON 응답
    Failure Indicators: 404 (파일 없음), 403 (권한), HTML 에러 페이지
    Evidence: .sisyphus/evidence/task-5-artifacts-curl.txt

  Scenario: 404 리다이렉트가 서브패스로 정상 동작
    Tool: Bash (curl)
    Preconditions: 404.html 수정 완료 및 배포됨
    Steps:
      1. curl -s -L -o /dev/null -w "%{url_effective}" https://xodn348.github.io/museum-as-code/nonexistent-path
      2. Assert redirected URL contains "/museum-as-code/"
      3. Assert final HTTP status is 200
    Expected Result: 존재하지 않는 경로 → /museum-as-code/로 리다이렉트
    Failure Indicators: 리다이렉트가 /로 가거나, 404 에러 그대로 표시
    Evidence: .sisyphus/evidence/task-5-404-redirect.txt

  Scenario: 기존 유저 사이트가 영향받지 않음
    Tool: Bash (curl)
    Preconditions: museum-as-code 배포 완료
    Steps:
      1. curl -s -o /dev/null -w "%{http_code}" https://xodn348.github.io/
      2. Assert status code is 200
      3. curl -s https://xodn348.github.io/ | head -5
      4. Assert response does NOT contain "museum" or "박물관" (기존 사이트 콘텐츠 유지)
    Expected Result: 기존 유저 사이트 200 응답, museum 콘텐츠 아님
    Failure Indicators: 404 또는 museum-as-code 콘텐츠로 덮어씌워짐
    Evidence: .sisyphus/evidence/task-5-user-site-intact.txt
  ```

  **Commit**: NO (검증 태스크, 코드 변경 없음)

---

## Final Verification Wave (MANDATORY — after ALL implementation tasks)

> 4 review agents run in PARALLEL. ALL must APPROVE. Present consolidated results to user and get explicit "okay" before completing.

- [x] F1. **Plan Compliance Audit** — `oracle`
  Read the plan end-to-end. For each "Must Have": verify implementation exists (curl endpoint, read file). For each "Must NOT Have": search codebase for forbidden changes — reject with file:line if found. Check evidence files in `.sisyphus/evidence/`. Compare deliverables against plan.
  Output: `Must Have [4/4] | Must NOT Have [4/4] | Tasks [5/5] | VERDICT: APPROVE`

- [x] F2. **Code Quality Review** — `unspecified-high`
  Review all changed files: `docs/404.html`, `.github/workflows/deploy.yml`. Check for: hardcoded paths that should be parameterized, YAML syntax errors, security issues in workflow (e.g., `actions/checkout` version pinning). Run `yamllint` on workflow file if available.
  Output: `Files [2 clean/0 issues] | VERDICT: APPROVE`

- [x] F3. **Real Manual QA** — `unspecified-high` (+ `browse` skill)
  Start from clean state. Navigate to `https://xodn348.github.io/museum-as-code/`. Execute EVERY QA scenario from EVERY task. Test cross-task integration: 404 redirect → main page → artifact detail. Test edge cases: direct URL to non-existent path, refresh on detail page. Save to `.sisyphus/evidence/final-qa/`.
  Output: `Scenarios [5/5 pass] | Integration [3/3] | Edge Cases [2 tested] | VERDICT: APPROVE`

- [x] F4. **Scope Fidelity Check** — `deep`
  For each task: read "What to do", read actual diff (`git log --oneline`, `git diff`). Verify 1:1 — everything in spec was built, nothing beyond spec was built. Specifically verify: app.js NOT modified, manifest.json NOT modified, only 404.html and new workflow file changed.
  Output: `Tasks [5/5 compliant] | Contamination [CLEAN] | Unaccounted [CLEAN] | VERDICT: APPROVE`

---

## Commit Strategy

- **Wave 1 commit**: `fix(deploy): fix 404.html subpath redirect and add GitHub Actions workflow`
  - Files: `docs/404.html`, `.github/workflows/deploy.yml`
  - Pre-commit: `cat docs/404.html | grep museum-as-code` (verify subpath present)

---

## Success Criteria

### Verification Commands
```bash
curl -s -o /dev/null -w "%{http_code}" https://xodn348.github.io/museum-as-code/  # Expected: 200
curl -s -o /dev/null -w "%{http_code}" https://xodn348.github.io/museum-as-code/artifacts/national-treasures/nb_001.json  # Expected: 200
curl -s https://xodn348.github.io/museum-as-code/ | grep -c "디지털 국립중앙박물관"  # Expected: 1
```

### Final Checklist
- [ ] `xodn348.github.io` 유저 사이트 정상 동작 (영향 없음)
- [ ] `xodn348.github.io/museum-as-code/` 메인 페이지 로드
- [ ] 유물 카드 그리드 렌더링
- [ ] 유물 상세 페이지 데이터 로드
- [ ] 404 리다이렉트 정상 동작
- [ ] GitHub Actions 워크플로우 성공 완료
