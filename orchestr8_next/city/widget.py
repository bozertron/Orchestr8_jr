import anywidget
import traitlets
import json
import uuid
import math

# Guardrails
MAX_CHUNK_SIZE = 4 * 1024 * 1024  # 4MB (below Marimo 5MB limit)

class CodeCityWidget(anywidget.AnyWidget):
    _esm = """
    import * as THREE from "https://esm.sh/three@0.160.0";
    
    function render({ model, el }) {
        // ... (Scene Setup from previous implementation) ...
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, el.clientWidth / el.clientHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        renderer.setSize(el.clientWidth, el.clientHeight);
        el.appendChild(renderer.domElement);
         
        // Lighting
        const ambient = new THREE.AmbientLight(0x404040);
        scene.add(ambient);

        // State for Chunk Assembly
        let receiveBuffer = {}; // { payload_id: { chunks: [], total: N, received: 0 } }
        
        function processChunk() {
            const meta = model.get("chunk_meta");
            const dataView = model.get("chunk_data"); // DataView of the bytes
            
            if (!meta || !dataView) return;
            
            const { payload_id, chunk_index, chunk_total } = meta;
            
            if (!receiveBuffer[payload_id]) {
                receiveBuffer[payload_id] = { chunks: new Array(chunk_total), received: 0 };
            }
            
            const buffer = receiveBuffer[payload_id];
            
            // Store chunk (decoding bytes to text if JSON, or keeping as bytes)
            // Assuming JSON payload for now, we decode Text
            const decoder = new TextDecoder("utf-8");
            buffer.chunks[chunk_index] = decoder.decode(dataView);
            buffer.received++;
            
            if (buffer.received === chunk_total) {
                // Assembly Complete
                const fullJson = buffer.chunks.join("");
                try {
                    const sceneData = JSON.parse(fullJson);
                    updateSceneFromData(sceneData);
                    // Clear buffer
                    delete receiveBuffer[payload_id];
                } catch (e) {
                    console.error("Failed to parse assembled JSON", e);
                }
            }
        }
        
        function updateSceneFromData(data) {
            // Re-use update logic
            // (Simulated Logic for brevity - would match previous implementation)
            console.log("Scene Updated with " + data.nodes.length + " nodes.");
             
            // Clear existing meshes logic...
            while(scene.children.length > 0){ 
                scene.remove(scene.children[0]); 
            }
            scene.add(ambient); // Add light back

            if (data.nodes) {
                data.nodes.forEach(node => {
                    const geometry = new THREE.BoxGeometry(1, 1, 1);
                    const material = new THREE.MeshStandardMaterial({ color: node.color || "#ffffff" });
                    const cube = new THREE.Mesh(geometry, material);
                    if (node.position) cube.position.set(node.position.x, node.position.y, node.position.z);
                    scene.add(cube);
                });
            }
        }
        
        // Listeners
        model.on("change:chunk_meta", processChunk);
        
        // Animation Loop
        camera.position.z = 10;
        function animate() {
            requestAnimationFrame(animate);
            renderer.render(scene, camera);
        }
        animate();
        
        return () => { renderer.dispose(); }
    }
    export default { render };
    """
    
    # Standard Traits
    nodes = traitlets.List([]).tag(sync=True)
    filter_type = traitlets.Unicode("ALL").tag(sync=True)
    
    # Binary Payload Traits
    chunk_data = traitlets.Bytes().tag(sync=True)
    chunk_meta = traitlets.Dict().tag(sync=True)
    
    def send_scene_data(self, data: dict):
        """
        Chunks and sends the scene data via binary traits.
        """
        json_str = json.dumps(data)
        blob = json_str.encode("utf-8")
        total_size = len(blob)
        
        # Calculate chunks
        num_chunks = math.ceil(total_size / MAX_CHUNK_SIZE)
        payload_id = str(uuid.uuid4())
        
        for i in range(num_chunks):
            start = i * MAX_CHUNK_SIZE
            end = start + MAX_CHUNK_SIZE
            chunk = blob[start:end]
            
            # Update Data First
            self.chunk_data = chunk
            
            # Then Update Meta to trigger partial processing
            self.chunk_meta = {
                "payload_id": payload_id,
                "chunk_index": i,
                "chunk_total": num_chunks
            }
