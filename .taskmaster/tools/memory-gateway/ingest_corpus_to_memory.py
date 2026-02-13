#!/usr/bin/env python3
"""Ingest a corpus of files into claude-mem, preserving full line coverage.

Each observation stores:
- source path
- line range
- file hash
- exact line content with line numbers
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Dict, Any


DEFAULT_WORKER_URL = "http://127.0.0.1:37777"
SAVE_ENDPOINT = "/api/memory/save"


@dataclass
class ChunkRecord:
    source: str
    start_line: int
    end_line: int
    observation_id: int | None
    title: str
    ok: bool
    error: str | None = None


@dataclass
class FileRecord:
    source: str
    total_lines: int
    sha256: str
    chunk_size: int
    chunk_count: int
    saved_count: int
    chunks: List[ChunkRecord]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ingest full corpus into claude-mem")
    parser.add_argument("--targets-file", required=True, help="Path to newline-delimited file list")
    parser.add_argument("--manifest", required=True, help="Output manifest JSON path")
    parser.add_argument("--worker-url", default=DEFAULT_WORKER_URL, help="claude-mem worker base URL")
    parser.add_argument("--chunk-lines", type=int, default=80, help="Lines per memory chunk")
    parser.add_argument("--project", default="orchestr8-code-city-corpus", help="Memory project label")
    parser.add_argument("--sleep-ms", type=int, default=20, help="Delay between requests")
    return parser.parse_args()


def read_targets(path: Path) -> List[Path]:
    targets: List[Path] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        item = raw.strip()
        if not item or item.startswith("#"):
            continue
        targets.append(Path(item))
    return targets


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            block = f.read(65536)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


def post_json(url: str, payload: Dict[str, Any], timeout: float = 30.0) -> Dict[str, Any]:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url=url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = resp.read().decode("utf-8")
        return json.loads(body) if body else {}


def build_chunk_text(source: str, start_line: int, end_line: int, total_lines: int, sha: str, lines: List[str]) -> str:
    numbered = []
    for idx, content in enumerate(lines, start=start_line):
        numbered.append(f"{idx:06d}|{content.rstrip()}")
    return "\n".join(
        [
            f"SOURCE: {source}",
            f"LINE_RANGE: {start_line}-{end_line}",
            f"TOTAL_LINES: {total_lines}",
            f"SHA256: {sha}",
            "CONTENT:",
            *numbered,
        ]
    )


def ingest_file(path: Path, worker_url: str, chunk_lines: int, project: str, sleep_ms: int) -> FileRecord:
    source = str(path)
    raw_lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    total = len(raw_lines)
    sha = file_sha256(path)

    chunks: List[ChunkRecord] = []
    for start in range(1, total + 1, chunk_lines):
        end = min(total, start + chunk_lines - 1)
        slice_lines = raw_lines[start - 1 : end]
        title = f"corpus::{source}::L{start}-L{end}"
        text = build_chunk_text(source, start, end, total, sha, slice_lines)
        payload = {"title": title, "text": text, "project": project}

        obs_id: int | None = None
        ok = False
        err_msg: str | None = None

        for attempt in range(1, 4):
            try:
                resp = post_json(f"{worker_url.rstrip('/')}{SAVE_ENDPOINT}", payload)
                if resp.get("success") is True and isinstance(resp.get("id"), int):
                    obs_id = int(resp["id"])
                    ok = True
                    break
                err_msg = f"unexpected response: {resp}"
            except urllib.error.HTTPError as e:
                body = e.read().decode("utf-8", errors="replace")
                err_msg = f"http {e.code}: {body}"
            except Exception as e:  # pragma: no cover - defensive
                err_msg = str(e)
            time.sleep(0.2 * attempt)

        chunks.append(
            ChunkRecord(
                source=source,
                start_line=start,
                end_line=end,
                observation_id=obs_id,
                title=title,
                ok=ok,
                error=err_msg,
            )
        )

        if sleep_ms > 0:
            time.sleep(sleep_ms / 1000.0)

    saved_count = sum(1 for c in chunks if c.ok)
    return FileRecord(
        source=source,
        total_lines=total,
        sha256=sha,
        chunk_size=chunk_lines,
        chunk_count=len(chunks),
        saved_count=saved_count,
        chunks=chunks,
    )


def main() -> int:
    args = parse_args()
    targets_file = Path(args.targets_file)
    manifest_path = Path(args.manifest)

    targets = read_targets(targets_file)
    if not targets:
        print("No targets found.", file=sys.stderr)
        return 1

    missing = [str(p) for p in targets if not p.exists()]
    if missing:
        print("Missing target files:", file=sys.stderr)
        for m in missing:
            print(f"  - {m}", file=sys.stderr)
        return 2

    file_records: List[FileRecord] = []
    started_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    for target in targets:
        record = ingest_file(
            path=target,
            worker_url=args.worker_url,
            chunk_lines=args.chunk_lines,
            project=args.project,
            sleep_ms=args.sleep_ms,
        )
        file_records.append(record)
        print(
            f"[ingested] {record.source} lines={record.total_lines} "
            f"chunks={record.chunk_count} saved={record.saved_count}"
        )

    finished_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    total_lines = sum(r.total_lines for r in file_records)
    total_chunks = sum(r.chunk_count for r in file_records)
    total_saved = sum(r.saved_count for r in file_records)
    ok = total_saved == total_chunks

    manifest_payload: Dict[str, Any] = {
        "started_at_utc": started_at,
        "finished_at_utc": finished_at,
        "worker_url": args.worker_url,
        "project": args.project,
        "chunk_lines": args.chunk_lines,
        "summary": {
            "file_count": len(file_records),
            "total_lines": total_lines,
            "total_chunks": total_chunks,
            "saved_chunks": total_saved,
            "all_saved": ok,
        },
        "files": [
            {
                **asdict(fr),
                "chunks": [asdict(c) for c in fr.chunks],
            }
            for fr in file_records
        ],
    }

    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest_payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[manifest] {manifest_path}")
    print(
        f"[summary] files={len(file_records)} lines={total_lines} "
        f"chunks={total_chunks} saved={total_saved} all_saved={ok}"
    )
    return 0 if ok else 3


if __name__ == "__main__":
    raise SystemExit(main())
