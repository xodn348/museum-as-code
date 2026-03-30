# 디지털 국립중앙박물관 — Museum as Code

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Han Language](https://img.shields.io/badge/han-.hgl-green.svg)](https://github.com/han-lang/han)
[![Python Pipeline](https://img.shields.io/badge/Pipeline-Python-orange.svg)](pipeline/)

---

## 소개 / Introduction

**Museum as Code**는 국보·보물 등 한국의 소중한 문화재를 **han** (`.hgl`) 프로그래밍 언어 소스 코드로 디지털화하는 프로젝트입니다. 각 문화재를 구조체(struct)로建模하여 코드로서 보존하고, 파이프라인을 통해 e뮤지엄 API에서 자동으로 데이터를 가져와 `.hgl` 파일을 생성합니다.

**Museum as Code** is a project that digitizes Korea's precious cultural heritage — national treasures and treasures — as source code in the **han** (`.hgl`) programming language. Each artifact is modeled as a struct, preserved as code, and automatically generated from the e뮤지엄 API via a Python pipeline.

---

## 한(han) 언어 / Han Language

**han** (.hgl)은 한국어 문법으로 작성하는 범용 프로그래밍 언어입니다. 한국어 키워드(`구조`, `함수`, `변수`, `문자열`, `정수`)를 사용해 코드를 작성합니다.

**han** (`.hgl`) is a general-purpose programming language written in Korean grammar. You write code using Korean keywords like `구조`, `함수`, `변수`, `문자열`, `정수`.

### 예시 / Example

```hgl
// 국보 제1호 — 서울 숭례문 (예시 / Example)
// Designated: National Treasure No. 1
// Era: Joseon Dynasty / 조선시대
// Material: Stone / 석재

구조 문화재 {
    명칭: 문자열,
    지정번호: 정수,
    분류: 문자열,
    소재지: 문자열,
    시대: 문자열,
    재질: 문자열,
}

구현 문화재 {
    함수 정보출력(자신: 문화재) {
        반환 ()
    }
}

함수 main() {
    변수 유물 = 문화재 {
        명칭: "서울 숭례문",
        지정번호: 1,
        분류: "유적건조물",
        소재지: "서울특별시 종로구",
        시대: "조선시대",
        재질: "석재",
    }
}
```

> **참고 / Note**: han 컴파일러(`hgl`)는 `$ hgl check <file.hgl>` 명령으로 `.hgl` 파일의 문법을 검증할 수 있습니다.
> Run `$ hgl check <file.hgl>` to validate `.hgl` file syntax.

---

## 디렉토리 구조 / Directory Structure

```
museum-as-code/
├── artifacts/                    # 문화재 소스 코드 / Artifact source code
│   ├── national-treasures/        # 국보 코드 / National Treasures (.hgl)
│   ├── treasures/                 # 보물 코드 / Treasures (.hgl)
│   └── special/
│       └── kdh/                   # 케이팝 데몬 헌터스 컬렉션 / K-pop Demon Hunters collection
├── pipeline/                     # 데이터 파이프라인 / Data pipeline
│   ├── api_client.py             # e뮤지엄 API 클라이언트 / eMuseumn API client
│   ├── config.py                 # 설정 및 API 키 로딩 / Configuration & API key loading
│   ├── templates/                # Jinja2 .hgl 템플릿 / Jinja2 .hgl templates
│   └── schemas/                   # JSON 스키마 / JSON schemas
├── docs/                         # 문서 / Documentation
├── requirements.txt              # Python 의존성 / Python dependencies
├── LICENSE                       # MIT 라이선스 / MIT License
└── README.md
```

---

## 파이프라인 / Pipeline

Python 파이프라인은 **e뮤지엄 Open API**에서 문화재 데이터를 가져와 `.hgl` 파일로 생성합니다.

The Python pipeline fetches cultural heritage data from the **e뮤지엄 Open API** and generates `.hgl` files.

### 설정 / Setup

```bash
# API 키 내보내기 / Export your API key
export EMUSEUM_API_KEY='your_key_here'

# 의존성 설치 / Install dependencies
pip install -r requirements.txt

# 파이프라인 실행 / Run the pipeline
python -m pipeline.api_client
```

> API 키는 [공공데이터포털](https://www.data.go.kr)에서 "전국 박물관 유물정보" 데이터셋을 신청하면 발급받을 수 있습니다.
> Get your API key from [공공데이터포털](https://www.data.go.kr) by applying for the "전국 박물관 유물정보" dataset.

---

## 기여하기 / Contributing

새로운 문화재를 추가하거나 버그를 수정하는 기여를 환영합니다!

Contributions are welcome — add new artifacts, fix bugs, or improve the pipeline!

### 방법 / How to Contribute

1. `artifacts/national-treasures/` 또는 `artifacts/treasures/` 디렉토리에 `.hgl` 파일을 추가하세요.
   Add a `.hgl` file to `artifacts/national-treasures/` or `artifacts/treasures/`.

2. 동일한 이름의 `.json` 사이드카 파일을 추가하세요 (메타데이터 포함).
   Add a `.json` sidecar file with the same name (include metadata).

3. `$ hgl check`로 문법을 검증하세요.
   Validate syntax with `$ hgl check`.

4. Pull Request를 제출하세요.
   Submit a Pull Request.

---

## 라이선스 / License

이 프로젝트는 **MIT License** 하에 배포됩니다.

This project is distributed under the **MIT License**.

See [LICENSE](LICENSE) for details.
