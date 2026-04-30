"""
국가유산청(CHA) 공식 Open API 에서 국보·보물 이미지 URL을 가져와
artifacts/national-treasures/*.json 사이드카에 매핑하는 파이프라인.

CHA Open API (인증 불필요, 무료, 공공누리 제1유형):
  - 목록: https://www.cha.go.kr/cha/SearchKindOpenapiList.do
      params: ccbaKdcd=11(국보)/12(보물), pageUnit, pageIndex
      응답: <item> ... <ccbaAsno>0000010000000</ccbaAsno> ... </item>
  - 상세: https://www.cha.go.kr/cha/SearchKindOpenapiDt.do
      params: ccbaKdcd, ccbaAsno (13자리), ccbaCtcd
      응답: <imageUrl>http://www.khs.go.kr/.../X.jpg</imageUrl>, <content>...</content>

매칭 키:
  사이드카 designation = "국보 제83호" → asno_index = 83
  CHA item ccbaAsno = "0000830000000" → 첫 6자리(000083) → asno_index 83
  → 같은 asno_index 끼리 매칭.

매칭된 항목에 다음 필드 추가:
  image_official_url      : str  (CHA 응답 imageUrl)
  image_source_api        : "cha"
  image_official_license  : "공공누리 제1유형(출처표시)"
  image_official_credit   : "국가유산청 (Cultural Heritage Administration of Korea)"
  image_fetched_at        : ISO-8601 UTC

EMUSEUM 보조 fallback은 추후 작업 (키 발급 필요). 본 모듈은 CHA만 다룬다.
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from xml.etree import ElementTree as ET

from pipeline.artifact_io import (
    PROJECT_ROOT,
    iter_artifact_records,
    read_json,
    write_json,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

CHA_LIST_URL = "https://www.cha.go.kr/cha/SearchKindOpenapiList.do"
CHA_DETAIL_URL = "https://www.cha.go.kr/cha/SearchKindOpenapiDt.do"

DESIGNATION_KDCD = {
    "국보": "11",
    "보물": "12",
}

CHA_LICENSE = "공공누리 제1유형(출처표시)"
CHA_CREDIT = "국가유산청 (Cultural Heritage Administration of Korea)"
CHA_SOURCE_API = "cha"

REQUEST_TIMEOUT = 15  # seconds
RATE_LIMIT_GAP = 0.5  # seconds between HTTP calls
USER_AGENT = "museum-as-code/1.0 (+https://github.com/xodn348/museum-as-code)"

DESIGNATION_PATTERN = re.compile(r"제\s*(\d+)\s*호")

logger = logging.getLogger("fetch_official_images")


# ---------------------------------------------------------------------------
# HTTP helper (stdlib urllib, no external deps)
# ---------------------------------------------------------------------------


_last_request_time: float = 0.0


def _throttled_get(url: str, params: dict[str, str]) -> bytes:
    """Throttled GET. Returns raw bytes. One retry on transient failure."""
    global _last_request_time
    elapsed = time.monotonic() - _last_request_time
    if elapsed < RATE_LIMIT_GAP:
        time.sleep(RATE_LIMIT_GAP - elapsed)

    qs = urllib.parse.urlencode(params)
    full_url = f"{url}?{qs}"
    req = urllib.request.Request(full_url, headers={"User-Agent": USER_AGENT})

    last_err: Optional[Exception] = None
    for attempt in range(2):
        try:
            with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
                _last_request_time = time.monotonic()
                return resp.read()
        except (urllib.error.URLError, TimeoutError) as exc:
            last_err = exc
            logger.warning("HTTP attempt %d failed for %s: %s", attempt + 1, full_url, exc)
            time.sleep(1.0 * (attempt + 1))

    raise RuntimeError(f"HTTP failed after retries: {full_url}: {last_err}")


# ---------------------------------------------------------------------------
# Designation parsing
# ---------------------------------------------------------------------------


def parse_designation_number(designation: str) -> Optional[int]:
    """'국보 제83호' / '보물 제1234호' → 83 / 1234. Returns None if unparseable."""
    if not designation:
        return None
    match = DESIGNATION_PATTERN.search(designation)
    if not match:
        return None
    return int(match.group(1))


def parse_designation_type(designation: str) -> Optional[str]:
    """'국보 제83호' → '국보'."""
    if not designation:
        return None
    for label in DESIGNATION_KDCD:
        if designation.startswith(label):
            return label
    return None


def asno_to_index(asno: str) -> Optional[int]:
    """CHA `ccbaAsno` → designation number index.

    13 digit ccbaAsno format: first 6 digits encode the heritage number,
    remaining 7 digits encode sub-treasure / part. e.g. '0000010000000' → 1.
    """
    if not asno or not asno.isdigit():
        return None
    if len(asno) >= 6:
        try:
            return int(asno[:6])
        except ValueError:
            return None
    try:
        return int(asno)
    except ValueError:
        return None


# ---------------------------------------------------------------------------
# CHA API calls
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ChaListItem:
    name_ko: str
    name_hanja: str
    ccba_kdcd: str
    ccba_ctcd: str
    ccba_asno: str
    asno_index: int


def fetch_cha_list(kdcd: str, page_unit: int = 200) -> list[ChaListItem]:
    """Fetch the full CHA list for a designation type. One paginated sweep."""
    items: list[ChaListItem] = []
    page_index = 1
    while True:
        body = _throttled_get(
            CHA_LIST_URL,
            {
                "ccbaKdcd": kdcd,
                "pageUnit": str(page_unit),
                "pageIndex": str(page_index),
            },
        )
        try:
            root = ET.fromstring(body)
        except ET.ParseError as exc:
            raise RuntimeError(f"CHA list page {page_index} returned invalid XML: {exc}")

        total_cnt = int((root.findtext("totalCnt") or "0").strip() or 0)
        page_items = root.findall("item")
        for el in page_items:
            asno = (el.findtext("ccbaAsno") or "").strip()
            idx = asno_to_index(asno)
            if idx is None:
                continue
            items.append(
                ChaListItem(
                    name_ko=(el.findtext("ccbaMnm1") or "").strip(),
                    name_hanja=(el.findtext("ccbaMnm2") or "").strip(),
                    ccba_kdcd=(el.findtext("ccbaKdcd") or kdcd).strip(),
                    ccba_ctcd=(el.findtext("ccbaCtcd") or "").strip(),
                    ccba_asno=asno,
                    asno_index=idx,
                )
            )
        if len(items) >= total_cnt or not page_items:
            break
        page_index += 1
        if page_index > 50:  # safety circuit breaker
            logger.warning("CHA list pagination exceeded 50 pages, stopping")
            break

    logger.info("CHA list (kdcd=%s): fetched %d items (total=%d)", kdcd, len(items), total_cnt)
    return items


@dataclass(frozen=True)
class ChaDetail:
    image_url: str
    content: str
    name_ko: str
    era: str


def fetch_cha_detail(kdcd: str, asno: str, ctcd: str) -> Optional[ChaDetail]:
    """Fetch detail (incl. imageUrl) for one heritage item.

    Returns None if no usable imageUrl on the record.
    """
    body = _throttled_get(
        CHA_DETAIL_URL,
        {"ccbaKdcd": kdcd, "ccbaAsno": asno, "ccbaCtcd": ctcd},
    )
    try:
        root = ET.fromstring(body)
    except ET.ParseError as exc:
        logger.warning("CHA detail (asno=%s) invalid XML: %s", asno, exc)
        return None

    item = root.find("item")
    if item is None:
        return None

    image_url = (item.findtext("imageUrl") or "").strip()
    if not image_url:
        return None
    # Normalize to https (CHA serves both, but http triggers mixed-content
    # warnings on GitHub Pages).
    if image_url.startswith("http://"):
        image_url = "https://" + image_url[len("http://"):]

    return ChaDetail(
        image_url=image_url,
        content=(item.findtext("content") or "").strip(),
        name_ko=(item.findtext("ccbaMnm1") or "").strip(),
        era=(item.findtext("ccceName") or "").strip(),
    )


# ---------------------------------------------------------------------------
# Sidecar update logic
# ---------------------------------------------------------------------------


@dataclass
class MatchResult:
    sidecar_path: Path
    artifact_id: str
    designation: str
    designation_index: Optional[int]
    cha_item: Optional[ChaListItem]
    image_url: str = ""
    skipped_reason: str = ""


def collect_national_treasures() -> list[Path]:
    """Return sorted sidecar JSON paths for the national-treasures collection."""
    paths: list[Path] = []
    for record in iter_artifact_records():
        if record.collection_id != "national-treasures":
            continue
        paths.append(record.path)
    return paths


def build_index(items: list[ChaListItem]) -> dict[int, ChaListItem]:
    """Map asno_index → first matching CHA item.

    Multiple items can share the same designation number when there are
    sub-treasures (제N-1호, 제N-2호 …). Currently the encoding lives in the
    last 7 digits of ccbaAsno; we keep the first encountered (sub=0000000) and
    log conflicts.
    """
    out: dict[int, ChaListItem] = {}
    for item in items:
        existing = out.get(item.asno_index)
        if existing is None:
            out[item.asno_index] = item
            continue
        # Prefer the entry whose tail is all zeros (root designation).
        if item.ccba_asno.endswith("0000000") and not existing.ccba_asno.endswith("0000000"):
            out[item.asno_index] = item
    return out


def update_sidecar(path: Path, detail: ChaDetail, item: ChaListItem, dry_run: bool) -> bool:
    """Write the new image fields into the sidecar. Return True if file changed."""
    payload = read_json(path)

    new_fields = {
        "image_official_url": detail.image_url,
        "image_source_api": CHA_SOURCE_API,
        "image_official_license": CHA_LICENSE,
        "image_official_credit": CHA_CREDIT,
        "image_official_source_name_ko": item.name_ko,
        "image_fetched_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    changed = False
    for key, value in new_fields.items():
        if payload.get(key) != value:
            payload[key] = value
            changed = True

    if changed and not dry_run:
        write_json(path, payload)
    return changed


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def run(
    *,
    dry_run: bool,
    limit: Optional[int],
    designation_label: str = "국보",
) -> int:
    kdcd = DESIGNATION_KDCD.get(designation_label)
    if not kdcd:
        raise ValueError(f"Unsupported designation label: {designation_label}")

    sidecars = collect_national_treasures()
    if not sidecars:
        logger.warning("No national-treasures sidecars found.")
        return 0

    logger.info("Found %d national-treasures sidecars", len(sidecars))

    if dry_run:
        # Dry run: no HTTP, only show what we *would* match against the
        # designation index. Useful for catching parse failures locally.
        no_designation = 0
        for path in sidecars:
            data = read_json(path)
            idx = parse_designation_number(data.get("designation", ""))
            if idx is None:
                no_designation += 1
                logger.info("[dry-run] %s: cannot parse designation %r", path.name, data.get("designation"))
                continue
            logger.info("[dry-run] %s: designation=%s → asno_index=%d", path.name, data.get("designation"), idx)
        logger.info("[dry-run] %d sidecars without parseable designation.", no_designation)
        return 0

    # Real run: fetch CHA list once, build index, then per-sidecar detail call.
    cha_items = fetch_cha_list(kdcd)
    cha_index = build_index(cha_items)

    matched = 0
    fetched = 0
    skipped: list[MatchResult] = []

    for path in sidecars:
        if limit is not None and fetched >= limit:
            break
        data = read_json(path)
        designation = data.get("designation", "")
        d_label = parse_designation_type(designation) or designation_label
        if d_label != designation_label:
            # Only handle the requested type in this run.
            continue
        idx = parse_designation_number(designation)
        if idx is None:
            skipped.append(
                MatchResult(
                    sidecar_path=path,
                    artifact_id=data.get("id", ""),
                    designation=designation,
                    designation_index=None,
                    cha_item=None,
                    skipped_reason="unparseable_designation",
                )
            )
            continue
        item = cha_index.get(idx)
        if item is None:
            skipped.append(
                MatchResult(
                    sidecar_path=path,
                    artifact_id=data.get("id", ""),
                    designation=designation,
                    designation_index=idx,
                    cha_item=None,
                    skipped_reason="no_cha_match",
                )
            )
            continue

        try:
            detail = fetch_cha_detail(item.ccba_kdcd, item.ccba_asno, item.ccba_ctcd)
        except RuntimeError as exc:
            logger.warning("Detail fetch failed for %s: %s", path.name, exc)
            skipped.append(
                MatchResult(
                    sidecar_path=path,
                    artifact_id=data.get("id", ""),
                    designation=designation,
                    designation_index=idx,
                    cha_item=item,
                    skipped_reason="detail_fetch_error",
                )
            )
            continue
        fetched += 1

        if detail is None:
            skipped.append(
                MatchResult(
                    sidecar_path=path,
                    artifact_id=data.get("id", ""),
                    designation=designation,
                    designation_index=idx,
                    cha_item=item,
                    skipped_reason="no_image_url_on_detail",
                )
            )
            continue

        changed = update_sidecar(path, detail, item, dry_run=False)
        if changed:
            matched += 1
            logger.info(
                "✔ %s ← %s (%s) %s",
                path.name,
                item.name_ko,
                designation,
                detail.image_url,
            )
        else:
            logger.info("· %s already up-to-date", path.name)

    logger.info("Done. matched=%d fetched=%d skipped=%d", matched, fetched, len(skipped))
    if skipped:
        logger.info("Skipped breakdown:")
        from collections import Counter
        for reason, count in Counter(s.skipped_reason for s in skipped).items():
            logger.info("  %s: %d", reason, count)
    return matched


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Skip HTTP, only show parsing.")
    parser.add_argument("--limit", type=int, default=None, help="Max sidecars to process.")
    parser.add_argument(
        "--type",
        dest="designation_label",
        choices=sorted(DESIGNATION_KDCD.keys()),
        default="국보",
        help="Designation type to process.",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Debug logging.")
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    try:
        run(
            dry_run=args.dry_run,
            limit=args.limit,
            designation_label=args.designation_label,
        )
    except Exception as exc:  # noqa: BLE001
        logger.exception("Pipeline failed: %s", exc)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
