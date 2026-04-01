
## 2026-03-31 Task 0d: Pipeline Audit
Pipeline file: pipeline/manifest.py (CORRECTION: task description said generate_graph.py but actual file is manifest.py)
Manifest output: docs/manifest.json
Sidecar extraction location: line 90-99 in function _load_artifact_entry()
Fields currently extracted: id, collection, hgl_path, json_path, name_ko, name_en, period, designation
Code to add in _load_artifact_entry() (after line 98):
    "image_url": _string_field(sidecar, "image_url"),
Also update ManifestArtifact TypedDict (lines 17-25) to add: image_url: str
Regen command: python3 pipeline/manifest.py
Note: generate_graph.py produces docs/data/graph.json (Cytoscape), NOT manifest.json

## 2026-03-31 Task 0d: Pipeline Audit

**IMPORTANT CORRECTION**: The task description incorrectly named `generate_graph.py` as the source of `manifest.json`. The CORRECT file is `pipeline/manifest.py`.

| Item | Value |
|------|-------|
| Pipeline file | `pipeline/manifest.py` |
| Manifest output | `docs/manifest.json` |
| Sidecar extraction location | `_load_artifact_entry()` function, lines 86-99 |
| TypedDict location | `ManifestArtifact` class, lines 17-25 |
| Fields currently extracted (8) | `id`, `collection`, `hgl_path`, `json_path`, `name_ko`, `name_en`, `period`, `designation` |
| `image_url` in sidecar | YES — present in `nb_001.json` line 13 |
| `image_url` in manifest | NO — currently missing |

**Code to add (after line 98 in `_load_artifact_entry()`)**:
```python
"image_url": _string_field(sidecar, "image_url"),
```

**Also add to `ManifestArtifact` TypedDict (after line 25)**:
```python
image_url: str
```

**Regeneration command**:
```bash
cd /Users/jnnj92/museum-as-code && python -m pipeline.manifest
```

**Evidence file**: `.sisyphus/evidence/task-0d-pipeline-audit.txt`

## 2026-04-01 F4 Scope Fidelity Audit Decision
- Audit baseline chosen: range `df95a5a^..HEAD` (from first rename task commit through current HEAD), then mapped by commit message + touched files.
- Rationale: commit-order indexing (`HEAD~N`) was unsafe due to duplicate commit messages and interleaved non-plan commits.
- Compliance policy applied: any file touched outside declared task scope counts as contamination; any file changed in baseline outside all declared task scopes counts as unaccounted.

## 2026-04-01 Final Verification Remediation Decision
- Implemented id deduplication inside `pipeline/manifest.py` generation path (not post-process in frontend) so `docs/manifest.json` is guaranteed safe for all consumers.
