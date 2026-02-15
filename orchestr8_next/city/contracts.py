import json
from enum import Enum
from typing import List, Optional, Literal, Dict, Any, Union
from typing_extensions import Annotated
from pydantic import BaseModel, Field, ConfigDict, Discriminator, TypeAdapter

# --- Primitive Models ---

class Coordinate(BaseModel):
    x: float
    y: float
    z: float
    model_config = ConfigDict(extra='forbid')

class Rotation(BaseModel):
    x: float
    y: float
    z: float
    model_config = ConfigDict(extra='forbid')

class NodeType(str, Enum):
    FILE = "FILE"
    DIRECTORY = "DIRECTORY"
    CLASS = "CLASS"
    FUNCTION = "FUNCTION"
    UNKNOWN = "UNKNOWN"

# --- Scene Composition Models ---

class CityNodeModel(BaseModel):
    id: str
    type: NodeType
    position: Coordinate
    label: str
    size: float = 1.0
    color: str = "#FFFFFF"
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    model_config = ConfigDict(extra='forbid')

class CityConnectionModel(BaseModel):
    source_id: str
    target_id: str
    type: str = "dependency"
    weight: float = 1.0
    
    model_config = ConfigDict(extra='forbid')

class CodeCitySceneModel(BaseModel):
    session_id: str
    nodes: List[CityNodeModel] = Field(default_factory=list)
    connections: List[CityConnectionModel] = Field(default_factory=list)
    timestamp: float
    
    model_config = ConfigDict(extra='forbid')

# --- Event Models ---

class BaseCityEvent(BaseModel):
    version: Literal["1.0.0"] = "1.0.0"
    timestamp: float
    model_config = ConfigDict(extra='forbid')

# Inbound Events (JS -> Python)

class NodeClickedEvent(BaseCityEvent):
    type: Literal["node_clicked"] = "node_clicked"
    node_id: str
    button: int = 0

class CameraMovedEvent(BaseCityEvent):
    type: Literal["camera_moved"] = "camera_moved"
    position: Coordinate
    rotation: Rotation

class ConnectionRequestedEvent(BaseCityEvent):
    type: Literal["connect_request"] = "connect_request"
    source_id: str
    target_id: str

# Discriminated Union for Inbound Events
InboundEvent = Annotated[
    Union[NodeClickedEvent, CameraMovedEvent, ConnectionRequestedEvent],
    Discriminator("type")
]
InboundEventAdapter = TypeAdapter(InboundEvent)

# Outbound Commands (Python -> JS)

class UpdateSceneCommand(BaseCityEvent):
    type: Literal["update_scene"] = "update_scene"
    scene: CodeCitySceneModel

class HighlightNodeCommand(BaseCityEvent):
    type: Literal["highlight_node"] = "highlight_node"
    node_id: str
    color: str

# Discriminated Union for Outbound Commands
OutboundCommand = Annotated[
    Union[UpdateSceneCommand, HighlightNodeCommand],
    Discriminator("type")
]
OutboundCommandAdapter = TypeAdapter(OutboundCommand)

# --- Utilities ---

def generate_frontend_schemas() -> Dict[str, Any]:
    """
    Exports generic JSON schemas for frontend validation.
    """
    return {
        "InboundEvent": InboundEventAdapter.json_schema(),
        "OutboundCommand": OutboundCommandAdapter.json_schema(),
        "CodeCitySceneModel": CodeCitySceneModel.model_json_schema()
    }
