"""Code City rendering assembly for Marimo integration."""

from __future__ import annotations

import html
import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

from IP.features.code_city.assets import (
    load_woven_maps_template,
    read_text_if_exists,
    script_tag,
)
from IP.features.code_city.graph_builder import (
    build_from_connection_graph,
    build_from_health_results,
    build_graph_data,
)


def create_code_city(
    root: str,
    width: int = 800,
    height: int = 600,
    max_height: int = 200,
    wire_count: int = 10,
    health_results: Optional[Dict[str, Any]] = None,
) -> Any:
    """Create a Woven Maps Code City visualization for Marimo."""
    try:
        import marimo as mo
    except ImportError:
        raise ImportError("marimo is required. Install with: pip install marimo")

    if not root or not os.path.isdir(root):
        return mo.md(
            f"**Set a valid project root to visualize the codebase.**\n\nCurrent: `{root or 'None'}`"
        )

    try:
        graph_data = build_from_connection_graph(
            root,
            width=width,
            height=height,
            max_height=max_height,
            wire_count=wire_count,
        )
    except Exception:
        graph_data = build_graph_data(root, width, height, max_height, wire_count)

    if not graph_data.nodes:
        return mo.md(f"**No code files found in project.**\n\nScanned: `{root}`")

    if health_results:
        graph_data.nodes = build_from_health_results(graph_data.nodes, health_results)

    stream_bps_raw = os.getenv("ORCHESTR8_CODE_CITY_STREAM_BPS", "5000000").strip()
    try:
        stream_bps = max(100_000, int(stream_bps_raw))
    except ValueError:
        stream_bps = 5_000_000

    inline_building_data = os.getenv(
        "ORCHESTR8_CODE_CITY_INLINE_BUILDING_DATA", ""
    ).strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }

    if inline_building_data:
        from IP import woven_maps as wm

        building_data = wm.create_3d_code_city(graph_data, layout_scale=10.0)
        building_data_json = json.dumps(building_data)
    else:
        building_data_json = "null"

    from IP.contracts.camera_state import get_default_camera_state

    camera_state = get_default_camera_state()
    camera_state_json = json.dumps(
        {
            "mode": camera_state.mode,
            "position": camera_state.position,
            "target": camera_state.target,
            "zoom": camera_state.zoom,
            "return_stack": camera_state.return_stack,
            "transition_ms": camera_state.transition_ms,
            "easing": camera_state.easing,
        }
    )
    patchbay_apply_enabled = os.getenv(
        "ORCHESTR8_PATCHBAY_APPLY", ""
    ).strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }

    repo_root = Path(__file__).resolve().parents[3]
    js_3d_path = repo_root / "IP" / "static" / "woven_maps_3d.js"
    delaunay_local_path = repo_root / "Barradeau" / "woven_map" / "delaunay.js"
    three_core_local_path = (
        repo_root / "Barradeau" / "FBO-master" / "vendor" / "three.min.js"
    )
    three_orbit_local_path = (
        repo_root / "Barradeau" / "FBO-master" / "vendor" / "OrbitControls.js"
    )

    js_3d_content = read_text_if_exists(js_3d_path)
    delaunay_tag = script_tag(
        read_text_if_exists(delaunay_local_path),
        "https://cdn.jsdelivr.net/npm/d3-delaunay@6",
    )
    three_core_tag = script_tag(
        read_text_if_exists(three_core_local_path),
        "https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js",
    )
    three_orbit_tag = script_tag(
        read_text_if_exists(three_orbit_local_path),
        "https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js",
    )

    iframe_html = (
        load_woven_maps_template()
        .replace("__GRAPH_DATA__", graph_data.to_json())
        .replace("__BUILDING_DATA__", building_data_json)
        .replace("__BUILDING_STREAM_BPS__", str(stream_bps))
        .replace("__CAMERA_STATE__", camera_state_json)
        .replace(
            "__PATCHBAY_APPLY_ENABLED__", "true" if patchbay_apply_enabled else "false"
        )
        .replace("__DELAUNAY_LIB_TAG__", delaunay_tag)
        .replace("__THREE_CORE_TAG__", three_core_tag)
        .replace("__THREE_ORBIT_TAG__", three_orbit_tag)
        .replace("__WOVEN_MAPS_3D_JS__", js_3d_content)
    )
    escaped = html.escape(iframe_html)

    return mo.Html(
        f"""
        <div style="
            background: #050505;
            border-radius: 8px;
            overflow: hidden;
            width: 100%;
            max-width: 100%;
            height: clamp(360px, 78vh, 1200px);
        ">
            <iframe
                srcdoc="{escaped}"
                width="100%"
                height="100%"
                style="border: none; display: block; width: 100%; height: 100%;"
                sandbox="allow-scripts"
                allow="microphone"
            ></iframe>
        </div>
    """
    )
