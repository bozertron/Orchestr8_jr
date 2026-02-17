from pyvis.network import Network
import networkx as nx
import os
import json

def generate_wiring_view(nodes: list, connections: list, filename: str = "wiring_view.html") -> str:
    """
    Generates a 2D interactive wiring diagram using Pyvis.
    Returns the HTML content string suitable for embedding in Marimo.
    """
    net = Network(height="600px", width="100%", bgcolor="#222222", font_color="white",  notebook=False)
    
    # Configure Physics
    net.force_atlas_2based()
    
    # Add Nodes
    for node in nodes:
        net.add_node(
            node['id'], 
            label=node.get('label', node['id']), 
            color=node.get('color', '#97C2FC'),
            size=int(float(node.get('size', 10)) * 5), # Scale up
            title=json.dumps(node, indent=2) # Tooltip
        )
        
    # Add Edges
    for conn in connections:
        net.add_edge(conn['source_id'], conn['target_id'], title=conn.get('type', 'connection'))
        
    # Generate HTML content
    # Note: net.generate_html() writes to file or returns string depending on version/config
    # We can use net.html property or write to temporary file and read back.
    
    # Force use of local template or disable CDN if needed
    # For now, rely on default CDN for vis.js
    
    net.write_html(filename)
    
    # Return path or content? 
    # Marimo iframe usually needs src path if serving, or srcdoc content.
    # We'll return the absolute path for now.
    return os.path.abspath(filename)

import json
