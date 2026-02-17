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
    // Colors - CANONICAL per VISUAL_TOKEN_LOCK
    COLOR_WORKING: 0xD4AF37,     // Gold-metallic (#D4AF37)
    COLOR_BROKEN: 0x1fbdea,      // Teal/Blue (#1fbdea)
    COLOR_COMBAT: 0x9D4EDD,      // Purple (#9D4EDD)
    COLOR_LOCKED: 0xff6b6b,      // Red for locked files
    COLOR_VOID: 0x050505,        // The Void - obsidian background (#050505)
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
        if (typeof THREE.OrbitControls === "function") {
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
            return;
        }

        console.warn("[woven_maps_3d] OrbitControls unavailable; using static camera controls");
        this.controls = {
            target: new THREE.Vector3(
                CONFIG_3D.CAMERA_TARGET.x,
                CONFIG_3D.CAMERA_TARGET.y,
                CONFIG_3D.CAMERA_TARGET.z
            ),
            autoRotate: false,
            autoRotateSpeed: CONFIG_3D.AUTO_ROTATE_SPEED,
            update() {},
            dispose() {},
        };
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
        this.composer = null;
        this.bloomPass = null;

        if (
            typeof THREE.EffectComposer !== "function" ||
            typeof THREE.RenderPass !== "function" ||
            typeof THREE.UnrealBloomPass !== "function"
        ) {
            console.info("[woven_maps_3d] Post-processing addons missing; using renderer fallback");
            return;
        }

        try {
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
        } catch (error) {
            console.warn("[woven_maps_3d] Composer init failed; using renderer fallback", error);
            this.composer = null;
            this.bloomPass = null;
        }
    }
    
    _initResizeHandler() {
        window.addEventListener('resize', () => {
            const width = this.container.clientWidth;
            const height = this.container.clientHeight;
            
            this.camera.aspect = width / height;
            this.camera.updateProjectionMatrix();
            
            this.renderer.setSize(width, height);
            if (this.composer && typeof this.composer.setSize === "function") {
                this.composer.setSize(width, height);
            }
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
        if (typeof THREE.Float32BufferAttribute === "function") {
            geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
        } else {
            geometry.setAttribute('position', new THREE.BufferAttribute(new Float32Array(positions), 3));
        }
        
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
        
        // Add lock indicator for locked buildings
        let lockIndicator = null;
        if (buildingData.isLocked) {
            lockIndicator = this.createLockIndicator(buildingData);
            if (lockIndicator) {
                this.scene.add(lockIndicator);
            }
        }
        
        this.buildingMeshes.push({
            particles: particleMesh,
            lines: lineMesh,
            lockIndicator: lockIndicator,
            data: buildingData
        });
        
        this.buildings.push(buildingData);

        if (animateEmergence) {
            this.playEmergenceForMeshGroup(this.buildingMeshes[this.buildingMeshes.length - 1]);
        }
    }
    
    /**
     * Create a lock indicator sprite above the building.
     * 
     * @param {Object} buildingData - BuildingData from barradeau_builder.py
     * @returns {THREE.Sprite|null} Lock indicator sprite or null
     */
    createLockIndicator(buildingData) {
        // Create a canvas-based lock icon
        const canvas = document.createElement('canvas');
        canvas.width = 32;
        canvas.height = 32;
        const ctx = canvas.getContext('2d');
        
        // Draw lock icon
        ctx.fillStyle = '#ff6b6b';
        ctx.font = '20px sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('🔒', 16, 16);
        
        const texture = new THREE.CanvasTexture(canvas);
        texture.needsUpdate = true;
        
        const material = new THREE.SpriteMaterial({ 
            map: texture, 
            transparent: true,
            opacity: 0.85
        });
        
        const sprite = new THREE.Sprite(material);
        
        // Position above the building
        const buildingHeight = buildingData.height || 5;
        const x = buildingData.position?.x || 0;
        const z = buildingData.position?.z || 0;
        
        sprite.position.set(x, buildingHeight + 1.5, z);
        sprite.scale.set(2, 2, 1);
        
        // Store reference for updates
        sprite.userData = {
            type: 'lockIndicator',
            buildingPath: buildingData.path
        };
        
        return sprite;
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
            
            // Clean up lock indicator if present
            if (meshGroup.lockIndicator) {
                this.scene.remove(meshGroup.lockIndicator);
                if (meshGroup.lockIndicator.material.map) {
                    meshGroup.lockIndicator.material.map.dispose();
                }
                meshGroup.lockIndicator.material.dispose();
            }
        }
        
        this.buildingMeshes = [];
        this.buildings = [];
    }

    // ═══════════════════════════════════════════════════════════════════════════════
    // NEIGHBORHOOD BOUNDARY OVERLAYS
    // ═══════════════════════════════════════════════════════════════════════════════

    /**
     * Add neighborhood boundary overlays.
     * 
     * Creates semi-transparent boundary polygons with labels and integration badges.
     * Things EMERGE from the Void — NO breathing/pulsing animations.
     * 
     * @param {Array} neighborhoods - Array of neighborhood data from Python
     * @param {number} scale - Scale factor for converting 2D coords to 3D (default: 10)
     */
    addNeighborhoodBoundaries(neighborhoods, scale = 10) {
        if (!neighborhoods || neighborhoods.length === 0) {
            console.info("[woven_maps_3d] No neighborhoods to render");
            return;
        }

        // Clear existing boundary meshes
        this.clearNeighborhoodBoundaries();

        this.neighborhoodBoundaries = [];
        this.neighborhoodLabels = [];
        this.neighborhoodBadges = [];

        const LAYER_HEIGHT = 0.5; // Slightly above ground

        for (const neighborhood of neighborhoods) {
            const boundaryPoints = neighborhood.boundaryPoints;
            if (!boundaryPoints || boundaryPoints.length < 3) {
                continue;
            }

            // Determine boundary color based on status
            const isWorking = neighborhood.status === "working";
            const boundaryColor = isWorking ? CONFIG_3D.COLOR_WORKING : CONFIG_3D.COLOR_BROKEN;
            const boundaryAlpha = 0.15; // Low alpha so buildings remain visible

            // Create boundary polygon shape
            const shape = new THREE.Shape();
            
            // Convert 2D canvas coordinates to 3D space
            const points3D = boundaryPoints.map(p => {
                return new THREE.Vector3(
                    (p.x - 400) * (scale / 400), // Center the coordinates
                    LAYER_HEIGHT,
                    (p.y - 300) * (scale / 300)
                );
            });

            // Build the shape from boundary points
            shape.moveTo(points3D[0].x, points3D[0].z);
            for (let i = 1; i < points3D.length; i++) {
                shape.lineTo(points3D[i].x, points3D[i].z);
            }
            shape.closePath();

            // Create geometry from shape
            const geometry = new THREE.ShapeGeometry(shape);
            
            // Create material with low alpha for subtle overlay
            const material = new THREE.MeshBasicMaterial({
                color: boundaryColor,
                transparent: true,
                opacity: boundaryAlpha,
                side: THREE.DoubleSide,
                depthWrite: false, // Don't block other objects
            });

            const boundaryMesh = new THREE.Mesh(geometry, material);
            boundaryMesh.rotation.x = -Math.PI / 2; // Rotate to lie flat
            boundaryMesh.userData = {
                type: "neighborhoodBoundary",
                name: neighborhood.name,
                status: neighborhood.status,
            };

            this.scene.add(boundaryMesh);
            this.neighborhoodBoundaries.push(boundaryMesh);

            // Create boundary edge lines for visibility
            const edgePoints = points3D.map(p => new THREE.Vector3(p.x, LAYER_HEIGHT + 0.01, p.z));
            edgePoints.push(edgePoints[0]); // Close the loop
            
            const edgeGeometry = new THREE.BufferGeometry().setFromPoints(edgePoints);
            const edgeMaterial = new THREE.LineBasicMaterial({
                color: boundaryColor,
                transparent: true,
                opacity: 0.4,
            });
            
            const edgeMesh = new THREE.Line(edgeGeometry, edgeMaterial);
            this.scene.add(edgeMesh);
            this.neighborhoodBoundaries.push(edgeMesh);

            // Create floating label above the boundary
            const label = this._createNeighborhoodLabel(
                neighborhood.name,
                neighborhood.centerX,
                neighborhood.centerY,
                neighborhood.status,
                scale
            );
            if (label) {
                this.scene.add(label);
                this.neighborhoodLabels.push(label);
            }

            // Create integration crossing badge if there are crossings
            if (neighborhood.integrationCount > 0) {
                const badge = this._createIntegrationBadge(
                    neighborhood.integrationCount,
                    neighborhood.centerX,
                    neighborhood.centerY,
                    scale
                );
                if (badge) {
                    this.scene.add(badge);
                    this.neighborhoodBadges.push(badge);
                }
            }
        }

        console.log("[woven_maps_3d] Added", neighborhoods.length, "neighborhood boundaries");
    }

    /**
     * Create a floating neighborhood label.
     * 
     * @param {string} name - Neighborhood name
     * @param {number} centerX - 2D canvas X coordinate
     * @param {number} centerY - 2D canvas Y coordinate
     * @param {string} status - Status (working|broken)
     * @param {number} scale - Scale factor
     * @returns {THREE.Group} Label group
     */
    _createNeighborhoodLabel(name, centerX, centerY, status, scale) {
        // Use canvas to create text texture
        const canvas = document.createElement("canvas");
        const ctx = canvas.getContext("2d");
        
        // Canvas size for high DPI text
        const fontSize = 24;
        canvas.width = 256;
        canvas.height = 64;
        
        // Draw text
        ctx.fillStyle = "transparent";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        ctx.font = `bold ${fontSize}px monospace`;
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        
        // Color based on status
        const color = status === "working" ? "#D4AF37" : "#1fbdea";
        ctx.fillStyle = color;
        
        // Truncate long names
        const displayName = name.length > 20 ? name.substring(0, 17) + "..." : name;
        ctx.fillText(displayName, canvas.width / 2, canvas.height / 2);
        
        // Create texture from canvas
        const texture = new THREE.CanvasTexture(canvas);
        texture.needsUpdate = true;
        
        const material = new THREE.SpriteMaterial({
            map: texture,
            transparent: true,
            depthTest: false, // Always render on top
        });
        
        const sprite = new THREE.Sprite(material);
        
        // Position in 3D space (above buildings)
        sprite.position.set(
            (centerX - 400) * (scale / 400),
            15, // Height above ground
            (centerY - 300) * (scale / 300)
        );
        
        // Scale sprite
        const aspectRatio = canvas.width / canvas.height;
        sprite.scale.set(8 * aspectRatio, 8, 1);
        
        return sprite;
    }

    /**
     * Create an integration crossing badge.
     * 
     * @param {number} count - Number of integrations
     * @param {number} centerX - 2D canvas X coordinate
     * @param {number} centerY - 2D canvas Y coordinate
     * @param {number} scale - Scale factor
     * @returns {THREE.Group} Badge group
     */
    _createIntegrationBadge(count, centerX, centerY, scale) {
        // Use canvas to create badge texture
        const canvas = document.createElement("canvas");
        const ctx = canvas.getContext("2d");
        
        canvas.width = 64;
        canvas.height = 64;
        
        // Draw circle badge
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Background circle
        ctx.beginPath();
        ctx.arc(32, 32, 28, 0, Math.PI * 2);
        ctx.fillStyle = "rgba(157, 78, 221, 0.8)"; // Purple for integrations
        ctx.fill();
        
        // Border
        ctx.strokeStyle = "#D4AF37";
        ctx.lineWidth = 2;
        ctx.stroke();
        
        // Count text
        ctx.font = "bold 20px monospace";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillStyle = "#FFFFFF";
        ctx.fillText(count.toString(), 32, 32);
        
        // Create texture
        const texture = new THREE.CanvasTexture(canvas);
        texture.needsUpdate = true;
        
        const material = new THREE.SpriteMaterial({
            map: texture,
            transparent: true,
            depthTest: false,
        });
        
        const sprite = new THREE.Sprite(material);
        
        // Position at corner of boundary
        sprite.position.set(
            (centerX - 400) * (scale / 400) + 5,
            12,
            (centerY - 300) * (scale / 300) - 3
        );
        
        sprite.scale.set(3, 3, 1);
        
        return sprite;
    }

    /**
     * Clear all neighborhood boundary overlays.
     */
    clearNeighborhoodBoundaries() {
        // Clear boundary meshes
        if (this.neighborhoodBoundaries) {
            for (const mesh of this.neighborhoodBoundaries) {
                this.scene.remove(mesh);
                if (mesh.geometry) mesh.geometry.dispose();
                if (mesh.material) mesh.material.dispose();
            }
        }
        this.neighborhoodBoundaries = [];

        // Clear labels
        if (this.neighborhoodLabels) {
            for (const label of this.neighborhoodLabels) {
                this.scene.remove(label);
                if (label.material) {
                    if (label.material.map) label.material.map.dispose();
                    label.material.dispose();
                }
            }
        }
        this.neighborhoodLabels = [];

        // Clear badges
        if (this.neighborhoodBadges) {
            for (const badge of this.neighborhoodBadges) {
                this.scene.remove(badge);
                if (badge.material) {
                    if (badge.material.map) badge.material.map.dispose();
                    badge.material.dispose();
                }
            }
        }
        this.neighborhoodBadges = [];
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
    
    // ═══════════════════════════════════════════════════════════════════════════════
    // EMERGENCE ANIMATION - 7 PHASES
    // ═══════════════════════════════════════════════════════════════════════════════
    
    /**
     * Emergence sequence phases - 7 phases at 2s each (14s total, cycles at 28s)
     * Uses --transition-emergence 2s timing per phase
     */
    EMERGENCE_PHASES = [
        { name: "void", color: 0x1fbdea, opacity: 0.1, label: "VOID EMERGENCE" },      // Phase 1: Void scatter
        { name: "coalesce", color: 0x1fbdea, opacity: 0.3, label: "COALESCING" },      // Phase 2: Start coalescing
        { name: "forming", color: 0x1fbdea, opacity: 0.5, label: "FORMING" },         // Phase 3: Forming shapes
        { name: "crystallizing", color: 0xD4AF37, opacity: 0.6, label: "CRYSTALLIZING" }, // Phase 4: Start gold transition
        { name: "solidifying", color: 0xD4AF37, opacity: 0.7, label: "SOLIDIFYING" },  // Phase 5: Solidify
        { name: "finalizing", color: 0xD4AF37, opacity: 0.85, label: "FINALIZING" },   // Phase 6: Almost done
        { name: "emerged", color: null, opacity: 1.0, label: "EMERGED" }               // Phase 7: Complete
    ];
    
    /**
     * Play multi-phase emergence animation for all buildings.
     * 7 phases × 2s = 14s for full cycle (28s with pause between cycles)
     * 
     * @param {number} phaseDuration - Duration per phase in ms (default: 2000)
     * @param {Function} onPhaseChange - Optional callback when phase changes
     */
    playEmergenceSequence(phaseDuration = 2000, onPhaseChange = null) {
        const self = this;
        const totalPhases = this.EMERGENCE_PHASES.length;
        let currentPhase = 0;
        
        // Store original positions
        this._originalPositions = [];
        for (const meshGroup of this.buildingMeshes) {
            const positions = meshGroup.particles.geometry.attributes.position;
            this._originalPositions.push({
                positions: positions.array.slice(),
                count: positions.count,
                targetColor: new THREE.Color(this.getStatusColor(meshGroup.data.status))
            });
        }
        
        function runPhase(phaseIndex) {
            if (phaseIndex >= totalPhases) {
                // Cycle complete, restart after brief pause
                setTimeout(() => {
                    if (self._emergenceActive) {
                        currentPhase = 0;
                        runPhase(0);
                    }
                }, 14000); // 14s pause before restart = 28s full cycle
                return;
            }
            
            const phase = self.EMERGENCE_PHASES[phaseIndex];
            
            // Notify phase change
            if (onPhaseChange) {
                onPhaseChange(phase, phaseIndex + 1, totalPhases);
            }
            
            // Dispatch custom event for UI updates
            self._dispatchEmergenceEvent(phase, phaseIndex + 1, totalPhases);
            
            // Animate this phase
            self._animatePhase(phase, phaseIndex, () => {
                currentPhase = phaseIndex + 1;
                if (self._emergenceActive) {
                    runPhase(currentPhase);
                }
            });
        }
        
        this._emergenceActive = true;
        runPhase(0);
    }
    
    /**
     * Dispatch emergence phase event for UI synchronization.
     */
    _dispatchEmergenceEvent(phase, current, total) {
        const event = new CustomEvent('emergencePhase', {
            detail: {
                phase: phase.name,
                label: phase.label,
                current: current,
                total: total,
                color: phase.color,
                opacity: phase.opacity
            }
        });
        window.dispatchEvent(event);
    }
    
    /**
     * Animate a single emergence phase.
     */
    _animatePhase(phase, phaseIndex, onComplete) {
        const self = this;
        const duration = 2000; // 2s per phase - matches --transition-emergence
        const startTime = performance.now();
        
        // Determine start/end colors based on phase
        let startColor, endColor;
        
        if (phaseIndex === 0) {
            // Phase 1: Start from scattered teal void
            startColor = new THREE.Color(CONFIG_3D.COLOR_BROKEN);
            endColor = new THREE.Color(CONFIG_3D.COLOR_BROKEN);
        } else if (phaseIndex < 4) {
            // Phases 2-3: Coalescing in teal
            const prevPhase = this.EMERGENCE_PHASES[phaseIndex - 1];
            startColor = new THREE.Color(prevPhase.color || CONFIG_3D.COLOR_BROKEN);
            endColor = new THREE.Color(phase.color || CONFIG_3D.COLOR_BROKEN);
        } else {
            // Phases 4-7: Transition to gold (final state color)
            startColor = new THREE.Color(CONFIG_3D.COLOR_BROKEN);
            endColor = new THREE.Color(CONFIG_3D.COLOR_WORKING); // Gold for working
        }
        
        for (let i = 0; i < this.buildingMeshes.length; i++) {
            const meshGroup = this.buildingMeshes[i];
            const positions = meshGroup.particles.geometry.attributes.position;
            const origData = this._originalPositions[i];
            
            // Phase-specific position scattering
            const scatterAmount = 1 - (phaseIndex / this.EMERGENCE_PHASES.length);
            const scatteredPositions = new Float32Array(origData.count * 3);
            
            for (let j = 0; j < origData.count; j++) {
                const j3 = j * 3;
                // Gradually reduce scatter as phases progress
                scatteredPositions[j3] = origData.positions[j3] + (Math.random() - 0.5) * 100 * scatterAmount;
                scatteredPositions[j3 + 1] = origData.positions[j3 + 1] + Math.random() * 50 * scatterAmount;
                scatteredPositions[j3 + 2] = origData.positions[j3 + 2] + (Math.random() - 0.5) * 100 * scatterAmount;
            }
            
            // Initialize to scattered if first phase
            if (phaseIndex === 0) {
                positions.array.set(scatteredPositions);
                positions.needsUpdate = true;
            }
            
            // Set initial color
            if (meshGroup.particles.userData.useCustomShader) {
                meshGroup.particles.material.uniforms.color.value.copy(startColor);
            } else {
                meshGroup.particles.material.color.copy(startColor);
            }
            meshGroup.lines.material.color.copy(startColor);
        }
        
        const animate = () => {
            const elapsed = performance.now() - startTime;
            const t = Math.min(1, elapsed / duration);
            
            // Cubic ease
            const eased = t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
            
            for (let i = 0; i < this.buildingMeshes.length; i++) {
                const meshGroup = this.buildingMeshes[i];
                const positions = meshGroup.particles.geometry.attributes.position;
                const origData = this._originalPositions[i];
                
                // Calculate scattered positions for this phase
                const scatterAmount = 1 - (phaseIndex / this.EMERGENCE_PHASES.length);
                const scatteredPositions = new Float32Array(origData.count * 3);
                
                for (let j = 0; j < origData.count; j++) {
                    const j3 = j * 3;
                    scatteredPositions[j3] = origData.positions[j3] + (Math.random() - 0.5) * 100 * scatterAmount;
                    scatteredPositions[j3 + 1] = origData.positions[j3 + 1] + Math.random() * 50 * scatterAmount;
                    scatteredPositions[j3 + 2] = origData.positions[j3 + 2] + (Math.random() - 0.5) * 100 * scatterAmount;
                }
                
                // Interpolate positions
                for (let j = 0; j < origData.count * 3; j++) {
                    positions.array[j] = scatteredPositions[j] + (origData.positions[j] - scatteredPositions[j]) * eased;
                }
                positions.needsUpdate = true;
                
                // Interpolate color
                const currentColor = new THREE.Color().lerpColors(startColor, endColor, eased);
                
                if (meshGroup.particles.userData.useCustomShader) {
                    meshGroup.particles.material.uniforms.color.value.copy(currentColor);
                } else {
                    meshGroup.particles.material.color.copy(currentColor);
                }
                meshGroup.lines.material.color.copy(currentColor);
            }
            
            if (t < 1) {
                requestAnimationFrame(animate);
            } else {
                // Apply final state color for later phases
                if (phaseIndex >= 3) {
                    const finalColor = new THREE.Color(CONFIG_3D.COLOR_WORKING);
                    for (const meshGroup of this.buildingMeshes) {
                        if (meshGroup.particles.userData.useCustomShader) {
                            meshGroup.particles.material.uniforms.color.value.copy(finalColor);
                        } else {
                            meshGroup.particles.material.color.copy(finalColor);
                        }
                        meshGroup.lines.material.color.copy(finalColor);
                    }
                }
                if (onComplete) onComplete();
            }
        };
        
        requestAnimationFrame(animate);
    }
    
    /**
     * Stop the emergence sequence.
     */
    stopEmergenceSequence() {
        this._emergenceActive = false;
    }
    
    /**
     * Legacy single-phase emergence for backward compatibility.
     * @deprecated Use playEmergenceSequence() instead
     */
    playEmergenceAnimation(duration = 2000) {
        this.playEmergenceSequence(duration);
    }
    
    // ═══════════════════════════════════════════════════════════════════════════════
    // NODE HOVER EFFECTS
    // ═══════════════════════════════════════════════════════════════════════════════
    
    /**
     * Enable node hover detection with gold glow effect.
     * Uses --transition-normal 0.3s for smooth transitions
     * Uses --glow-gold-hover: 0 0 20px rgba(197,160,40,0.3)
     */
    enableHoverEffects() {
        const self = this;
        
        // Raycaster for mouse picking
        this._raycaster = new THREE.Raycaster();
        this._mouse = new THREE.Vector2();
        this._hoveredMesh = null;
        this._hoverGlowIntensity = 0;
        
        // Mouse move handler
        this._onMouseMove = function(event) {
            const rect = self.renderer.domElement.getBoundingClientRect();
            self._mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
            self._mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
        };
        
        // Mouse out handler - clear hover
        this._onMouseOut = function() {
            self._clearHover();
        };
        
        this.renderer.domElement.addEventListener('mousemove', this._onMouseMove);
        this.renderer.domElement.addEventListener('mouseout', this._onMouseOut);
        
        this._hoverEnabled = true;
        
        // Add hover update to render loop
        this._originalAnimate = this._animate;
        this._animate = function() {
            self._updateHover();
            self._originalAnimate.call(self);
        };
    }
    
    /**
     * Disable hover effects.
     */
    disableHoverEffects() {
        if (this._onMouseMove) {
            this.renderer.domElement.removeEventListener('mousemove', this._onMouseMove);
        }
        if (this._onMouseOut) {
            this.renderer.domElement.removeEventListener('mouseout', this._onMouseOut);
        }
        this._hoverEnabled = false;
        this._clearHover();
    }
    
    /**
     * Update hover state each frame.
     * Uses --transition-normal 0.3s (300ms)
     */
    _updateHover() {
        if (!this._hoverEnabled || !this._raycaster) return;
        
        this._raycaster.setFromCamera(this._mouse, this.camera);
        
        // Get particle meshes
        const meshes = this.buildingMeshes.map(m => m.particles);
        const intersects = this._raycaster.intersectObjects(meshes);
        
        if (intersects.length > 0) {
            const mesh = intersects[0].object;
            
            if (this._hoveredMesh !== mesh) {
                // Clear previous hover
                this._clearHover();
                
                // Set new hover
                this._hoveredMesh = mesh;
                this._hoverTargetGlow = 1;
                
                // Find building data
                const meshGroup = this.buildingMeshes.find(m => m.particles === mesh);
                if (meshGroup && meshGroup.data) {
                    this._dispatchHoverEvent(meshGroup.data, true);
                }
            }
            
            // Animate glow intensity - smooth 0.3s transition
            this._hoverGlowIntensity += (this._hoverTargetGlow - this._hoverGlowIntensity) * 0.15;
            
            // Apply glow effect: 0 0 20px rgba(197,160,40,0.3)
            this._applyHoverGlow(mesh, this._hoverGlowIntensity);
            
        } else if (this._hoveredMesh) {
            this._clearHover();
        }
    }
    
    /**
     * Apply gold hover glow effect.
     * Token: --glow-gold-hover: 0 0 20px rgba(197,160,40,0.3)
     */
    _applyHoverGlow(mesh, intensity) {
        const goldColor = new THREE.Color(0xD4AF37);
        const baseColor = new THREE.Color(this.getStatusColor(mesh.userData.status || 'working'));
        
        // Lerp toward gold with glow
        const glowColor = new THREE.Color().lerpColors(baseColor, goldColor, intensity * 0.7);
        
        if (mesh.userData.useCustomShader) {
            mesh.material.uniforms.color.value.copy(glowColor);
            // Adjust opacity for glow effect
            mesh.material.opacity = 0.9 + intensity * 0.1;
        } else {
            mesh.material.color.copy(glowColor);
            mesh.material.opacity = 0.9 + intensity * 0.1;
        }
    }
    
    /**
     * Clear hover state.
     */
    _clearHover() {
        if (this._hoveredMesh) {
            const meshGroup = this.buildingMeshes.find(m => m.particles === this._hoveredMesh);
            if (meshGroup && meshGroup.data) {
                this._dispatchHoverEvent(meshGroup.data, false);
            }
            
            // Reset color
            const baseColor = new THREE.Color(this.getStatusColor(this._hoveredMesh.userData.status || 'working'));
            if (this._hoveredMesh.userData.useCustomShader) {
                this._hoveredMesh.material.uniforms.color.value.copy(baseColor);
            } else {
                this._hoveredMesh.material.color.copy(baseColor);
            }
            this._hoveredMesh.material.opacity = 1;
            
            this._hoveredMesh = null;
        }
        this._hoverGlowIntensity = 0;
        this._hoverTargetGlow = 0;
    }
    
    /**
     * Dispatch hover event for UI updates.
     */
    _dispatchHoverEvent(buildingData, isHovering) {
        const event = new CustomEvent('nodeHover', {
            detail: {
                path: buildingData.path,
                status: buildingData.status,
                isHovering: isHovering
            }
        });
        window.dispatchEvent(event);
    }
    
    /**
     * Get hovered building data.
     */
    getHoveredBuilding() {
        if (!this._hoveredMesh) return null;
        
        const meshGroup = this.buildingMeshes.find(m => m.particles === this._hoveredMesh);
        return meshGroup ? meshGroup.data : null;
    }
    
    // ═══════════════════════════════════════════════════════════════════════════
    // CAMERA CONTROLS - PAN, ZOOM, ROTATE
    // ═══════════════════════════════════════════════════════════════════════════
    
    /**
     * Enable full camera controls: pan, zoom, rotate.
     * Uses OrbitControls with damping for smooth movement.
     * --transition-normal 0.3s is handled by damping.
     */
    enableCameraControls() {
        if (!this.controls) return;
        
        // Ensure all controls are enabled
        this.controls.enableDamping = true;
        this.controls.dampingFactor = 0.05; // Smooth 0.3s-like feel
        this.controls.enablePan = true;
        this.controls.enableZoom = true;
        this.controls.enableRotate = true;
        
        // Zoom settings
        this.controls.zoomSpeed = 1.0;
        this.controls.minDistance = 5;
        this.controls.maxDistance = 100;
        
        // Pan settings
        this.controls.panSpeed = 0.8;
        
        // Rotate settings
        this.controls.rotateSpeed = 0.5;
        
        console.log("[woven_maps_3d] Camera controls enabled: pan, zoom, rotate");
    }
    
    /**
     * Disable camera controls.
     */
    disableCameraControls() {
        if (this.controls) {
            this.controls.enablePan = false;
            this.controls.enableZoom = false;
            this.controls.enableRotate = false;
        }
    }
    
    /**
     * Reset camera to default position.
     */
    resetCamera() {
        this.transitionTo('overview', 1000);
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
        if (this.composer && typeof this.composer.render === "function") {
            this.composer.render();
        } else {
            this.renderer.render(this.scene, this.camera);
        }
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
        if (this.composer && typeof this.composer.dispose === "function") {
            this.composer.dispose();
        }
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
