# 디지털 국립중앙박물관 — Museum as Code

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Han Language](https://img.shields.io/badge/Language-han-7B2CBF)](https://github.com/han-lang/han)
[![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Linux-black)](https://github.com/han-lang/han)

---

## 소개 / Introduction

Museum as Code는 한국의 **국보·보물** 등 문화재를 [han](https://github.com/han-lang/han) 프로그래밍 언어(`.hgl`)로 디지털화하는 프로젝트입니다. 각 유물을 구조체(struct)로 정의하여 소스 코드로서 보존하고, Python 파이프라인을 통해 e뮤지엄 Open API에서 자동으로 데이터를 수집합니다.

> **Museum as Code** is a project that digitizes Korean national treasures and cultural heritage artifacts as [han](https://github.com/han-lang/han) programming language (`.hgl`) source code. Each artifact is defined as a struct and preserved as readable code, with a Python pipeline fetching data from the e뮤지엄 Open API.

---

## 한(han) 언어 / Han Language

[han](https://github.com/han-lang/han)은 한국어 문법으로 작성된 범용 프로그래밍 언어입니다. 변수, 함수, 구조체, 제네릭, 모듈 등 현대적 프로그래밍 개념을 한국어로 표현할 수 있습니다.

[han](https://github.com/han-lang/han) is a general-purpose programming language written in Korean grammar. It supports modern programming concepts like variables, functions, structs, generics, and modules — all expressed in Korean.

### 구조체 예시 / Struct Example

```hgl
// 국보 제1호 — 서울 숭례문 (예시 / Example)
구조 문화재 {
    명칭: 문자열,
    지정번호: 정수,
    분류: 문자열,
    소재지: 문자열,
}

함수 main() {
    변수 유물 = 문화재 {
        명칭: "서울 숭례문",
        지정번호: 1,
        분류: "유적건조물",
        소재지: "서울특별시 종로구",
    }
}
```

---

## 디렉토리 구조 / Directory Structure

```
museum-as-code/
├── artifacts/
│   ├── national-treasures/   # 국보 (National Treasures)
│   ├── treasures/             # 보물 (Treasures)
│   └── special/
│       └── kdh/               # 케이팝 데몬 헌터스 컬렉션
│       └── kpop-demon-hunters/
├── pipeline/                  # Python automation pipeline
│   ├── api_client.py          # e뮤지엄 API 클라이언트 / eMuseum API client
│   ├── config.py              # 설정 / Configuration
│   ├── templates/             # Jinja2 .hgl 템플릿 / Jinja2 .hgl templates
│   └── schemas/               # JSON 스키마 / JSON schemas
├── docs/                      # 문서 / Documentation
├── LICENSE                    # MIT 라이선스
└── README.md
```

---

## 파이프라인 / Pipeline

Python 기반 파이프라인이 e뮤지엄 Open API에서 유물 데이터를 수집하고, Jinja2 템플릿을 통해 `.hgl` 소스 코드를 자동으로 생성합니다.

A Python-based pipeline fetches artifact data from the e뮤지엄 Open API and generates `.hgl` source code automatically using Jinja2 templates.

### 환경 변수 설정 / Environment Setup

```bash
# e뮤지엄 API 키 발급: https://www.data.go.kr → "전국 박물관 유물정보" 검색
# Get eMuseum API key: https://www.data.go.kr → search "전국 박물관 유물정보"
export EMUSEUM_API_KEY='your_key_here'
export DATA_GO_KR_API_KEY='your_key_here'
```

### 실행 / Run

```bash
python3 -m pipeline.api_client --ccbaKdcd 11 --numOfRows 10
```

---

## 기여하기 / Contributing

새로운 유물을 추가하고 싶으신가요? 아래 방식으로 기여할 수 있습니다:

Want to add a new artifact? Here's how you can contribute:

1. **수동 추가** / Manual addition: `artifacts/national-treasures/nb_XXX.hgl` 파일 생성 / Create file
2. **자동 수집** / Auto-fetch: API 키 설정 후 파이프라인 실행 / Set API keys and run pipeline
3. **PR 환영** / PRs welcome: 모든 기여를 환영합니다 — 버그 수정, 새 유물, 템플릿 개선 등 / All contributions welcome

---

## 라이선스 / License

MIT License — 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

See [LICENSE](LICENSE) for details.
