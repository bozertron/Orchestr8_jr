"""Agent group presets for Collabor8 deployment controls."""

from __future__ import annotations

from copy import deepcopy
from typing import Dict, List


_SETTLEMENT_AGENT_GROUPS: Dict[str, List[dict]] = {
    "Explore": [
        {
            "id": "surveyor",
            "name": "Surveyor",
            "tier": 1,
            "brief": "Comprehensive room/tokens/signature survey.",
        },
        {
            "id": "complexity_analyzer",
            "name": "Complexity Analyzer",
            "tier": 1,
            "brief": "Scores complexity for scaling and partitioning.",
        },
        {
            "id": "pattern_identifier",
            "name": "Pattern Identifier",
            "tier": 2,
            "brief": "Extracts conventions and anti-patterns.",
        },
        {
            "id": "import_export_mapper",
            "name": "Import/Export Mapper",
            "tier": 2,
            "brief": "Maps wiring and cross-boundary crossings.",
        },
    ],
    "Plan": [
        {
            "id": "cartographer",
            "name": "Cartographer",
            "tier": 3,
            "brief": "Defines explicit boundaries and deployment maps.",
        },
        {
            "id": "border_agent",
            "name": "Border Agent",
            "tier": 3,
            "brief": "Defines allowed/forbidden border contracts.",
        },
        {
            "id": "architect",
            "name": "Architect",
            "tier": 7,
            "brief": "Designs implementation order by room.",
        },
        {
            "id": "work_order_compiler",
            "name": "Work Order Compiler",
            "tier": 8,
            "brief": "Compiles atomic execution work orders.",
        },
    ],
    "Execute": [
        {
            "id": "integration_synthesizer",
            "name": "Integration Synthesizer",
            "tier": 8,
            "brief": "Produces cross-boundary integration packets.",
        },
        {
            "id": "instruction_writer",
            "name": "Instruction Writer",
            "tier": 8,
            "brief": "Writes exact file/line execution packets.",
        },
        {
            "id": "sentinel",
            "name": "Sentinel",
            "tier": 9,
            "brief": "Maintains watchdog probe/investigate/fix cycle.",
        },
    ],
    "Monitor": [
        {
            "id": "wiring_mapper",
            "name": "Wiring Mapper",
            "tier": 8,
            "brief": "Tracks gold/teal/purple wire state changes.",
        },
        {
            "id": "failure_pattern_logger",
            "name": "Failure Pattern Logger",
            "tier": 10,
            "brief": "Archives recurring failure classes and fixes.",
        },
    ],
    "Strategic": [
        {
            "id": "luminary",
            "name": "Luminary",
            "tier": 0,
            "brief": "Strategic oversight and escalation authority.",
        },
        {
            "id": "city_manager",
            "name": "City Manager",
            "tier": 0,
            "brief": "Wave orchestration and sentinel coverage owner.",
        },
        {
            "id": "civic_council",
            "name": "Civic Council",
            "tier": 0,
            "brief": "Founder-alignment quality gate.",
        },
        {
            "id": "vision_walker",
            "name": "Vision Walker",
            "tier": 5,
            "brief": "Captures and locks founder intent.",
        },
        {
            "id": "context_analyst",
            "name": "Context Analyst",
            "tier": 6,
            "brief": "Converts alignment output into structured context.",
        },
    ],
}


def get_settlement_agent_groups() -> Dict[str, List[dict]]:
    """Return a defensive copy of the canonical agent group map."""
    return deepcopy(_SETTLEMENT_AGENT_GROUPS)

