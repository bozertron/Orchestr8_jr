# IP/combat_tracker.py
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional


class CombatTracker:
    """Tracks active LLM General deployments (COMBAT status)"""

    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.combat_state_file = self.project_root / ".orchestr8" / "combat_state.json"
        self.combat_state_file.parent.mkdir(parents=True, exist_ok=True)

    def _load_state(self) -> dict:
        """Load combat state from file"""
        if self.combat_state_file.exists():
            with open(self.combat_state_file) as f:
                return json.load(f)
        return {"active_deployments": {}}

    def _save_state(self, state: dict) -> None:
        """Save combat state to file"""
        with open(self.combat_state_file, "w") as f:
            json.dump(state, f, indent=2)

    def deploy(self, file_path: str, terminal_id: str, model: str = "unknown") -> None:
        """Mark a file as having an LLM General deployed"""
        state = self._load_state()
        state["active_deployments"][file_path] = {
            "deployed_at": datetime.now().isoformat(),
            "terminal_id": terminal_id,
            "model": model,
        }
        self._save_state(state)

    def withdraw(self, file_path: str) -> None:
        """Remove LLM General deployment from a file"""
        state = self._load_state()
        if file_path in state["active_deployments"]:
            del state["active_deployments"][file_path]
            self._save_state(state)

    def is_in_combat(self, file_path: str) -> bool:
        """Check if a file currently has an LLM General deployed"""
        state = self._load_state()
        return file_path in state["active_deployments"]

    def get_active_deployments(self) -> Dict[str, dict]:
        """Get all active deployment information"""
        state = self._load_state()
        return state["active_deployments"].copy()

    def get_combat_files(self) -> List[str]:
        """Get list of files currently in COMBAT status"""
        state = self._load_state()
        return list(state["active_deployments"].keys())

    def cleanup_stale_deployments(self, max_age_hours: int = 24) -> None:
        """Remove deployments older than max_age_hours"""
        state = self._load_state()
        cutoff = datetime.now() - timedelta(hours=max_age_hours)

        stale_files = []
        for file_path, deployment in state["active_deployments"].items():
            deployed_at = datetime.fromisoformat(deployment["deployed_at"])
            if deployed_at < cutoff:
                stale_files.append(file_path)

        for file_path in stale_files:
            del state["active_deployments"][file_path]

        if stale_files:
            self._save_state(state)

    def get_deployment_info(self, file_path: str) -> Optional[dict]:
        """Get detailed deployment info for a specific file"""
        state = self._load_state()
        return state["active_deployments"].get(file_path)


if __name__ == "__main__":
    # Standalone test
    import sys

    # Use current directory if no argument provided
    project_root = sys.argv[1] if len(sys.argv) > 1 else "."

    tracker = CombatTracker(project_root)

    print("🎯 Combat Tracker Status")
    print("=" * 40)

    # Clean up stale deployments
    tracker.cleanup_stale_deployments()

    active = tracker.get_active_deployments()

    if active:
        print(f"📊 Active Deployments: {len(active)}")
        for file_path, deployment in active.items():
            deployed_at = deployment["deployed_at"]
            terminal_id = deployment["terminal_id"]
            model = deployment["model"]
            print(f"  🔥 {file_path}")
            print(f"     Terminal: {terminal_id}")
            print(f"     Model: {model}")
            print(f"     Deployed: {deployed_at}")
            print()
    else:
        print("📋 No active deployments")

    print(f"Combat files: {tracker.get_combat_files()}")
