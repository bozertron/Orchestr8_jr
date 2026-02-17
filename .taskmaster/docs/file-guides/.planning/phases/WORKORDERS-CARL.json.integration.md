# WORKORDERS-CARL.json Integration Guide

- Source: `.planning/phases/WORKORDERS-CARL.json`
- Total lines: `455`
- SHA256: `6d6e585f87af2c75c82ca477cc3a8d342ee2a52a12cff1dd9b74e1ac2de85770`
- Memory chunks: `4`
- Observation IDs: `1062..1065`

## Why This Is Painful

- Medium-large surface area: requires strict scope control during integration.
- Constraint-heavy document: treat as canonical rules, not optional guidance.
- State pipeline coupling: root state keys and health flow ordering must stay aligned.

## Anchor Lines

- `.planning/phases/WORKORDERS-CARL.json:48` "constraints": {
- `.planning/phases/WORKORDERS-CARL.json:54` "border_contracts": [
- `.planning/phases/WORKORDERS-CARL.json:55` "FiefdomContext structure is LOCKED per CONTEXT.md - exact fields required"
- `.planning/phases/WORKORDERS-CARL.json:58` "Output format must match LOCKED structure: fiefdom, health, connections, combat, tickets, locks"
- `.planning/phases/WORKORDERS-CARL.json:109` "Import: HealthChecker from .health_checker",
- `.planning/phases/WORKORDERS-CARL.json:115` "code_block": "from .health_checker import HealthChecker\nfrom .connection_verifier import ConnectionVerifier\nfrom .combat_tracker import CombatTracker\nfrom .ticket_manager import TicketManager\nfrom .louis_core import LouisWarden, LouisConfig"
- `.planning/phases/WORKORDERS-CARL.json:117` "constraints": {
- `.planning/phases/WORKORDERS-CARL.json:122` "border_contracts": [
- `.planning/phases/WORKORDERS-CARL.json:126` "Signal sources: HealthChecker, ConnectionVerifier, CombatTracker, TicketManager, LouisWarden per CONTEXT.md"
- `.planning/phases/WORKORDERS-CARL.json:178` "Initialize self.health_checker = HealthChecker(str(self.root))",
- `.planning/phases/WORKORDERS-CARL.json:185` "code_block": "def __init__(self, root_path: str, timeout: int = DEFAULT_TIMEOUT, state_managers: Optional[Dict] = None):\n    self.root = Path(root_path)\n    self.timeout = timeout\n    self.ts_tool = self.root / TS_TOOL_PATH\n    self.context_file = self.root / CONTEXT_OUTPUT_PATH\n    self.state_managers = state_managers or {}\n    \n    self.health_checker = HealthChecker(str(self.root))\n    self.connection_verifier = ConnectionVerifier(str(self.root))\n    self.combat_tracker = CombatTracker(str(self.root))\n    self.ticket_manager = TicketManager(str(self.root))\n    \n    louis_config = LouisConfig(str(self.root))\n    self.louis_warden = LouisWarden(louis_config)"
- `.planning/phases/WORKORDERS-CARL.json:187` "constraints": {
- `.planning/phases/WORKORDERS-CARL.json:193` "border_contracts": [
- `.planning/phases/WORKORDERS-CARL.json:198` "Carl does NOT block operations per CONTEXT.md constraints"
- `.planning/phases/WORKORDERS-CARL.json:208` "Signal sources accessible: `carl.health_checker` returns HealthChecker instance"
- `.planning/phases/WORKORDERS-CARL.json:259` "constraints": {
- `.planning/phases/WORKORDERS-CARL.json:265` "border_contracts": [
- `.planning/phases/WORKORDERS-CARL.json:266` "HealthChecker.check_fiefdom() returns HealthCheckResult at health_checker.py:426",
- `.planning/phases/WORKORDERS-CARL.json:273` "Output JSON structure is LOCKED per CONTEXT.md",
- `.planning/phases/WORKORDERS-CARL.json:275` "Louis remains unchanged per CONTEXT.md constraints"
- `.planning/phases/WORKORDERS-CARL.json:337` "constraints": {
- `.planning/phases/WORKORDERS-CARL.json:342` "border_contracts": [
- `.planning/phases/WORKORDERS-CARL.json:346` "JSON output must match LOCKED structure from CONTEXT.md"
- `.planning/phases/WORKORDERS-CARL.json:381` "building": "IP/plugins/06_maestro.py",
- `.planning/phases/WORKORDERS-CARL.json:397` "Import CarlContextualizer at top of 06_maestro.py",

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.
