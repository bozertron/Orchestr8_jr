import dataclasses
from orchestr8_next.shell.contracts import State, ShellState, ActionType, MaestroState
from orchestr8_next.shell.actions import UIAction

def root_reducer(current_state: State, action: UIAction) -> State:
    """
    Pure function that takes the current immutable state and an action,
    and returns the new immutable state.
    """
    new_shell = shell_reducer(current_state.shell, action)
    
    # Using dataclasses.replace guarantees a shallow copy with modifications
    return dataclasses.replace(current_state, shell=new_shell)

def shell_reducer(current_shell: ShellState, action: UIAction) -> ShellState:
    # 1. Maestro State Machine Logic (OFF -> OBSERVE -> ON -> OFF)
    if action.type == ActionType.MAESTRO_CLICK:
        next_status = MaestroState.OFF
        if current_shell.maestro_status == MaestroState.OFF:
            next_status = MaestroState.OBSERVE
        elif current_shell.maestro_status == MaestroState.OBSERVE:
            next_status = MaestroState.ON
        elif current_shell.maestro_status == MaestroState.ON:
            next_status = MaestroState.OFF
            
        return dataclasses.replace(current_shell, maestro_status=next_status)

    # 2. Navigation Logic (Left Cluster)
    if action.type == ActionType.NAVIGATE_APPS:
        return dataclasses.replace(current_shell, current_view="apps")
        
    if action.type == ActionType.NAVIGATE_MATRIX:
        return dataclasses.replace(current_shell, current_view="matrix")
        
    if action.type == ActionType.NAVIGATE_CALENDAR:
        return dataclasses.replace(current_shell, current_view="calendar")

    if action.type == ActionType.NAVIGATE_COMMS:
        return dataclasses.replace(current_shell, current_view="comms")

    if action.type == ActionType.NAVIGATE_FILES:
        return dataclasses.replace(current_shell, current_view="files")
        
    # 3. Right Cluster Logic
    if action.type == ActionType.TOGGLE_SEARCH:
        return dataclasses.replace(current_shell, search_active=not current_shell.search_active)

    if action.type == ActionType.RECORD_START:
        return dataclasses.replace(current_shell, is_recording=True)

    if action.type == ActionType.RECORD_STOP:
        return dataclasses.replace(current_shell, is_recording=False)

    if action.type == ActionType.PLAYBACK_TOGGLE:
        return dataclasses.replace(current_shell, is_playing=not current_shell.is_playing)

    if action.type == ActionType.PHREAK_MODE:
        return dataclasses.replace(current_shell, phreak_active=not current_shell.phreak_active)
        
    if action.type == ActionType.INPUT_UPDATE:
        new_text = action.payload if action.payload is not None else ""
        return dataclasses.replace(current_shell, input_text=str(new_text))
        
    # Default: Return state unchanged
    return current_shell
