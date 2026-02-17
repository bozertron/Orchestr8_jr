import pytest
from orchestr8_next.city.agent_conversation import AgentConversationService, MessageType

def test_streaming_message_lifecycle():
    """Verify C3-02 Conversation logic."""
    service = AgentConversationService()
    
    # Post User Message
    msg_id = service.post_message(MessageType.USER, "Hello Agent", "user-123")
    assert msg_id
    
    # Tool Execution (Thinking)
    exec_id = service.start_thinking("file_scan")
    service.add_tool_log(exec_id, "Found file A")
    service.add_tool_log(exec_id, "Found file B")
    
    active = service.get_active_thinking_tasks()
    assert len(active) == 1
    assert active[0].tool_name == "file_scan"
    assert len(active[0].logs) == 2
    
    # Complete
    service.complete_thinking(exec_id, success=True)
    
    active_now = service.get_active_thinking_tasks()
    assert len(active_now) == 0
    # But it should exist in history or separate query if implemented
    # My impl stores in _active_tools still but status='complete'
    
    # Post Agent Response
    agent_id = service.post_message(MessageType.AGENT, "Scan Complete", "agent-007")
    
    history = service.get_history()
    assert len(history) == 2
    assert history[0].content == "Hello Agent"
    assert history[1].content == "Scan Complete"

def test_empty_state():
    service = AgentConversationService()
    assert len(service.get_history()) == 0
    assert len(service.get_active_thinking_tasks()) == 0
