from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path
from typing import Callable

import requests

BASE_URL = "https://www.emuseum.go.kr"
SEARCH_URL = f"{BASE_URL}/headerSearch"
DETAIL_URL = f"{BASE_URL}/detail"
REQUEST_DELAY_SECONDS = 0.5
RETRY_COUNT = 3
RETRY_DELAY_SECONDS = 1.0

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SIDECAR_DIR = PROJECT_ROOT / "artifacts" / "national-treasures"
OUTPUT_DIR = PROJECT_ROOT / "docs" / "images" / "artifacts"

RELIC_ID_PATTERN = re.compile(r"PS\d{22}")
IMG_PATH_PATTERN = re.compile(r"/IMG/[A-Za-z0-9+/=]+")
TITLE_PATTERN = re.compile(r"<title>\s*([^<]+?)\s*</title>", re.IGNORECASE)
NON_WORD_PATTERN = re.compile(r"[^0-9A-Za-z가-힣]+")


@dataclass(frozen=True)
class ArtifactSource:
    sidecar_id: str
    name: str
    image_code: str


@dataclass(frozen=True)
class DetailInfo:
    relic_id: str
    title: str
    img_path: str


class RateLimitedSession:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/123.0.0.0 Safari/537.36"
                )
            }
        )
        self._last_request_time = 0.0

    def get(self, url: str, **kwargs: object) -> requests.Response:
        elapsed = time.monotonic() - self._last_request_time
        if elapsed < REQUEST_DELAY_SECONDS:
            time.sleep(REQUEST_DELAY_SECONDS - elapsed)

        response = self.session.get(url, timeout=30, **kwargs)
        self._last_request_time = time.monotonic()
        return response


def load_sources() -> list[ArtifactSource]:
    sources: list[ArtifactSource] = []
    for sidecar_path in sorted(SIDECAR_DIR.glob("nb_*.json")):
        data = json.loads(sidecar_path.read_text(encoding="utf-8"))
        image_url = str(data.get("image_url", ""))
        image_code = image_url.rsplit("/", maxsplit=1)[-1].split(".")[0]
        if not image_code:
            raise ValueError(f"Missing image code in {sidecar_path}")
        sources.append(
            ArtifactSource(
                sidecar_id=str(data.get("id", sidecar_path.stem)),
                name=str(data.get("name", sidecar_path.stem)),
                image_code=image_code,
            )
        )

    if len(sources) != 57:
        raise ValueError(f"Expected 57 sidecars, found {len(sources)}")
    return sources


def with_retries(fetch_fn: Callable[[], requests.Response]) -> requests.Response:
    last_error: Exception | None = None
    for attempt in range(1, RETRY_COUNT + 1):
        try:
            response = fetch_fn()
            if response.status_code >= 500:
                raise RuntimeError(f"Server error {response.status_code}")
            return response
        except Exception as error:  # noqa: BLE001
            last_error = error
            if attempt < RETRY_COUNT:
                time.sleep(RETRY_DELAY_SECONDS)
    raise RuntimeError(f"Request failed after {RETRY_COUNT} attempts: {last_error}")


def normalize_text(value: str) -> str:
    return NON_WORD_PATTERN.sub("", value).lower()


def score_similarity(left: str, right: str) -> float:
    left_norm = normalize_text(left)
    right_norm = normalize_text(right)
    if not left_norm or not right_norm:
        return 0.0
    return SequenceMatcher(None, left_norm, right_norm).ratio()


def _extract_relic_ids_from_keyword(
    client: RateLimitedSession, keyword: str, page_limit: int = 2
) -> list[str]:
    collected: list[str] = []
    seen: set[str] = set()

    for page_num in range(1, page_limit + 1):
        response = with_retries(
            lambda: client.get(
                SEARCH_URL,
                params={
                    "keyword": keyword,
                    "pageNum": str(page_num),
                },
            )
        )
        raw_ids = RELIC_ID_PATTERN.findall(response.text)
        if not raw_ids:
            break

        for relic_id in raw_ids:
            if relic_id in seen:
                continue
            seen.add(relic_id)
            collected.append(relic_id)

    return collected


def find_candidate_relic_ids(
    client: RateLimitedSession, source: ArtifactSource
) -> list[str]:
    designation_no = str(int(source.image_code))
    query_list = [
        str(int(source.image_code)),
        source.name,
        f"국보 {designation_no}호",
        f"국보{designation_no}호",
    ]

    unique_ids: list[str] = []
    seen: set[str] = set()

    for query in query_list:
        for relic_id in _extract_relic_ids_from_keyword(client, query):
            if relic_id in seen:
                continue
            seen.add(relic_id)
            unique_ids.append(relic_id)

    if not unique_ids:
        raise RuntimeError(f"No relicId found for image code {source.image_code}")
    return unique_ids[:20]


def fetch_detail_info(
    client: RateLimitedSession,
    relic_id: str,
    detail_cache: dict[str, DetailInfo],
) -> DetailInfo:
    cached = detail_cache.get(relic_id)
    if cached:
        return cached

    detail_page_url = f"{DETAIL_URL}?relicId={relic_id}"
    response = with_retries(lambda: client.get(detail_page_url))

    title_match = TITLE_PATTERN.search(response.text)
    title_text = title_match.group(1).strip() if title_match else relic_id
    title_text = title_text.split("- e뮤지엄")[0].strip()

    img_paths = IMG_PATH_PATTERN.findall(response.text)
    if not img_paths:
        raise RuntimeError(f"No /IMG endpoint found for relicId {relic_id}")

    info = DetailInfo(relic_id=relic_id, title=title_text, img_path=img_paths[0])
    detail_cache[relic_id] = info
    return info


def choose_detail_info(
    source: ArtifactSource,
    candidate_ids: list[str],
    client: RateLimitedSession,
    detail_cache: dict[str, DetailInfo],
    used_names: set[str],
) -> DetailInfo:
    scored_details: list[tuple[float, DetailInfo]] = []
    for relic_id in candidate_ids:
        try:
            detail_info = fetch_detail_info(client, relic_id, detail_cache)
            score = score_similarity(source.name, detail_info.title)
            scored_details.append((score, detail_info))
        except Exception:  # noqa: BLE001
            continue

    if not scored_details:
        raise RuntimeError(
            f"No valid detail candidates with /IMG endpoint for {source.sidecar_id}"
        )

    scored_details.sort(key=lambda item: item[0], reverse=True)

    for _, detail_info in scored_details:
        file_name = build_output_name(detail_info.relic_id)
        if file_name not in used_names:
            return detail_info

    return scored_details[0][1]


def build_output_name(relic_id: str) -> str:
    kdcd = relic_id[:10]
    asno = relic_id[10:19]
    return f"{kdcd}_{asno}.jpg"


def download_image_bytes(client: RateLimitedSession, detail_info: DetailInfo) -> bytes:
    detail_page_url = f"{DETAIL_URL}?relicId={detail_info.relic_id}"
    image_url = f"{BASE_URL}{detail_info.img_path}"
    response = with_retries(
        lambda: client.get(
            image_url,
            headers={"Referer": detail_page_url},
        )
    )

    content_type = response.headers.get("Content-Type", "").lower()
    if not content_type.startswith("image/jpeg"):
        raise RuntimeError(
            "Invalid Content-Type for "
            f"{detail_info.relic_id}: {response.headers.get('Content-Type', '')}"
        )

    image_bytes = response.content
    if not image_bytes.startswith(b"\xff\xd8"):
        raise RuntimeError(f"Invalid JPEG magic bytes for {detail_info.relic_id}")
    return image_bytes


def main() -> None:
    sources = load_sources()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    client = RateLimitedSession()
    detail_cache: dict[str, DetailInfo] = {}
    # Pre-populate used_file_names from files already downloaded
    used_file_names: set[str] = set(
        f.name for f in OUTPUT_DIR.iterdir() if f.is_file() and f.suffix == ".jpg"
    )
    print(f"Found {len(used_file_names)} already-downloaded files, will skip them.")
    downloaded = 0
    failed: list[str] = []
    total_size_bytes = 0

    for index, source in enumerate(sources, start=1):
        print(f"Downloading {index}/57: {source.name}...")
        try:
            candidate_ids = find_candidate_relic_ids(client, source)
            detail_info = choose_detail_info(
                source,
                candidate_ids,
                client,
                detail_cache,
                used_file_names,
            )
            file_name = build_output_name(detail_info.relic_id)
            output_path = OUTPUT_DIR / file_name

            if output_path.exists():
                print(
                    f"  [{index}/57] SKIP {source.name} → already exists as {file_name}"
                )
                used_file_names.add(file_name)
                downloaded += 1
                total_size_bytes += output_path.stat().st_size
                continue

            image_bytes = download_image_bytes(client, detail_info)
            output_path.write_bytes(image_bytes)

            used_file_names.add(file_name)
            downloaded += 1
            total_size_bytes += len(image_bytes)
        except Exception as error:  # noqa: BLE001
            failed.append(f"{source.sidecar_id}: {error}")

    total_size_mb = total_size_bytes / (1024 * 1024)
    print(
        f"Downloaded: {downloaded}/57, Failed: {len(failed)}, Total size: {total_size_mb:.2f} MB"
    )

    if failed:
        print("Failed items:")
        for item in failed:
            print(f"- {item}")


if __name__ == "__main__":
    main()
