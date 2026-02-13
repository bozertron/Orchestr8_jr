"""
Health Watcher - Real-time file change detection with debouncing.

Provides two implementations:
- HealthWatcher: Simple watchdog-based watcher with callback
- HealthWatcherManager: Marimo-integrated watcher with reactive state updates

Data flow: File Change → Debounce → HealthChecker → State → Code City
"""

__all__ = ["HealthWatcher", "HealthWatcherManager"]

import asyncio
import threading
from collections import defaultdict
from pathlib import Path
from typing import Callable, Dict, Any, Optional, List

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler, FileModifiedEvent

    HAS_WATCHDOG = True
except ImportError:
    Observer = None
    FileSystemEventHandler = object
    FileModifiedEvent = None
    HAS_WATCHDOG = False

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
        if not HAS_WATCHDOG:
            print("HealthWatcher: watchdog not installed, file watching disabled")
            return

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

    def _map_to_fiefdom(self, path: Path) -> str:
        """
        Map a file path to its parent fiefdom identifier.

        Args:
            path: Path object for the changed file

        Returns:
            Fiefdom string (e.g., "IP/" or "vscode-marimo/")
        """
        try:
            rel_path = path.relative_to(self.project_root)
            parts = rel_path.parts

            if parts and parts[0] == "IP":
                return "IP/"

            # Return parent directory as fiefdom
            if len(parts) > 1:
                return str(rel_path.parent) + "/"
            return str(rel_path) + "/"

        except ValueError:
            # Path not relative to project root
            return str(path.parent) + "/"

    async def _on_file_change(self, path: Path) -> None:
        """
        Handle file change event with debouncing.

        Adds the changed file to pending queue and schedules
        a debounced health check.

        Args:
            path: Path to the changed file
        """
        suffix = path.suffix.lower()
        if suffix not in {".py", ".ts", ".tsx", ".js", ".jsx"}:
            return

        fiefdom = self._map_to_fiefdom(path)

        self._pending[fiefdom].add(str(path))

        if self._debounce_task is not None:
            try:
                self._debounce_task.cancel()
            except Exception:
                pass

        self._debounce_task = asyncio.create_task(self._debounced_check())

    async def _debounced_check(self) -> None:
        """
        Execute batched health checks after debounce period.

        Waits DEBOUNCE_MS, then runs health checks on all pending
        fiefdoms and updates state_managers.
        """
        try:
            await asyncio.sleep(self.DEBOUNCE_MS / 1000)

            pending_fiefdoms = list(self._pending.keys())

            if not pending_fiefdoms:
                return

            results = {}
            for fiefdom in pending_fiefdoms:
                try:
                    result = self._health_checker.check_fiefdom(fiefdom)

                    results[fiefdom] = {
                        "status": result.status,
                        "errors": [
                            {"file": e.file, "line": e.line, "message": e.message}
                            for e in result.errors
                        ],
                        "warnings": [
                            {"file": w.file, "line": w.line, "message": w.message}
                            for w in result.warnings
                        ],
                        "last_check": result.last_check,
                        "checker_used": result.checker_used,
                    }
                except Exception as e:
                    results[fiefdom] = {
                        "status": "broken",
                        "errors": [{"file": fiefdom, "line": 0, "message": str(e)}],
                    }

            if "health" in self._state_managers:
                get_health, set_health = self._state_managers["health"]
                current = get_health() or {}
                current.update(results)
                set_health(current)

            self._pending.clear()

        except asyncio.CancelledError:
            pass
        except Exception as e:
            print(f"HealthWatcherManager._debounced_check error: {e}")

    def start(self) -> None:
        """
        Start watching files for changes.

        Uses Marimo's FileWatcherManager for integration with
        Marimo's reactive update system.
        """
        try:
            from marimo._utils.file_watcher import FileWatcherManager

            self._file_watcher = FileWatcherManager()

            for watch_path in self._watch_paths:
                full_path = self.project_root / watch_path
                if full_path.exists():
                    self._file_watcher.add_callback(
                        full_path,
                        lambda p: asyncio.create_task(self._on_file_change(p)),
                    )

        except ImportError:
            print(
                "HealthWatcherManager: Marimo FileWatcherManager not available, using polling"
            )
            self._start_polling_fallback()

    def stop(self) -> None:
        """Stop watching files and cleanup resources."""
        if self._debounce_task is not None:
            self._debounce_task.cancel()
            self._debounce_task = None

        if self._file_watcher is not None:
            try:
                self._file_watcher.stop_all()
            except Exception:
                pass
            self._file_watcher = None

    def _start_polling_fallback(self) -> None:
        """
        Fallback polling implementation when Marimo's FileWatcherManager
        is not available.
        """
        if not HAS_WATCHDOG:
            print(
                "HealthWatcherManager: watchdog not installed, file watching disabled"
            )
            return

        class Handler(FileSystemEventHandler):
            def __init__(self, manager):
                self.manager = manager

            def on_modified(self, event):
                if not event.is_directory:
                    try:
                        loop = asyncio.get_event_loop()
                        loop.create_task(
                            self.manager._on_file_change(Path(event.src_path))
                        )
                    except Exception:
                        pass

        self._observer = Observer()
        for watch_path in self._watch_paths:
            full_path = self.project_root / watch_path
            if full_path.exists():
                self._observer.schedule(Handler(self), str(full_path), recursive=True)
        self._observer.start()
