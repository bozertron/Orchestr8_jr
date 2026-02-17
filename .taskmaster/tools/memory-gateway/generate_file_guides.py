#!/usr/bin/env python3
"""Generate per-file integration sidecars with deterministic naming.

Output naming convention:
  <source_filename>.integration.md
  <source_filename>.integration.json

The output directory mirrors source relative paths so files stay collision-safe.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Any


ANCHOR_RE = re.compile(r"^(.*?):(\d+):(.*)$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate per-file integration guides")
    parser.add_argument("--manifest", required=True, help="Corpus ingest manifest JSON")
    parser.add_argument("--key-lines", required=True, help="key_lines_with_files.tsv path")
    parser.add_argument("--output-root", required=True, help="Root folder for generated guides")
    parser.add_argument("--max-anchors", type=int, default=20, help="Max anchors per file guide")
    return parser.parse_args()


def load_manifest(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_anchors(path: Path) -> Dict[str, List[Dict[str, Any]]]:
    by_file: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line:
            continue
        match = ANCHOR_RE.match(line)
        if not match:
            continue
        src, line_no, text = match.group(1), int(match.group(2)), match.group(3).strip()
        by_file[src].append({"line": line_no, "text": text})
    return by_file


def extract_risks(total_lines: int, anchors: List[Dict[str, Any]]) -> List[str]:
    text_blob = " ".join(a["text"].lower() for a in anchors)
    risks: List[str] = []

    if total_lines > 600:
        risks.append("Large surface area: high chance of hidden coupling and missed assumptions.")
    elif total_lines > 300:
        risks.append("Medium-large surface area: requires strict scope control during integration.")

    if "authoritative" in text_blob or "locked" in text_blob or "must" in text_blob:
        risks.append("Constraint-heavy document: treat as canonical rules, not optional guidance.")

    if "state_managers" in text_blob or "healthwatcher" in text_blob or "healthchecker" in text_blob:
        risks.append("State pipeline coupling: root state keys and health flow ordering must stay aligned.")

    if "postmessage" in text_blob or "woven_maps_node_click" in text_blob or "handle_node_click" in text_blob:
        risks.append("JS/Python bridge risk: event transport and payload validation can silently fail.")

    if "gold" in text_blob or "teal" in text_blob or "purple" in text_blob or "no breathing" in text_blob:
        risks.append("Visual canon risk: color/motion contract regressions are easy to introduce.")

    if "sitting room" in text_blob or "zoom" in text_blob or "warp" in text_blob or "camera" in text_blob:
        risks.append("Behavioral sequencing risk: mode transitions need explicit state machine handling.")

    if "edge" in text_blob and "relationship" in text_blob:
        risks.append("Data truth risk: edges must come from relationship graph, not UI-local assumptions.")

    if not risks:
        risks.append("General integration risk: enforce tests around schema, state, and behavior contracts.")

    return risks


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def render_markdown(
    source: str,
    total_lines: int,
    sha256: str,
    chunk_count: int,
    observation_ids: List[int],
    anchors: List[Dict[str, Any]],
    risks: List[str],
) -> str:
    obs_min = min(observation_ids) if observation_ids else None
    obs_max = max(observation_ids) if observation_ids else None
    obs_range = f"{obs_min}..{obs_max}" if obs_min is not None else "none"
    out: List[str] = []
    out.append(f"# {Path(source).name} Integration Guide")
    out.append("")
    out.append(f"- Source: `{source}`")
    out.append(f"- Total lines: `{total_lines}`")
    out.append(f"- SHA256: `{sha256}`")
    out.append(f"- Memory chunks: `{chunk_count}`")
    out.append(f"- Observation IDs: `{obs_range}`")
    out.append("")
    out.append("## Why This Is Painful")
    out.append("")
    for risk in risks:
        out.append(f"- {risk}")
    out.append("")
    out.append("## Anchor Lines")
    out.append("")
    if not anchors:
        out.append("- No extracted anchors for this file.")
    else:
        for anchor in anchors:
            line_no = anchor["line"]
            text = anchor["text"]
            out.append(f"- `{source}:{line_no}` {text}")
    out.append("")
    out.append("## Integration Use")
    out.append("")
    out.append("- Read this first to avoid re-deriving constraints.")
    out.append("- Implement against these anchors, then verify in runtime tests.")
    out.append("")
    return "\n".join(out)


def main() -> int:
    args = parse_args()
    manifest_path = Path(args.manifest)
    key_lines_path = Path(args.key_lines)
    output_root = Path(args.output_root)

    manifest = load_manifest(manifest_path)
    anchors_by_file = load_anchors(key_lines_path)

    index_rows: List[Dict[str, str]] = []

    for file_entry in manifest.get("files", []):
        source = file_entry["source"]
        total_lines = int(file_entry["total_lines"])
        sha256 = file_entry["sha256"]
        chunk_count = int(file_entry["chunk_count"])
        chunks = file_entry.get("chunks", [])
        observation_ids = [c["observation_id"] for c in chunks if isinstance(c.get("observation_id"), int)]

        anchors = anchors_by_file.get(source, [])[: args.max_anchors]
        risks = extract_risks(total_lines, anchors)

        source_path = Path(source)
        rel_parent = source_path.parent
        base_name = source_path.name
        out_parent = output_root / rel_parent
        md_path = out_parent / f"{base_name}.integration.md"
        json_path = out_parent / f"{base_name}.integration.json"

        md_content = render_markdown(
            source=source,
            total_lines=total_lines,
            sha256=sha256,
            chunk_count=chunk_count,
            observation_ids=observation_ids,
            anchors=anchors,
            risks=risks,
        )
        write_file(md_path, md_content)

        json_payload = {
            "source": source,
            "total_lines": total_lines,
            "sha256": sha256,
            "chunk_count": chunk_count,
            "observation_ids": observation_ids,
            "risks": risks,
            "anchors": anchors,
            "generated_from": {
                "manifest": str(manifest_path),
                "key_lines": str(key_lines_path),
            },
        }
        write_file(json_path, json.dumps(json_payload, indent=2, ensure_ascii=False))

        index_rows.append(
            {
                "basename": base_name,
                "source": source,
                "md": str(md_path),
                "json": str(json_path),
            }
        )

    index_rows.sort(key=lambda x: (x["basename"].lower(), x["source"].lower()))

    index_md_lines: List[str] = []
    index_md_lines.append("# File Guides Index")
    index_md_lines.append("")
    index_md_lines.append("| Basename | Source | Guide | Data |")
    index_md_lines.append("|---|---|---|---|")
    for row in index_rows:
        index_md_lines.append(
            f"| `{row['basename']}` | `{row['source']}` | `{row['md']}` | `{row['json']}` |"
        )
    write_file(output_root / "FILE_GUIDES_INDEX.md", "\n".join(index_md_lines) + "\n")

    tsv_lines = ["basename\tsource\tguide_md\tguide_json"]
    for row in index_rows:
        tsv_lines.append(
            f"{row['basename']}\t{row['source']}\t{row['md']}\t{row['json']}"
        )
    write_file(output_root / "_SORT_BY_FILENAME.tsv", "\n".join(tsv_lines) + "\n")

    print(f"Generated {len(index_rows)} per-file guides at {output_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
