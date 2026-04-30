from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Final, TypedDict, cast

from pipeline.artifact_io import COLLECTIONS, PROJECT_ROOT, DOCS_DIR, docs_artifact_data_path, docs_artifact_hgl_path, resolve_local_artifact_image


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
    image_url: str
    exact_image_verified: bool


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


MANIFEST_PATH = DOCS_DIR / "manifest.json"

COLLECTION_SPECS: Final[list[CollectionSpec]] = [
    {
        "id": collection["id"],
        "name_ko": collection["name_ko"],
        "name_en": collection["name_en"],
        "glob": collection["glob"],
        "sort_order": index,
    }
    for index, collection in enumerate(COLLECTIONS)
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


def _bool_field(sidecar: dict[str, object], key: str) -> bool:
    return sidecar.get(key) is True


def _resolve_local_image_url(sidecar_path: Path, artifact_id: str) -> str:
    return resolve_local_artifact_image(sidecar_path, artifact_id)


def _load_artifact_entry(sidecar_path: Path, collection_id: str) -> ManifestArtifact:
    sidecar = _read_sidecar(sidecar_path)
    artifact_id = _string_field(sidecar, "id")

    return {
        "id": artifact_id,
        "collection": collection_id,
        "hgl_path": docs_artifact_hgl_path(collection_id, sidecar_path),
        "json_path": docs_artifact_data_path(collection_id, sidecar_path),
        "name_ko": _string_field(sidecar, "name"),
        "name_en": _string_field(sidecar, "name_en"),
        "period": _string_field(sidecar, "era"),
        "designation": _string_field(sidecar, "designation"),
        "image_url": _resolve_local_image_url(sidecar_path, artifact_id) or _string_field(sidecar, "image_url"),
        "exact_image_verified": _bool_field(sidecar, "exact_image_verified"),
        "license": _string_field(sidecar, "license"),
        "credit": _string_field(sidecar, "credit"),
        "source_url": _string_field(sidecar, "source_url"),
        "confidence": _string_field(sidecar, "confidence"),
        "needs_verification": _string_field(sidecar, "needs_verification"),
        "verification_note": _string_field(sidecar, "verification_note"),
        "room_tags": sidecar.get("room_tags", []),
    }


def _deduplicate_artifact_ids(artifacts: list[ManifestArtifact]) -> None:
    id_counts: dict[str, int] = {}

    for artifact in artifacts:
        original_id = artifact["id"]
        occurrence = id_counts.get(original_id, 0) + 1
        id_counts[original_id] = occurrence

        if occurrence > 1:
            artifact["id"] = f"{original_id}_{occurrence}"


def build_manifest() -> ManifestDocument:
    artifacts: list[ManifestArtifact] = []
    collection_counts: dict[str, int] = {}
    collection_sort_order: dict[str, int] = {}
    artifact_id_counts: dict[str, int] = {}

    for collection in COLLECTION_SPECS:
        collection_id = collection["id"]
        sidecar_files = sorted(PROJECT_ROOT.glob(collection["glob"]))
        collection_counts[collection_id] = len(sidecar_files)
        collection_sort_order[collection_id] = collection["sort_order"]

        for sidecar_path in sidecar_files:
            artifact = _load_artifact_entry(sidecar_path, collection_id)
            base_id = artifact["id"]
            duplicate_count = artifact_id_counts.get(base_id, 0) + 1
            artifact_id_counts[base_id] = duplicate_count

            if duplicate_count > 1:
                artifact["id"] = f"{base_id}_{duplicate_count}"

            artifacts.append(artifact)

    artifacts.sort(
        key=lambda artifact: (
            collection_sort_order[artifact["collection"]],
            artifact["id"],
        )
    )

    _deduplicate_artifact_ids(artifacts)

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
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
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
