"""
Health Watcher - Real-time file change detection with debouncing.
Bridges file system events to HealthChecker for Code City visualization.
"""

import threading
from collections import defaultdict
from pathlib import Path
from typing import Callable, Dict, Any, Optional, List
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent

from IP.health_checker import HealthChecker, HealthCheckResult


class HealthWatcher:
    """
    File watcher with 100ms debounce for triggering health checks.

    Data flow: File Change → Debounce → HealthChecker → Callback → UI State
    """

    DEBOUNCE_MS = 100  # 100ms debounce per CONTEXT.md

    def __init__(self, project_root: str, callback: Callable[[Dict[str, Any]], None]):
        self.project_root = Path(project_root)
        self.callback = callback
        self.health_checker = HealthChecker(str(self.project_root))
        self._observer: Optional[Observer] = None
        self._debounce_timer: Optional[threading.Timer] = None
        self._pending_file: Optional[str] = None
        self._lock = threading.Lock()

    def _on_file_change(self, event):
        """Handle file change event with debouncing."""
        if event.is_directory:
            return

        file_path = str(event.src_path)
        # Only watch .py, .ts, .tsx files
        if not any(
            file_path.endswith(ext) for ext in [".py", ".ts", ".tsx", ".js", ".jsx"]
        ):
            return

        with self._lock:
            self._pending_file = file_path

            # Cancel existing timer
            if self._debounce_timer:
                self._debounce_timer.cancel()

            # Schedule new check after debounce period
            self._debounce_timer = threading.Timer(
                self.DEBOUNCE_MS / 1000.0, self._debounced_check
            )
            self._debounce_timer.start()

    def _debounced_check(self):
        """Execute health check after debounce period."""
        with self._lock:
            if not self._pending_file:
                return
            file_path = self._pending_file
            self._pending_file = None

        try:
            # Get relative path from project root
            rel_path = str(Path(file_path).relative_to(self.project_root))

            # Run health check
            result = self.health_checker.check_fiefdom(rel_path)

            # Invoke callback with result
            self.callback({rel_path: result})
        except Exception as e:
            # Log error but don't crash
            print(f"HealthWatcher error: {e}")

    def start_watching(self) -> None:
        """Start watching the project for file changes."""
        if self._observer:
            return  # Already watching

        class Handler(FileSystemEventHandler):
            def __init__(self, watcher):
                self.watcher = watcher

            def on_modified(self, event):
                self.watcher._on_file_change(event)

        self._observer = Observer()
        self._observer.schedule(Handler(self), str(self.project_root), recursive=True)
        self._observer.start()

    def stop_watching(self) -> None:
        """Stop watching for file changes."""
        if self._debounce_timer:
            self._debounce_timer.cancel()
            self._debounce_timer = None

        if self._observer:
            self._observer.stop()
            self._observer.join()
            self._observer = None


# =============================================================================
# HealthWatcherManager - Marimo FileWatcherManager Integration
# =============================================================================


class HealthWatcherManager:
    """
    File watcher using Marimo's FileWatcherManager for health checking.

    Integrates with Marimo's reactive state for real-time Code City updates.
    Debounces file changes to prevent CPU spikes during bulk modifications.

    Data flow: File Change → Debounce → HealthChecker → state_managers → Code City
    """

    DEBOUNCE_MS = 300  # 300ms debounce per CONTEXT.md

    def __init__(
        self,
        project_root: Path,
        state_managers: Dict[str, Any],
        watch_paths: List[str] = None,
    ):
        """
        Initialize HealthWatcherManager.

        Args:
            project_root: Path to project root directory
            state_managers: Dict with "health" state getter/setter
            watch_paths: List of paths to watch (default: ["IP/"])
        """
        self.project_root = Path(project_root)
        self._state_managers = state_managers
        self._watch_paths = watch_paths or ["IP/"]

        # Pending file changes grouped by fiefdom
        self._pending: Dict[str, set] = defaultdict(set)

        # Debounce task reference
        self._debounce_task = None

        # Health checker instance
        self._health_checker = HealthChecker(str(self.project_root))

        # File watcher manager (Marimo)
        self._file_watcher = None
