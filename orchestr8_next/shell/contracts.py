from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Optional, List, Dict
import threading

class ActionType(str, Enum):
    # Left Cluster Actions
    NAVIGATE_APPS = "NAVIGATE_APPS"
    NAVIGATE_MATRIX = "NAVIGATE_MATRIX"
    NAVIGATE_CALENDAR = "NAVIGATE_CALENDAR"
    NAVIGATE_COMMS = "NAVIGATE_COMMS"
    NAVIGATE_FILES = "NAVIGATE_FILES"
    
    # Center Cluster Actions
    MAESTRO_CLICK = "MAESTRO_CLICK"
    
    # Right Cluster Actions
    TOGGLE_SEARCH = "TOGGLE_SEARCH"
    RECORD_START = "RECORD_START"
    RECORD_STOP = "RECORD_STOP"
    PLAYBACK_TOGGLE = "PLAYBACK_TOGGLE"
    PHREAK_MODE = "PHREAK_MODE"
    SEND_MESSAGE = "SEND_MESSAGE"
    ATTACH_FILE = "ATTACH_FILE"
    INPUT_UPDATE = "INPUT_UPDATE"

class MaestroState(str, Enum):
    OFF = "OFF"
    OBSERVE = "OBSERVE"
    ON = "ON"

@dataclass(frozen=True)
class ShellState:
    # Navigation
    current_view: str = "matrix"
    sidebar_expanded: bool = True
    
    # Maestro State Machine
    maestro_status: MaestroState = MaestroState.OFF
    
    # Media / Input State
    is_recording: bool = False
    is_playing: bool = False
    search_active: bool = False
    phreak_active: bool = False
    
    # Input Buffer
    input_text: str = ""
    last_input_timestamp: float = 0.0

@dataclass(frozen=True)
class State:
    shell: ShellState
    # Future expansion for other domains
    # domain: DomainState
    
    @staticmethod
    def initial() -> 'State':
        return State(
            shell=ShellState()
        )
