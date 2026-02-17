# connection_verifier.py Integration Guide

- Source: `IP/connection_verifier.py`
- Total lines: `1302`
- SHA256: `99166891fd16adca86d47c7f93bfe9b21c45b837952db31ea3d8ab64d6c95ec7`
- Role: **Import resolution + patchbay validator/apply engine** — resolves imports, builds connection graph, validates rewires, and applies guarded rewrites with rollback

## Why This Is Painful

- Resolver, graph logic, dry-run validation, and apply/rollback logic now coexist in one module.
- Apply behavior depends on regex rewrite helpers; import syntax drift can break line-level rewrites.
- Post-write verification semantics are strict and can auto-rollback on unresolved proposed targets.

## Anchor Lines

- `IP/connection_verifier.py:172` `PatchbayDryRunResult` payload contract
- `IP/connection_verifier.py:969` `dry_run_patchbay_rewire(...)`
- `IP/connection_verifier.py:978` `_rewrite_python_import_line(...)`
- `IP/connection_verifier.py:996` `_rewrite_js_import_line(...)`
- `IP/connection_verifier.py:1151` `apply_patchbay_rewire(...)` guarded write path
- `IP/connection_verifier.py:1185` apply result checks (`dryRunPassed`, post-write checks)
- `IP/connection_verifier.py:1295` auto-rollback guard

## Integration Use

- Always gate real rewires through `dry_run_patchbay_rewire(...)`.
- Use `apply_patchbay_rewire(..., auto_rollback=True)` for safe writes.
- Treat warning `currentTargetRemoved == False` as a potential multi-import scenario, not immediate failure.

## Open Gaps

- No multi-line/multi-import transform engine yet.
- No border-contract enforcement in apply path yet.
