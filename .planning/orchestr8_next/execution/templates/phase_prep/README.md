# Phase Prep Template Package

Purpose: make phase/wave prep repeatable from one collaborative input file and one synthesis script.

## What This Package Covers

It templates each prep step used in live operations:

1. Target exploration notes
2. Lane TODO generation
3. Boundary generation
4. Launch/resume prompt generation
5. Launch prompt pack generation
6. Shared-memory unlock broadcast command generation
7. Canonical kickoff command generation
8. Status/guidance update snippet generation

## Files

- `NEXT_PHASE_COLLAB_TEMPLATE.toml` (single collaborative source document)
- `TARGET_EXPLORATION_TEMPLATE.md`
- `LANE_TODO_TEMPLATE.md`
- `GUIDANCE_ENTRY_TEMPLATE.md`
- `STATUS_DELTA_TEMPLATE.md`
- `scripts/phase_prep_builder.py`

## Collaboration Model

1. Start from one TOML file.
2. Fill sections in order:
   - `meta`, `paths`
   - `exploration`
   - `founder_direction`
   - `phase_questions` (this is the question/answer loop)
   - lane packet specs
3. Render artifacts.
4. Review generated output.
5. Run generated broadcast/kickoff scripts, or render with `--send --kickoff-canonical`.

This supports the intended loop:
- mayor asks structured next-phase questions
- founder answers in `[[phase_questions]]`
- one render pass converts that into actionable lane TODOs/prompts/broadcast scripts

## Commands

Initialize a working spec:

```bash
python scripts/phase_prep_builder.py init --output SOT/CODEBASE_TODOS/NEXT_PHASE_COLLAB_WORKING.toml
```

Render prep package (write files only):

```bash
python scripts/phase_prep_builder.py render --spec SOT/CODEBASE_TODOS/NEXT_PHASE_COLLAB_WORKING.toml
```

Render + send unlocks + kickoff canonical:

```bash
python scripts/phase_prep_builder.py render --spec SOT/CODEBASE_TODOS/NEXT_PHASE_COLLAB_WORKING.toml --send --kickoff-canonical
```

Run generated scripts manually:

```bash
bash scripts/generated/P07_wave3_unlock_broadcast.sh
bash scripts/generated/P07_wave3_canonical_kickoff.sh
```

## Notes

- Render blocks if any `<placeholder>` tokens remain in the spec.
- Broadcasts use `scripts/agent_comms.sh`.
- All generated prompts enforce long-run mode and the no-assumptions ambiguity rule.
