# IP/briefing_generator.py
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import json


class BriefingGenerator:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)

    def load_campaign_log(self, fiefdom_path: str, limit: int = 5) -> List[Dict]:
        """Load recent entries from CAMPAIGN_LOG.md."""
        log_path = self.project_root / fiefdom_path / "CAMPAIGN_LOG.md"
        if not log_path.exists():
            return []

        # Parse markdown entries (simplified - would need proper parser)
        entries = []
        # ... parsing logic ...
        return entries[-limit:]

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
