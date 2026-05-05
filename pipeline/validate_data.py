from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from pipeline.artifact_io import PROJECT_ROOT, DOCS_DIR, is_remote_url, iter_artifact_records, read_json, string_field


# Modes the frontend renderer (docs/app.js resolveImageCaption + image rendering branches)
# treats as image-bearing. Anything else falls through to the IMAGE WITHHELD placeholder.
RENDERABLE_IMAGE_MODES = {"exact", "official", "representative"}
WITHHELD_MODE = "withheld"
ALLOWED_IMAGE_MODES = RENDERABLE_IMAGE_MODES | {WITHHELD_MODE, ""}


def _resolve_image(data: dict[str, Any]) -> tuple[str, str]:
    """Return (path, mode) using the same precedence as the frontend."""
    images = data.get("images") or []
    first = images[0] if images and isinstance(images[0], dict) else {}
    path = (
        first.get("path")
        or data.get("cover_image")
        or data.get("image_url")
        or ""
    )
    mode = data.get("image_display_mode") or first.get("image_display_mode") or ""
    return path, mode


def _check_path(errors: list[str], rel_path: str, label: str) -> None:
    path = PROJECT_ROOT / rel_path
    if not path.exists():
        errors.append(f"missing {label}: {rel_path}")


def _check_docs_path(errors: list[str], rel_path: str, label: str) -> None:
    path = DOCS_DIR / rel_path
    if not path.exists():
        errors.append(f"missing {label}: {rel_path}")


def _is_exact_image_verified(data: dict[str, Any]) -> bool:
    return data.get("exact_image_verified") is True


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
        if _is_exact_image_verified(data):
            if not image_url:
                errors.append(f"{record.path}: exact_image_verified requires image_url")
            if string_field(data, "needs_verification"):
                errors.append(f"{record.path}: exact_image_verified conflicts with needs_verification")
        # Renderable-image guard — catches the nb_057-class bug where mode is set
        # to a value the frontend doesn't recognise and the card silently falls
        # through to the IMAGE WITHHELD placeholder.
        path, mode = _resolve_image(data)
        if mode and mode not in ALLOWED_IMAGE_MODES:
            errors.append(
                f"{record.path}: unknown image_display_mode {mode!r} "
                f"(allowed: {sorted(ALLOWED_IMAGE_MODES)})"
            )
        if mode in RENDERABLE_IMAGE_MODES and not path:
            errors.append(
                f"{record.path}: image_display_mode={mode!r} requires an image path"
            )
        if mode == WITHHELD_MODE and not (
            string_field(data, "needs_verification") or string_field(data, "verification_note")
        ):
            errors.append(
                f"{record.path}: image_display_mode='withheld' must provide "
                f"needs_verification or verification_note explaining why"
            )
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
        if _is_exact_image_verified(artifact):
            if not image_url:
                errors.append(f"manifest exact_image_verified requires image_url for {artifact.get('id')}")
            if string_field(artifact, "needs_verification"):
                errors.append(f"manifest exact_image_verified conflicts with needs_verification for {artifact.get('id')}")
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
        data_file = string_field(hero, "data_file")
        hero_data_path = DOCS_DIR / data_file
        if hero_data_path.exists():
            hero_data = read_json(hero_data_path)
            exact = _is_exact_image_verified(hero_data) or _is_exact_image_verified(hero)
            if exact:
                primary_image = hero_data.get("images", [{}])
                if isinstance(primary_image, list) and primary_image and isinstance(primary_image[0], dict):
                    image_record = primary_image[0]
                else:
                    image_record = {}
                for field in ["path", "source_url", "license", "credit", "confidence"]:
                    if not string_field(image_record, field):
                        errors.append(f"{hero_data_path}: exact hero image missing {field}")
                if string_field(hero_data, "needs_verification") or string_field(image_record, "needs_verification"):
                    errors.append(f"{hero_data_path}: exact hero image conflicts with needs_verification")


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
