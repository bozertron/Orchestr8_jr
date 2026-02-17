#!/usr/bin/env python3
"""Build reusable long-run phase prep artifacts from one shared TOML spec."""

from __future__ import annotations

import argparse
import re
import shlex
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import tomllib

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = ROOT / ".planning/orchestr8_next/execution/templates/phase_prep"
TEMPLATE_SPEC = TEMPLATE_DIR / "NEXT_PHASE_COLLAB_TEMPLATE.toml"

PLACEHOLDER_RE = re.compile(r"<[^>]+>")
OBS_ID_RE = re.compile(r"saved_id=(\d+)")


@dataclass
class LaneSpec:
    lane: str
    agent_id: str
    is_canonical: bool
    prompt_group: str
    packet_id: str
    boundary_file: str
    launch_file: str
    resume_file: str
    todo_output_file: str
    objective: str
    scope: str
    allowed_work: list[str]
    must_not: list[str]
    required_evidence: list[str]
    validation_commands: list[str]
    read_paths: list[str]
    completion_artifact: str
    checkout_scope: str
    tasks: list[str]


@dataclass
class LaneRuntime:
    spec: LaneSpec
    boundary_path: Path
    launch_path: Path
    resume_path: Path
    todo_path: Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Synthesize phase prep boundaries, prompts, TODOs, launch packs, and comms scripts."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    init_cmd = sub.add_parser("init", help="Copy the shared planning TOML template to a target path.")
    init_cmd.add_argument(
        "--output",
        default="SOT/CODEBASE_TODOS/NEXT_PHASE_COLLAB_WORKING.toml",
        help="Output TOML path (repo-relative or absolute).",
    )
    init_cmd.add_argument("--force", action="store_true", help="Overwrite existing output file.")

    render_cmd = sub.add_parser("render", help="Render artifacts from a filled planning TOML spec.")
    render_cmd.add_argument(
        "--spec",
        required=True,
        help="Path to the filled phase prep TOML spec (repo-relative or absolute).",
    )
    render_cmd.add_argument(
        "--send",
        action="store_true",
        help="Send unlock guidance broadcasts using scripts/agent_comms.sh.",
    )
    render_cmd.add_argument(
        "--kickoff-canonical",
        action="store_true",
        help="Execute canonical kickoff preflight + checkout + worklist + lint.",
    )

    return parser.parse_args()


def abort(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def root_path(path_str: str) -> Path:
    path = Path(path_str)
    if path.is_absolute():
        return path
    return ROOT / path


def rel_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    normalized = text.rstrip() + "\n"
    path.write_text(normalized, encoding="utf-8")


def load_spec(spec_path: Path) -> dict[str, Any]:
    if not spec_path.exists():
        abort(f"spec not found: {spec_path}")
    try:
        return tomllib.loads(spec_path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        abort(f"invalid TOML in {spec_path}: {exc}")


def validate_placeholders(value: Any, prefix: str, findings: list[str]) -> None:
    if isinstance(value, str):
        if PLACEHOLDER_RE.search(value):
            findings.append(f"{prefix}: {value}")
        return
    if isinstance(value, list):
        for idx, item in enumerate(value):
            validate_placeholders(item, f"{prefix}[{idx}]", findings)
        return
    if isinstance(value, dict):
        for key, item in value.items():
            validate_placeholders(item, f"{prefix}.{key}", findings)


def parse_lane(raw: dict[str, Any]) -> LaneSpec:
    required = [
        "lane",
        "agent_id",
        "is_canonical",
        "prompt_group",
        "packet_id",
        "boundary_file",
        "launch_file",
        "resume_file",
        "todo_output_file",
        "objective",
        "scope",
        "allowed_work",
        "must_not",
        "required_evidence",
        "validation_commands",
        "read_paths",
        "completion_artifact",
        "checkout_scope",
        "tasks",
    ]
    missing = [key for key in required if key not in raw]
    if missing:
        abort(f"lane entry missing keys: {', '.join(missing)}")

    def to_list(name: str) -> list[str]:
        value = raw[name]
        if not isinstance(value, list):
            abort(f"lane '{raw.get('lane', '<unknown>')}' field '{name}' must be a list")
        return [str(item) for item in value]

    return LaneSpec(
        lane=str(raw["lane"]),
        agent_id=str(raw["agent_id"]),
        is_canonical=bool(raw["is_canonical"]),
        prompt_group=str(raw["prompt_group"]),
        packet_id=str(raw["packet_id"]),
        boundary_file=str(raw["boundary_file"]),
        launch_file=str(raw["launch_file"]),
        resume_file=str(raw["resume_file"]),
        todo_output_file=str(raw["todo_output_file"]),
        objective=str(raw["objective"]),
        scope=str(raw["scope"]),
        allowed_work=to_list("allowed_work"),
        must_not=to_list("must_not"),
        required_evidence=to_list("required_evidence"),
        validation_commands=to_list("validation_commands"),
        read_paths=to_list("read_paths"),
        completion_artifact=str(raw["completion_artifact"]),
        checkout_scope=str(raw["checkout_scope"]),
        tasks=to_list("tasks"),
    )


def prompt_dir_for_group(paths_cfg: dict[str, Any], prompt_group: str) -> Path:
    mapping = {
        "execution": root_path(str(paths_cfg["exec_prompt_dir"])),
        "founder_console": root_path(str(paths_cfg["founder_prompt_dir"])),
        "mingos_settlement_lab": root_path(str(paths_cfg["mingos_prompt_dir"])),
    }
    if prompt_group not in mapping:
        abort(f"unsupported prompt_group '{prompt_group}'")
    return mapping[prompt_group]


def normalize_questions(raw_questions: Any) -> list[dict[str, str]]:
    if raw_questions is None:
        return []
    if not isinstance(raw_questions, list):
        abort("phase_questions must be a TOML array of tables")
    normalized: list[dict[str, str]] = []
    for idx, item in enumerate(raw_questions, start=1):
        if not isinstance(item, dict):
            abort(f"phase_questions[{idx}] must be a table")
        normalized.append(
            {
                "id": str(item.get("id", f"Q{idx}")),
                "question": str(item.get("question", "")).strip(),
                "owner": str(item.get("owner", "founder")).strip(),
                "answer": str(item.get("answer", "")).strip(),
                "status": str(item.get("status", "open")).strip().lower(),
                "impact_if_unanswered": str(item.get("impact_if_unanswered", "")).strip(),
            }
        )
    return normalized


def list_block(items: list[str], fallback: str = "none") -> str:
    if not items:
        return f"- {fallback}"
    return "\n".join(f"- {item}" for item in items)


def code_block(commands: list[str]) -> str:
    body = "\n".join(commands) if commands else "# no explicit command gate"
    return f"```bash\n{body}\n```"


def shell_quote(value: str) -> str:
    return shlex.quote(value)


def table_cell(value: str) -> str:
    return value.replace("|", r"\|").strip()


def render_boundary(lane: LaneSpec, unlock_authority: str, effective_date: str) -> str:
    validation = ""
    if lane.validation_commands:
        validation = (
            "\n## Required Validation\n\n"
            f"{code_block(lane.validation_commands)}\n"
        )
    return (
        f"# Autonomy Boundary: {lane.packet_id} ({lane.lane})\n\n"
        "## Objective\n\n"
        f"{lane.objective}\n\n"
        "## Scope\n\n"
        f"{lane.scope}\n\n"
        "## Allowed Work\n\n"
        f"{list_block(lane.allowed_work)}\n\n"
        "## Must Not Do\n\n"
        f"{list_block(lane.must_not)}\n\n"
        "## Required Evidence\n\n"
        f"{list_block(lane.required_evidence)}\n"
        f"{validation}"
        "## Unlock Authority\n\n"
        f"- Unlocked by: {unlock_authority}\n"
        f"- Effective: {effective_date}\n"
    )


def render_resume(
    lane: LaneSpec,
    phase_id: str,
    readme_path: Path,
    hard_requirements_path: Path,
    long_run_path: Path,
    guidance_path: Path,
    runtime: LaneRuntime,
    artifact_dir: Path,
) -> str:
    read_paths = [
        str(readme_path),
        str(hard_requirements_path),
        str(long_run_path),
        str(runtime.boundary_path),
        str(guidance_path),
        *lane.read_paths,
    ]
    dedup_reads = list(dict.fromkeys(read_paths))

    completion_artifact = lane.completion_artifact
    if "*" in completion_artifact or " and " in completion_artifact:
        delivery_commands = [
            f"install -d {artifact_dir}/",
            f"cp <lane_output_files> {artifact_dir}/",
            f"ls -l {completion_artifact}",
        ]
    else:
        delivery_commands = [
            f"install -d {artifact_dir}/",
            f"cp <lane_report> {completion_artifact}",
            f"ls -l {completion_artifact}",
        ]

    validation_section = ""
    if lane.validation_commands:
        validation_section = (
            "\nValidation:\n\n"
            f"{code_block(lane.validation_commands)}\n"
        )

    return (
        f"# Resume Prompt - {lane.lane} ({lane.packet_id})\n\n"
        f"Long-run mode: follow `{long_run_path}` for kickoff, low-interruption execution, and end-of-window bundle submission.\n\n"
        f"You are executing packet `{lane.packet_id}`.\n\n"
        "## Packet\n\n"
        f"- Packet ID: `{lane.packet_id}`\n"
        f"- Scope: {lane.scope}\n\n"
        "## Objective\n\n"
        f"{lane.objective}\n\n"
        "## Preconditions (required)\n\n"
        f"{code_block([f'/home/bozertron/Orchestr8_jr/scripts/agent_flags.sh unread {lane.agent_id} {phase_id}', '/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh health'])}\n\n"
        "Read:\n"
        f"{list_block([f'`{item}`' for item in dedup_reads])}\n\n"
        "Checkout (requires ack):\n\n"
        f"{code_block([f'/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh send {lane.agent_id} codex {phase_id} checkout true \"packet={lane.packet_id}; scope={lane.checkout_scope}; files=<files>; tests=<tests>; eta=<eta>\"'])}\n\n"
        "Worklist + lint:\n\n"
        f"{code_block([f'/home/bozertron/Orchestr8_jr/scripts/packet_bootstrap.sh {phase_id} {lane.packet_id} {lane.agent_id}', f'/home/bozertron/Orchestr8_jr/scripts/packet_lint.sh {runtime.resume_path} {runtime.boundary_path}'])}\n\n"
        "## Required outputs\n\n"
        f"{list_block([f'`{item}`' for item in lane.required_evidence])}\n\n"
        "Canonical delivery proof:\n\n"
        f"{code_block(delivery_commands)}\n"
        f"{validation_section}"
        "Closeout + ping:\n\n"
        f"{code_block([f'/home/bozertron/Orchestr8_jr/scripts/packet_closeout.sh {phase_id} {lane.packet_id}', f'OR8_PHASE={phase_id} /home/bozertron/Orchestr8_jr/scripts/ping_codex.sh 100 \"{lane.packet_id} long-run bundle complete; updated TODO + evidence posted\"'])}\n"
    )


def render_launch(
    lane: LaneSpec,
    long_run_path: Path,
    hard_requirements_path: Path,
    guidance_path: Path,
    runtime: LaneRuntime,
) -> str:
    return (
        f"# Launch Prompt - {lane.packet_id} ({lane.lane})\n\n"
        f"Long-run mode: follow `{long_run_path}` for kickoff, low-interruption execution, and end-of-window bundle submission.\n\n"
        "Read shared memory instructions at:\n"
        f"- `{runtime.resume_path}`\n"
        f"- `{runtime.boundary_path}`\n"
        f"- `{guidance_path}`\n"
        f"- `{hard_requirements_path}`\n"
        f"- `{long_run_path}`\n\n"
        f"Execute only packet `{lane.packet_id}`.\n\n"
        "When complete, respond exactly:\n"
        f"`please retrieve update at {lane.completion_artifact} and provide further direction.`\n"
    )


def render_todo(
    lane: LaneSpec,
    phase_id: str,
    date_str: str,
    open_questions: list[dict[str, str]],
) -> str:
    rows: list[str] = []
    evidence_pool = lane.required_evidence or [lane.completion_artifact]
    for idx, task in enumerate(lane.tasks, start=1):
        depends = "none" if idx == 1 else str(idx - 1)
        evidence = evidence_pool[min(idx - 1, len(evidence_pool) - 1)]
        rows.append(
            f"| {idx} | {table_cell(task)} | {depends} | ready | {table_cell(evidence)} |"
        )

    if not rows:
        rows.append("| 1 | Define packet work items from scope | none | ready | report + test proof |")

    q_rows: list[str] = []
    for question in open_questions:
        q_rows.append(
            "| {id} | {q} | pending | pending | open |".format(
                id=table_cell(question["id"]),
                q=table_cell(question["question"] or "Founder clarification required"),
            )
        )
    if not q_rows:
        q_rows.append("| 1 | none logged | n/a | n/a | n/a |")

    return (
        f"# {lane.lane} TODO ({phase_id}/{lane.packet_id})\n\n"
        f"Date: {date_str}\n"
        "Mode: Long-run\n\n"
        "## Objective\n\n"
        f"{lane.objective}\n\n"
        "## Scope\n\n"
        f"{lane.scope}\n\n"
        "## Task Queue\n\n"
        "| ID | Task | Depends On | Status | Required Evidence |\n"
        "|---|---|---|---|---|\n"
        f"{chr(10).join(rows)}\n\n"
        "## Validation\n\n"
        f"{code_block(lane.validation_commands)}\n\n"
        "## Ambiguity Log (No Assumptions)\n\n"
        "Rules:\n"
        "1. Add ambiguity line item.\n"
        "2. Probe local facts once.\n"
        "3. Probe cross-codebase facts once.\n"
        "4. If still unresolved: `deferred_due_to_missing_facts` and continue.\n\n"
        "| Item | Ambiguity | Probe 1 | Probe 2 | Outcome |\n"
        "|---|---|---|---|---|\n"
        f"{chr(10).join(q_rows)}\n"
    )


def render_exploration_notes(
    meta: dict[str, Any],
    lanes: list[LaneSpec],
    questions: list[dict[str, str]],
    exploration_cfg: dict[str, Any],
) -> str:
    def cfg_list(name: str) -> list[str]:
        value = exploration_cfg.get(name, [])
        if isinstance(value, list):
            return [str(item) for item in value]
        return []

    posture = cfg_list("current_posture")
    if not posture:
        posture = ["Packet prep workflow is initialized.", "Founder inputs are required to finalize next-wave scope."]

    open_questions = [
        q for q in questions if q["status"] != "answered" and not q["answer"]
    ]

    risk_rows: list[str] = []
    for idx, question in enumerate(questions, start=1):
        fact_check = question["answer"] if question["answer"] else "pending founder response"
        risk_rows.append(
            f"| {idx} | {table_cell(question['question'])} | {table_cell(fact_check)} |"
        )
    if not risk_rows:
        risk_rows.append("| 1 | none logged | n/a |")

    founder_inputs: list[str] = []
    for question in open_questions:
        founder_inputs.append(f"{question['id']}: {question['question']}")
    if not founder_inputs:
        founder_inputs.append("No open founder questions in this planning cycle.")

    readiness = [f"{lane.lane}: {lane.packet_id} - {lane.objective}" for lane in lanes]

    return (
        f"# Target Exploration Notes ({meta['phase_id']} {meta['wave_id']})\n\n"
        f"Date: {meta['date']}\n"
        "Owner: Codex\n\n"
        "## Scope Explored\n\n"
        f"- SOT sources:\n{list_block(cfg_list('sot_sources'))}\n"
        f"- check-in sources:\n{list_block(cfg_list('checkin_sources'))}\n"
        f"- artifact sources:\n{list_block(cfg_list('artifact_sources'))}\n"
        f"- roadmap/task queue sources:\n{list_block(cfg_list('roadmap_sources'))}\n"
        f"- runtime/code anchors:\n{list_block(cfg_list('runtime_anchors'))}\n\n"
        "## Current Program Posture\n\n"
        + "\n".join(f"{idx}. {point}" for idx, point in enumerate(posture, start=1))
        + "\n\n## Lane Readiness Snapshot\n\n"
        + list_block(readiness)
        + "\n\n## Risks and Ambiguities\n\n"
        "| Item | Risk/Ambiguity | Initial fact check |\n"
        "|---|---|---|\n"
        + "\n".join(risk_rows)
        + "\n\n## Inputs Required From Founder\n\n"
        + "\n".join(f"{idx}. {item}" for idx, item in enumerate(founder_inputs, start=1))
        + "\n"
    )


def render_guidance_snippet(
    meta: dict[str, Any],
    runtimes: list[LaneRuntime],
    launch_pack_path: Path,
    obs_ids: list[str],
    open_questions: list[dict[str, str]],
) -> str:
    non_canonical = [runtime for runtime in runtimes if not runtime.spec.is_canonical]
    unlocked = ", ".join(runtime.spec.packet_id for runtime in non_canonical) or "none"
    obs_text = ", ".join(obs_ids) if obs_ids else "<append_after_send>"

    impacted_files: list[str] = []
    for runtime in runtimes:
        impacted_files.extend(
            [
                rel_path(runtime.boundary_path),
                rel_path(runtime.resume_path),
                rel_path(runtime.launch_path),
                rel_path(runtime.todo_path),
            ]
        )
    impacted_files.append(rel_path(launch_pack_path))

    open_q_text = ", ".join(q["id"] for q in open_questions) if open_questions else "none"

    return (
        f"- Date: {meta['date']}\n"
        "- Author: Codex\n"
        f"- Context: {meta['wave_id']} unlock prep from one shared collaboration spec.\n"
        "- Guidance:\n"
        f"  - Unlocked packets: {unlocked}\n"
        "  - Required read order: README.AGENTS -> HARD_REQUIREMENTS.md -> LONG_RUN_MODE.md -> boundary -> resume -> lane TODO\n"
        "  - Long-run mode enforced: low interruption, one end-of-window bundle, no assumptions\n"
        "  - Ambiguity rule enforced: local probe + cross-codebase probe, then defer and continue\n"
        f"  - Founder questions still open: {open_q_text}\n"
        f"  - Unlock observation IDs: {obs_text}\n"
        "- Impacted Files:\n"
        + "\n".join(f"  - {path}" for path in impacted_files)
        + "\n- Required Follow-up:\n"
        "  - Collect checkout ACKs for every non-canonical lane.\n"
        "  - Intake one long-run evidence bundle per lane and replay before acceptance.\n"
    )


def render_status_snippet(
    meta: dict[str, Any],
    lanes: list[LaneSpec],
    obs_ids: list[str],
) -> str:
    canonical = next((lane for lane in lanes if lane.is_canonical), None)
    canonical_packet = canonical.packet_id if canonical else "<canonical_packet>"
    non_canonical_packets = [lane.packet_id for lane in lanes if not lane.is_canonical]
    packet_delta = [f"{canonical_packet} (ACTIVE)"] + [f"{pkt} (UNLOCKED)" for pkt in non_canonical_packets]
    obs_text = ", ".join(obs_ids) if obs_ids else "<append_after_send>"

    return (
        f"## Status Delta ({meta['phase_id']}/{meta['wave_id']})\n\n"
        f"- Packet IDs updated: {', '.join(packet_delta)}\n"
        f"- In-progress section updated: `{canonical_packet}` active governance + replay intake.\n"
        "- Next three actions updated:\n"
        "  1. Monitor checkout ACKs.\n"
        "  2. Intake lane bundles and replay before decisions.\n"
        "  3. Prepare subsequent unlock set without parking active lanes.\n"
        "- Proof entries updated: boundaries/prompts/TODOs/launch-pack generated from shared TOML spec.\n"
        f"- Memory observation IDs appended: {obs_text}\n"
    )


def render_launch_pack(
    meta: dict[str, Any],
    runtimes: list[LaneRuntime],
    readme_path: Path,
    hard_requirements_path: Path,
    long_run_path: Path,
) -> str:
    non_canonical = [runtime for runtime in runtimes if not runtime.spec.is_canonical]
    canonical = next((runtime for runtime in runtimes if runtime.spec.is_canonical), None)

    sections: list[str] = []
    for runtime in non_canonical:
        lane = runtime.spec
        tests = ", ".join(lane.validation_commands) if lane.validation_commands else "artifact contract checks"
        section = (
            f"## {lane.lane} ({lane.packet_id})\n\n"
            "```text\n"
            f"You are the `{lane.agent_id}` execution agent.\n\n"
            "Read in order:\n"
            f"1) {readme_path}\n"
            f"2) {hard_requirements_path}\n"
            f"3) {long_run_path}\n"
            f"4) {runtime.boundary_path}\n"
            f"5) {runtime.resume_path}\n"
            f"6) {runtime.todo_path}\n\n"
            "Execute in long-run mode. NO ASSUMPTIONS.\n"
            "If ambiguous: add to Ambiguity Log in the TODO, do two hard-fact probes max (local then cross-codebase), then mark deferred_due_to_missing_facts and continue.\n\n"
            "Kickoff:\n"
            f"/home/bozertron/Orchestr8_jr/scripts/agent_flags.sh unread {lane.agent_id} {meta['phase_id']}\n"
            "/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh health\n"
            f"/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh send {lane.agent_id} codex {meta['phase_id']} checkout true \"packet={lane.packet_id}; scope={lane.checkout_scope}; files=<files>; tests={tests}; eta=<eta>\"\n"
            f"/home/bozertron/Orchestr8_jr/scripts/packet_bootstrap.sh {meta['phase_id']} {lane.packet_id} {lane.agent_id}\n"
            f"/home/bozertron/Orchestr8_jr/scripts/packet_lint.sh {runtime.resume_path} {runtime.boundary_path}\n\n"
            "Closeout:\n"
            f"/home/bozertron/Orchestr8_jr/scripts/packet_closeout.sh {meta['phase_id']} {lane.packet_id}\n"
            f"OR8_PHASE={meta['phase_id']} /home/bozertron/Orchestr8_jr/scripts/ping_codex.sh 100 \"{lane.packet_id} long-run bundle complete; updated TODO + evidence posted\"\n"
            "```\n"
        )
        sections.append(section)

    canonical_section = ""
    if canonical is not None:
        lane = canonical.spec
        canonical_section = (
            f"## {lane.lane} (Internal Canonical Lane, {lane.packet_id})\n\n"
            "```text\n"
            "Use this repo and execute:\n"
            f"1) {canonical.resume_path}\n"
            f"2) {canonical.boundary_path}\n"
            "3) Keep replay authority active while other lanes run.\n"
            "4) Do not park lanes waiting for micro-checkins.\n"
            "5) Batch decisions at end-of-window from evidence bundles.\n"
            "```\n"
        )

    return (
        f"# Copy/Paste Launch Prompts ({meta['phase_id']} Long-Run, {meta['wave_id']})\n\n"
        f"Last Updated: {meta['date']}\n\n"
        "Use these prompts as-is when launching each lane agent.\n\n"
        + "\n".join(sections)
        + ("\n" + canonical_section if canonical_section else "")
    )


def render_unlock_script(
    meta: dict[str, Any],
    runtimes: list[LaneRuntime],
) -> str:
    non_canonical = [runtime for runtime in runtimes if not runtime.spec.is_canonical]
    mirror = str(meta.get("canonical_agent_mirror", "")).strip()

    lines = [
        "#!/usr/bin/env bash",
        "set -euo pipefail",
        "",
        f"PHASE={shell_quote(str(meta['phase_id']))}",
        "",
        "/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh health",
        "",
    ]

    for runtime in non_canonical:
        lane = runtime.spec
        message = (
            f"unlock={lane.packet_id}; wave={meta['wave_id']}; "
            f"scope={lane.checkout_scope}; resume={runtime.resume_path}; boundary={runtime.boundary_path}; "
            "mode=long-run; assumptions=none; ambiguity=local_probe+cross_probe_then_defer"
        )
        lines.append(
            "/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh send codex "
            f"{shell_quote(lane.agent_id)} \"$PHASE\" guidance true {shell_quote(message)}"
        )

    if mirror:
        unlocked = ", ".join(runtime.spec.packet_id for runtime in non_canonical)
        mirror_message = (
            f"{meta['wave_id']} unlock mirror; packets={unlocked}; "
            "long-run active; no assumptions; use canonical guidance files"
        )
        lines.append(
            "/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh send codex "
            f"{shell_quote(mirror)} \"$PHASE\" guidance true {shell_quote(mirror_message)}"
        )

    return "\n".join(lines) + "\n"


def render_kickoff_script(
    meta: dict[str, Any],
    canonical: LaneRuntime,
) -> str:
    lane = canonical.spec
    message = (
        f"packet={lane.packet_id}; scope={lane.checkout_scope}; "
        "files=<files>; tests=<tests>; eta=<eta>"
    )
    return (
        "#!/usr/bin/env bash\n"
        "set -euo pipefail\n\n"
        f"PHASE={shell_quote(str(meta['phase_id']))}\n"
        f"PACKET={shell_quote(lane.packet_id)}\n\n"
        f"/home/bozertron/Orchestr8_jr/scripts/agent_flags.sh unread {shell_quote(lane.agent_id)} \"$PHASE\"\n"
        "/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh health\n"
        f"/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh send {shell_quote(lane.agent_id)} codex \"$PHASE\" checkout true {shell_quote(message)}\n"
        f"/home/bozertron/Orchestr8_jr/scripts/packet_bootstrap.sh \"$PHASE\" \"$PACKET\" {shell_quote(lane.agent_id)}\n"
        f"/home/bozertron/Orchestr8_jr/scripts/packet_lint.sh {shell_quote(str(canonical.resume_path))} {shell_quote(str(canonical.boundary_path))}\n"
    )


def run_command(command: list[str]) -> str:
    proc = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        stderr = proc.stderr.strip()
        stdout = proc.stdout.strip()
        detail = stderr or stdout or "unknown failure"
        abort(f"command failed: {' '.join(command)} :: {detail}")
    return proc.stdout.strip()


def extract_obs_id(output: str) -> str:
    match = OBS_ID_RE.search(output)
    if not match:
        return "unknown"
    return match.group(1)


def send_unlocks(meta: dict[str, Any], runtimes: list[LaneRuntime]) -> list[str]:
    run_command([str(ROOT / "scripts/agent_comms.sh"), "health"])
    obs_ids: list[str] = []
    for runtime in [item for item in runtimes if not item.spec.is_canonical]:
        lane = runtime.spec
        message = (
            f"unlock={lane.packet_id}; wave={meta['wave_id']}; "
            f"scope={lane.checkout_scope}; resume={runtime.resume_path}; boundary={runtime.boundary_path}; "
            "mode=long-run; assumptions=none; ambiguity=local_probe+cross_probe_then_defer"
        )
        output = run_command(
            [
                str(ROOT / "scripts/agent_comms.sh"),
                "send",
                "codex",
                lane.agent_id,
                str(meta["phase_id"]),
                "guidance",
                "true",
                message,
            ]
        )
        obs_ids.append(extract_obs_id(output))

    mirror = str(meta.get("canonical_agent_mirror", "")).strip()
    if mirror:
        packets = ", ".join(runtime.spec.packet_id for runtime in runtimes if not runtime.spec.is_canonical)
        mirror_message = (
            f"{meta['wave_id']} unlock mirror; packets={packets}; "
            "long-run active; no assumptions; use canonical guidance files"
        )
        output = run_command(
            [
                str(ROOT / "scripts/agent_comms.sh"),
                "send",
                "codex",
                mirror,
                str(meta["phase_id"]),
                "guidance",
                "true",
                mirror_message,
            ]
        )
        obs_ids.append(extract_obs_id(output))
    return obs_ids


def kickoff_canonical(meta: dict[str, Any], canonical: LaneRuntime) -> str:
    lane = canonical.spec
    phase_id = str(meta["phase_id"])
    run_command([str(ROOT / "scripts/agent_flags.sh"), "unread", lane.agent_id, phase_id])
    run_command([str(ROOT / "scripts/agent_comms.sh"), "health"])
    checkout_message = (
        f"packet={lane.packet_id}; scope={lane.checkout_scope}; "
        "files=<files>; tests=<tests>; eta=<eta>"
    )
    checkout_output = run_command(
        [
            str(ROOT / "scripts/agent_comms.sh"),
            "send",
            lane.agent_id,
            "codex",
            phase_id,
            "checkout",
            "true",
            checkout_message,
        ]
    )
    run_command([str(ROOT / "scripts/packet_bootstrap.sh"), phase_id, lane.packet_id, lane.agent_id])
    run_command(
        [
            str(ROOT / "scripts/packet_lint.sh"),
            str(canonical.resume_path),
            str(canonical.boundary_path),
        ]
    )
    return extract_obs_id(checkout_output)


def validate_schema(data: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], list[LaneSpec], list[dict[str, str]]]:
    for key in ("meta", "paths", "lanes"):
        if key not in data:
            abort(f"spec missing top-level [{key}]")

    meta = data["meta"]
    paths_cfg = data["paths"]
    lanes_raw = data["lanes"]

    if not isinstance(meta, dict):
        abort("[meta] must be a TOML table")
    if not isinstance(paths_cfg, dict):
        abort("[paths] must be a TOML table")
    if not isinstance(lanes_raw, list) or not lanes_raw:
        abort("[[lanes]] must include at least one lane entry")

    required_meta = [
        "phase_id",
        "wave_id",
        "window_id",
        "date",
        "unlock_authority",
    ]
    for key in required_meta:
        if key not in meta:
            abort(f"[meta] missing '{key}'")

    required_paths = [
        "checkin_dir",
        "exec_prompt_dir",
        "founder_prompt_dir",
        "mingos_prompt_dir",
        "artifact_dir",
        "launch_pack_output",
        "exploration_notes_output",
        "guidance_snippet_output",
        "status_snippet_output",
        "unlock_commands_output",
        "kickoff_commands_output",
    ]
    for key in required_paths:
        if key not in paths_cfg:
            abort(f"[paths] missing '{key}'")

    lanes = [parse_lane(raw) for raw in lanes_raw]
    canonical_count = sum(1 for lane in lanes if lane.is_canonical)
    if canonical_count != 1:
        abort("spec must contain exactly one canonical lane (is_canonical=true)")

    questions = normalize_questions(data.get("phase_questions"))
    return meta, paths_cfg, lanes, questions


def command_init(output: str, force: bool) -> None:
    if not TEMPLATE_SPEC.exists():
        abort(f"template missing: {TEMPLATE_SPEC}")
    out_path = root_path(output)
    if out_path.exists() and not force:
        abort(f"output exists: {out_path} (use --force to overwrite)")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(TEMPLATE_SPEC, out_path)
    print(f"initialized spec template: {rel_path(out_path)}")


def command_render(spec: str, send: bool, kickoff: bool) -> None:
    spec_path = root_path(spec)
    data = load_spec(spec_path)
    meta, paths_cfg, lanes, questions = validate_schema(data)

    placeholder_findings: list[str] = []
    validate_placeholders(data, "spec", placeholder_findings)
    if placeholder_findings:
        preview = "\n".join(f"- {item}" for item in placeholder_findings[:20])
        extra = ""
        if len(placeholder_findings) > 20:
            extra = f"\n... ({len(placeholder_findings) - 20} more)"
        abort(
            "spec still contains placeholder values. Fill these fields before render:\n"
            + preview
            + extra
        )

    checkin_dir = root_path(str(paths_cfg["checkin_dir"]))
    guidance_path = checkin_dir / "GUIDANCE.md"
    hard_requirements_path = ROOT / ".planning/orchestr8_next/execution/HARD_REQUIREMENTS.md"
    long_run_path = ROOT / ".planning/orchestr8_next/execution/LONG_RUN_MODE.md"
    readme_path = ROOT / "README.AGENTS"
    artifact_dir = root_path(str(paths_cfg["artifact_dir"]))

    runtimes: list[LaneRuntime] = []
    for lane in lanes:
        prompt_dir = prompt_dir_for_group(paths_cfg, lane.prompt_group)
        runtime = LaneRuntime(
            spec=lane,
            boundary_path=checkin_dir / lane.boundary_file,
            launch_path=prompt_dir / lane.launch_file,
            resume_path=prompt_dir / lane.resume_file,
            todo_path=root_path(lane.todo_output_file),
        )
        runtimes.append(runtime)

    open_questions = [
        q for q in questions if q["status"] != "answered" and not q["answer"]
    ]

    for runtime in runtimes:
        write_text(
            runtime.boundary_path,
            render_boundary(runtime.spec, str(meta["unlock_authority"]), str(meta["date"])),
        )
        write_text(
            runtime.resume_path,
            render_resume(
                runtime.spec,
                str(meta["phase_id"]),
                readme_path,
                hard_requirements_path,
                long_run_path,
                guidance_path,
                runtime,
                artifact_dir,
            ),
        )
        write_text(
            runtime.launch_path,
            render_launch(
                runtime.spec,
                long_run_path,
                hard_requirements_path,
                guidance_path,
                runtime,
            ),
        )
        write_text(
            runtime.todo_path,
            render_todo(runtime.spec, str(meta["phase_id"]), str(meta["date"]), open_questions),
        )

    launch_pack_path = root_path(str(paths_cfg["launch_pack_output"]))
    write_text(
        launch_pack_path,
        render_launch_pack(meta, runtimes, readme_path, hard_requirements_path, long_run_path),
    )

    exploration_cfg = data.get("exploration", {})
    if not isinstance(exploration_cfg, dict):
        abort("[exploration] must be a TOML table when provided")
    exploration_notes_path = root_path(str(paths_cfg["exploration_notes_output"]))
    write_text(
        exploration_notes_path,
        render_exploration_notes(meta, lanes, questions, exploration_cfg),
    )

    unlock_script_path = root_path(str(paths_cfg["unlock_commands_output"]))
    kickoff_script_path = root_path(str(paths_cfg["kickoff_commands_output"]))
    write_text(unlock_script_path, render_unlock_script(meta, runtimes))

    canonical_runtime = next(runtime for runtime in runtimes if runtime.spec.is_canonical)
    write_text(kickoff_script_path, render_kickoff_script(meta, canonical_runtime))
    unlock_script_path.chmod(0o755)
    kickoff_script_path.chmod(0o755)

    obs_ids: list[str] = []
    if send:
        obs_ids.extend(send_unlocks(meta, runtimes))
    if kickoff:
        obs_ids.append(kickoff_canonical(meta, canonical_runtime))

    guidance_snippet_path = root_path(str(paths_cfg["guidance_snippet_output"]))
    status_snippet_path = root_path(str(paths_cfg["status_snippet_output"]))
    write_text(
        guidance_snippet_path,
        render_guidance_snippet(meta, runtimes, launch_pack_path, obs_ids, open_questions),
    )
    write_text(status_snippet_path, render_status_snippet(meta, lanes, obs_ids))

    print("render complete")
    print(f"- spec: {rel_path(spec_path)}")
    print(f"- boundaries/prompts/todos: {len(runtimes)} lanes")
    print(f"- launch pack: {rel_path(launch_pack_path)}")
    print(f"- exploration notes: {rel_path(exploration_notes_path)}")
    print(f"- guidance snippet: {rel_path(guidance_snippet_path)}")
    print(f"- status snippet: {rel_path(status_snippet_path)}")
    print(f"- unlock commands: {rel_path(unlock_script_path)}")
    print(f"- canonical kickoff commands: {rel_path(kickoff_script_path)}")
    if obs_ids:
        print(f"- observation ids: {', '.join(obs_ids)}")


def main() -> None:
    args = parse_args()
    if args.command == "init":
        command_init(args.output, args.force)
        return
    if args.command == "render":
        command_render(args.spec, args.send, args.kickoff_canonical)
        return
    abort(f"unsupported command: {args.command}")


if __name__ == "__main__":
    main()
