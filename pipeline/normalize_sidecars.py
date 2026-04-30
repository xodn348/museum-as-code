from __future__ import annotations

from datetime import datetime, timezone

from pipeline.artifact_io import iter_artifact_records, resolve_local_artifact_image, write_json, string_field

DEFAULT_LICENSE = "needs_verification"
DEFAULT_CREDIT = "Museum as Code local artifact image; original source requires verification"


def normalize() -> tuple[int, int]:
    changed = 0
    total = 0
    timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    for record in iter_artifact_records():
        total += 1
        data = dict(record.data)
        before = dict(data)
        artifact_id = string_field(data, "id") or record.path.stem
        local_image = resolve_local_artifact_image(record.path, artifact_id)
        previous_image = string_field(data, "image_url")

        if local_image:
            data["source_url"] = data.get("source_url") or previous_image or "needs_verification"
            data["image_url"] = local_image
            data["images"] = data.get("images") or [
                {
                    "path": local_image,
                    "source_url": data["source_url"],
                    "license": data.get("license") or DEFAULT_LICENSE,
                    "credit": data.get("credit") or DEFAULT_CREDIT,
                }
            ]
        else:
            data["source_url"] = data.get("source_url") or previous_image or "needs_verification"
            data["image_url"] = ""
            data["images"] = data.get("images") or []
            data["needs_verification"] = data.get("needs_verification") or "No local artifact image resolved."

        data["license"] = data.get("license") or DEFAULT_LICENSE
        data["credit"] = data.get("credit") or DEFAULT_CREDIT
        data["confidence"] = data.get("confidence") or "low" if data.get("source") == "e뮤지엄 Open API (fallback)" else data.get("confidence") or "medium"
        data["updated_at"] = data.get("updated_at") or timestamp

        if data != before:
            write_json(record.path, data)
            changed += 1
    return total, changed


if __name__ == "__main__":
    total, changed = normalize()
    print(f"Normalized {changed}/{total} sidecars")
