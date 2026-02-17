# /// script
# [tool.marimo.runtime]
# auto_instantiate = false
# ///

import marimo

__generated_with = "ai"
app = marimo.App(width="medium")

@app.cell
def _():
    import marimo as mo
    
    mo.md("""
    # 3D Particle Opening Sequence with Morphing 2D UI
    
    This notebook demonstrates how you might architect a web-based 3D particle opening sequence that transitions into a 2D UI, using modern browser technologies such as WebGPU, three.js, and particles.js. While marimo notebooks cannot directly run JavaScript or WebGPU code, the following provides a conceptual overview and an HTML/JS embedding example for prototyping.
    
    - **3D Opening**: Rendered with three.js (WebGPU backend if available)
    - **Morph to 2D UI**: Uses particles.js for a dynamic 2D particle background
    - **UI**: Simple HTML/CSS overlay
    
    Below is an embedded HTML/JS prototype. To run this outside the notebook, copy the code into an `.html` file and open in your browser.
    """)
    return

@app.cell
def _():
    mo.Html(r'''
    <style>
      body { margin: 0; overflow: hidden; }
      #overlay-ui {
        position: absolute;
        top: 0; left: 0; width: 100vw; height: 100vh;
        display: flex; align-items: center; justify-content: center;
        pointer-events: none;
        opacity: 0; transition: opacity 1s;
        z-index: 10;
      }
      #overlay-ui.active { opacity: 1; pointer-events: auto; }
      .ui-box {
        background: rgba(255,255,255,0.9); padding: 2em 4em; border-radius: 1em;
        box-shadow: 0 4px 32px rgba(0,0,0,0.2);
        font-size: 2em;
      }
      #particles-js { position: absolute; width: 100vw; height: 100vh; top: 0; left: 0; z-index: 5; display: none; }
    </style>
    <div id="three-container" style="width:100vw;height:100vh;position:relative;"></div>
    <div id="particles-js"></div>
    <div id="overlay-ui"><div class="ui-box">Welcome to the 2D UI!</div></div>
    <script src="https://cdn.jsdelivr.net/npm/three@0.153.0/build/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.153.0/examples/jsm/controls/OrbitControls.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/particles.js@2.0.0/particles.min.js"></script>
    <script>
    // 3D Particle Scene with Three.js
    const container = document.getElementById('three-container');
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({antialias:true});
    renderer.setSize(window.innerWidth, window.innerHeight);
    container.appendChild(renderer.domElement);
    
    // Particle geometry
    const particleCount = 1000;
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(particleCount * 3);
    for (let i = 0; i < particleCount; i++) {
      positions[i*3] = (Math.random()-0.5)*20;
      positions[i*3+1] = (Math.random()-0.5)*20;
      positions[i*3+2] = (Math.random()-0.5)*20;
    }
    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    const material = new THREE.PointsMaterial({ color: 0x00aaff, size: 0.2 });
    const points = new THREE.Points(geometry, material);
    scene.add(points);
    
    camera.position.z = 30;
    const controls = new THREE.OrbitControls(camera, renderer.domElement);
    
    let frame = 0;
    function animate() {
      requestAnimationFrame(animate);
      points.rotation.y += 0.002;
      points.rotation.x += 0.001;
      renderer.render(scene, camera);
      frame++;
      // After 5 seconds, morph to 2D UI
      if (frame === 300) morphTo2D();
    }
    animate();
    
    function morphTo2D() {
      // Fade out 3D
      renderer.domElement.style.transition = 'opacity 1s';
      renderer.domElement.style.opacity = 0;
      setTimeout(() => {
        renderer.domElement.style.display = 'none';
        document.getElementById('particles-js').style.display = 'block';
        document.getElementById('overlay-ui').classList.add('active');
        // Start particles.js
        particlesJS('particles-js', {
          particles: {
            number: { value: 80 },
            color: { value: '#00aaff' },
            shape: { type: 'circle' },
            opacity: { value: 0.5 },
            size: { value: 5 },
            line_linked: { enable: true, distance: 150, color: '#00aaff', opacity: 0.4, width: 1 },
            move: { enable: true, speed: 2 }
          },
          interactivity: {
            detect_on: 'canvas',
            events: { onhover: { enable: true, mode: 'repulse' } },
            modes: { repulse: { distance: 100 } }
          },
          retina_detect: true
        });
      }, 1000);
    }
    window.addEventListener('resize', () => {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    });
    </script>
    ''')
    return

@app.cell
def _():
    mo.md("""
    ## How it works
    
    - The 3D scene is rendered with three.js, showing a rotating particle cloud.
    - After a few seconds, the 3D canvas fades out and a 2D UI overlay appears, with a dynamic particle background powered by particles.js.
    - This approach can be adapted for use in frameworks like NiceGUI by embedding the HTML/JS or using custom components.
    
    **Note:** This is a conceptual prototype. For full integration with NiceGUI and WebGPU, you would implement the 3D scene and UI as custom frontend components, possibly using [NiceGUI's custom element support](https://nicegui.io/documentation/custom_elements).
    """)
    return

if __name__ == "__main__":
    app.run()
