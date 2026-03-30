"""
Museum as Code - Pipeline Configuration
환경변수에서 API 키와 설정을 로드합니다.
"""

import os
from pathlib import Path

# ── 프로젝트 경로 ────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).parent.parent
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
NATIONAL_TREASURES_DIR = ARTIFACTS_DIR / "national-treasures"
TREASURES_DIR = ARTIFACTS_DIR / "treasures"
PIPELINE_DIR = PROJECT_ROOT / "pipeline"
TEMPLATES_DIR = PIPELINE_DIR / "templates"
SCHEMAS_DIR = PIPELINE_DIR / "schemas"
API_SAMPLES_DIR = PIPELINE_DIR / "api_samples"

# ── API 키 설정 ──────────────────────────────────────────────────────────────
# .env 파일이나 환경변수에서 로드
# 사용법: export EMUSEUM_API_KEY="your_key_here"
#         export DATA_GO_KR_API_KEY="your_key_here"

EMUSEUM_API_KEY = os.environ.get("EMUSEUM_API_KEY", "")
DATA_GO_KR_API_KEY = os.environ.get("DATA_GO_KR_API_KEY", "")

# ── API 엔드포인트 ───────────────────────────────────────────────────────────
EMUSEUM_BASE_URL = "https://www.emuseum.go.kr/openapi"
API_BASE_URL = "https://www.emuseum.go.kr/openapi/"
EMUSEUM_RELIC_LIST_URL = f"{EMUSEUM_BASE_URL}/relic/list"
EMUSEUM_RELIC_DETAIL_URL = f"{EMUSEUM_BASE_URL}/relic/detail"

DATA_GO_KR_BASE_URL = "https://www.data.go.kr/openapi"

# ── 분류 코드 ────────────────────────────────────────────────────────────────
# 국가문화유산포털 분류 코드
DESIGNATION_CODES = {
    "국보": "11",  # National Treasure
    "보물": "12",  # Treasure
    "사적": "13",  # Historic Site
    "명승": "14",  # Scenic Site
    "천연기념물": "15",  # Natural Monument
}

# ── 파이프라인 설정 ──────────────────────────────────────────────────────────
DEFAULT_PAGE_SIZE = 100  # items per API page
MAX_RETRIES = 3
REQUEST_TIMEOUT = 30  # seconds
RATE_LIMIT_DELAY = 0.5  # seconds between API calls

# ── Han 컴파일러 경로 ────────────────────────────────────────────────────────
HAN_COMPILER_PATH = os.environ.get(
    "HAN_COMPILER_PATH", str(Path.home() / "han" / "target" / "release" / "han")
)


# ── 설정 검증 ────────────────────────────────────────────────────────────────
def validate_config() -> dict:
    """설정을 검증하고 상태를 반환합니다."""
    status = {
        "emuseum_api_key": bool(EMUSEUM_API_KEY),
        "data_go_kr_api_key": bool(DATA_GO_KR_API_KEY),
        "han_compiler_exists": Path(HAN_COMPILER_PATH).exists(),
        "artifacts_dir_exists": ARTIFACTS_DIR.exists(),
        "national_treasures_dir_exists": NATIONAL_TREASURES_DIR.exists(),
        "treasures_dir_exists": TREASURES_DIR.exists(),
    }
    return status


def get_api_key() -> str:
    """Return the e뮤지엄 API key from environment, raising if missing."""
    key = EMUSEUM_API_KEY.strip()
    if not key:
        raise EnvironmentError(
            "Missing required environment variable 'EMUSEUM_API_KEY'. "
            "Set it before running the pipeline: export EMUSEUM_API_KEY='your_key'"
        )
    return key


if __name__ == "__main__":
    print("=== Museum as Code 파이프라인 설정 ===")
    status = validate_config()
    for key, value in status.items():
        icon = "✅" if value else "❌"
        print(f"  {icon} {key}: {value}")

    if not status["emuseum_api_key"]:
        print("\n⚠️  EMUSEUM_API_KEY 환경변수가 설정되지 않았습니다.")
        print("   export EMUSEUM_API_KEY='your_key_here'")

    if not status["data_go_kr_api_key"]:
        print("\n⚠️  DATA_GO_KR_API_KEY 환경변수가 설정되지 않았습니다.")
        print("   export DATA_GO_KR_API_KEY='your_key_here'")
