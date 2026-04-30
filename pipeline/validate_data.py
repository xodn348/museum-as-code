from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from pipeline.artifact_io import PROJECT_ROOT, DOCS_DIR, is_remote_url, iter_artifact_records, read_json, string_field


def _check_path(errors: list[str], rel_path: str, label: str) -> None:
    path = PROJECT_ROOT / rel_path
    if not path.exists():
        errors.append(f"missing {label}: {rel_path}")


def _check_docs_path(errors: list[str], rel_path: str, label: str) -> None:
    path = DOCS_DIR / rel_path
    if not path.exists():
        errors.append(f"missing {label}: {rel_path}")


def validate_artifact_sidecars(errors: list[str]) -> None:
    seen: dict[str, int] = {}
    for record in iter_artifact_records():
        data = record.data
        artifact_id = string_field(data, "id") or record.path.stem
        seen[artifact_id] = seen.get(artifact_id, 0) + 1
        for field in ["name", "designation", "era", "material", "location", "hgl_file"]:
            if not string_field(data, field):
                errors.append(f"{record.path}: missing {field}")
        image_url = string_field(data, "image_url")
        if is_remote_url(image_url):
            errors.append(f"{record.path}: image_url must be local, got {image_url}")
        if image_url:
            _check_path(errors, f"docs/{image_url}", f"image for {artifact_id}")
        for field in ["license", "source_url", "credit", "confidence"]:
            if not string_field(data, field):
                errors.append(f"{record.path}: missing provenance field {field}")
    duplicates = sorted(k for k, v in seen.items() if v > 1)
    if duplicates:
        print(f"Intentional duplicate artifact ids deduplicated in manifest: {', '.join(duplicates)}")


def validate_manifest(errors: list[str]) -> None:
    manifest = read_json(DOCS_DIR / "manifest.json")
    for artifact in manifest.get("artifacts", []):
        if not isinstance(artifact, dict):
            errors.append("manifest contains non-object artifact")
            continue
        image_url = string_field(artifact, "image_url")
        if is_remote_url(image_url):
            errors.append(f"manifest remote image_url for {artifact.get('id')}: {image_url}")
        if image_url:
            _check_path(errors, f"docs/{image_url}", f"manifest image for {artifact.get('id')}")
        for key in ["json_path", "hgl_path"]:
            rel_path = string_field(artifact, key)
            if rel_path.startswith("data/"):
                _check_docs_path(errors, rel_path, f"manifest {key} for {artifact.get('id')}")
            else:
                _check_path(errors, rel_path, f"manifest {key} for {artifact.get('id')}")


def validate_heroes(errors: list[str]) -> None:
    index_path = DOCS_DIR / "data" / "heroes" / "index.json"
    if not index_path.exists():
        return
    index = read_json(index_path)
    heroes = index.get("heroes", [])
    if len(heroes) != 10:
        errors.append(f"hero index expected 10 heroes, found {len(heroes)}")
    for hero in heroes:
        if not isinstance(hero, dict):
            errors.append("hero index contains non-object hero")
            continue
        hero_id = string_field(hero, "id")
        _check_path(errors, f"docs/{string_field(hero, 'data_file')}", f"hero data for {hero_id}")
        hgl_path = string_field(hero, "hgl_path")
        if hgl_path.startswith("data/"):
            _check_docs_path(errors, hgl_path, f"hero hgl for {hero_id}")
        else:
            _check_path(errors, hgl_path.replace("../", ""), f"hero hgl for {hero_id}")
        image = string_field(hero, "cover_image")
        if image:
            _check_path(errors, f"docs/{image}", f"hero image for {hero_id}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate Museum as Code data and local image references")
    parser.add_argument("--skip-heroes", action="store_true", help="Do not validate Phase C hero files")
    args = parser.parse_args()

    errors: list[str] = []
    validate_artifact_sidecars(errors)
    validate_manifest(errors)
    if not args.skip_heroes:
        validate_heroes(errors)
    read_json(DOCS_DIR / "data" / "graph.json")

    if errors:
        print("Data validation failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print("Data validation passed")


if __name__ == "__main__":
    main()
