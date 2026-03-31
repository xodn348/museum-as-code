# Museum as Code — 파이프라인

이 디렉토리에는 국립중앙박물관 유물 데이터를 .hgl 파일로 변환하는 Python 파이프라인이 포함되어 있습니다.

## 구조

```
pipeline/
├── config.py          # 환경변수 설정 및 경로 관리
├── fetcher.py         # API 데이터 수집 (T6에서 구현)
├── generator.py       # .hgl 파일 생성 (T7에서 구현)
├── validator.py       # Han 컴파일러 검증 (T8에서 구현)
├── manifest.py        # manifest.json 업데이트 (T9에서 구현)
├── templates/
│   └── artifact_template.hgl.tmpl   # .hgl 파일 템플릿
├── schemas/
│   └── artifact_schema.json         # JSON 사이드카 스키마
├── api_samples/
│   └── README.md                    # API 샘플 데이터 설명
└── README.md          # 이 파일
```

## 설치

```bash
cd museum-as-code
pip install -r requirements.txt
```

## 환경변수 설정

```bash
# e뮤지엄 Open API 키
export EMUSEUM_API_KEY="your_emuseum_api_key"

# 공공데이터포털 API 키  
export DATA_GO_KR_API_KEY="your_data_go_kr_api_key"

# Han 컴파일러 경로 (기본값: ~/han/target/release/han)
export HAN_COMPILER_PATH="/path/to/han"
```

## API 키 발급

### e뮤지엄 Open API
1. https://www.emuseum.go.kr/openApi 접속
2. 회원가입 및 API 키 신청
3. 발급된 키를 EMUSEUM_API_KEY 환경변수에 설정

### 공공데이터포털 API
1. https://www.data.go.kr 접속
2. 회원가입 후 "문화재청_국가문화유산포털_문화재검색서비스" 활용 신청
3. 발급된 키를 DATA_GO_KR_API_KEY 환경변수에 설정

## 설정 확인

```bash
python pipeline/config.py
```

## 파이프라인 실행 (T6-T9 구현 후)

```bash
# 국보 목록 수집 및 .hgl 생성
python pipeline/fetcher.py --type 국보 --limit 10

# 전체 파이프라인 실행
python pipeline/run.py --type 국보
```
