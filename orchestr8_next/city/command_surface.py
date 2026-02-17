from typing import Dict, Any, Callable, Optional, List
from dataclasses import dataclass, field
import uuid
import json

@dataclass
class Command:
    """Represents a city-wide command."""
    id: str
    intent: str
    handler: Callable
    description: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

class CommandSurface:
    """
    Registry for city data-layer commands.
    Provides a unified interface for front-end visual layers to trigger core logic.
    """
    def __init__(self):
        self._commands: Dict[str, Command] = {}

    def register_default_commands(self, temporal: Any):
        """Register core city commands."""
        self.register_command(
            intent="time_machine",
            handler=lambda quantum_id: temporal.get_snapshot_by_quantum(quantum_id),
            description="Jump to a specific point in the city timeline."
        )
        self.register_command(
            intent="query_history",
            handler=lambda **kwargs: temporal.search_history(**kwargs),
            description="Search the city event ledger."
        )

    def register_command(self, intent: str, handler: Callable, description: str = "", meta: Dict = None):
        """Register a new command handler."""
        cmd_id = f"cmd-{intent}"
        self._commands[cmd_id] = Command(
            id=cmd_id,
            intent=intent,
            handler=handler,
            description=description,
            metadata=meta or {}
        )
        return cmd_id

    def execute_command(self, intent: str, **kwargs) -> Any:
        """Execute a command by intent."""
        cmd_id = f"cmd-{intent}"
        if cmd_id not in self._commands:
            raise ValueError(f"Command '{intent}' not found in surface.")
        
        result = self._commands[cmd_id].handler(**kwargs)
        
        # Optional: auto-signal result to shared memory if configured
        # This acts as the 'ingestion hook' for visual layers
        return result

    def signal_event(self, event_type: str, payload: Dict[str, Any]):
        """
        Post an event to the shared memory gateway for visual lane ingestion.
        Ref: ACP-05.
        """
        import requests
        try:
            requests.post(
                "http://127.0.0.1:37888/v1/memory/save",
                json={
                    "title": f"CITY_EVENT: {event_type}",
                    "text": json.dumps(payload)
                },
                timeout=1
            )
        except Exception:
            # Silent fail for now if gateway is down
            pass

    def list_commands(self) -> List[Dict[str, Any]]:
        """List all available commands for the UI."""
        return [
            {
                "id": c.id,
                "intent": c.intent,
                "description": c.description,
                "metadata": c.metadata
            }
            for c in self._commands.values()
        ]
