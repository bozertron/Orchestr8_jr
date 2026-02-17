"""Health/combat flow integration checks for Code City graph assembly."""

from __future__ import annotations

from pathlib import Path

from IP.features.code_city.graph_builder import build_from_health_results, compute_neighborhoods
from IP.health_checker import HealthCheckResult, ParsedError
from IP.health_watcher import HealthWatcher


class _DummyNode:
    def __init__(self, path: str, status: str) -> None:
        self.path = path
        self.status = status
        self.health_errors = []
        self.x = 0.0
        self.y = 0.0


def test_health_watcher_debounced_check_invokes_callback(tmp_path: Path) -> None:
    seen: dict = {}

    def _callback(payload: dict) -> None:
        seen.update(payload)

    project_root = tmp_path / "workspace"
    watched_file = project_root / "IP" / "plugins" / "sample.py"
    watched_file.parent.mkdir(parents=True)
    watched_file.write_text("print('ok')\n", encoding="utf-8")

    watcher = HealthWatcher(str(project_root), _callback)
    expected = HealthCheckResult(
        status="broken",
        errors=[ParsedError(file="IP/plugins/sample.py", line=3, message="boom")],
        warnings=[],
        checker_used="test",
        last_check="now",
    )
    watcher.health_checker.check_fiefdom = lambda _path: expected
    watcher._pending_file = str(watched_file)

    watcher._debounced_check()

    assert "IP/plugins/sample.py" in seen
    assert seen["IP/plugins/sample.py"].status == "broken"
    assert seen["IP/plugins/sample.py"].errors[0].line == 3


def test_health_results_merge_promotes_working_to_broken() -> None:
    node = _DummyNode(path="IP/foo.py", status="working")
    result = HealthCheckResult(
        status="broken",
        errors=[ParsedError(file="IP/foo.py", line=9, message="type mismatch")],
        checker_used="test",
    )

    merged = build_from_health_results([node], {"IP": result})

    assert merged[0].status == "broken"
    assert merged[0].health_errors[0]["line"] == 9


def test_health_results_merge_preserves_combat_precedence() -> None:
    node = _DummyNode(path="IP/foo.py", status="combat")
    result = HealthCheckResult(
        status="broken",
        errors=[ParsedError(file="IP/foo.py", line=4, message="runtime error")],
        checker_used="test",
    )

    merged = build_from_health_results([node], {"IP": result})

    assert merged[0].status == "combat"
    assert merged[0].health_errors[0]["message"] == "runtime error"


def test_health_results_merge_accepts_dict_payloads() -> None:
    node = _DummyNode(path="IP/bar.py", status="working")
    merged = build_from_health_results(
        [node],
        {
            "IP": {
                "status": "broken",
                "errors": [
                    {"file": "IP/bar.py", "line": 12, "message": "import failure"},
                ],
            }
        },
    )

    assert merged[0].status == "broken"
    assert merged[0].health_errors[0]["line"] == 12


def test_compute_neighborhoods_groups_nodes_by_parent_directory() -> None:
    node_a = _DummyNode(path="IP/a.py", status="working")
    node_b = _DummyNode(path="IP/sub/b.py", status="broken")
    node_c = _DummyNode(path="docs/readme.md", status="working")

    node_a.x, node_a.y = (100.0, 120.0)
    node_b.x, node_b.y = (180.0, 200.0)
    node_c.x, node_c.y = (320.0, 340.0)

    neighborhoods = compute_neighborhoods([node_a, node_b, node_c], [], 800, 600)
    names = {n.name for n in neighborhoods}

    assert "IP" in names
    assert "IP/sub" in names
    assert "docs" in names
