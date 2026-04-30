from __future__ import annotations

import shutil
from pathlib import Path

from pipeline.artifact_io import DOCS_ARTIFACT_DATA_DIR, PROJECT_ROOT, iter_artifact_records


def sync_docs_artifacts() -> list[Path]:
    written: list[Path] = []
    for record in iter_artifact_records():
        target_dir = DOCS_ARTIFACT_DATA_DIR / record.collection_id
        target_dir.mkdir(parents=True, exist_ok=True)

        json_target = target_dir / record.path.name
        shutil.copy2(record.path, json_target)
        written.append(json_target)

        hgl_source = record.path.with_suffix('.hgl')
        if hgl_source.exists():
            hgl_target = target_dir / hgl_source.name
            shutil.copy2(hgl_source, hgl_target)
            written.append(hgl_target)
    return written


def main() -> None:
    written = sync_docs_artifacts()
    print(f"Synced {len(written)} web artifact files under {DOCS_ARTIFACT_DATA_DIR.relative_to(PROJECT_ROOT)}")


if __name__ == '__main__':
    main()
