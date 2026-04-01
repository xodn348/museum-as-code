from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, cast

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


@dataclass(frozen=True)
class ArtifactSource:
    sidecar_id: str
    name: str
    image_code: str


@dataclass(frozen=True)
class DetailInfo:
    relic_id: str
    img_path: str


class RateLimitedSession:
    def __init__(self) -> None:
        self.session: requests.Session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/123.0.0.0 Safari/537.36"
                )
            }
        )
        self._last_request_time: float = 0.0

    def get(self, url: str, **kwargs: Any) -> requests.Response:
        elapsed = time.monotonic() - self._last_request_time
        if elapsed < REQUEST_DELAY_SECONDS:
            time.sleep(REQUEST_DELAY_SECONDS - elapsed)

        response = self.session.get(url, timeout=30, **kwargs)
        self._last_request_time = time.monotonic()
        return response


def load_sources() -> list[ArtifactSource]:
    sources: list[ArtifactSource] = []
    for sidecar_path in sorted(SIDECAR_DIR.glob("nb_*.json")):
        raw_data = json.loads(sidecar_path.read_text(encoding="utf-8"))
        if not isinstance(raw_data, dict):
            raise ValueError(f"Invalid sidecar payload in {sidecar_path}")
        data = cast(dict[str, Any], raw_data)
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


def find_relic_id_candidates(
    client: RateLimitedSession,
    image_code: str,
    page_limit: int = 2,
) -> list[str]:
    keyword = str(int(image_code))
    unique_ids: list[str] = []
    seen: set[str] = set()

    for page_number in range(1, page_limit + 1):
        response = with_retries(
            lambda: client.get(
                SEARCH_URL,
                params={
                    "detailFlag": "true",
                    "filedOp": "keyword",
                    "keyword": keyword,
                    "keywordHistory": keyword,
                    "pageNum": str(page_number),
                },
            )
        )
        raw_ids = cast(list[str], RELIC_ID_PATTERN.findall(response.text))
        for relic_id in raw_ids:
            if relic_id in seen:
                continue
            seen.add(relic_id)
            unique_ids.append(relic_id)

    if not unique_ids:
        raise RuntimeError(f"No relicId found for image code {image_code}")
    return unique_ids[:20]


def fetch_detail_info(
    client: RateLimitedSession,
    relic_id: str,
    cache: dict[str, DetailInfo],
) -> DetailInfo:
    cached = cache.get(relic_id)
    if cached:
        return cached

    detail_url = f"{DETAIL_URL}?relicId={relic_id}"
    response = with_retries(lambda: client.get(detail_url))
    img_paths = cast(list[str], IMG_PATH_PATTERN.findall(response.text))
    if not img_paths:
        raise RuntimeError(f"No /IMG endpoint found for relicId {relic_id}")

    info = DetailInfo(relic_id=relic_id, img_path=img_paths[0])
    cache[relic_id] = info
    return info


def pick_unique_detail(
    source: ArtifactSource,
    candidates: list[str],
    client: RateLimitedSession,
    cache: dict[str, DetailInfo],
) -> DetailInfo:
    valid_details: list[DetailInfo] = []
    for relic_id in candidates:
        try:
            valid_details.append(fetch_detail_info(client, relic_id, cache))
        except Exception:  # noqa: BLE001
            continue

    if not valid_details:
        raise RuntimeError(f"No valid /IMG detail page for {source.sidecar_id}")

    return valid_details[0]


def build_output_name(sequence: int) -> str:
    kdcd = "PS01002001"
    asno = f"{sequence:05d}0000"
    return f"{kdcd}_{asno}.jpg"


def download_image_bytes(client: RateLimitedSession, detail: DetailInfo) -> bytes:
    detail_url = f"{DETAIL_URL}?relicId={detail.relic_id}"
    image_url = f"{BASE_URL}{detail.img_path}"
    response = with_retries(
        lambda: client.get(
            image_url,
            headers={
                "Referer": detail_url,
                "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
            },
        )
    )

    content_type = response.headers.get("Content-Type", "").lower()
    if not content_type.startswith("image/jpeg"):
        raise RuntimeError(
            f"Invalid Content-Type for {detail.relic_id}: {response.headers.get('Content-Type', '')}"
        )

    image_bytes = response.content
    if not image_bytes.startswith(b"\xff\xd8"):
        raise RuntimeError(f"Invalid JPEG magic bytes for {detail.relic_id}")
    return image_bytes


def main() -> None:
    sources = load_sources()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    client = RateLimitedSession()
    detail_cache: dict[str, DetailInfo] = {}
    downloaded = 0
    failed: list[str] = []
    total_size_bytes = 0
    used_file_names: set[str] = set(
        file_path.name
        for file_path in OUTPUT_DIR.iterdir()
        if file_path.is_file() and file_path.suffix == ".jpg"
    )
    print(f"Found {len(used_file_names)} already-downloaded files, will skip them.")

    for index, source in enumerate(sources, start=1):
        print(f"Downloading {index}/57: {source.name}...")
        try:
            file_name = build_output_name(index)
            output_path = OUTPUT_DIR / file_name
            if output_path.exists():
                print(
                    f"  [{index}/57] SKIP {source.name} → already exists as {file_name}"
                )
                used_file_names.add(file_name)
                downloaded += 1
                total_size_bytes += output_path.stat().st_size
                continue

            candidates = find_relic_id_candidates(client, source.image_code)
            detail = pick_unique_detail(
                source,
                candidates,
                client,
                detail_cache,
            )
            image_bytes = download_image_bytes(client, detail)
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
