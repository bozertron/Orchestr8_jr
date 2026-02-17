import marimo as mo
import json
import os
from orchestr8_next.city.contracts import generate_frontend_schemas, CodeCitySceneModel

# Feature Flag for Rendering Engine
RENDER_MODE = os.environ.get("ORCHESTR8_RENDER_MODE", "WIDGET")

if RENDER_MODE == "WIDGET":
    from orchestr8_next.city.widget import CodeCityWidget

from orchestr8_next.city.wiring import generate_wiring_view

app = mo.App(title="Orchestr8 Code City")

@app.cell
def __(mo, RENDER_MODE):
    mo.md(f"# Orchestr8 Code City 🏙️ ({RENDER_MODE} Mode)")
    return

@app.cell
def __():
    # 1. Load Data
    mock_data = {
        "session_id": "demo-001",
        "timestamp": 123456789,
        "nodes": [
            {"id": "n1", "type": "DIRECTORY", "position": {"x": 0, "y": 0, "z": 0}, "label": "orchestr8_next", "color": "#1fbdea", "size": 2.0},
            {"id": "n2", "type": "FILE", "position": {"x": 2, "y": 0, "z": 0}, "label": "app.py", "color": "#D4AF37", "size": 1.0},
            {"id": "n3", "type": "FILE", "position": {"x": 0, "y": 0, "z": 2}, "label": "contracts.py", "color": "#D4AF37", "size": 1.0}
        ],
        "connections": [
            {"source_id": "n1", "target_id": "n2", "type": "contains"},
            {"source_id": "n1", "target_id": "n3", "type": "contains"}
        ]
    }
    return mock_data,

@app.cell
def __(mock_data, mo):
    # 2. Control Layout
    filter_type = mo.ui.dropdown(["ALL", "FILE", "DIRECTORY"], value="ALL", label="Filter Type")
    show_labels = mo.ui.checkbox(value=True, label="Show Labels")
    
    controls = mo.vstack([
        mo.md("## Controls"),
        filter_type,
        show_labels
    ])
    return controls, filter_type, show_labels

@app.cell
def __(mock_data, filter_type, mo, json, RENDER_MODE, generate_wiring_view):
    # 3. Visualization Logic
    
    # 3A. 3D City View
    if RENDER_MODE == "WIDGET":
        from orchestr8_next.city.widget import CodeCityWidget
        city_viz = CodeCityWidget(nodes=mock_data['nodes'], filter_type=filter_type.value)
    else:
        # Legacy Iframe
        scene_json = json.dumps(mock_data)
        html_content = f"""
        <div id="city-container" style="width: 100%; height: 600px; background: #000; border: 1px solid #333;"></div>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <script>
            (function() {{
                const container = document.getElementById('city-container');
                if (!container) return;
                container.innerHTML = '';
                const scene = new THREE.Scene();
                const camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
                const renderer = new THREE.WebGLRenderer({{ antialias: true }});
                renderer.setSize(container.clientWidth, container.clientHeight);
                container.appendChild(renderer.domElement);
                
                const data = {scene_json};
                data.nodes.forEach(node => {{
                    const geometry = new THREE.BoxGeometry(1, 1, 1);
                    const material = new THREE.MeshBasicMaterial({{ color: 0x00ff00 }});
                    const cube = new THREE.Mesh(geometry, material);
                    cube.position.set(node.position.x, node.position.y, node.position.z);
                    scene.add(cube);
                }});
                
                camera.position.z = 5;
                camera.position.y = 5;
                camera.lookAt(0,0,0);
                renderer.render(scene, camera);
            }})();
        </script>
        """
        city_viz = mo.Html(html_content)
        
    # 3B. 2D Wiring View
    # Use relative path for serving
    wiring_path = "wiring_view.html"
    abs_path = generate_wiring_view(mock_data['nodes'], mock_data['connections'], filename=wiring_path)
    
    # Embed using iframe srcdoc to avoid server config issues, or serve statically?
    # Reading content is safer for standalone.
    with open(abs_path, 'r') as f:
        wiring_html = f.read()
        
    wiring_viz = mo.Html(f'<iframe srcdoc="{wiring_html.replace("\"", "&quot;")}" width="100%" height="600px" frameborder="0"></iframe>')
    # Alternatively use mo.iframe if it supports srcdoc, but doc isn't explicit here.
    # Safe bet: mo.Html containing iframe with srcdoc
    
    return city_viz, wiring_viz

@app.cell
def __(controls, city_viz, wiring_viz, mo):
    # 4. Final Layout with Tabs
    tabs = mo.ui.tabs({
        "🏙️ 3D City": city_viz,
        "🕸️ Wiring": wiring_viz
    })
    
    mo.hstack([
        controls,
        tabs
    ], widths=[1, 3])
    return

if __name__ == "__main__":
    app.run()
