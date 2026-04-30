# museum-as-code · CLAUDE.md

## 🚨 HARD RULE: HAN-LANG ONLY 🚨

**Every single line of code in this project — homepage cards, hero pages, downloadable artifact files, README examples, demo snippets, anything — MUST be written in real, executable Han-lang (.hgl).**

Pseudocode is forbidden. Korean-keyword-flavored fake syntax is forbidden. If you can't run it with `hgl interpret file.hgl`, it doesn't go in this repo.

This rule overrides aesthetic, brevity, or clarity preferences. The museum is simultaneously a Korean cultural archive AND a real-world demo of the Han programming language. Both jobs require valid Han.

### What "real Han" means

Reference: https://github.com/xodn348/han · docs: https://xodn348.github.io/han/

```han
// struct DEFINITION — fields are typed, no values
구조 히어로유물 {
    이름: 문자열,
    지정번호: 문자열,
    출처검증: 불
}

// struct INSTANTIATION — use 변수 to bind
변수 pensive = 히어로유물 {
    이름: "금동미륵보살반가사유상",
    지정번호: "국보 제83호",
    출처검증: 참
}

// function definition + invocation
함수 main() {
    출력(형식("{0} ({1})", pensive.이름, pensive.지정번호))
}

main()
```

### Keywords (Korean → English)

함수(fn) 반환(return) 변수(let) 상수(const) 만약(if) 이면(then) 아니면(else) 그리고(and) 또는(or) 반복(for) 동안(while) 멈춰(break) 계속(continue) 구조(struct) 구현(impl) 열거(enum) 시도(try) 처리(catch) 맞춤(match) 포함(import) 안에서(in)

### Types

정수(i64) 실수(f64) 문자열(string) 불(bool) 없음(void) — boolean literals: 참 / 거짓

### Built-ins (most common)

출력(print) 형식(format) 길이(len) 입력(input) 정수변환(int) 실수변환(float) 사전(dict) 파일읽기(read_file) 파일쓰기(write_file)

### File / tooling

- File extension: `.hgl`
- Comments: `//`
- Run: `hgl interpret file.hgl`
- Build: `hgl build file.hgl`
- REPL: `hgl repl`
- Playground: https://xodn348.github.io/han/playground/

## PR review gate

Any PR that introduces or modifies code in this repo must satisfy:

1. Every `.hgl` snippet runs cleanly in Han playground OR `hgl interpret`
2. No invented keywords (`변수 X = "..."` inside `구조 { ... }` is INVALID — fields use `이름: 타입` syntax)
3. Struct instances must use the `구조명 { 필드: 값 }` form, bound via `변수 name = ...`
4. Website code blocks must mirror an actual `.hgl` file in `artifacts/` or `examples/` — no mock or demo-only Han

## Skill routing

When the user's request matches an available skill, invoke it via the Skill tool. When in doubt, invoke the skill.

Key routing rules:
- Han syntax questions → check https://xodn348.github.io/han/api/keywords.html or read xodn348/han examples
- Product ideas / brainstorming → invoke /office-hours
- Strategy / scope → invoke /plan-ceo-review
- Architecture → invoke /plan-eng-review
- Design system / plan review → invoke /design-consultation or /plan-design-review
- Bugs / errors → invoke /investigate
- QA / testing → invoke /qa or /qa-only
- Code review → invoke /review
- Visual polish → invoke /design-review
- Ship / deploy / PR → invoke /ship or /land-and-deploy

## Repo layout (current)

- `artifacts/heroes/*.hgl` — 10 hero artifact source files (canonical)
- `artifacts/national-treasures/*.hgl` — 50+ catalog entries
- `docs/` — GitHub Pages site (index.html, hero.html, app.js, hero.js, graph.js, style.css, hero.css)
- `pipeline/` — Python build pipeline (extracts `.hgl` data into JSON for the site)
- `DESIGN.md` — design system notes (live document)
