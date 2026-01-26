# ORCHESTR8 EXECUTION PROMPT
## For Cloud-Claude to Build the Complete VS Code Fork + 3D Visualization Layer

**Target:** Complete IDE with "Code City" 3D visualization overlay  
**Base:** Fork VS Code via VSCodium build process  
**Visualization:** Three.js with low-poly city buildings representing code structure

---

## EXECUTIVE SUMMARY

Build "Orchestr8" - a VS Code fork with a 3D "Code City" overlay that visualizes the codebase as an abstract cityscape. Gold buildings = working code, Blue = broken, Purple = active debugging. LLM "Generals" are assigned to neighborhoods (directories) to fix problems.

**Key Insight:** We're NOT building an extension. We're forking VS Code itself and adding a WebGL layer on top.

---

## PART 1: VS CODE FORK (FOUNDATION)

### 1.1 Base Repository Setup

Use VSCodium's build process as reference:
- **Repo:** https://github.com/VSCodium/vscodium
- **Build Guide:** https://github.com/VSCodium/vscodium/blob/master/docs/howto-build.md

```bash
# Clone VS Code source (not VSCodium - we want our own brand)
git clone https://github.com/microsoft/vscode.git orchestr8-editor
cd orchestr8-editor

# Install dependencies
yarn

# Build electron app
yarn run build

# Package for your platform
yarn run package
```

### 1.2 Branding Changes

Files to modify for "Orchestr8" branding:
```
product.json                    # Change name, version, updateUrl
resources/linux/code.desktop    # Desktop entry
resources/darwin/Info.plist     # macOS app info
resources/win32/code.iss        # Windows installer
src/vs/platform/product/common/product.ts
```

Product.json changes:
```json
{
  "nameShort": "Orchestr8",
  "nameLong": "Orchestr8 Editor",
  "applicationName": "orchestr8",
  "dataFolderName": ".orchestr8",
  "win32DirName": "Orchestr8",
  "darwinBundleIdentifier": "com.epoinc.orchestr8",
  "licenseName": "MIT",
  "licenseUrl": "https://github.com/yourusername/orchestr8/blob/main/LICENSE",
  "serverLicenseUrl": "...",
  "reportIssueUrl": "https://github.com/yourusername/orchestr8/issues",
  "urlProtocol": "orchestr8"
}
```

### 1.3 Remove Telemetry

From VSCodium's approach:
```bash
# In build scripts
export VSCODE_GALLERY_SERVICE_URL=''
export VSCODE_GALLERY_CACHE_URL=''
export VSCODE_GALLERY_ITEM_URL=''
export VSCODE_TELEMETRY_LEVEL='off'
```

---

## PART 2: THE CODE CITY OVERLAY (THE SOUL)

### 2.1 Injection Point

Add WebGL overlay as a new VS Code workbench part:
```
src/vs/workbench/contrib/orchestr8/
├── browser/
│   ├── orchestr8.contribution.ts    # Register the contribution
│   ├── codeCity.ts                  # Main 3D visualization
│   ├── codeCityRenderer.ts          # Three.js rendering
│   └── media/
│       ├── codeCity.css             # Overlay styles
│       └── assets/                  # 3D models (glTF)
├── common/
│   └── orchestr8.ts                 # Shared types
└── node/
    └── codeAnalyzer.ts              # Analyze codebase structure
```

### 2.2 Three.js Integration

Add Three.js to VS Code's dependencies:
```json
// package.json additions
"dependencies": {
  "three": "^0.160.0",
  "@types/three": "^0.160.0"
}
```

### 2.3 Code City Renderer (Core Implementation)

```typescript
// src/vs/workbench/contrib/orchestr8/browser/codeCityRenderer.ts
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';

// Color constants (from MaestroView.vue)
const COLORS = {
  working: 0xD4AF37,  // Gold
  broken: 0x1fbdea,   // Blue  
  combat: 0x9D4EDD,   // Purple
  void: 0x0A0A0B      // Background
};

interface CodeBuilding {
  path: string;
  status: 'working' | 'broken' | 'combat';
  height: number;      // Based on lines of code
  width: number;       // Based on complexity
  connections: string[];
  errors: string[];
}

export class CodeCityRenderer {
  private scene: THREE.Scene;
  private camera: THREE.PerspectiveCamera;
  private renderer: THREE.WebGLRenderer;
  private controls: OrbitControls;
  private buildings: Map<string, THREE.Mesh> = new Map();
  private gltfLoader: GLTFLoader;
  
  // Low-poly building models (load from glTF)
  private buildingModels: THREE.Object3D[] = [];
  
  constructor(container: HTMLElement) {
    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color(COLORS.void);
    
    this.camera = new THREE.PerspectiveCamera(
      60, 
      container.clientWidth / container.clientHeight, 
      0.1, 
      1000
    );
    this.camera.position.set(50, 50, 50);
    
    this.renderer = new THREE.WebGLRenderer({ antialias: true });
    this.renderer.setSize(container.clientWidth, container.clientHeight);
    this.renderer.setPixelRatio(window.devicePixelRatio);
    container.appendChild(this.renderer.domElement);
    
    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
    this.controls.enableDamping = true;
    
    // Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
    this.scene.add(ambientLight);
    
    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(50, 100, 50);
    this.scene.add(directionalLight);
    
    // Grid floor (the void)
    const gridHelper = new THREE.GridHelper(200, 50, 0x333333, 0x222222);
    this.scene.add(gridHelper);
    
    this.gltfLoader = new GLTFLoader();
    this.loadBuildingModels();
    
    this.animate();
  }
  
  private async loadBuildingModels(): Promise<void> {
    // Load low-poly building models
    // Sources: poly.pizza, sketchfab, free3d.com
    const modelUrls = [
      'assets/buildings/office_small.glb',
      'assets/buildings/office_medium.glb', 
      'assets/buildings/office_large.glb',
      'assets/buildings/skyscraper.glb',
      'assets/buildings/warehouse.glb'
    ];
    
    for (const url of modelUrls) {
      try {
        const gltf = await this.gltfLoader.loadAsync(url);
        this.buildingModels.push(gltf.scene);
      } catch (e) {
        // Fallback to procedural geometry
        console.warn(`Failed to load ${url}, using procedural building`);
      }
    }
  }
  
  private createProceduralBuilding(building: CodeBuilding): THREE.Mesh {
    // Fallback procedural buildings if glTF fails to load
    const geometry = new THREE.BoxGeometry(
      building.width,
      building.height,
      building.width
    );
    
    const material = new THREE.MeshLambertMaterial({
      color: COLORS[building.status],
      emissive: building.status === 'broken' ? COLORS.broken : 0x000000,
      emissiveIntensity: building.status === 'broken' ? 0.3 : 0
    });
    
    return new THREE.Mesh(geometry, material);
  }
  
  public updateCity(codeStructure: CodeBuilding[]): void {
    // Clear existing buildings
    this.buildings.forEach(mesh => this.scene.remove(mesh));
    this.buildings.clear();
    
    // Position buildings in grid layout (directory = neighborhood)
    const pathToPosition = this.calculateLayout(codeStructure);
    
    for (const building of codeStructure) {
      const position = pathToPosition.get(building.path);
      if (!position) continue;
      
      let mesh: THREE.Mesh;
      
      // Try to use loaded glTF model
      if (this.buildingModels.length > 0) {
        const modelIndex = Math.min(
          Math.floor(building.height / 10), 
          this.buildingModels.length - 1
        );
        mesh = this.buildingModels[modelIndex].clone() as THREE.Mesh;
        mesh.scale.setY(building.height / 10);
        
        // Apply status color
        mesh.traverse((child) => {
          if (child instanceof THREE.Mesh) {
            (child.material as THREE.MeshStandardMaterial).color.setHex(
              COLORS[building.status]
            );
          }
        });
      } else {
        mesh = this.createProceduralBuilding(building);
      }
      
      mesh.position.set(position.x, building.height / 2, position.z);
      mesh.userData = { building };
      
      this.scene.add(mesh);
      this.buildings.set(building.path, mesh);
      
      // Add "error pollution" particles for broken buildings
      if (building.status === 'broken' && building.errors.length > 0) {
        this.addErrorParticles(mesh, building.errors);
      }
    }
    
    // Draw connections between buildings
    this.drawConnections(codeStructure);
  }
  
  private calculateLayout(buildings: CodeBuilding[]): Map<string, {x: number, z: number}> {
    // Group by directory (neighborhood)
    const neighborhoods = new Map<string, CodeBuilding[]>();
    
    for (const b of buildings) {
      const dir = b.path.split('/').slice(0, -1).join('/');
      if (!neighborhoods.has(dir)) neighborhoods.set(dir, []);
      neighborhoods.get(dir)!.push(b);
    }
    
    // Position neighborhoods in a grid
    const result = new Map<string, {x: number, z: number}>();
    let neighborhoodX = 0;
    
    for (const [dir, dirBuildings] of neighborhoods) {
      let localZ = 0;
      let localX = 0;
      
      for (const b of dirBuildings) {
        result.set(b.path, {
          x: neighborhoodX + localX * 5,
          z: localZ * 5
        });
        
        localX++;
        if (localX > 5) {
          localX = 0;
          localZ++;
        }
      }
      
      neighborhoodX += 40; // Space between neighborhoods
    }
    
    return result;
  }
  
  private addErrorParticles(building: THREE.Mesh, errors: string[]): void {
    // Floating text/particles showing errors
    const particleCount = Math.min(errors.length * 10, 100);
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(particleCount * 3);
    
    for (let i = 0; i < particleCount; i++) {
      const i3 = i * 3;
      positions[i3] = building.position.x + (Math.random() - 0.5) * 5;
      positions[i3 + 1] = building.position.y + Math.random() * 10;
      positions[i3 + 2] = building.position.z + (Math.random() - 0.5) * 5;
    }
    
    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    
    const material = new THREE.PointsMaterial({
      color: COLORS.broken,
      size: 0.3,
      transparent: true,
      opacity: 0.6
    });
    
    const particles = new THREE.Points(geometry, material);
    this.scene.add(particles);
    
    // Animate particles rising
    const animate = () => {
      const positions = geometry.attributes.position.array as Float32Array;
      for (let i = 0; i < particleCount; i++) {
        positions[i * 3 + 1] += 0.05; // Rise up
        if (positions[i * 3 + 1] > building.position.y + 20) {
          positions[i * 3 + 1] = building.position.y;
        }
      }
      geometry.attributes.position.needsUpdate = true;
      requestAnimationFrame(animate);
    };
    animate();
  }
  
  private drawConnections(buildings: CodeBuilding[]): void {
    const material = new THREE.LineBasicMaterial({ 
      color: 0x444444, 
      transparent: true, 
      opacity: 0.3 
    });
    
    for (const building of buildings) {
      const sourceMesh = this.buildings.get(building.path);
      if (!sourceMesh) continue;
      
      for (const conn of building.connections) {
        const targetMesh = this.buildings.get(conn);
        if (!targetMesh) continue;
        
        const points = [
          sourceMesh.position.clone(),
          targetMesh.position.clone()
        ];
        
        const geometry = new THREE.BufferGeometry().setFromPoints(points);
        const line = new THREE.Line(geometry, material);
        this.scene.add(line);
      }
    }
  }
  
  public focusOnBuilding(path: string): void {
    const building = this.buildings.get(path);
    if (!building) return;
    
    // Smooth camera animation to building
    const target = building.position.clone();
    target.y += 20;
    target.z += 30;
    
    // Use GSAP or simple lerp for animation
    const duration = 1000;
    const start = this.camera.position.clone();
    const startTime = Date.now();
    
    const animateCamera = () => {
      const elapsed = Date.now() - startTime;
      const t = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - t, 3); // Ease out cubic
      
      this.camera.position.lerpVectors(start, target, eased);
      this.controls.target.copy(building.position);
      
      if (t < 1) requestAnimationFrame(animateCamera);
    };
    
    animateCamera();
  }
  
  private animate(): void {
    requestAnimationFrame(() => this.animate());
    this.controls.update();
    this.renderer.render(this.scene, this.camera);
  }
  
  public dispose(): void {
    this.renderer.dispose();
    this.scene.clear();
  }
}
```

### 2.4 Code Analyzer (Extract Structure)

```typescript
// src/vs/workbench/contrib/orchestr8/node/codeAnalyzer.ts
import * as fs from 'fs';
import * as path from 'path';

interface FileAnalysis {
  path: string;
  lines: number;
  complexity: number;  // Cyclomatic complexity estimate
  imports: string[];
  exports: string[];
  errors: string[];
  warnings: string[];
}

export class CodeAnalyzer {
  constructor(private workspaceRoot: string) {}
  
  public async analyzeWorkspace(): Promise<FileAnalysis[]> {
    const files: FileAnalysis[] = [];
    await this.walkDirectory(this.workspaceRoot, files);
    return files;
  }
  
  private async walkDirectory(dir: string, files: FileAnalysis[]): Promise<void> {
    const entries = await fs.promises.readdir(dir, { withFileTypes: true });
    
    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);
      const relativePath = path.relative(this.workspaceRoot, fullPath);
      
      // Skip node_modules, .git, etc.
      if (this.shouldSkip(entry.name)) continue;
      
      if (entry.isDirectory()) {
        await this.walkDirectory(fullPath, files);
      } else if (this.isCodeFile(entry.name)) {
        const analysis = await this.analyzeFile(fullPath, relativePath);
        files.push(analysis);
      }
    }
  }
  
  private shouldSkip(name: string): boolean {
    return ['node_modules', '.git', 'dist', 'build', '__pycache__'].includes(name);
  }
  
  private isCodeFile(name: string): boolean {
    return /\.(ts|tsx|js|jsx|py|java|go|rs|cpp|c|h)$/.test(name);
  }
  
  private async analyzeFile(fullPath: string, relativePath: string): Promise<FileAnalysis> {
    const content = await fs.promises.readFile(fullPath, 'utf-8');
    const lines = content.split('\n').length;
    
    // Extract imports (simplified - would need proper AST parsing)
    const imports = this.extractImports(content);
    const exports = this.extractExports(content);
    
    // Estimate complexity (simplified)
    const complexity = this.estimateComplexity(content);
    
    return {
      path: relativePath,
      lines,
      complexity,
      imports,
      exports,
      errors: [],  // Populated by diagnostics service
      warnings: []
    };
  }
  
  private extractImports(content: string): string[] {
    const imports: string[] = [];
    
    // JavaScript/TypeScript imports
    const jsImports = content.matchAll(/import\s+.*?\s+from\s+['"](.+?)['"]/g);
    for (const match of jsImports) {
      imports.push(match[1]);
    }
    
    // Python imports
    const pyImports = content.matchAll(/(?:from|import)\s+([\w.]+)/g);
    for (const match of pyImports) {
      imports.push(match[1]);
    }
    
    return imports;
  }
  
  private extractExports(content: string): string[] {
    const exports: string[] = [];
    
    // JavaScript/TypeScript exports
    const jsExports = content.matchAll(/export\s+(?:default\s+)?(?:class|function|const|let|var)\s+(\w+)/g);
    for (const match of jsExports) {
      exports.push(match[1]);
    }
    
    return exports;
  }
  
  private estimateComplexity(content: string): number {
    // Simplified cyclomatic complexity
    let complexity = 1;
    
    const controlFlow = /\b(if|else|for|while|switch|case|catch|&&|\|\||\?)\b/g;
    const matches = content.match(controlFlow);
    if (matches) complexity += matches.length;
    
    return Math.min(complexity, 100);  // Cap at 100
  }
}
```

---

## PART 3: 3D ASSET SOURCES

### 3.1 FREE Low-Poly Building Assets (CC0 - No Attribution Required)

**KENNEY ASSETS (Gold Standard - CC0 License, glTF format):**

| Pack | URL | Files | Notes |
|------|-----|-------|-------|
| **City Kit (Commercial)** | https://kenney.nl/assets/city-kit-commercial | 50 | Skyscrapers, large buildings |
| **City Kit (Suburban)** | https://kenney.nl/assets/city-kit-suburban | 40 | Houses, small buildings |
| **City Kit (Industrial)** | https://kenney.nl/assets/city-kit-industrial | 25 | Factories, warehouses |
| **All-in-1 Bundle** | https://kenney.nl/assets | 1000+ | Everything Kenney makes |

**QUATERNIUS (CC0 License):**

| Pack | URL | Notes |
|------|-----|-------|
| Ultimate Buildings | https://quaternius.com/packs/ultimatetexturedbuildings.html | Modular, textured |
| Simple Buildings | https://quaternius.com/packs/simplebuildings.html | 10 basic models |
| Sci-Fi Megakit | https://quaternius.com/packs/modularscifimegakit.html | 270+ pieces, glTF |

**Other Sources:**

| Source | URL | License | Notes |
|--------|-----|---------|-------|
| Poly Pizza | https://poly.pizza/explore/Buildings | CC0/CC-BY | Aggregates Kenney/Quaternius |
| Sketchfab | https://sketchfab.com/3d-models/low-poly-city-buildings-e0209ac5bb684d2d85e5ade96c92d2ff | CC-BY | 7.2k triangles |
| OpenGameArt | https://opengameart.org/content/city-kit-suburban | CC0 | Mirror of Kenney |

### 3.2 Model Requirements

- **Format:** glTF/glb (native Three.js support)
- **Poly count:** <500 triangles per building
- **Texture:** Optional - solid colors work well
- **Variations needed:**
  - Small office (1-2 stories) → Functions/small files
  - Medium office (3-5 stories) → Classes/medium files
  - Large office (6-10 stories) → Modules/large files
  - Skyscraper (10+ stories) → Entry points/main files
  - Warehouse → Data files/configs

### 3.3 OPEN SOURCE CODE CITY IMPLEMENTATIONS (Copy Their Code!)

**JSCity (1.4k+ stars) - THE REFERENCE IMPLEMENTATION:**
- **URL:** https://github.com/aserg-ufmg/JSCity
- **Stack:** Node.js + MySQL + Three.js
- **How it works:** 
  - Files are sub-districts, functions are buildings
  - LOC = building height, Variables = base size
  - Blue = named functions, Green = anonymous
- **Why use:** Mature, well-documented, Three.js rendering code

**CoderCity (Code Ownership Visualization):**
- **URL:** https://github.com/INSO-World/CoderCity
- **Stack:** Angular + NestJS + Three.js + Nodegit
- **How it works:**
  - Uses git blame for ownership colors
  - Each hunk = building segment colored by author
  - Docker-compose ready
- **Why use:** Modern stack, ownership visualization

**City Blocks (Git Repo 3D):**
- **URL:** https://github.com/cjayawickrema/city-blocks
- **Stack:** Node.js + Three.js
- **How it works:**
  - Visualizes file sizes and commit churn
  - Shell script + Node server + WebGL
- **Why use:** Simple, focused on git metrics

**Code Is Beautiful (Collection):**
- **URL:** https://quantifiedcode.github.io/code-is-beautiful/
- **Includes:** Multiple visualizations including Code City
- **Live demo:** https://quantifiedcode.github.io/code-city/index.html

### 3.4 VS Code Customization References

**vscode-custom-ui-style (Inject CSS/JS into VS Code):**
- **URL:** https://github.com/subframe7536/vscode-custom-ui-style
- **Marketplace:** https://marketplace.visualstudio.com/items?itemName=subframe7536.custom-ui-style
- **Features:** Modify CSS/JS, set background images, Electron BrowserWindow options
- **Why relevant:** Shows how to inject custom rendering into VS Code

**VS Code Extension Samples (Microsoft official):**
- **Webview Sample:** https://github.com/microsoft/vscode-extension-samples/tree/main/webview-sample
- **Custom Editor:** https://github.com/microsoft/vscode-extension-samples/tree/main/custom-editor-sample
- **Webview UI Toolkit:** https://github.com/microsoft/vscode-webview-ui-toolkit

---

## PART 4: UI ARCHITECTURE

### 4.1 Layout Specification

```
┌─────────────────────────────────────────────────────────────────┐
│  [SYSTEM]       [JFDI]        [Projects]      [Waves/Settings]  │  ← Top Bar
├─────────────────────────────────────────────────────────────────┤
│                                                           │ J │
│                                                           │ F │
│                                                           │ D │
│                    THE CODE MAP                           │ I │
│              (3D City Visualization)                      │   │
│                                                           │ T │
│         Gold = Working    Blue = Broken                   │ I │
│                Purple = Combat                            │ C │
│                                                           │ K │
│                                                           │ E │
│                                                           │ T │
│                                                           │ S │
├─────────────────────────────────────────────────────────────────┤
│  [File] [Terminal] [Note] [___]  (m)  [___] [___] [___] [Camp]  │  ← Bottom 5th
└─────────────────────────────────────────────────────────────────┘
                                 ↑
                            maestro toggle
                       OFF (blue) / OBSERVE (dark gold) / ON (bright gold)
```

### 4.2 Color System

```css
:root {
  /* Status Colors */
  --gold-metallic: #D4AF37;    /* Working / ON */
  --gold-dark: #B8960C;        /* OBSERVE mode */
  --blue-dominant: #1fbdea;    /* Broken / OFF */
  --purple-combat: #9D4EDD;    /* Combat / Active debug */
  
  /* Background (The Void) */
  --bg-primary: #0A0A0B;
  --bg-elevated: #121214;
  --bg-surface: #1A1A1C;
  
  /* Text */
  --text-primary: #FFFFFF;
  --text-secondary: #A0A0A0;
  --text-muted: #666666;
}
```

### 4.3 Interaction Flows

**Click Blue Building (broken code):**
1. Camera animates to that neighborhood
2. Top panel drops down (synchronized with camera)
3. Panel shows "House a Digital Native?" provider selection
4. User selects provider → LLM "General" moves in
5. Chat interface appears for human-LLM-system conversation
6. On resolution → ship to Public Services (SQLite/VectorDB)

**maestro Toggle:**
- **OFF** (blue): No LLM agency
- **OBSERVE** (dark gold): Read-only, @ mentions only
- **ON** (bright gold): Full Tier 2 agency

---

## PART 5: WOVEN MAPS ALTERNATIVE

### 5.1 Abstract Cityscape (Nicolas Barradeau Style)

If glTF models are too heavy, use Woven Maps algorithm:
- Source: https://barradeau.com/blog/?p=1001
- Demo: https://www.barradeau.com/2017/wovenmaps/index.html

**Algorithm:**
1. Collect points (file positions in codebase)
2. Delaunay triangulation
3. Compute edge lengths
4. Draw gradient layers (translate canvas + opacity)
5. Render wireframes at intervals
6. Overlay color (gold/blue/purple)
7. Add white glow wireframes

```javascript
// Simplified Woven Maps for Code City
function renderWovenCity(points, ctx, config) {
  // Delaunay triangulation
  const tris = Delaunay.from(points).triangles;
  
  // Compute edges
  const edges = [];
  for (let i = 0; i < tris.length; i += 3) {
    const p0 = points[tris[i]];
    const p1 = points[tris[i+1]];
    const p2 = points[tris[i+2]];
    edges.push(
      [distance(p0, p1), p0, p1],
      [distance(p1, p2), p1, p2],
      [distance(p2, p0), p2, p0]
    );
  }
  
  // Draw gradient (stacked layers)
  ctx.save();
  for (let i = 0; i < config.height; i++) {
    ctx.translate(0, 1);
    ctx.globalAlpha = (1 - i / config.height) * 0.05;
    renderEdges(ctx, edges, i);
  }
  ctx.restore();
  
  // Wireframe overlays
  for (let i = 0; i < config.wireCount; i++) {
    const t = i / config.wireCount;
    ctx.save();
    ctx.translate(0, config.height * (1 - t));
    ctx.globalAlpha = 0.05 + 0.15 * t;
    renderEdges(ctx, edges, i * 10);
    ctx.restore();
  }
}
```

---

## PART 6: EMERGENCE ANIMATIONS

### 6.1 Animation Catalog (CSS-first)

```css
/* emerge-void: Panel appearances */
@keyframes emerge-void {
  from {
    opacity: 0;
    transform: scale(0.95) translateY(-10px);
    filter: blur(4px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
    filter: blur(0);
  }
}

/* camera-suck: Zoom into neighborhood */
@keyframes camera-suck {
  from {
    transform: scale(1);
  }
  to {
    transform: scale(2.5);
  }
}

/* pollution-rise: Error particles floating up */
@keyframes pollution-rise {
  0% {
    transform: translateY(0) rotate(0deg);
    opacity: 0.6;
  }
  50% {
    opacity: 0.8;
  }
  100% {
    transform: translateY(-100px) rotate(180deg);
    opacity: 0;
  }
}

/* materialize: LLM General appears */
@keyframes materialize {
  from {
    opacity: 0;
    transform: scale(0) rotate(-180deg);
    filter: blur(10px);
  }
  to {
    opacity: 1;
    transform: scale(1) rotate(0);
    filter: blur(0);
  }
}

/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## PART 7: MCP SERVER (LLM BRIDGE)

### 7.1 MCP Server for LLM Tools

Already implemented at: `orchestr8_mcp.py`

Tools available:
- `scan_directory`: Get codebase structure
- `generate_mermaid_diagram`: Create visualizations
- `analyze_imports`: Dependency analysis
- `get_file_info`: File metadata

### 7.2 LLM Provider Integration

Settings panel allows configuring:
- Anthropic (Claude)
- OpenAI (GPT)
- OpenRouter
- x.AI
- Groq
- Ollama (local)
- etc.

Each provider needs API key storage in:
```
~/.orchestr8/providers.json
```

---

## PART 8: EXECUTION CHECKLIST

### Phase 1: VS Code Fork (Week 1)
- [ ] Clone VS Code source
- [ ] Update product.json for Orchestr8 branding
- [ ] Remove telemetry
- [ ] Build and test base editor
- [ ] Set up CI/CD for builds

### Phase 2: Three.js Integration (Week 2)
- [ ] Add Three.js dependency
- [ ] Create orchestr8 workbench contribution
- [ ] Implement CodeCityRenderer class
- [ ] Add WebGL overlay container
- [ ] Test basic scene rendering

### Phase 3: Code Analysis (Week 3)
- [ ] Implement CodeAnalyzer
- [ ] Hook into VS Code diagnostics API
- [ ] Extract file structure and imports
- [ ] Calculate building positions
- [ ] Test with sample codebase

### Phase 4: 3D Assets (Week 3-4)
- [ ] Download low-poly building models
- [ ] Convert to glTF format
- [ ] Import into Three.js loader
- [ ] Test different building types
- [ ] Implement fallback procedural geometry

### Phase 5: Interactions (Week 4-5)
- [ ] Click building → camera animation
- [ ] Top panel drop-down
- [ ] Provider selection
- [ ] Chat interface
- [ ] Error pollution particles

### Phase 6: LLM Integration (Week 5-6)
- [ ] Settings panel for API keys
- [ ] Provider abstraction layer
- [ ] MCP server integration
- [ ] General assignment flow
- [ ] Resolution → memory storage

### Phase 7: Polish (Week 6+)
- [ ] Animations (emerge-void, etc.)
- [ ] Reduced motion support
- [ ] Performance optimization
- [ ] Documentation
- [ ] Release builds

---

## CRITICAL SUCCESS FACTORS

1. **Performance**: Must stay above 30fps with 1000+ files
2. **Memory**: WebGL + VS Code must fit in 4GB RAM
3. **Startup**: Code Map should render within 3 seconds
4. **Accuracy**: Building status must match real diagnostics
5. **Delight**: Animations should feel "magical"

---

## REFERENCES

### Repositories
- VS Code: https://github.com/microsoft/vscode
- VSCodium: https://github.com/VSCodium/vscodium
- software-city-project: https://github.com/jonaslanzlinger/software-city-project

### 3D Assets
- Poly Pizza Buildings: https://poly.pizza/explore/Buildings
- Sketchfab Low-Poly City: https://sketchfab.com/3d-models/low-poly-city-buildings-e0209ac5bb684d2d85e5ade96c92d2ff

### Visualization Research
- CodeCity Paper: https://wettel.github.io/download/Wettel08b-wasdett.pdf
- Woven Maps: https://barradeau.com/blog/?p=1001

### Documentation
- This spec file location: Big Pickle/CLAUDE_EXECUTION_PROMPT.md
- UI Architecture: Big Pickle/UI_ARCHITECTURE_SPEC.md
- Animation Catalog: Big Pickle/EMERGENCE_ANIMATION_CATALOG.md

---

**END EXECUTION PROMPT**

*Copy this entire document to Cloud-Claude for execution.*
