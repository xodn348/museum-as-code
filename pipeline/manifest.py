from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Final, TypedDict, cast


class CollectionSpec(TypedDict):
    id: str
    name_ko: str
    name_en: str
    glob: str
    sort_order: int


class ManifestArtifact(TypedDict):
    id: str
    collection: str
    hgl_path: str
    json_path: str
    name_ko: str
    name_en: str
    period: str
    designation: str


class ManifestCollection(TypedDict):
    id: str
    name_ko: str
    name_en: str
    count: int


class ManifestDocument(TypedDict):
    generated_at: str
    total_count: int
    artifacts: list[ManifestArtifact]
    collections: list[ManifestCollection]


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"
MANIFEST_PATH = DOCS_DIR / "manifest.json"

COLLECTION_SPECS: Final[list[CollectionSpec]] = [
    {
        "id": "national-treasures",
        "name_ko": "국보·보물",
        "name_en": "National Treasures",
        "glob": "artifacts/national-treasures/*.json",
        "sort_order": 0,
    },
    {
        "id": "kdh",
        "name_ko": "케이팝 데몬 헌터스",
        "name_en": "K-pop Demon Hunters",
        "glob": "artifacts/special/kdh/*.json",
        "sort_order": 1,
    },
]


def _read_sidecar(path: Path) -> dict[str, object]:
    raw_data = cast(object, json.loads(path.read_text(encoding="utf-8")))
    if not isinstance(raw_data, dict):
        raise ValueError(f"Invalid sidecar format: {path}")

    raw_map = cast(dict[object, object], raw_data)
    sidecar: dict[str, object] = {}
    for key, value in raw_map.items():
        if isinstance(key, str):
            sidecar[key] = value
    return sidecar


def _string_field(sidecar: dict[str, object], key: str) -> str:
    value = sidecar.get(key)
    if isinstance(value, str):
        return value
    if value is None:
        return ""
    return str(value)


def _load_artifact_entry(sidecar_path: Path, collection_id: str) -> ManifestArtifact:
    sidecar = _read_sidecar(sidecar_path)
    relative_json_path = sidecar_path.relative_to(PROJECT_ROOT).as_posix()

    return {
        "id": _string_field(sidecar, "id"),
        "collection": collection_id,
        "hgl_path": relative_json_path.replace(".json", ".hgl"),
        "json_path": relative_json_path,
        "name_ko": _string_field(sidecar, "name"),
        "name_en": _string_field(sidecar, "name_en"),
        "period": _string_field(sidecar, "era"),
        "designation": _string_field(sidecar, "designation"),
    }


def build_manifest() -> ManifestDocument:
    artifacts: list[ManifestArtifact] = []
    collection_counts: dict[str, int] = {}
    collection_sort_order: dict[str, int] = {}

    for collection in COLLECTION_SPECS:
        collection_id = collection["id"]
        sidecar_files = sorted(PROJECT_ROOT.glob(collection["glob"]))
        collection_counts[collection_id] = len(sidecar_files)
        collection_sort_order[collection_id] = collection["sort_order"]

        for sidecar_path in sidecar_files:
            artifacts.append(_load_artifact_entry(sidecar_path, collection_id))

    artifacts.sort(
        key=lambda artifact: (
            collection_sort_order[artifact["collection"]],
            artifact["id"],
        )
    )

    collections: list[ManifestCollection] = [
        {
            "id": spec["id"],
            "name_ko": spec["name_ko"],
            "name_en": spec["name_en"],
            "count": collection_counts[spec["id"]],
        }
        for spec in COLLECTION_SPECS
    ]

    return {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "total_count": len(artifacts),
        "artifacts": artifacts,
        "collections": collections,
    }


def write_manifest(manifest: ManifestDocument) -> Path:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    _ = MANIFEST_PATH.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return MANIFEST_PATH


def main() -> None:
    manifest = build_manifest()
    output_path = write_manifest(manifest)
    total_count = manifest["total_count"]
    collection_count = len(manifest["collections"])
    relative_output_path = output_path.relative_to(PROJECT_ROOT).as_posix()
    print(
        f"Generated {relative_output_path}: {total_count} artifacts in {collection_count} collections"
    )


if __name__ == "__main__":
    main()
