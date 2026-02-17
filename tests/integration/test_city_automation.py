from orchestr8_next.city.automation import QueueService, UndoRedoService, AutomationTask

def test_automation_queue_flow():
    """Verify QueueService (C2-01) logic."""
    queue = QueueService()
    
    # Enqueue
    task_id = queue.enqueue("target-123", "Modify File A")
    assert task_id is not None
    assert queue.get_pending_count() == 1
    
    # Process
    task = queue.next_task()
    assert task is not None
    assert task.status == "processing"
    assert task.id == task_id
    
    # Empty Handling
    assert queue.get_pending_count() == 0
    assert queue.next_task() is None

def test_undo_redo_service():
    """Verify UndoRedoService (C2-01) logic."""
    service = UndoRedoService()
    
    # Push States
    service.capture_snapshot("State 1") # Ptr 0
    service.capture_snapshot("State 2") # Ptr 1
    service.capture_snapshot("State 3") # Ptr 2
    
    # Current Pointer = 2 (State 3)
    
    # Undo -> Ptr 1 (State 2)
    new_state = service.undo()
    assert new_state == "State 2"
    
    # Undo Again -> Ptr 0 (State 1)
    new_state = service.undo()
    assert new_state == "State 1"
    
    # Undo Limit -> Ptr 0 (No change, return None)
    new_state = service.undo()
    assert new_state is None 
    
    # Redo -> Ptr 1 (State 2)
    redo_state = service.redo()
    assert redo_state == "State 2"
