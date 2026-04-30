from __future__ import annotations

import json
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = PROJECT_ROOT / "docs"
MANIFEST_PATH = DOCS_DIR / "manifest.json"
HEROES_DIR = DOCS_DIR / "data" / "heroes"
AUDIT_JSON_PATH = DOCS_DIR / "data" / "image-audit.json"
AUDIT_MD_PATH = DOCS_DIR / "data" / "image-audit.md"


def _load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Expected JSON object in {path}")
    return data


def _as_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return str(value)


def _first_text(values: list[Any]) -> str:
    for value in values:
        text = _as_text(value).strip()
        if text:
            return text
    return ""


def _source_from_urls(value: Any) -> str:
    if isinstance(value, list):
        return _first_text(value)
    return _as_text(value)


def _is_explicit_true(mapping: dict[str, Any], key: str) -> bool:
    return key in mapping and mapping[key] is True


def _truthy_status(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return bool(value.strip())
    return value is not None


def _display_status(exact_image_verified: bool) -> str:
    return "photo" if exact_image_verified else "withheld"


def _recommended_action(exact_image_verified: bool, verification_note: Any) -> str:
    if exact_image_verified:
        return "Display the local image; keep source/license metadata with the record."
    note = _as_text(verification_note).strip()
    if note:
        return f"Keep code fallback; {note}"
    return "Keep code fallback until an exact local image, source URL, license, and credit are verified."


def _select_hero_image(hero: dict[str, Any]) -> dict[str, Any]:
    images = hero.get("images")
    if not isinstance(images, list):
        images = []

    normalized_images = [image for image in images if isinstance(image, dict)]
    preferred_path = _first_text([hero.get("cover_image"), hero.get("image_url")])

    for image in normalized_images:
        if _as_text(image.get("path")) == preferred_path:
            return image

    if normalized_images:
        return normalized_images[0]

    return {}


def _manifest_entries(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list):
        raise ValueError(f"Expected artifacts list in {MANIFEST_PATH}")

    entries: list[dict[str, Any]] = []
    for artifact in artifacts:
        if not isinstance(artifact, dict):
            continue

        exact_image_verified = _is_explicit_true(artifact, "exact_image_verified")
        explicit_needs_verification = artifact.get("needs_verification")
        license_text = _as_text(artifact.get("license"))
        needs_verification = _truthy_status(explicit_needs_verification) or license_text == "needs_verification" or not exact_image_verified

        entries.append(
            {
                "record_type": "manifest_artifact",
                "id": _as_text(artifact.get("id")),
                "name": _first_text([artifact.get("name_en"), artifact.get("name_ko")]),
                "collection": _as_text(artifact.get("collection")),
                "image_path": _as_text(artifact.get("image_url")),
                "source": _as_text(artifact.get("source_url")),
                "license": license_text,
                "confidence": _as_text(artifact.get("confidence")),
                "needs_verification": needs_verification,
                "verification_note": _as_text(explicit_needs_verification),
                "exact_image_verified": exact_image_verified,
                "display_status": _display_status(exact_image_verified),
                "action": _recommended_action(exact_image_verified, explicit_needs_verification),
                "input_path": MANIFEST_PATH.relative_to(PROJECT_ROOT).as_posix(),
            }
        )

    return entries


def _hero_entries() -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for hero_path in sorted(HEROES_DIR.glob("*.json")):
        hero = _load_json(hero_path)
        hero_id = _as_text(hero.get("id"))
        if not hero_id:
            # docs/data/heroes/index.json is an aggregate index, not an image-bearing hero record.
            continue

        image = _select_hero_image(hero)
        exact_image_verified = _is_explicit_true(image, "exact_image_verified") or _is_explicit_true(
            hero, "exact_image_verified"
        )
        explicit_needs_verification = image.get("needs_verification", hero.get("needs_verification"))
        license_text = _first_text([image.get("license"), hero.get("license")])
        needs_verification = _truthy_status(explicit_needs_verification) or not exact_image_verified

        entries.append(
            {
                "record_type": "hero",
                "id": hero_id,
                "name": _first_text([hero.get("name_en"), hero.get("name_ko")]),
                "collection": "heroes",
                "image_path": _first_text([image.get("path"), hero.get("cover_image"), hero.get("image_url")]),
                "source": _first_text(
                    [image.get("source_url"), hero.get("source_url"), _source_from_urls(hero.get("source_urls"))]
                ),
                "license": license_text,
                "confidence": _first_text([image.get("confidence"), hero.get("confidence")]),
                "needs_verification": needs_verification,
                "verification_note": _as_text(explicit_needs_verification),
                "exact_image_verified": exact_image_verified,
                "display_status": _display_status(exact_image_verified),
                "action": _recommended_action(exact_image_verified, explicit_needs_verification),
                "input_path": hero_path.relative_to(PROJECT_ROOT).as_posix(),
            }
        )

    return entries


def build_audit() -> dict[str, Any]:
    manifest = _load_json(MANIFEST_PATH)
    entries = _manifest_entries(manifest) + _hero_entries()
    entries.sort(key=lambda entry: (entry["record_type"], entry["collection"], entry["id"]))

    return {
        "schema_version": 1,
        "source_manifest": MANIFEST_PATH.relative_to(PROJECT_ROOT).as_posix(),
        "source_manifest_generated_at": _as_text(manifest.get("generated_at")),
        "source_hero_glob": HEROES_DIR.relative_to(PROJECT_ROOT).as_posix() + "/*.json",
        "summary": {
            "total_records": len(entries),
            "needs_verification": sum(1 for entry in entries if entry["needs_verification"]),
            "exact_image_verified": sum(1 for entry in entries if entry["exact_image_verified"]),
        },
        "entries": entries,
    }


def _md_escape(value: Any) -> str:
    return _as_text(value).replace("|", "\\|").replace("\n", " ")


def render_markdown(audit: dict[str, Any]) -> str:
    summary = audit["summary"]
    lines = [
        "# Image Audit",
        "",
        "Generated from `docs/manifest.json` and `docs/data/heroes/*.json`.",
        "",
        "## Summary",
        "",
        f"- Total records: {summary['total_records']}",
        f"- Needs verification: {summary['needs_verification']}",
        f"- Exact image verified: {summary['exact_image_verified']}",
        "",
        "## Records",
        "",
        "| Type | ID | Name | Image path | Source | License | Confidence | Display | Needs verification | Exact image verified | Action |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]

    for entry in audit["entries"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    _md_escape(entry["record_type"]),
                    _md_escape(entry["id"]),
                    _md_escape(entry["name"]),
                    _md_escape(entry["image_path"]),
                    _md_escape(entry["source"]),
                    _md_escape(entry["license"]),
                    _md_escape(entry["confidence"]),
                    _md_escape(entry["display_status"]),
                    "yes" if entry["needs_verification"] else "no",
                    "yes" if entry["exact_image_verified"] else "no",
                    _md_escape(entry["action"]),
                ]
            )
            + " |"
        )

    return "\n".join(lines) + "\n"


def write_audit(audit: dict[str, Any]) -> None:
    AUDIT_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    AUDIT_JSON_PATH.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    AUDIT_MD_PATH.write_text(render_markdown(audit), encoding="utf-8")


def main() -> None:
    audit = build_audit()
    write_audit(audit)
    summary = audit["summary"]
    print(
        f"Wrote {AUDIT_JSON_PATH.relative_to(PROJECT_ROOT)} and {AUDIT_MD_PATH.relative_to(PROJECT_ROOT)} "
        f"({summary['total_records']} records; {summary['needs_verification']} need verification; "
        f"{summary['exact_image_verified']} exact images verified)."
    )


if __name__ == "__main__":
    main()
