# IP/terminal_spawner.py
import platform
import subprocess
import json
from datetime import datetime
from pathlib import Path
from typing import Optional


class TerminalSpawner:
    # TODO: Make terminal preference configurable via settings
    # Currently hardcoded - could be extended to read from pyproject_orchestr8_settings.toml
    DEFAULT_TERMINAL_PREFERENCES = {
        "linux": ["gnome-terminal", "xterm", "konsole", "xfce4-terminal"],
        "darwin": ["Terminal", "iTerm.app", "Hyper"],
        "win32": ["cmd.exe", "PowerShell.exe", "WindowsTerminal.exe"],
    }

    def __init__(self, project_root: str, preferred_terminal: Optional[str] = None):
        self.project_root = Path(project_root)
        self.state_file = (
            self.project_root / ".orchestr8" / "state" / "fiefdom-status.json"
        )
        self.preferred_terminal = preferred_terminal

    def update_fiefdom_status(self, fiefdom_path: str, status: str) -> None:
        """Update fiefdom status in state file."""
        self.state_file.parent.mkdir(parents=True, exist_ok=True)

        if self.state_file.exists():
            with open(self.state_file) as f:
                state = json.load(f)
        else:
            state = {"fiefdoms": {}}

        state["fiefdoms"][fiefdom_path] = {
            "status": status,
            "updated_at": datetime.now().isoformat(),
        }

        with open(self.state_file, "w") as f:
            json.dump(state, f, indent=2)

    def spawn(
        self,
        fiefdom_path: str,
        briefing_ready: bool = True,
        auto_start_claude: bool = False,
    ) -> bool:
        """
        Spawn terminal at fiefdom path and update status to COMBAT.

        Args:
            fiefdom_path: Relative path from project root
            briefing_ready: Whether BRIEFING.md has been generated
            auto_start_claude: Whether to auto-run claude command

        Returns:
            True if spawn succeeded
        """
        abs_path = str(self.project_root / fiefdom_path)

        # Update status to COMBAT (purple)
        self.update_fiefdom_status(fiefdom_path, "combat")

        # Build startup message
        if briefing_ready:
            msg = 'echo "BRIEFING.md ready. Type: claude --print \\"Read BRIEFING.md and begin.\\""'
        else:
            msg = 'echo "Read CLAUDE.md for orders. Type: claude"'

        if auto_start_claude:
            msg += ' && claude --print "Read BRIEFING.md and begin."'
        else:
            msg += " && bash"

        # Platform-specific spawn
        system = platform.system()

        try:
            if system == "Linux":
                # Try gnome-terminal first, fall back to xterm
                try:
                    subprocess.Popen(
                        [
                            "gnome-terminal",
                            "--working-directory",
                            abs_path,
                            "--",
                            "bash",
                            "-c",
                            msg,
                        ]
                    )
                except FileNotFoundError:
                    subprocess.Popen(["xterm", "-e", f'cd "{abs_path}" && {msg}'])

            elif system == "Darwin":  # macOS
                script = f"""
                tell application "Terminal"
                    do script "cd '{abs_path}' && {msg}"
                    activate
                end tell
                """
                subprocess.Popen(["osascript", "-e", script])

            elif system == "Windows":
                subprocess.Popen(
                    ["cmd", "/c", "start", "cmd", "/k", f'cd /d "{abs_path}" && {msg}']
                )

            return True

        except Exception as e:
            print(f"Failed to spawn terminal: {e}")
            # Revert status on failure
            self.update_fiefdom_status(fiefdom_path, "broken")
            return False

    def mark_combat_complete(self, fiefdom_path: str, success: bool) -> None:
        """
        Mark combat as complete. Called when general finishes.

        Args:
            fiefdom_path: The fiefdom that was worked on
            success: Whether mission succeeded (for status update)
        """
        # Status will be updated by next health check
        # This just logs the completion
        self.update_fiefdom_status(fiefdom_path, "pending_health_check")
