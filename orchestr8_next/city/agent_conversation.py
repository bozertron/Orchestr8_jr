from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import time

class MessageType(Enum):
    USER = "user"
    AGENT = "agent"
    SYSTEM = "system"
    TOOL = "tool"
    ERROR = "error"

@dataclass
class ConversationMessage:
    """
    Standardized conversation message schema for City Comms.
    Ref: C3-02 WizardConversation.
    """
    id: str
    type: MessageType
    content: str
    timestamp: float
    sender_id: str
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ToolExecution:
    """
    Represents an active tool execution (for 'Thinking' visualization).
    """
    id: str
    tool_name: str
    status: str = "running" # 'running', 'complete', 'failed'
    logs: List[str] = field(default_factory=list)
    start_time: float = field(default_factory=lambda: time.time())
    end_time: Optional[float] = None

class AgentConversationService:
    """
    Core logic for in-world agent communication and tool feedback.
    """
    def __init__(self, temporal_service: Optional[Any] = None):
        self._history: List[ConversationMessage] = []
        self._active_tools: Dict[str, ToolExecution] = {}
        self._temporal = temporal_service

    def post_message(self, type: MessageType, content: str, sender: str = "system") -> str:
        msg_id = f"msg-{int(time.time() * 1000)}"
        msg = ConversationMessage(
            id=msg_id,
            type=type,
            content=content,
            timestamp=time.time(),
            sender_id=sender
        )
        self._history.append(msg)
        if self._temporal:
            self._temporal.record_quantum("conversation_msg", sender, {
                "msg_id": msg_id, 
                "type": type.value,
                "preview": content[:100] + ("..." if len(content) > 100 else "")
            })
        return msg_id

    def get_history(self, limit: int = 50) -> List[ConversationMessage]:
        return self._history[-limit:]

    # Tool / Thinking Logic
    def start_thinking(self, tool_name: str) -> str:
        exec_id = f"exec-{int(time.time() * 1000)}"
        self._active_tools[exec_id] = ToolExecution(id=exec_id, tool_name=tool_name)
        if self._temporal:
            self._temporal.record_quantum("tool_start", "agent", {"exec_id": exec_id, "tool": tool_name})
        return exec_id

    def add_tool_log(self, exec_id: str, log_line: str) -> bool:
        if exec_id in self._active_tools:
            self._active_tools[exec_id].logs.append(log_line)
            return True
        return False

    def complete_thinking(self, exec_id: str, success: bool = True) -> Optional[ToolExecution]:
        if exec_id in self._active_tools:
            tool = self._active_tools[exec_id]
            tool.status = "complete" if success else "failed"
            tool.end_time = time.time()
            if self._temporal:
                self._temporal.record_quantum("tool_complete", "agent", {"exec_id": exec_id, "success": success})
            return tool
        return None

    def get_active_thinking_tasks(self) -> List[ToolExecution]:
        """Returns currently running tools for visualization (particle effects)."""
        return [t for t in self._active_tools.values() if t.status == "running"]
