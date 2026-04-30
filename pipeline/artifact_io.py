from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Iterator, Mapping

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"
ARTIFACT_IMAGES_DIR = DOCS_DIR / "images" / "artifacts"
DOCS_ARTIFACT_DATA_DIR = DOCS_DIR / "data" / "artifacts"

COLLECTIONS: tuple[dict[str, str], ...] = (
    {
        "id": "national-treasures",
        "name_ko": "국보·보물",
        "name_en": "National Treasures",
        "glob": "artifacts/national-treasures/*.json",
    },
    {
        "id": "kdh",
        "name_ko": "케이팝 데몬 헌터스",
        "name_en": "K-pop Demon Hunters",
        "glob": "artifacts/special/kdh/*.json",
    },
)


@dataclass(frozen=True)
class ArtifactRecord:
    path: Path
    collection_id: str
    data: dict[str, Any]


def read_json(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError(f"Expected object JSON in {path}")
    return raw


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def string_field(data: Mapping[str, Any], key: str) -> str:
    value = data.get(key)
    if value is None:
        return ""
    return value.strip() if isinstance(value, str) else str(value).strip()


def normalize_era(era: str) -> str:
    return re.sub(r"\s*\(.*?\)\s*$", "", era).strip()


def split_materials(material: str) -> list[str]:
    return [part.strip() for part in re.split(r"[,/·]", material) if part.strip()]


def iter_artifact_records(collections: Iterable[Mapping[str, str]] = COLLECTIONS) -> Iterator[ArtifactRecord]:
    for collection in collections:
        collection_id = collection["id"]
        for path in sorted(PROJECT_ROOT.glob(collection["glob"])):
            yield ArtifactRecord(path=path, collection_id=collection_id, data=read_json(path))


def resolve_local_artifact_image(sidecar_path: Path, artifact_id: str) -> str:
    if not artifact_id or not ARTIFACT_IMAGES_DIR.exists():
        return ""

    image_paths = sorted(ARTIFACT_IMAGES_DIR.glob("*.jpg"))
    for image_path in image_paths:
        if image_path.stem.startswith(artifact_id):
            return f"images/artifacts/{image_path.name}"

    sidecar_stem = sidecar_path.stem
    stem_parts = sidecar_stem.rsplit("_", 1)
    if sidecar_stem.startswith("nb_") and len(stem_parts) == 2 and stem_parts[1].isdigit():
        image_suffix = f"_{int(stem_parts[1]) * 10000:09d}"
        for image_path in image_paths:
            if image_path.stem.endswith(image_suffix):
                return f"images/artifacts/{image_path.name}"
    return ""


def docs_artifact_data_path(collection_id: str, sidecar_path: Path) -> str:
    return f"data/artifacts/{collection_id}/{sidecar_path.name}"


def docs_artifact_hgl_path(collection_id: str, sidecar_path: Path) -> str:
    return docs_artifact_data_path(collection_id, sidecar_path).replace(".json", ".hgl")


def is_remote_url(value: str) -> bool:
    return value.startswith("http://") or value.startswith("https://")
