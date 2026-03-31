import glob
import json
import os
import re
import sys


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NB_GLOB = os.path.join(PROJECT_ROOT, "artifacts", "national-treasures", "nb_*.json")
KDH_GLOB = os.path.join(PROJECT_ROOT, "artifacts", "special", "kdh", "kdh_*.json")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "docs", "data")
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "graph.json")


def _string_field(sidecar, key):
    value = sidecar.get(key)
    if isinstance(value, str):
        return value.strip()
    if value is None:
        return ""
    return str(value).strip()


def _warn_missing(artifact_id, field):
    print(f"WARNING: {artifact_id} missing {field}", file=sys.stderr)


def _normalize_era(era):
    return re.sub(r"\s*\(.*?\)\s*$", "", era).strip()


def _split_materials(material):
    return [part.strip() for part in material.split(",") if part.strip()]


def _load_sidecars():
    sidecar_paths = sorted(glob.glob(NB_GLOB)) + sorted(glob.glob(KDH_GLOB))
    artifacts = []

    for path in sidecar_paths:
        with open(path, "r", encoding="utf-8") as file:
            sidecar = json.load(file)

        artifact_id = _string_field(sidecar, "id")
        name_ko = _string_field(sidecar, "name")
        name_en = _string_field(sidecar, "name_en")

        era_raw = _string_field(sidecar, "era")
        era = _normalize_era(era_raw) if era_raw else ""
        if not era:
            _warn_missing(artifact_id, "era")

        category = _string_field(sidecar, "category")
        if not category:
            _warn_missing(artifact_id, "category")

        location = _string_field(sidecar, "location")
        if not location:
            _warn_missing(artifact_id, "location")

        material_raw = _string_field(sidecar, "material")
        materials = _split_materials(material_raw) if material_raw else []
        if not materials:
            _warn_missing(artifact_id, "material")

        artifacts.append(
            {
                "id": artifact_id,
                "label_ko": name_ko,
                "label_en": name_en,
                "era": era,
                "category": category,
                "location": location,
                "materials": materials,
            }
        )

    artifacts.sort(key=lambda artifact: artifact["id"])
    return artifacts


def _build_nodes(artifacts):
    nodes = []
    for artifact in artifacts:
        nodes.append(
            {
                "data": {
                    "id": artifact["id"],
                    "label_ko": artifact["label_ko"],
                    "label_en": artifact["label_en"],
                }
            }
        )
    return nodes


def _add_edge(edges, seen, source, target, edge_type, value):
    if not value:
        return
    key = (source, target, edge_type, value)
    if key in seen:
        return
    seen.add(key)
    edges.append(
        {
            "data": {
                "source": source,
                "target": target,
                "type": edge_type,
                "value": value,
            }
        }
    )


def _build_edges(artifacts):
    edges = []
    seen = set()

    for index in range(len(artifacts)):
        artifact_a = artifacts[index]
        for other_index in range(index + 1, len(artifacts)):
            artifact_b = artifacts[other_index]
            source = artifact_a["id"]
            target = artifact_b["id"]

            if artifact_a["era"] and artifact_a["era"] == artifact_b["era"]:
                _add_edge(edges, seen, source, target, "era", artifact_a["era"])

            if (
                artifact_a["category"]
                and artifact_a["category"] == artifact_b["category"]
            ):
                _add_edge(
                    edges, seen, source, target, "category", artifact_a["category"]
                )

            if (
                artifact_a["location"]
                and artifact_a["location"] == artifact_b["location"]
            ):
                _add_edge(
                    edges, seen, source, target, "location", artifact_a["location"]
                )

            material_overlap = sorted(
                set(artifact_a["materials"]).intersection(artifact_b["materials"])
            )
            for material in material_overlap:
                _add_edge(edges, seen, source, target, "material", material)

    return edges


def main():
    artifacts = _load_sidecars()
    nodes = _build_nodes(artifacts)
    edges = _build_edges(artifacts)
    graph = {"elements": {"nodes": nodes, "edges": edges}}

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
        _ = file.write(json.dumps(graph, ensure_ascii=False, indent=2) + "\n")

    relative_path = os.path.relpath(OUTPUT_PATH, PROJECT_ROOT)
    print(f"Generated {relative_path}: {len(nodes)} nodes, {len(edges)} edges")


if __name__ == "__main__":
    main()
