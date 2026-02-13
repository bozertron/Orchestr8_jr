/**
 * woven_maps_3d.js - Three.js 3D Renderer for Code City
 * 
 * Uses Barradeau particle technique for building visualization.
 * Things EMERGE from the Void — NO breathing/pulsing animations.
 * 
 * Dependencies: Three.js, OrbitControls, EffectComposer, UnrealBloomPass
 */

// ═══════════════════════════════════════════════════════════════════════════════
// CONFIGURATION
// ═══════════════════════════════════════════════════════════════════════════════

const CONFIG_3D = {
    // Colors - CANONICAL per CLAUDE.md
    COLOR_WORKING: 0xD4AF37,     // Gold-metallic
    COLOR_BROKEN: 0x1fbdea,      // Teal/Blue
    COLOR_COMBAT: 0x9D4EDD,      // Purple
    COLOR_VOID: 0x0A0A0B,        // The Void (background)
    COLOR_SURFACE: 0x121214,     // Elevated elements
    
    // Camera
    CAMERA_FOV: 50,
    CAMERA_NEAR: 0.1,
    CAMERA_FAR: 500,
    CAMERA_INITIAL: { x: 20, y: 15, z: 20 },
    CAMERA_TARGET: { x: 0, y: 5, z: 0 },
    
    // Controls
    DAMPING_FACTOR: 0.05,
    AUTO_ROTATE_SPEED: 0.3,
    
    // Camera Keyframes
    CAMERA_KEYFRAMES: {
        overview: { 
            position: { x: 0, y: 60, z: 60 }, 
            target: { x: 0, y: 5, z: 0 },
            autoRotate: false
        },
        street: { 
            position: { x: 25, y: 3, z: 25 }, 
            target: { x: 0, y: 2, z: 0 },
            autoRotate: false
        },
        focus: { 
            position: { x: 12, y: 18, z: 12 }, 
            target: { x: 0, y: 8, z: 0 },
            autoRotate: false
        },
        orbit: { 
            position: { x: 30, y: 25, z: 30 }, 
            target: { x: 0, y: 5, z: 0 },
            autoRotate: true,
            autoRotateSpeed: 0.5
        }
    },
    
    // Animation
    KEYFRAME_DURATION: 2000,
    EASE_CUBIC: t => t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2,
    
    // Post-processing
    BLOOM_STRENGTH: 1.0,
    BLOOM_RADIUS: 0.4,
    BLOOM_THRESHOLD: 0.15,
    
    // Fog
    FOG_DENSITY: 0.025,
    
    // Particle sizes
    PARTICLE_MIN_SIZE: 0.3,
    PARTICLE_MAX_SIZE: 0.7,
};


// ═══════════════════════════════════════════════════════════════════════════════
// CODE CITY 3D SCENE
// ═══════════════════════════════════════════════════════════════════════════════

class CodeCityScene {
    /**
     * Three.js scene manager for Code City 3D visualization.
     * 
     * @param {HTMLElement} container - DOM element to render into
     */
    constructor(container) {
        this.container = container;
        this.buildings = [];
        this.buildingMeshes = [];
        this.isInitialized = false;
        
        this._initScene();
        this._initCamera();
        this._initControls();
        this._initLights();
        this._initPostProcessing();
        this._initResizeHandler();
        
        this.isInitialized = true;
    }
    
    _initScene() {
        // Renderer
        this.renderer = new THREE.WebGLRenderer({ 
            antialias: true,
            alpha: true 
        });
        this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
        this.renderer.setClearColor(CONFIG_3D.COLOR_VOID);
        this.container.appendChild(this.renderer.domElement);
        
        // Scene with fog
        this.scene = new THREE.Scene();
        this.scene.fog = new THREE.FogExp2(CONFIG_3D.COLOR_VOID, CONFIG_3D.FOG_DENSITY);
    }
    
    _initCamera() {
        const width = this.container.clientWidth;
        const height = this.container.clientHeight;
        const aspect = width / height;
        
        this.camera = new THREE.PerspectiveCamera(
            CONFIG_3D.CAMERA_FOV,
            aspect,
            CONFIG_3D.CAMERA_NEAR,
            CONFIG_3D.CAMERA_FAR
        );
        this.camera.position.set(
            CONFIG_3D.CAMERA_INITIAL.x,
            CONFIG_3D.CAMERA_INITIAL.y,
            CONFIG_3D.CAMERA_INITIAL.z
        );
    }
    
    _initControls() {
        this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
        this.controls.enableDamping = true;
        this.controls.dampingFactor = CONFIG_3D.DAMPING_FACTOR;
        this.controls.autoRotate = true;
        this.controls.autoRotateSpeed = CONFIG_3D.AUTO_ROTATE_SPEED;
        this.controls.target.set(
            CONFIG_3D.CAMERA_TARGET.x,
            CONFIG_3D.CAMERA_TARGET.y,
            CONFIG_3D.CAMERA_TARGET.z
        );
    }
    
    _initLights() {
        // Ambient light for base illumination
        const ambient = new THREE.AmbientLight(0xffffff, 0.3);
        this.scene.add(ambient);
        
        // Directional light for depth
        const directional = new THREE.DirectionalLight(0xffffff, 0.5);
        directional.position.set(10, 20, 10);
        this.scene.add(directional);
    }
    
    _initPostProcessing() {
        // Effect composer for bloom
        this.composer = new THREE.EffectComposer(this.renderer);
        
        // Render pass
        const renderPass = new THREE.RenderPass(this.scene, this.camera);
        this.composer.addPass(renderPass);
        
        // Bloom pass for soft glow
        this.bloomPass = new THREE.UnrealBloomPass(
            new THREE.Vector2(
                this.container.clientWidth,
                this.container.clientHeight
            ),
            CONFIG_3D.BLOOM_STRENGTH,
            CONFIG_3D.BLOOM_RADIUS,
            CONFIG_3D.BLOOM_THRESHOLD
        );
        this.composer.addPass(this.bloomPass);
    }
    
    _initResizeHandler() {
        window.addEventListener('resize', () => {
            const width = this.container.clientWidth;
            const height = this.container.clientHeight;
            
            this.camera.aspect = width / height;
            this.camera.updateProjectionMatrix();
            
            this.renderer.setSize(width, height);
            this.composer.setSize(width, height);
        });
    }
    
    // ═══════════════════════════════════════════════════════════════════════════
    // BUILDING MANAGEMENT
    // ═══════════════════════════════════════════════════════════════════════════
    
    /**
     * Get color for status.
     * @param {string} status - Status name or alias
     * @returns {number} Three.js color integer
     */
    getStatusColor(status) {
        const colorMap = {
            "working": CONFIG_3D.COLOR_WORKING,
            "broken": CONFIG_3D.COLOR_BROKEN,
            "combat": CONFIG_3D.COLOR_COMBAT,
            "needs_work": CONFIG_3D.COLOR_BROKEN,
            "agents_active": CONFIG_3D.COLOR_COMBAT,
            "gold": CONFIG_3D.COLOR_WORKING,
            "teal": CONFIG_3D.COLOR_BROKEN,
            "purple": CONFIG_3D.COLOR_COMBAT
        };
        return colorMap[status] || CONFIG_3D.COLOR_WORKING;
    }
    
    /**
     * Get inline vertex shader for Barradeau particles.
     * (Also available at IP/static/shaders/barradeau.vert)
     */
    getVertexShader() {
        return `
            attribute float size;
            attribute float opacity;
            
            varying float vOpacity;
            varying float vDistance;
            
            void main() {
                vOpacity = opacity;
                
                vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
                vDistance = -mvPosition.z;
                
                // Size attenuation: closer = larger
                gl_PointSize = size * (300.0 / vDistance);
                gl_PointSize = clamp(gl_PointSize, 1.0, 50.0);
                
                gl_Position = projectionMatrix * mvPosition;
            }
        `;
    }
    
    /**
     * Get inline fragment shader for Barradeau particles.
     * (Also available at IP/static/shaders/barradeau.frag)
     */
    getFragmentShader() {
        return `
            varying float vOpacity;
            varying float vDistance;
            
            uniform vec3 color;
            
            void main() {
                // Create circular point with soft falloff
                vec2 center = gl_PointCoord - vec2(0.5);
                float dist = length(center);
                
                // Soft edge falloff (Barradeau style)
                float alpha = 1.0 - smoothstep(0.3, 0.5, dist);
                alpha *= vOpacity;
                
                // Add subtle glow
                float glow = exp(-dist * 3.0) * 0.5;
                
                vec3 finalColor = color + glow * color;
                
                // Discard transparent fragments for performance
                if (alpha < 0.01) discard;
                
                gl_FragColor = vec4(finalColor, alpha);
            }
        `;
    }
    
    /**
     * Create a particle mesh from BuildingData.
     * 
     * @param {Object} buildingData - BuildingData from barradeau_builder.py
     * @param {boolean} useCustomShader - Use custom ShaderMaterial (default: true)
     * @returns {THREE.Points} Particle mesh
     */
    createBuildingMesh(buildingData, useCustomShader = true) {
        const particles = buildingData.particles;
        const positions = new Float32Array(particles.length * 3);
        const opacities = new Float32Array(particles.length);
        const sizes = new Float32Array(particles.length);
        
        const color = new THREE.Color(this.getStatusColor(buildingData.status));
        
        for (let i = 0; i < particles.length; i++) {
            const p = particles[i];
            const i3 = i * 3;
            
            positions[i3] = p.x;
            positions[i3 + 1] = p.y;
            positions[i3 + 2] = p.z;
            
            opacities[i] = p.opacity !== undefined ? p.opacity : 1.0;
            sizes[i] = p.size || (CONFIG_3D.PARTICLE_MIN_SIZE + Math.random() * 0.2);
        }
        
        const geometry = new THREE.BufferGeometry();
        geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        geometry.setAttribute('opacity', new THREE.BufferAttribute(opacities, 1));
        geometry.setAttribute('size', new THREE.BufferAttribute(sizes, 1));
        
        let material;
        
        if (useCustomShader) {
            // Custom ShaderMaterial with Barradeau glow
            material = new THREE.ShaderMaterial({
                uniforms: {
                    color: { value: color },
                    time: { value: 0.0 }
                },
                vertexShader: this.getVertexShader(),
                fragmentShader: this.getFragmentShader(),
                transparent: true,
                blending: THREE.AdditiveBlending,
                depthWrite: false,
            });
        } else {
            // Fallback PointsMaterial
            material = new THREE.PointsMaterial({
                size: 0.5,
                color: color,
                transparent: true,
                opacity: 0.9,
                sizeAttenuation: true,
                blending: THREE.AdditiveBlending,
            });
        }
        
        const mesh = new THREE.Points(geometry, material);
        mesh.userData = {
            path: buildingData.path,
            status: buildingData.status,
            particleCount: particles.length,
            useCustomShader: useCustomShader
        };
        
        return mesh;
    }
    
    /**
     * Create line segments mesh from BuildingData edges.
     * 
     * @param {Object} buildingData - BuildingData from barradeau_builder.py
     * @returns {THREE.LineSegments} Wireframe mesh
     */
    createBuildingLines(buildingData) {
        const edges = buildingData.edges;
        const positions = [];
        
        for (const edge of edges) {
            positions.push(edge.a.x, edge.a.y, edge.a.z);
            positions.push(edge.b.x, edge.b.y, edge.b.z);
        }
        
        const geometry = new THREE.BufferGeometry();
        geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
        
        const color = new THREE.Color(this.getStatusColor(buildingData.status));
        
        const material = new THREE.LineBasicMaterial({
            color: color,
            transparent: true,
            opacity: 0.3,
            blending: THREE.AdditiveBlending,
        });
        
        const mesh = new THREE.LineSegments(geometry, material);
        return mesh;
    }
    
    /**
     * Add a building to the scene.
     * 
     * @param {Object} buildingData - BuildingData from barradeau_builder.py
     */
    addBuilding(buildingData, animateEmergence = false) {
        const particleMesh = this.createBuildingMesh(buildingData);
        const lineMesh = this.createBuildingLines(buildingData);
        
        this.scene.add(particleMesh);
        this.scene.add(lineMesh);
        
        this.buildingMeshes.push({
            particles: particleMesh,
            lines: lineMesh,
            data: buildingData
        });
        
        this.buildings.push(buildingData);

        if (animateEmergence) {
            this.playEmergenceForMeshGroup(this.buildingMeshes[this.buildingMeshes.length - 1]);
        }
    }

    /**
     * Play emergence animation for one building mesh group.
     *
     * @param {Object} meshGroup - Mesh group from this.buildingMeshes
     * @param {number} duration - Animation duration in ms
     */
    playEmergenceForMeshGroup(meshGroup, duration = 1200) {
        if (!meshGroup || !meshGroup.particles?.geometry?.attributes?.position) {
            return;
        }

        const emergenceColor = new THREE.Color(CONFIG_3D.COLOR_BROKEN);
        const positions = meshGroup.particles.geometry.attributes.position;
        const originalPositions = positions.array.slice();
        const count = positions.count;
        const targetColor = new THREE.Color(this.getStatusColor(meshGroup.data.status));

        const scatteredPositions = new Float32Array(count * 3);
        for (let i = 0; i < count; i++) {
            const i3 = i * 3;
            scatteredPositions[i3] = (Math.random() - 0.5) * 100;
            scatteredPositions[i3 + 1] = Math.random() * 50;
            scatteredPositions[i3 + 2] = (Math.random() - 0.5) * 100;
        }

        positions.array.set(scatteredPositions);
        positions.needsUpdate = true;

        if (meshGroup.particles.userData.useCustomShader) {
            meshGroup.particles.material.uniforms.color.value.copy(emergenceColor);
        } else {
            meshGroup.particles.material.color.copy(emergenceColor);
        }
        meshGroup.lines.material.color.copy(emergenceColor);

        const startTime = performance.now();
        const animate = () => {
            const elapsed = performance.now() - startTime;
            const t = Math.min(1, elapsed / duration);
            const positionEased = 1 - Math.pow(1 - t, 3);

            for (let i = 0; i < count * 3; i++) {
                positions.array[i] =
                    scatteredPositions[i] +
                    (originalPositions[i] - scatteredPositions[i]) * positionEased;
            }
            positions.needsUpdate = true;

            const colorT = Math.pow(t, 1.5);
            const currentColor = new THREE.Color().lerpColors(
                emergenceColor,
                targetColor,
                colorT,
            );

            if (meshGroup.particles.userData.useCustomShader) {
                meshGroup.particles.material.uniforms.color.value.copy(currentColor);
            } else {
                meshGroup.particles.material.color.copy(currentColor);
            }
            meshGroup.lines.material.color.copy(currentColor);

            if (t < 1) {
                requestAnimationFrame(animate);
            }
        };

        requestAnimationFrame(animate);
    }
    
    /**
     * Clear all buildings from the scene.
     */
    clearBuildings() {
        for (const meshGroup of this.buildingMeshes) {
            this.scene.remove(meshGroup.particles);
            this.scene.remove(meshGroup.lines);
            
            meshGroup.particles.geometry.dispose();
            meshGroup.particles.material.dispose();
            meshGroup.lines.geometry.dispose();
            meshGroup.lines.material.dispose();
        }
        
        this.buildingMeshes = [];
        this.buildings = [];
    }
    
    /**
     * Load buildings from array of BuildingData.
     * 
     * @param {Array} buildingsData - Array of BuildingData objects
     */
    loadBuildings(buildingsData) {
        this.clearBuildings();
        
        for (const data of buildingsData) {
            this.addBuilding(data);
        }
    }
    
    /**
     * Update building status (changes color).
     * 
     * @param {string} path - Building path
     * @param {string} newStatus - "working" | "broken" | "combat"
     */
    updateBuildingStatus(path, newStatus) {
        for (const meshGroup of this.buildingMeshes) {
            if (meshGroup.data.path === path) {
                const color = new THREE.Color(this.getStatusColor(newStatus));
                
                // Update particle colors - ShaderMaterial uses uniform, PointsMaterial uses vertex colors
                if (meshGroup.particles.userData.useCustomShader) {
                    // ShaderMaterial: update uniform
                    meshGroup.particles.material.uniforms.color.value = color;
                } else {
                    // PointsMaterial: update vertex colors (if present)
                    const colors = meshGroup.particles.geometry.attributes.color;
                    if (colors) {
                        for (let i = 0; i < colors.count; i++) {
                            const variation = 0.9 + Math.random() * 0.2;
                            colors.setXYZ(
                                i,
                                color.r * variation,
                                color.g * variation,
                                color.b * variation
                            );
                        }
                        colors.needsUpdate = true;
                    } else {
                        // No vertex colors, update material color
                        meshGroup.particles.material.color = color;
                    }
                }
                
                // Update line colors
                meshGroup.lines.material.color = color;
                
                meshGroup.data.status = newStatus;
                break;
            }
        }
    }
    
    // ═══════════════════════════════════════════════════════════════════════════
    // EMERGENCE ANIMATION
    // ═══════════════════════════════════════════════════════════════════════════
    
    /**
     * Play emergence animation for all buildings.
     * Particles start scattered in teal and coalesce to building positions,
     * transitioning to their final state color (crystallization effect).
     * 
     * @param {number} duration - Animation duration in ms (default: 2000)
     */
    playEmergenceAnimation(duration = 2000) {
        const emergenceColor = new THREE.Color(CONFIG_3D.COLOR_BROKEN);
        
        for (const meshGroup of this.buildingMeshes) {
            const positions = meshGroup.particles.geometry.attributes.position;
            const originalPositions = positions.array.slice();
            const count = positions.count;
            
            const targetColor = new THREE.Color(this.getStatusColor(meshGroup.data.status));
            
            const scatteredPositions = new Float32Array(count * 3);
            for (let i = 0; i < count; i++) {
                const i3 = i * 3;
                scatteredPositions[i3] = (Math.random() - 0.5) * 100;
                scatteredPositions[i3 + 1] = Math.random() * 50;
                scatteredPositions[i3 + 2] = (Math.random() - 0.5) * 100;
            }
            
            positions.array.set(scatteredPositions);
            positions.needsUpdate = true;
            
            if (meshGroup.particles.userData.useCustomShader) {
                meshGroup.particles.material.uniforms.color.value.copy(emergenceColor);
            } else {
                meshGroup.particles.material.color.copy(emergenceColor);
            }
            meshGroup.lines.material.color.copy(emergenceColor);
            
            const startTime = performance.now();
            
            const animate = () => {
                const elapsed = performance.now() - startTime;
                const t = Math.min(1, elapsed / duration);
                
                const positionEased = 1 - Math.pow(1 - t, 3);
                
                for (let i = 0; i < count * 3; i++) {
                    positions.array[i] = scatteredPositions[i] + (originalPositions[i] - scatteredPositions[i]) * positionEased;
                }
                positions.needsUpdate = true;
                
                const colorT = Math.pow(t, 1.5);
                const currentColor = new THREE.Color().lerpColors(emergenceColor, targetColor, colorT);
                
                if (meshGroup.particles.userData.useCustomShader) {
                    meshGroup.particles.material.uniforms.color.value.copy(currentColor);
                } else {
                    meshGroup.particles.material.color.copy(currentColor);
                }
                meshGroup.lines.material.color.copy(currentColor);
                
                if (t < 1) {
                    requestAnimationFrame(animate);
                }
            };
            
            requestAnimationFrame(animate);
        }
    }
    
    // ═══════════════════════════════════════════════════════════════════════════
    // CAMERA KEYFRAMES
    // ═══════════════════════════════════════════════════════════════════════════
    
    /**
     * Linear interpolation.
     */
    _lerp(start, end, t) {
        return start + (end - start) * t;
    }
    
    /**
     * Cubic ease-in-out.
     */
    _easeInOutCubic(t) {
        return CONFIG_3D.EASE_CUBIC(t);
    }
    
    /**
     * Transition camera to a named keyframe.
     * 
     * @param {string} keyframeName - 'overview' | 'street' | 'focus' | 'orbit'
     * @param {number} duration - Transition duration in ms (default: 2000)
     * @returns {Promise} Resolves when transition completes
     */
    transitionTo(keyframeName, duration = CONFIG_3D.KEYFRAME_DURATION) {
        const keyframe = CONFIG_3D.CAMERA_KEYFRAMES[keyframeName];
        if (!keyframe) {
            console.warn(`Unknown keyframe: ${keyframeName}`);
            return Promise.reject(new Error(`Unknown keyframe: ${keyframeName}`));
        }
        
        if (this._transitionAnimation) {
            cancelAnimationFrame(this._transitionAnimation);
        }
        
        return new Promise((resolve) => {
            const startPosition = {
                x: this.camera.position.x,
                y: this.camera.position.y,
                z: this.camera.position.z
            };
            const startTarget = {
                x: this.controls.target.x,
                y: this.controls.target.y,
                z: this.controls.target.z
            };
            
            const startTime = performance.now();
            
            const animateTransition = () => {
                const elapsed = performance.now() - startTime;
                const t = Math.min(1, elapsed / duration);
                const eased = this._easeInOutCubic(t);
                
                this.camera.position.x = this._lerp(startPosition.x, keyframe.position.x, eased);
                this.camera.position.y = this._lerp(startPosition.y, keyframe.position.y, eased);
                this.camera.position.z = this._lerp(startPosition.z, keyframe.position.z, eased);
                
                this.controls.target.x = this._lerp(startTarget.x, keyframe.target.x, eased);
                this.controls.target.y = this._lerp(startTarget.y, keyframe.target.y, eased);
                this.controls.target.z = this._lerp(startTarget.z, keyframe.target.z, eased);
                
                if (t < 1) {
                    this._transitionAnimation = requestAnimationFrame(animateTransition);
                } else {
                    if (keyframe.autoRotate !== undefined) {
                        this.controls.autoRotate = keyframe.autoRotate;
                        if (keyframe.autoRotateSpeed !== undefined) {
                            this.controls.autoRotateSpeed = keyframe.autoRotateSpeed;
                        }
                    }
                    this._transitionAnimation = null;
                    resolve();
                }
            };
            
            this.controls.autoRotate = false;
            this._transitionAnimation = requestAnimationFrame(animateTransition);
        });
    }
    
    /**
     * Set auto-orbit mode.
     * 
     * @param {boolean} enabled - Enable or disable auto-rotate
     * @param {number} speed - Rotation speed (default: 0.5)
     */
    setAutoOrbit(enabled, speed = 0.5) {
        this.controls.autoRotate = enabled;
        this.controls.autoRotateSpeed = enabled ? speed : CONFIG_3D.AUTO_ROTATE_SPEED;
    }
    
    /**
     * Start demo mode - cycle through all keyframes automatically.
     * 
     * @param {number} interval - Time at each keyframe in ms (default: 5000)
     */
    startDemoMode(interval = 5000) {
        this.stopDemoMode();
        
        const keyframes = Object.keys(CONFIG_3D.CAMERA_KEYFRAMES);
        let currentIndex = 0;
        
        const cycleKeyframe = async () => {
            await this.transitionTo(keyframes[currentIndex]);
            currentIndex = (currentIndex + 1) % keyframes.length;
        };
        
        cycleKeyframe();
        this._demoInterval = setInterval(cycleKeyframe, interval);
        this._demoModeActive = true;
    }
    
    /**
     * Stop demo mode.
     */
    stopDemoMode() {
        if (this._demoInterval) {
            clearInterval(this._demoInterval);
            this._demoInterval = null;
        }
        this._demoModeActive = false;
    }
    
    /**
     * Get available keyframe names.
     * @returns {string[]} Keyframe names
     */
    getKeyframeNames() {
        return Object.keys(CONFIG_3D.CAMERA_KEYFRAMES);
    }
    
    /**
     * Get current keyframe (closest match).
     * @returns {string|null} Keyframe name or null
     */
    getCurrentKeyframe() {
        const pos = this.camera.position;
        
        let closest = null;
        let closestDist = Infinity;
        
        for (const [name, kf] of Object.entries(CONFIG_3D.CAMERA_KEYFRAMES)) {
            const dx = pos.x - kf.position.x;
            const dy = pos.y - kf.position.y;
            const dz = pos.z - kf.position.z;
            const dist = Math.sqrt(dx*dx + dy*dy + dz*dz);
            
            if (dist < closestDist && dist < 5) {
                closestDist = dist;
                closest = name;
            }
        }
        
        return closest;
    }
    
    // ═══════════════════════════════════════════════════════════════════════════
    // RENDER LOOP
    // ═══════════════════════════════════════════════════════════════════════════
    
    /**
     * Start the render loop.
     */
    start() {
        this.isRunning = true;
        this._animate();
    }
    
    /**
     * Stop the render loop.
     */
    stop() {
        this.isRunning = false;
    }
    
    _animate() {
        if (!this.isRunning) return;
        
        requestAnimationFrame(() => this._animate());
        
        this.controls.update();
        this.composer.render();
    }
    
    /**
     * Dispose of all resources.
     */
    dispose() {
        this.stop();
        this.stopDemoMode();
        
        if (this._transitionAnimation) {
            cancelAnimationFrame(this._transitionAnimation);
            this._transitionAnimation = null;
        }
        
        this.clearBuildings();
        
        this.renderer.dispose();
        this.composer.dispose();
        this.controls.dispose();
        
        if (this.renderer.domElement.parentNode) {
            this.renderer.domElement.parentNode.removeChild(this.renderer.domElement);
        }
    }
}


// ═══════════════════════════════════════════════════════════════════════════════
// EXPORTS
// ═══════════════════════════════════════════════════════════════════════════════

// For use in browser global scope
if (typeof window !== 'undefined') {
    window.CodeCityScene = CodeCityScene;
    window.CONFIG_3D = CONFIG_3D;
}

// For module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { CodeCityScene, CONFIG_3D };
}
