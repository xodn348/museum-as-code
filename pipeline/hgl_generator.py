from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader

from pipeline.config import TEMPLATES_DIR


def _safe_identifier(designation: str) -> str:
    return designation.replace(" ", "")


def _build_artifact_id(kdcd: str, asno: str) -> str:
    return kdcd + asno.lstrip("0")


class HglGenerator:
    def __init__(self) -> None:
        self._env = Environment(
            loader=FileSystemLoader(str(TEMPLATES_DIR)),
            keep_trailing_newline=True,
        )

    def generate(self, artifact: dict[str, Any]) -> tuple[str, str]:
        kdcd = artifact.get("ccbaKdcd", "11")
        asno_padded = artifact["ccbaAsno"]
        asno_int = int(asno_padded)
        designation_type = "국보" if kdcd == "11" else "보물"
        designation = f"{designation_type} 제{asno_int}호"
        identifier = _safe_identifier(designation)
        image_rel = artifact.get("ccbaImage", "")
        image_url = f"https://www.emuseum.go.kr{image_rel}" if image_rel else ""
        created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        hgl_vars = {
            "이름": artifact["ccbaMnm1"],
            "영문명": artifact.get("ccbaMnm2", ""),
            "지정번호": designation,
            "지정번호_식별자": identifier,
            "분류": artifact.get("ccbaClas", ""),
            "시대": artifact.get("ccbsChrcd", ""),
            "재질": artifact.get("ccmiName", ""),
            "크기": artifact.get("ccbaSize", ""),
            "소장처": artifact.get("ccmaName", ""),
            "설명": artifact.get("ccbaCncl", ""),
            "이미지URL": image_url,
            "API출처": "e뮤지엄 Open API (fallback)",
            "생성일": created_at[:10],
        }

        template = self._env.get_template("artifact_template.hgl.tmpl")
        hgl_content = template.render(**hgl_vars)

        id_suffix = asno_padded.lstrip("0") or "0"
        artifact_id = f"nb_{int(id_suffix):03d}"

        sidecar: dict[str, Any] = {
            "id": artifact_id,
            "name": artifact["ccbaMnm1"],
            "name_en": artifact.get("ccbaMnm2", ""),
            "designation": designation,
            "designation_type": designation_type,
            "era": artifact.get("ccbsChrcd", ""),
            "material": artifact.get("ccmiName", ""),
            "size": artifact.get("ccbaSize", ""),
            "location": artifact.get("ccmaName", ""),
            "description": artifact.get("ccbaCncl", ""),
            "category": artifact.get("ccbaClas", ""),
            "image_url": image_url,
            "hgl_file": f"national-treasures/{artifact_id}.hgl",
            "source": "e뮤지엄 Open API (fallback)",
            "created_at": created_at,
        }

        json_content = json.dumps(sidecar, ensure_ascii=False, indent=2) + "\n"

        return hgl_content, json_content
