from typing import List, Dict, Any, Protocol, Tuple, Optional
from orchestr8_next.city.contracts import CityNodeModel, CityConnectionModel, NodeType, Coordinate
import math
import os

class ILayoutEngine(Protocol):
    def layout(self, nodes: List[CityNodeModel], connections: List[CityConnectionModel]) -> None:
        ...

class ForceDirectedLayout:
    """
    Simulates force-directed layout (mocked clean-room implementation).
    Distributes nodes in a circle for minimal overlaps.
    """
    def layout(self, nodes: List[CityNodeModel], connections: List[CityConnectionModel]) -> None:
        count = len(nodes)
        if count == 0: return
        
        radius = count * 1.5  # Heuristic spacing
        for i, node in enumerate(nodes):
             angle = (i / count) * 2 * math.pi
             node.position = Coordinate(
                 x=radius * math.cos(angle),
                 y=radius * math.sin(angle),
                 z=0.0
             )

class CityTopologyBuilder:
    """
    Builds City Graph from generic sources.
    Uses generic layout engine.
    """
    def __init__(self, layout_engine: Optional[ILayoutEngine] = None):
        self.layout_engine = layout_engine or ForceDirectedLayout()

    def build_from_file_system(self, root_path: str) -> Tuple[List[CityNodeModel], List[CityConnectionModel]]:
        """Scans filesystem and returns City Model."""
        nodes = []
        connections = []
        
        # Simple mock implementation for B2 scope (just proves abstraction)
        # In real-world, we'd use 'fd' or recursive walk with excludes
        
        node_id_map = {}
        
        try:
            for root, dirs, files in os.walk(root_path):
                root_id = str(hash(root))
                # Root Node (Dir)
                if root_id not in node_id_map:
                    root_node = CityNodeModel(
                        id=root_id,
                        type=NodeType.DIRECTORY,
                        position=Coordinate(x=0, y=0, z=0),
                        label=os.path.basename(root) or "root"
                    )
                    nodes.append(root_node)
                    node_id_map[root_id] = root_node

                for f in files:
                    file_path = os.path.join(root, f)
                    file_id = str(hash(file_path))
                    file_node = CityNodeModel(
                        id=file_id,
                        type=NodeType.FILE,
                        position=Coordinate(x=0, y=0, z=0),
                        label=f
                    )
                    nodes.append(file_node)
                    # Edge
                    connections.append(CityConnectionModel(
                        source_id=root_id,
                        target_id=file_id,
                        type="contains"
                    ))
                    
        except Exception as e:
            # Handle permission errors etc
            pass

        # Apply Layout
        self.layout_engine.layout(nodes, connections)
        
        return nodes, connections
