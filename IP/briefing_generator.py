# IP/briefing_generator.py
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import json

from IP.mermaid_generator import Fiefdom, FiefdomStatus, generate_empire_mermaid


class BriefingGenerator:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)

    def load_campaign_log(self, fiefdom_path: str, limit: int = 5) -> List[Dict]:
        """Load recent campaign entries from .orchestr8/campaigns/ (JSON format).

        Per canon (CONTEXT.md / VISION-ALIGNMENT.md):
        - Format: JSON files
        - Location: .orchestr8/campaigns/
        """
        campaigns_dir = self.project_root / ".orchestr8" / "campaigns"
        if not campaigns_dir.exists():
            return []

        entries = []
        for json_file in sorted(campaigns_dir.glob("*.json")):
            try:
                data = json.loads(json_file.read_text())
                # Accept single entry or list of entries
                if isinstance(data, list):
                    entries.extend(data)
                elif isinstance(data, dict):
                    entries.append(data)
            except (json.JSONDecodeError, OSError):
                continue

        # Filter to this fiefdom if entries have a fiefdom field
        fiefdom_entries = [
            e for e in entries
            if not e.get("fiefdom") or fiefdom_path in e.get("fiefdom", "")
        ]

        # Sort by date descending if available, return last N
        fiefdom_entries.sort(key=lambda e: e.get("date", ""), reverse=True)
        return fiefdom_entries[:limit]

    def get_locks_for_fiefdom(self, fiefdom_path: str) -> List[Dict]:
        """Get Louis locks relevant to this fiefdom."""
        config_path = self.project_root / ".louis-control" / "louis-config.json"
        if not config_path.exists():
            return []

        with open(config_path) as f:
            config = json.load(f)

        locks = []
        for filepath, lock_info in config.get("locks", {}).items():
            # Include locks in this fiefdom or that this fiefdom might touch
            if fiefdom_path in filepath or filepath.startswith("../"):
                locks.append(
                    {
                        "file": filepath,
                        "reason": lock_info.get("reason", "Protected"),
                        "locked_at": lock_info.get("locked_at", "Unknown"),
                    }
                )
        return locks

    def build_fiefdom_diagram(self, fiefdom_path: str, context: Optional[Dict] = None) -> str:
        """Generate Mermaid diagram of fiefdom structure for agent briefings.

        Per canon: Carl deploys Mermaid diagrams to agents in briefing documents.
        """
        fiefdoms = []
        # Build the target fiefdom node
        status = FiefdomStatus.WORKING
        error_count = 0
        if context:
            if context.get("health", {}).get("status") == "broken":
                status = FiefdomStatus.BROKEN
                error_count = len(context.get("health", {}).get("errors", []))
            if context.get("combat", {}).get("active"):
                status = FiefdomStatus.COMBAT

        connections = context.get("imports_from", []) if context else []
        fiefdoms.append(Fiefdom(
            path=fiefdom_path,
            status=status,
            connections=connections,
            error_count=error_count,
        ))

        # Add connected fiefdoms as nodes
        for conn in connections:
            fiefdoms.append(Fiefdom(
                path=conn,
                status=FiefdomStatus.WORKING,
                connections=[],
            ))

        if len(fiefdoms) < 2:
            return ""

        return generate_empire_mermaid(fiefdoms)

    def generate(
        self,
        fiefdom_path: str,
        ticket_id: str,
        ticket_status: str,
        mission: str,
        errors: List[str],
        warnings: List[str],
        notes: List[Dict],
        context: Optional[Dict] = None,
    ) -> str:
        """
        Generate BRIEFING.md with MAXIMUM context.

        We eat tokens to do job right the first time.
        """
        now = datetime.now()
        locks = self.get_locks_for_fiefdom(fiefdom_path)
        campaign_history = self.load_campaign_log(fiefdom_path, limit=5)
        mermaid_diagram = self.build_fiefdom_diagram(fiefdom_path, context)

        # Default context if not provided
        if context is None:
            context = {
                "related_files": [],
                "imports_from": [],
                "exports_to": [],
                "patterns": [],
            }

        briefing = f"""# MISSION BRIEFING: {ticket_id}

**Generated:** {now.isoformat()}
**Fiefdom:** {fiefdom_path}
**Absolute Path:** {self.project_root / fiefdom_path}
**Status:** You are being deployed to a {ticket_status.upper()} fiefdom

---

## Objective

{mission}

## Current Errors ({len(errors)} total)

```
{chr(10).join(errors) if errors else "No errors recorded"}
```

## Warnings ({len(warnings)} total)

```
{chr(10).join(warnings) if warnings else "No warnings recorded"}
```

## Carl's Reconnaissance

- **Error Count:** {len(errors)}
- **Warning Count:** {len(warnings)}
- **Related Files:** {", ".join(context.get("related_files", [])) or "None identified"}
- **Connections:**
  - Imports from: {", ".join(context.get("imports_from", [])) or "None identified"}
  - Exports to: {", ".join(context.get("exports_to", [])) or "None identified"}
- **Patterns to Follow:** {", ".join(context.get("patterns", [])) or "See CLAUDE.md"}

## Fiefdom Structure

```mermaid
{mermaid_diagram if mermaid_diagram else "graph TD\n    N0[\"No connections mapped\"]"}
```

## Louis's Restrictions

| File | Status | Reason |
|------|--------|--------|
"""

        if locks:
            for lock in locks:
                briefing += f"| `{lock['file']}` | LOCKED | {lock['reason']} |\n"
        else:
            briefing += "| (none) | - | No locks in this fiefdom |\n"

        briefing += """
## Recent Campaign History

"""

        if campaign_history:
            for entry in campaign_history:
                briefing += f"""### {entry.get("ticket", "Unknown")} ({entry.get("date", "Unknown")}) - {entry.get("status", "Unknown")}
- **Action:** {entry.get("summary", "No summary")}
- **Lesson:** {entry.get("lesson", "None recorded")}

"""
        else:
            briefing += (
                "*No previous campaigns recorded. You are the first general here.*\n\n"
            )

        briefing += """## Stacked Notes

| Time | Author | Note |
|------|--------|------|
"""

        if notes:
            for note in notes:
                briefing += f"| {note.get('time', '?')} | {note.get('author', '?')} | {note.get('text', '')} |\n"
        else:
            briefing += "| - | - | No notes yet |\n"

        briefing += f"""
## Health Check

```bash
npm run typecheck
# Victory = no errors containing "{fiefdom_path}"
```

## Your Checklist

1. [ ] Read CLAUDE.md for standing orders
2. [ ] Scan CAMPAIGN_LOG.md for recent lessons
3. [ ] Deploy Scout to analyze problem
4. [ ] Deploy Fixer to make surgical changes
5. [ ] Deploy Validator to run health check
6. [ ] Update CAMPAIGN_LOG.md with your actions
7. [ ] Report outcome

---

**BEGIN MISSION**
"""

        return briefing

    def write_briefing(self, fiefdom_path: str, **kwargs) -> Path:
        """Generate and write BRIEFING.md to fiefdom."""
        content = self.generate(fiefdom_path, **kwargs)
        briefing_path = self.project_root / fiefdom_path / "BRIEFING.md"
        briefing_path.write_text(content)
        return briefing_path
