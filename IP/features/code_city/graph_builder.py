"""Graph and neighborhood assembly for Code City."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from IP.contracts.status_merge_policy import merge_status


def compute_neighborhoods(
    nodes: List[Any],
    edges: List[Any],
    width: int,
    height: int,
    padding: int = 40,
) -> List[Any]:
    """Compute neighborhood boundaries from nodes and edges."""
    if not nodes:
        return []

    from IP import woven_maps as wm

    dirs: Dict[str, List[Any]] = {}
    for node in nodes:
        dir_path = str(Path(node.path).parent)
        if dir_path == ".":
            dir_path = "root"
        if dir_path not in dirs:
            dirs[dir_path] = []
        dirs[dir_path].append(node)

    neighborhoods: List[Any] = []

    node_to_neighborhood: Dict[str, str] = {}
    for dir_path, dir_nodes in dirs.items():
        for node in dir_nodes:
            node_to_neighborhood[node.path] = dir_path

    integration_counts: Dict[str, Dict[str, int]] = {}
    for edge in edges:
        source_neighborhood = node_to_neighborhood.get(edge.source)
        target_neighborhood = node_to_neighborhood.get(edge.target)

        if (
            source_neighborhood
            and target_neighborhood
            and source_neighborhood != target_neighborhood
        ):
            if source_neighborhood not in integration_counts:
                integration_counts[source_neighborhood] = {}
            integration_counts[source_neighborhood][target_neighborhood] = (
                integration_counts[source_neighborhood].get(target_neighborhood, 0) + 1
            )

    for dir_path, dir_nodes in dirs.items():
        if len(dir_nodes) < 1:
            continue

        center_x = sum(n.x for n in dir_nodes) / len(dir_nodes)
        center_y = sum(n.y for n in dir_nodes) / len(dir_nodes)

        status_counts = {"working": 0, "broken": 0, "combat": 0}
        for node in dir_nodes:
            if node.status in status_counts:
                status_counts[node.status] += 1

        if status_counts["combat"] > 0:
            status = "combat"
        elif status_counts["broken"] > status_counts["working"]:
            status = "broken"
        else:
            status = "working"

        min_x = min(n.x for n in dir_nodes)
        max_x = max(n.x for n in dir_nodes)
        min_y = min(n.y for n in dir_nodes)
        max_y = max(n.y for n in dir_nodes)

        min_x = max(0, min_x - padding)
        max_x = min(width, max_x + padding)
        min_y = max(0, min_y - padding)
        max_y = min(height, max_y + padding)

        boundary_points = [
            {"x": min_x, "y": min_y},
            {"x": max_x, "y": min_y},
            {"x": max_x, "y": max_y},
            {"x": min_x, "y": max_y},
        ]

        integration_count = sum(integration_counts.get(dir_path, {}).values())
        neighbors = []
        for neighbor_dir, count in integration_counts.get(dir_path, {}).items():
            neighbors.append({"name": neighbor_dir, "crossings": count})

        neighborhoods.append(
            wm.Neighborhood(
                name=dir_path,
                nodes=[n.path for n in dir_nodes],
                center_x=center_x,
                center_y=center_y,
                boundary_points=boundary_points,
                integration_count=integration_count,
                neighbors=neighbors,
                status=status,
            )
        )

    return neighborhoods


def build_graph_data(
    root: str,
    width: int = 800,
    height: int = 600,
    max_height: int = 200,
    wire_count: int = 10,
):
    """Build complete graph data from a codebase root."""
    from IP import woven_maps as wm

    nodes = wm.scan_codebase(root)
    nodes = wm.calculate_layout(nodes, width, height)

    try:
        from IP.combat_tracker import CombatTracker

        tracker = CombatTracker(root)
        combat_files = tracker.get_combat_files()
        for node in nodes:
            if node.path in combat_files:
                node.status = "combat"
    except ImportError:
        pass

    try:
        from IP.louis_core import LouisConfig, LouisWarden

        config = LouisConfig(root_path=root)
        if config.protected_list and config.protected_list.exists():
            warden = LouisWarden(config)
            for node in nodes:
                node.is_locked = warden.is_locked(node.path)
    except ImportError:
        pass

    config = wm.GraphConfig(
        width=width,
        height=height,
        max_height=max_height,
        wire_count=wire_count,
    )

    neighborhoods = compute_neighborhoods(nodes, [], width, height)

    return wm.GraphData(nodes=nodes, config=config, neighborhoods=neighborhoods)


def _extract_fiefdom(file_path: str) -> str:
    """Extract fiefdom name from file path (first directory component)."""
    parts = Path(file_path).parts
    if len(parts) >= 2:
        return parts[0]
    return ""


def build_from_connection_graph(
    project_root: str,
    width: int = 800,
    height: int = 600,
    max_height: int = 250,
    wire_count: int = 15,
):
    """Build GraphData from ConnectionGraph with real import relationships."""
    from IP import woven_maps as wm

    try:
        from IP.connection_verifier import build_connection_graph
    except ImportError:
        from connection_verifier import build_connection_graph

    conn_graph = build_connection_graph(project_root)
    graph_dict = conn_graph.to_dict()

    nodes = []
    node_lookup = {}
    root_path = Path(project_root).resolve()
    metrics_cache: Dict[str, tuple[int, int]] = {}

    for node_data in graph_dict["nodes"]:
        metrics = node_data.get("metrics", {})

        status = "working"
        if node_data.get("status") == "error":
            status = "broken"
        elif metrics.get("issueCount", 0) > 0:
            status = "broken"

        file_path = node_data["filePath"]
        if file_path not in metrics_cache:
            metrics_cache[file_path] = wm.get_file_metrics(root_path, file_path)
        loc, export_count = metrics_cache[file_path]
        building_height, footprint = wm.compute_building_geometry(loc, export_count)
        display_zone = wm.get_display_zone(file_path)

        code_node = wm.CodeNode(
            path=file_path,
            status=status,
            loc=loc,
            errors=[],
            node_type=node_data.get("type", "file"),
            centrality=metrics.get("centrality", 0.0),
            in_cycle=metrics.get("inCycle", False),
            depth=metrics.get("depth", 0),
            incoming_count=metrics.get("incomingCount", 0),
            outgoing_count=metrics.get("outgoingCount", 0),
            export_count=export_count,
            building_height=building_height,
            footprint=footprint,
            display_zone=display_zone,
        )
        nodes.append(code_node)
        node_lookup[code_node.path] = code_node

    nodes = wm.calculate_layout(nodes, width, height)

    try:
        from IP.combat_tracker import CombatTracker

        tracker = CombatTracker(project_root)
        combat_files = tracker.get_combat_files()
        for node in nodes:
            if node.path in combat_files:
                node.status = "combat"
    except ImportError:
        pass

    try:
        from IP.louis_core import LouisConfig, LouisWarden

        config = LouisConfig(root_path=project_root)
        if config.protected_list and config.protected_list.exists():
            warden = LouisWarden(config)
            for node in nodes:
                node.is_locked = warden.is_locked(node.path)
    except ImportError:
        pass

    boundary_contracts_map: Dict[tuple[str, str], Dict] = {}
    try:
        from IP.contracts.settlement_survey import parse_settlement_survey

        survey_paths = [
            Path(project_root) / ".settlement" / "survey.json",
            Path(project_root) / ".planning" / "survey.json",
            Path(project_root) / "settlement_survey.json",
        ]

        for survey_path in survey_paths:
            if survey_path.exists():
                survey_data = json.loads(survey_path.read_text(encoding="utf-8"))
                survey = parse_settlement_survey(survey_data)

                for contract in survey.boundary_contracts:
                    key = (contract.from_fiefdom, contract.to_fiefdom)
                    boundary_contracts_map[key] = {
                        "allowed_types": contract.allowed_types,
                        "forbidden_crossings": contract.forbidden_crossings,
                        "contract_status": contract.contract_status,
                    }
                break
    except ImportError:
        pass
    except Exception:
        pass

    edges = []
    for edge_data in graph_dict["edges"]:
        if edge_data["source"] in node_lookup and edge_data["target"] in node_lookup:
            source = edge_data["source"]
            target = edge_data["target"]

            from_fiefdom = _extract_fiefdom(source)
            to_fiefdom = _extract_fiefdom(target)
            is_boundary = bool(
                from_fiefdom and to_fiefdom and from_fiefdom != to_fiefdom
            )

            allowed_types = []
            forbidden_crossings = []
            contract_status = ""

            if is_boundary:
                contract = boundary_contracts_map.get((from_fiefdom, to_fiefdom))
                if contract:
                    allowed_types = contract["allowed_types"]
                    forbidden_crossings = contract["forbidden_crossings"]
                    contract_status = contract["contract_status"]
                else:
                    contract_status = "missing"

            edges.append(
                wm.EdgeData(
                    source=source,
                    target=target,
                    resolved=edge_data.get("resolved", True),
                    bidirectional=edge_data.get("bidirectional", False),
                    line_number=edge_data.get("lineNumber", 0),
                    from_fiefdom=from_fiefdom,
                    to_fiefdom=to_fiefdom,
                    is_boundary=is_boundary,
                    allowed_types=allowed_types,
                    forbidden_crossings=forbidden_crossings,
                    contract_status=contract_status,
                )
            )

    config = wm.GraphConfig(
        width=width,
        height=height,
        max_height=max_height,
        wire_count=wire_count,
    )

    neighborhoods = compute_neighborhoods(nodes, edges, width, height)

    return wm.GraphData(
        nodes=nodes, edges=edges, config=config, neighborhoods=neighborhoods
    )


def build_from_health_results(
    nodes: List[Any], health_results: Dict[str, Any]
) -> List[Any]:
    """Merge HealthChecker output into CodeNode objects."""

    def _status_of(result: Any) -> str:
        if isinstance(result, dict):
            return str(result.get("status", "") or "")
        return str(getattr(result, "status", "") or "")

    def _errors_of(result: Any) -> List[Any]:
        if isinstance(result, dict):
            errs = result.get("errors", [])
            return errs if isinstance(errs, list) else []
        errs = getattr(result, "errors", [])
        return errs if isinstance(errs, list) else []

    def _to_error_dict(error: Any) -> Dict[str, Any]:
        if isinstance(error, dict):
            return {
                "file": str(error.get("file", "")),
                "line": int(error.get("line", 0) or 0),
                "message": str(error.get("message", "")),
            }
        return {
            "file": str(getattr(error, "file", "")),
            "line": int(getattr(error, "line", 0) or 0),
            "message": str(getattr(error, "message", "")),
        }

    for node in nodes:
        for path, result in health_results.items():
            if path in node.path or node.path.startswith(path.rstrip("/")):
                status = _status_of(result)
                if status:
                    node.status = merge_status(node.status, status)

                errors = _errors_of(result)
                if errors:
                    node.health_errors = [_to_error_dict(e) for e in errors[:10]]
                break

    return nodes
